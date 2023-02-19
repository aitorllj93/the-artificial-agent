
import openai
from telegram import Update
from telegram.ext import ContextTypes

from engine.personalities import get_default_personality_prompt
from prompts import getChatPrompt
from messages import addMessage, Message


def remove_prefix(text, prefix):
    if text.strip().startswith(prefix):
        return text[len(prefix):]
    return text


async def run(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    print('running ai interpreter')

    personality_prompt = get_default_personality_prompt()

    print(personality_prompt)

    prompt = getChatPrompt(update.message.text, update, personality_prompt)

    print(prompt)

    completion = await openai.Completion.acreate(
        engine="text-davinci-003",
        prompt=prompt,
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

    addMessage(message)

    await update.message.reply_text(message.text)
