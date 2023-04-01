
import asyncio
import logging
import coloredlogs
from pydub import AudioSegment
from os import remove as remove_file
from typing import Any, Callable, Coroutine
import core.config as config
import core.registry as registry
from core.adapters import telegram, openai
from core.context import ChatContext

coloredlogs.install(
    fmt='%(asctime)s - %(name)s %(levelname)s %(message)s',
)

logging.basicConfig(
    level=logging.DEBUG,
)

logger = logging.getLogger()

registry.register_interpreters(config.get_value('interpreters', []))
registry.register_slash_commands(config.get_value('slashCommands', []))
registry.register_commands(config.get_value('commands', []))
registry.register_personalities(config.get_value('personalities', []))
telegram.register_schedule_jobs(config.get_value('schedules', []))

async def speech_to_text(update: telegram.Update, context: telegram.ContextTypes.DEFAULT_TYPE) -> str:
    bot = telegram.get_app().bot
    file = await bot.get_file(update.message.voice.file_id)
    ogg_file_path = file.file_id + '.ogg'
    mp3_file_path = file.file_id + '.mp3'
    await file.download_to_drive(ogg_file_path)
    AudioSegment.from_file(ogg_file_path).export(mp3_file_path, format='mp3')
    text = await openai.translate_audio(open(mp3_file_path, 'rb'))
    
    remove_file(ogg_file_path)
    remove_file(mp3_file_path)
    
    return text

async def run(update: telegram.Update, context: telegram.ContextTypes.DEFAULT_TYPE) -> None:
    runner: Callable[[ChatContext], Coroutine[Any, Any, str]] = registry.get_active_interpreter_runner()

    chat_context: ChatContext = None # type: ignore
    is_voice_message = update.message and update.message.voice
    text: str = update.message and update.message.text
        
    try:
        if (is_voice_message):
            text = await speech_to_text(update, context)
        
        chat_context = ChatContext(text=text, update=update, telegram=context)
        
        await runner(chat_context)
    except Exception as e:
        print(e)
        logger.exception(e)

telegram.connect(run)
