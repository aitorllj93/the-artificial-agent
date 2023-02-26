from core.adapters.telegram import Update, ContextTypes
from core.adapters.openai import generate_text_from_prompt
from core.messages import add_message, Message

from chat.commands.good_morning.prompt import prompt


async def handle(
    params: dict,
    update: Update,
    command: dict,
    context: ContextTypes.DEFAULT_TYPE
):
    prompt_text = prompt(command['personality'])

    text = await generate_text_from_prompt(prompt_text)

    message = Message(
        text or 'I don\'t know what to say', 'bot', update.message.date
    )

    add_message(message)

    await update.message.reply_text(message.text)
