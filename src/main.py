
from messages import addMessage, Message
from engine import get_active_interpreter_runner, register_slash_commands, register_commands, register_interpreters, register_personalities
from text_to_speech import get_speech
from bot import connect
from config import get_value
from telegram.ext import ContextTypes
from telegram import Update
import asyncio
import logging
logging.getLogger().setLevel(logging.DEBUG)


register_interpreters(get_value('interpreters', {}))
register_slash_commands(get_value('slashCommands', {}))
register_commands(get_value('commands', {}))
register_personalities(get_value('personalities', {}))


async def main() -> None:

    runner = get_active_interpreter_runner()

    await connect(onMessage)


async def onMessage(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if (update.message.reply_to_message and update.message.text == '🔊'):
        voiceMessage = await get_speech(update.message.reply_to_message.text)
        await update.message.reply_voice(voiceMessage, reply_to_message_id=update.message.reply_to_message.message_id)
        return

    if (update.message.text.startswith('/')):
        return

    addMessage(Message(update.message.text, "author", update.message.date))

    runner = get_active_interpreter_runner()

    await runner(update, context)


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
