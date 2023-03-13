
from core.interpreters.langchain.ChatAgent import ChatAgent
from core.messages import add_message_json, get_last_messages_json

from core.adapters import telegram, elevenlabs
from core.config import get_value
from core.registry.personalities import default_personality

async def run(update: telegram.Update, context: telegram.ContextTypes.DEFAULT_TYPE) -> None:
    if update.message.reply_to_message and update.message.text == '🔊':
        voiceMessage = await elevenlabs.get_speech(update.message.reply_to_message.text)
        await update.message.reply_voice(voiceMessage, reply_to_message_id=update.message.reply_to_message.message_id)
        return
    
    history_array = get_last_messages_json(5)
    
    chat_agent = ChatAgent(history_array=history_array)

    reply = chat_agent.run(update.message.text)
    
    add_message_json(update.message.text, reply)

    await update.message.reply_text(reply)
