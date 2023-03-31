from datetime import datetime
import logging

from core.context import ChatContext
from core.adapters import telegram, openai
from core.messages import add_message, Message

from chat.commands.good_night.prompt import prompt

logger = logging.getLogger(__name__)


async def handle(
    params: dict,
    command: dict,
    context: ChatContext,
):
    chat_id = telegram.get_chat_id()
    if (context.update is None and chat_id is None):
        logger.warning('No chat to send message to')
        return

    prompt_text = prompt(command['personality'])

    text = await openai.generate_text_from_prompt(prompt_text)

    date = context.update.message.date if context.update is not None else datetime.now()

    message = Message(
        text or 'I don\'t know what to say', 'assistant', date
    )

    add_message(message)

    await telegram.send_text_message(context, message.text)
