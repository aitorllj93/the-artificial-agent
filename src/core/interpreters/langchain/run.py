
from logging import getLogger
from typing import Callable

from core.interpreters.langchain.ChatAgent import ChatAgent
from core.messages import add_message_json, get_last_messages_json, get_prompt_from_message
from core.adapters import telegram, elevenlabs
from core.context import ChatContext
from core.config import get_config

logger = getLogger(__name__)

return_as_audio = get_config('common.alwaysGenerateAudio', False)

async def get_speech_for_text(text: str) -> str:
    speech = await elevenlabs.get_speech(text)
    return speech
    
async def reply_with_voice(voiceMessage, reply_to_message: telegram.Message, ctx: ChatContext) -> None:
    await reply_to_message.reply_voice(voiceMessage, reply_to_message_id=reply_to_message.message_id)
    return 

async def play_voice(context: ChatContext, reply_to_message: telegram.Message, text: str) -> None:
    speech = await get_speech_for_text(text)
    await reply_with_voice(speech, reply_to_message=reply_to_message, ctx=context)
    return

async def answer(context: ChatContext, reply_to_message: telegram.Message) -> None:
    logger.info('Answering to message: %s', context.text)
    last_messages = get_last_messages_json(5)
    
    chat_agent = ChatAgent(history_array=last_messages)

    reply = chat_agent.run(context.text)
    
    logger.info('Reply: %s', reply)
    
    add_message_json(context.text, reply)
    
    response = await telegram.send_text_message(context, reply, reply_to_message=reply_to_message)
    
    if (return_as_audio):
        print(response)
        logger.info('Playing voice for: %s', response.text)
        await play_voice(context, response, text=response.text)
        return

async def run(context: ChatContext) -> None:
    logger.info('Running interpreter')
    
    is_callback_query = context.update.callback_query is not None
    query_data = context.update.callback_query.data if is_callback_query else None
    
    
    reply_to_message = context.update.message
        
    if (query_data == '🔊'):
        reply_to_message = context.update.callback_query.message
        logger.info('Playing voice for: %s', reply_to_message.text)
        await play_voice(context, reply_to_message, text=reply_to_message.text)
        return
    
    if (query_data == '🔁'):
        selected_message = context.update.callback_query.message
        reply_to_message = selected_message
        context.text = get_prompt_from_message(selected_message.text)
        logger.info('Repeating message for: %s', context.text)
    
    await answer(context, reply_to_message=reply_to_message)
    