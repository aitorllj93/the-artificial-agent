
import config

from telegram import Update
from telegram.ext import ContextTypes
import openai

from bot import connect

from personalities import getPersonalityPrompt, getPersonality
from commands import getCommandNames
from messages import getLastMessages, addMessage, Message
from prompts import getChatPrompt

from text_to_speech import get_speech


def remove_prefix(text, prefix):
    if text.strip().startswith(prefix):
        return text[len(prefix):]
    return text


async def onMessage(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:

    if (update.message.reply_to_message and update.message.text == '🔊'):
        voiceMessage = await get_speech(update.message.reply_to_message.text)
        await update.message.reply_voice(voiceMessage, reply_to_message_id=update.message.reply_to_message.message_id)
        return

    if (update.message.text.startswith('/')):
        return

    addMessage(Message(update.message.text, "author", update.message.date))

    personality = getPersonality()

    print(personality)

    prompt = getChatPrompt(update.message.text, update, personality['prompt'])

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
        text or 'I don\'t know what to say', 'bot', update.message.date)

    addMessage(message)

    await update.message.reply_text(message.text)

#    await update.get_bot().send_voice(update.message.chat_id, voiceMessage)


connect(onMessage)
# from prompts import getChatPrompt
# from gpt_index import GPTSimpleVectorIndex, ObsidianReader
# import openai
# import os
# import sys
# import logging
# from dotenv import load_dotenv
# load_dotenv()

# personality = "You're Alfred Pennyworth, Bruce Wayne's loyal and tireless butler. You're now working for me. You help me with everything. Express yourself according to the character."


# logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
# logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))

# documents = ObsidianReader(os.environ['OBSIDIAN_VAULT_PATH']).load_data()

# # index = GPTSimpleVectorIndex(documents)

# index = GPTSimpleVectorIndex.load_from_disk('index.json')

# res = index.query(f"""{personality}

# question: Is the author working on Artificial Intelligence?""")

# print(res)


# async def onMessage(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
#     prompt = getChatPrompt(update.message.text, update, personality)

#     print(prompt)

#     completion = await openai.Completion.acreate(
#         engine="text-davinci-003",
#         prompt=prompt,
#         temperature=0.7,
#         max_tokens=256,
#         top_p=1,
#         frequency_penalty=0,
#         presence_penalty=0,
#     )

#     print('completed')
#     print(completion.choices[0].text)

#     await update.message.reply_text(completion.choices[0].text or 'I don\'t know what to say')

# # app = ApplicationBuilder().token(os.environ['TELEGRAM_BOT_API_KEY']
# #                                  ).build()

# # app.add_handler(MessageHandler(None, onMessage))

# # app.run_polling()
