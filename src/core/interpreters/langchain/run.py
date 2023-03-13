
import logging
import coloredlogs
from core.interpreters.langchain.ChatAgent import ChatAgent

from core.adapters import telegram, elevenlabs

coloredlogs.install(
    fmt='%(asctime)s - %(name)s %(levelname)s %(message)s',
)

logging.basicConfig(
    level=logging.DEBUG,
)

logger = logging.getLogger()


async def run(update: telegram.Update, context: telegram.ContextTypes.DEFAULT_TYPE) -> None:
    if update.message.reply_to_message and update.message.text == '🔊':
        voiceMessage = await elevenlabs.get_speech(update.message.reply_to_message.text)
        await update.message.reply_voice(voiceMessage, reply_to_message_id=update.message.reply_to_message.message_id)
        return

    chat_agent = ChatAgent(history_array=[])

    reply = chat_agent.run(update.message.text)

    await update.message.reply_text(reply)
