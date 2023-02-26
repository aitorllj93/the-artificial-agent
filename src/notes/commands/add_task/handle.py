
from core.adapters.telegram import Update
from core.adapters.openai import generate_text_from_prompt

from chat.commands.notify.prompt import prompt

from notes.get_notes import get_today_daily_note
from notes.task import Task


async def handle(
    params: dict,
    update: Update,
    command: dict,
):
    note = await get_today_daily_note()

    task = Task(params['text'])

    note.add_task_to_section("Assistant", task)

    prompt_text = prompt(
        f"""Task "{params['text']}" added to daily notes""", command['personality'])

    notification = await generate_text_from_prompt(prompt_text)

    await update.message.reply_text(notification)
