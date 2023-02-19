
import asyncio
import logging
import config
import engine
import bot

logger = logging.getLogger()
level = logging.INFO
logger.setLevel(level)
for handler in logger.handlers:
    handler.setLevel(level)

engine.register_interpreters(config.get_value('interpreters', {}))
engine.register_slash_commands(config.get_value('slashCommands', {}))
engine.register_commands(config.get_value('commands', {}))
engine.register_personalities(config.get_value('personalities', {}))


async def main() -> None:
    await bot.connect(engine.run)


asyncio.run(main())


# await index.save_to_disk('index.json')
# todayDailyNote = await get_today_daily_note()
# scheduledTasks = todayDailyNote.list_tasks_from_section('Schedule')

# for i, task in enumerate(scheduledTasks):
#     print(task)
#    if (i == 0):
#       print(task.childContent)

# print(
#     '\n'.join(
#         map(
#             lambda t: t.__str__(),
#             scheduledTasks
#         )
#     ))

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
