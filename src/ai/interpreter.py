
from telegram import Update
from telegram.ext import ContextTypes

from engine.personalities import get_default_personality_prompt
from engine.commands import get_command_handler


async def run(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    print('running ai interpreter')

    personality_prompt = get_default_personality_prompt()

    handle = get_command_handler('Chat')

    await handle({
        "message": update.message.text,
    }, update, {
        "personality": personality_prompt,
    }, context)
