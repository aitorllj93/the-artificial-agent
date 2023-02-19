
import asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes

from config import config


async def connect(onMessage) -> None:
    app = ApplicationBuilder().token(
        config['providers']['telegram']['apiKey']).build()
    app.add_handler(MessageHandler(None, onMessage))
    async with app:
        await app.start()
        await app.updater.start_polling()
        await asyncio.sleep(100)
        await app.updater.stop()
        await app.stop()
