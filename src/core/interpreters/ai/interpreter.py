
from core.adapters.telegram import ContextTypes, Update

from core.registry import get_default_personality_prompt, get_command_handler


async def run(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    print('running ai interpreter')

    personality_prompt = get_default_personality_prompt()

    handle = get_command_handler('Chat')

    await handle({
        "message": update.message.text,
    }, update, {
        "personality": personality_prompt,
    }, context)
