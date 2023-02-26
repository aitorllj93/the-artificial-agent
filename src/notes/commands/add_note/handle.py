
from core.adapters.telegram import Update
from core.adapters.openai import generate_text_from_prompt

from chat.commands.notify.prompt import prompt

from notes.get_notes import get_today_daily_note


async def handle(
    params: dict,
    update: Update,
    command: dict,
):
    note = await get_today_daily_note()

    note.append_to_section("Assistant", params['text'])

    prompt_text = prompt(
        f"""Note "{params['text']}" added to daily notes""", command['personality'])

    notification = await generate_text_from_prompt(prompt_text)

    await update.message.reply_text(notification)
