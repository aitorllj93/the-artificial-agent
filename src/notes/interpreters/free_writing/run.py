

from core.adapters.telegram import ContextTypes, Update
from core.adapters.openai import generate_text_from_prompt

from core.registry import get_slash_command_handler, get_slash_command

from notes.get_notes import get_today_daily_note
from notes.commands.complete_text import prompt


async def _run_slash_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    words = map(lambda word: word.strip(), update.message.text.split(' '))
    commandName = words[0][1:]
    params = words[1:]

    command = get_slash_command(commandName)
    handle = get_slash_command_handler(commandName)

    paramsDict = {}

    for index, param in enumerate(command['parameters']):
        paramsDict[param] = params[index]

    await handle(paramsDict, update, command, context)


async def run(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.message.text[0] == '/':
        return await _run_slash_command(update, context)

    note = await get_today_daily_note()

    note.append_to_section("Free Writing", update.message.text)

    prompt_text = prompt(update.message.text)

    suggestion = await generate_text_from_prompt(prompt_text)

    await update.message.reply_text(suggestion)
