
from core.adapters.openai import generate_text_from_prompt
from core.adapters.telegram import Update
from chat.commands.enumerate import prompt

from notes.get_notes import get_today_daily_note


async def handle(
    params: dict,
    update: Update,
    command: dict,
):
    note = await get_today_daily_note()

    tasks = note.list_tasks_from_section(
        "Assistant", params['completed'] or False)

    tasksStr = ''

    for index, task in enumerate(tasks):
        tasksStr += f'{index + 1}. {task.text}\n'

    prompt_text = prompt(
        tasksStr,
        command['personality']
    )

    message = await generate_text_from_prompt(prompt_text)

    await update.message.reply_text(message)
