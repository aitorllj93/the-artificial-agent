
from core.adapters.telegram import Update
from core.adapters.openai import generate_text_from_prompt

from chat.commands.notify.prompt import prompt as notify_prompt

from notes.get_notes import get_today_daily_note
from notes.task import Task
from notes.commands.complete_task.prompt import prompt


async def handle(
    params: dict,
    update: Update,
    command: dict,
):
    note = await get_today_daily_note()

    tasks = note.list_tasks_from_section("Assistant")

    prompt_text = prompt(tasks, params['text'])

    taskToComplete = await generate_text_from_prompt(prompt_text, {
        "temperature": 0.1
    })

    taskIndex = int(taskToComplete)

    task = tasks[taskIndex]

    if (task is None):
        await update.message.reply_text("Task not found")
        return

    if (task.completed):
        await update.message.reply_text("Task already completed")
        return

    note.complete_task(task)

    notify_prompt_text = notify_prompt(
        f"""Task "{task.text}" completed""",
        command['personality']
    )

    notification = await generate_text_from_prompt(notify_prompt_text)

    await update.message.reply_text(notification)
