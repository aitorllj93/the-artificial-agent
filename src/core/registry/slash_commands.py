
from logging import getLogger
from core.utils import set_value_into_dict, get_value_from_dict
from importlib import import_module

logger = getLogger(__name__)

slash_commands: dict = {}


def register_slash_command(slash_command: dict):
    name: str = get_value_from_dict(slash_command, 'name', 'default')
    set_value_into_dict(slash_commands, name, slash_command)
    logger.info(
        f'registered slash command: {name} with handler {slash_command["handler"]}')


def register_slash_commands(slash_commands: list):
    for slash_command in slash_commands:
        register_slash_command(slash_command)


def get_slash_command_names():
    return slash_commands.keys()


def get_slash_command(name: str):
    if name.startswith('/'):
        name = name[1:]

    return slash_commands[name] or None


def get_slash_command_handler(name: str):
    slash_command = get_slash_command(name)

    if slash_command is None or slash_command['handler'] is None:
        return None

    module = import_module(slash_command['handler'])

    return module.handle
