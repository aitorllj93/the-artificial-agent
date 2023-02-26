
from core.adapters import telegram, openai

from chat.commands.notify.prompt import prompt

from notes.get_notes import get_today_daily_note


async def handle(
    params: dict,
    command: dict,
    update: telegram.Update,
    context: telegram.ContextTypes.DEFAULT_TYPE
):
    note = await get_today_daily_note()

    note.append_to_section("Assistant", params['text'])

    prompt_text = prompt(
        f"""Note "{params['text']}" added to daily notes""", command['personality'])

    notification = await openai.generate_text_from_prompt(prompt_text)

    await telegram.send_text_message(update, context, notification)
