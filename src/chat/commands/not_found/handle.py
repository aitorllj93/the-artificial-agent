from core.adapters import telegram


async def handle(
    params: dict,
    command: dict,
    update: telegram.Update,
    context: telegram.ContextTypes.DEFAULT_TYPE
):
    await telegram.send_text_message(update, context, 'I don\'t know what to say')
