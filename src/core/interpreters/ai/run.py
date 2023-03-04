
import json
import logging

from core.adapters import elevenlabs, telegram, openai
from core.messages import Message, add_message

import core.registry as registry

from core.commands.get_command import prompt as get_command_prompt
from core.commands.get_parameters import prompt as get_parameters_prompt

logger = logging.getLogger(__name__)


async def _run_slash_command(update: telegram.Update, context: telegram.ContextTypes.DEFAULT_TYPE) -> None:
    words = map(lambda word: word.strip(), update.message.text.split(' '))
    commandName = words[0][1:]
    params = words[1:]

    command = registry.get_slash_command(commandName)
    handle = registry.get_slash_command_handler(commandName)

    paramsDict = {}

    for index, param in enumerate(command['parameters']):
        paramsDict[param] = params[index]

    logger.info(
        f'Running slash command {commandName} with params {paramsDict}')

    await handle(paramsDict, update, command, context)


async def _get_ai_command_name(update: telegram.Update) -> str:
    prompt_text = get_command_prompt(update.message.text)
    command_names = registry.get_public_command_names()

    logger.debug(f'Prompt text: {prompt_text}')

    text = await openai.generate_text_from_prompt(prompt_text, {
        "temperature": 0
    })

    logger.debug(f'Generated text: {text}')

    text = text.replace('"', '')

    command_name = registry.get_fallback_commmand_name()

    logger.debug(f'Fallback command name: {command_name}')

    for name in command_names:
        if name in text:
            print()
            command_name = name
            break

    logger.debug(f'Command name: {command_name}')

    return command_name


async def get_ai_command_parameters(command: dict, update: telegram.Update) -> dict:
    if command['name'] == registry.get_fallback_commmand_name():
        return {
            "message": update.message.text
        }

    prompt_text = get_parameters_prompt(update.message.text, command)

    logger.debug(f'Prompt text: {prompt_text}')

    text = await openai.generate_text_from_prompt(prompt_text)

    logger.debug(f'Generated text: {text}')

    return json.loads(text)


async def run(update: telegram.Update, context: telegram.ContextTypes.DEFAULT_TYPE) -> None:
    if update.message.reply_to_message and update.message.text == '🔊':
        voiceMessage = await elevenlabs.get_speech(update.message.reply_to_message.text)
        await update.message.reply_voice(voiceMessage, reply_to_message_id=update.message.reply_to_message.message_id)
        return

    if update.message.text[0] == '/':
        return await _run_slash_command(update, context)

    add_message(Message(update.message.text,
                        "user", update.message.date))

    command_name = await _get_ai_command_name(update)

    command = registry.get_command(command_name)
    parameters = await get_ai_command_parameters(command, update)
    handle = registry.get_command_handler(command_name)

    command["personality"] = registry.get_default_personality_prompt()

    logger.info(f'Running command {command_name} with params {parameters}')

    await handle(parameters, command, update, context)
