
import asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes

from config import config


async def connect(onMessage) -> None:
    app = ApplicationBuilder().token(
        config['providers']['telegram']['apiKey']).build()
    app.add_handler(MessageHandler(None, onMessage))
    async with app:
        await app.start()
        await app.updater.start_polling()
        await asyncio.sleep(100)
        await app.updater.stop()
        await app.stop()

# from telegram import Update
# from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes
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
