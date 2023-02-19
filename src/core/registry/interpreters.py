
from logging import getLogger
from importlib import import_module

from core.utils import set_value_into_dict, get_value_from_dict

logger = getLogger(__name__)

interpreters: dict = {
    'ai': {
        'name': 'ai',
        'runner': 'core.interpreters.ai'
    }
}
active_interpreter: str = 'ai'


def register_interpreters(interpreters: list):
    for interpreter in interpreters:
        register_interpreter(interpreter)


def register_interpreter(interpreter: dict):
    name: str = get_value_from_dict(interpreter, 'name', 'default')
    set_value_into_dict(interpreters, name, interpreter)
    logger.info(
        f'registered interpreter: {name} with runnner: {interpreter["runner"]}')


def get_interpreter_names():
    return interpreters.keys()


def get_interpreter(name: str):
    return interpreters[name]


def get_interpreter_runner(name: str):
    interpreter = get_interpreter(name)

    if interpreter is None or interpreter["runner"] is None:
        return None

    module = import_module(interpreter["runner"])

    return module.run


def set_active_interpreter(name: str):
    global active_interpreter
    active_interpreter = name
    logger.info(f'switched to {name} mode')


def get_active_interpreter():
    return interpreters[active_interpreter]


def get_active_interpreter_runner():
    return get_interpreter_runner(active_interpreter)
