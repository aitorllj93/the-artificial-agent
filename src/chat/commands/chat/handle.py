
import openai
from telegram import Update
from telegram.ext import ContextTypes

from core.messages import add_message, Message
from chat.commands.chat.prompt import prompt


def remove_prefix(text, prefix):
    if text.strip().startswith(prefix):
        return text[len(prefix):]
    return text


async def handle(
    params: dict,
    update: Update,
    command: dict,
    context: ContextTypes.DEFAULT_TYPE
):
    prompt_text = prompt(params['message'], update, command['personality'])

    print(prompt_text)

    completion = await openai.Completion.acreate(
        engine="text-davinci-003",
        prompt=prompt_text,
        temperature=0.7,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
    )

    print('completed')

    text = remove_prefix(completion.choices[0].text, 'bot:').strip()

    print(text)

    message = Message(
        text or 'I don\'t know what to say', 'bot', update.message.date
    )

    add_message(message)

    await update.message.reply_text(message.text)
