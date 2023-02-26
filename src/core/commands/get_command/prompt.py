
from core.registry.commands import get_fallback_command, get_public_command_names
from core.utils.dict import get_value_from_dict


def prompt(msg: str):
    fallback_command_name = get_value_from_dict(
        get_fallback_command(), "name", "Chat")
    commandsStr = ""

    for command in get_public_command_names():
        commandsStr += f'"{command}", '

    return f"""What's the command name for the following message given this list of commands? If you don't know, answer with "{fallback_command_name}"

Examples: 
Email Susan with the subject "Today's review" and the message "Can we reschedule this meeting?"
"Send Email"
How are you?
"Chat"

Commands: {commandsStr}

Message: {msg}"""
