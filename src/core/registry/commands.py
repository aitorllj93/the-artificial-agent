
from logging import getLogger
from core.utils import set_value_into_dict, get_value_from_dict
from importlib import import_module

logger = getLogger(__name__)

commands: dict = {}
fallback_command: str = None


def register_command(command: dict):
    name: str = get_value_from_dict(command, 'name', 'default')
    set_value_into_dict(commands, name, command)
    logger.info(
        f'registered command: {name} with handler {command["handler"]}')

    as_fallback = get_value_from_dict(command, 'asFallback', False)

    if as_fallback:
        global fallback_command
        fallback_command = name
        logger.info(f'registered fallback command: {name}')


def register_commands(commands: list):
    for command in commands:
        register_command(command)


def get_command_names():
    return commands.keys()


def get_command(name: str):
    if name in commands:
        return commands[name]
    else:
        return commands[fallback_command]


def get_command_handler(name: str):
    command = get_command(name)

    if command is None or command['handler'] is None:
        return None

    module = import_module(command['handler'])

    return module.handle


def get_fallback_command():
    return get_command(fallback_command)


def get_fallback_command_handler():
    return get_command_handler(fallback_command)


def get_fallback_commmand_name():
    return get_value_from_dict(get_fallback_command(), 'name', 'Chat')
