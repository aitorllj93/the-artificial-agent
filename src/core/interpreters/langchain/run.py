
from core.interpreters.langchain.ChatAgent import ChatAgent
from core.messages import add_message_json, get_last_messages_json

from core.adapters import telegram, elevenlabs
from core.context import ChatContext

async def run(context: ChatContext) -> None:
    # TODO: Refactor this function
    if context.update.message.reply_to_message and context.update.message.text == '🔊':
        voiceMessage = await elevenlabs.get_speech(context.update.message.reply_to_message.text)
        await context.update.message.reply_voice(voiceMessage, reply_to_message_id=context.update.message.reply_to_message.message_id)
        return
    
    history_array = get_last_messages_json(5)
    
    chat_agent = ChatAgent(history_array=history_array)

    reply = chat_agent.run(context.text)
    
    add_message_json(context.text, reply)

    await telegram.send_text_message(context, reply)