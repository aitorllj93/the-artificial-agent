
from logging import getLogger
from utils import set_value_into_dict, get_value_from_dict
from config import get_value

logger = getLogger(__name__)

personalities: dict = {}
default_personality: str = None


def register_personality(personality: dict):
    name: str = get_value_from_dict(personality, 'name', 'default')
    set_value_into_dict(personalities, name, personality)
    logger.info(f'registered personality: {name}')

    is_default = get_value_from_dict(personality, 'isDefault', False)

    if is_default or len(personalities) == 1:
        global default_personality
        default_personality = name
        logger.info(f'default personality: {name}')


def register_personalities(personalities: list):
    for personality in personalities:
        register_personality(personality)


def get_personality_names():
    return personalities.keys()


def get_personality(name: str = None):
    if name is None:
        name = default_personality

    if name in personalities:
        return personalities[name]
    else:
        return None


def get_personality_prompt(name: str = None):
    personality = get_personality(name)

    if personality is None:
        return None
    else:
        return get_value_from_dict(personality, 'prompt', None)


def get_default_personality():
    return get_personality(default_personality)


def get_default_personality_prompt():
    return get_personality_prompt(default_personality)
