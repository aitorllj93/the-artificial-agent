
import json

from core.adapters import elevenlabs, telegram, openai
from core.messages import Message, add_message

from core.registry import get_default_personality_prompt, get_slash_command_handler, get_slash_command, get_command, get_command_handler, get_command_names, get_fallback_commmand_name

from core.commands.get_command import prompt as get_command_prompt
from core.commands.get_parameters import prompt as get_parameters_prompt


async def _run_slash_command(update: telegram.Update, context: telegram.ContextTypes.DEFAULT_TYPE) -> None:
    words = map(lambda word: word.strip(), update.message.text.split(' '))
    commandName = words[0][1:]
    params = words[1:]

    command = get_slash_command(commandName)
    handle = get_slash_command_handler(commandName)

    paramsDict = {}

    for index, param in enumerate(command['parameters']):
        paramsDict[param] = params[index]

    await handle(paramsDict, update, command, context)


async def _get_ai_command_name(update: telegram.Update) -> str:
    prompt_text = get_command_prompt(update.message.text)
    command_names = get_command_names()

    text = await openai.generate_text_from_prompt(prompt_text, {
        "temperature": 0
    })

    text = text.replace('"', '')

    command_name = get_fallback_commmand_name()

    for name in command_names:
        if name in text:
            command_name = name
            break

    return command_name


async def get_ai_command_parameters(command: dict, update: telegram.Update) -> dict:
    if command['name'] == get_fallback_commmand_name():
        return {
            "message": update.message.text
        }

    prompt_text = get_parameters_prompt(update.message.text, command)

    text = await openai.generate_text_from_prompt(prompt_text)

    return json.loads(text)


async def run(update: telegram.Update, context: telegram.ContextTypes.DEFAULT_TYPE) -> None:
    if update.message.reply_to_message and update.message.text == '🔊':
        voiceMessage = await elevenlabs.get_speech(update.message.reply_to_message.text)
        await update.message.reply_voice(voiceMessage, reply_to_message_id=update.message.reply_to_message.message_id)
        return

    if update.message.text[0] == '/':
        return await _run_slash_command(update, context)

    add_message(Message(update.message.text,
                        "author", update.message.date))

    command_name = await _get_ai_command_name(update)
    command = get_command(command_name)
    parameters = await get_ai_command_parameters(command, update)
    handle = get_command_handler(command_name)

    command["personality"] = get_default_personality_prompt()

    await handle(parameters, update, command, context)
