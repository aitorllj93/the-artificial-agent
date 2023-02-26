
from core.adapters import telegram, openai

from chat.commands.notify.prompt import prompt as notify_prompt

from notes.get_notes import get_today_daily_note
from notes.task import Task
from notes.commands.complete_task.prompt import prompt


async def handle(
    params: dict,
    command: dict,
    update: telegram.Update,
    context: telegram.ContextTypes.DEFAULT_TYPE
):
    note = await get_today_daily_note()

    tasks = note.list_tasks_from_section("Assistant")

    prompt_text = prompt(tasks, params['text'])

    taskToComplete = await openai.generate_text_from_prompt(prompt_text, {
        "temperature": 0.1
    })

    taskIndex = int(taskToComplete)

    task = tasks[taskIndex]

    if (task is None):
        await telegram.send_text_message(update, context, "Task not found")
        return

    if (task.completed):
        await telegram.send_text_message(update, context, "Task already completed")
        return

    note.complete_task(task)

    notify_prompt_text = notify_prompt(
        f"""Task "{task.text}" completed""",
        command['personality']
    )

    notification = await openai.generate_text_from_prompt(notify_prompt_text)

    await telegram.send_text_message(update, context, notification)
