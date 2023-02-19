
import asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes

from core.config import get_value


async def connect(onMessage) -> None:
    app = ApplicationBuilder().token(
        get_value('providers.telegram.apiKey')).build()
    app.add_handler(MessageHandler(None, onMessage))
    async with app:
        await app.start()
        await app.updater.start_polling()
        await asyncio.sleep(100)
        await app.updater.stop()
        await app.stop()
