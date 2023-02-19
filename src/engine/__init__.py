
from telegram import Update
from telegram.ext import ContextTypes
from engine.personalities import register_personalities, get_default_personality, get_default_personality_prompt, get_personality, get_personality_prompt, get_personality_names
from engine.interpreters import register_interpreters, get_interpreter, get_interpreter_runner, get_interpreter_names, get_active_interpreter, set_active_interpreter, get_active_interpreter_runner
from engine.commands import register_commands, get_command, get_command_handler, get_command_names
from engine.slash_commands import register_slash_commands, get_slash_command, get_slash_command_handler, get_slash_command_names

from messages import add_message, Message
from text_to_speech import get_speech


async def run(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if (update.message.reply_to_message and update.message.text == '🔊'):
        voiceMessage = await get_speech(update.message.reply_to_message.text)
        await update.message.reply_voice(voiceMessage, reply_to_message_id=update.message.reply_to_message.message_id)
        return

    if (update.message.text.startswith('/')):
        return

    add_message(Message(update.message.text, "author", update.message.date))

    runner = get_active_interpreter_runner()

    await runner(update, context)
