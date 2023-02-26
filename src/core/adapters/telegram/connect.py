
import asyncio
from datetime import datetime, time
import pytz
import logging
from telegram import Update, Chat
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, CommandHandler

from core.config import get_value
from core.utils import dict_utils
from core.registry import get_command_handler, get_command, get_default_personality_prompt

chat_id = get_value('providers.telegram.chatId')

logger = logging.getLogger(__name__)

app: None or ApplicationBuilder = None
schedules = []


def get_chat_id() -> None or int:
    return chat_id


def __on_message(cb) -> None:

    async def handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
        global chat_id
        if (chat_id is not None and update.effective_chat.id != chat_id):
            update.message.reply_text(
                'I\'m already in a conversation with someone else. Please try again later.')
            return
        chat_id = update.effective_chat.id
        await cb(update, context)

    return handler


def connect(on_message) -> None:
    global app
    app = ApplicationBuilder().token(
        get_value('providers.telegram.apiKey')).build()
    app.add_handler(MessageHandler(None, __on_message(on_message)))
    for (commandName, when) in schedules:
        logger.info(
            f'Schedule job registered on running app: {commandName} at: {when}')
        app.job_queue.run_once(get_handler(commandName), when)

    app.run_polling()

    # async with app:
    #     await app.start()
    #     await app.updater.start_polling()
    #     await asyncio.sleep(100)
    #     await app.updater.stop()
    #     await app.stop()


async def send_text_message(update: Update or None, context: ContextTypes.DEFAULT_TYPE or None, text: str) -> None:
    chat_id = get_chat_id()

    if (update is None and chat_id is None):
        logger.warning('No chat to send message to')
        return

    if (update is not None):
        await update.message.reply_text(text)
        return

    if (chat_id is not None):
        await context.bot.send_message(chat_id, text)
        return


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
        return

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
