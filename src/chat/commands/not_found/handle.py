from core.adapters.telegram import Update, ContextTypes


async def handle(
    params: dict,
    update: Update,
    command: dict,
    context: ContextTypes.DEFAULT_TYPE
):
    await update.message.reply_text('I don\'t know what to say')
