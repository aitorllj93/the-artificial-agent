
import asyncio
import json
from enum import Enum
from typing import Callable
from datetime import datetime, time, timedelta
import pytz
import logging
from telegram import Update, Message, Chat, Bot, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, ApplicationBuilder, CallbackQueryHandler, MessageHandler, ContextTypes, CommandHandler

from core.context import ChatContext
from core.config import get_value
from core.utils import dict_utils
from core.registry import get_command_handler, get_command, get_default_personality_prompt

chat_id = get_value('providers.telegram.chatId')

logger = logging.getLogger(__name__)

app: None or Application = None
schedules = []

class Command(Enum):
    PLAY_VOICE = '🔊'
    RETRY = '🔁'


def get_chat_id() -> None or int:
    return chat_id

def get_app() -> None or Application:
    return app


def __on_message(cb) -> Callable[[Update, ContextTypes.DEFAULT_TYPE], None]:

    async def handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        global chat_id
        if (chat_id is not None and update.effective_chat.id != chat_id):
            update.message.reply_text(
                'I\'m already in a conversation with someone else. Please try again later.')
            return
        chat_id = update.effective_chat.id
        await cb(update, context)

    return handler

def __on_callback_query(cb) -> None:
    
    processMessage = __on_message(cb)

    async def handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Parses the CallbackQuery and updates the message text."""
        query = update.callback_query

        # CallbackQueries need to be answered, even if no notification to the user is needed
        # Some clients may have trouble otherwise. See https://core.telegram.org/bots/api#callbackquery
        await query.answer()

        await processMessage(update, context)
        
    return handler

def connect(on_message) -> None:
    global app
    app = ApplicationBuilder().token(
        get_value('providers.telegram.apiKey')).build()
    app.add_handler(MessageHandler(None, __on_message(on_message)))
    for (commandName, when) in schedules:
        logger.info(
            f'Schedule job registered on running app: {commandName} at: {when}')
        # app.job_queue.run_once(get_handler(commandName), when)
        app.job_queue.run_daily(get_handler(commandName), when)
                
    app.add_handler(CallbackQueryHandler(__on_callback_query(on_message)))


    app.run_polling()
    # async with app:
    #     await app.start()
    #     await app.updater.start_polling()
    #     await asyncio.sleep(100)
    #     await app.updater.stop()
    #     await app.stop()


async def send_text_message(context: ChatContext, text: str, reply_to_message: Message = None) -> None:
    chat_id = get_chat_id()

    if (context.update is None and chat_id is None):
        logger.warning('No chat to send message to')
        return
    
    keyboard = [
        [InlineKeyboardButton('🔊', callback_data='🔊'), InlineKeyboardButton('🔁', callback_data='🔁')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    if (context.update is not None):
        if (reply_to_message is None):
            reply_to_message = context.update.message
            
        response = await reply_to_message.reply_markdown(text, reply_markup=reply_markup)
        return response

    if (chat_id is not None):
        response = await context.context.bot.send_message(chat_id, text, reply_markup=reply_markup)
        return response


def register_schedule_job(schedule: dict) -> None:
    commandName = dict_utils.get_value_from_dict(schedule, 'command', None)
    rule = dict_utils.get_value_from_dict(schedule, 'rule', None)
    if (commandName is None or rule is None):
        logger.warning('Invalid schedule: %s', schedule)
        return

    hours = dict_utils.get_value_from_dict(rule, 'hours', None)
    minutes = dict_utils.get_value_from_dict(rule, 'minutes', None)

    if (hours is None or minutes is None):
        logger.warning('Invalid schedule: %s', schedule)
        return

    timezone = pytz.timezone(
        get_value('common.timezone', 'Europe/Madrid')
    )

    now = datetime.today().astimezone(tz=timezone)
    then = datetime.combine(datetime.today(), time(
        hours, minutes))
    when = then.astimezone(tz=timezone)

    isBeforeNow = when < now

    if (isBeforeNow):
        when = when + timedelta(days=1)

    if (app is None):
        schedules.append((commandName, when))
        logger.info('Schedule job registered: %s', schedule)
        return

    logger.info(
        f'Schedule job registered on running app: {commandName} when: {when}')
    app.job_queue.run_once(get_handler(commandName), when)


def get_handler(commandName: str) -> callable:
    async def command_handler(ctx: ContextTypes.DEFAULT_TYPE):
        command = get_command(commandName)
        handler = get_command_handler(commandName)
        command['personality'] = get_default_personality_prompt()

        await handler(None, command, None, ctx)

    return command_handler


def register_schedule_jobs(schedules: list) -> None:
    for schedule in schedules:
        register_schedule_job(schedule)
