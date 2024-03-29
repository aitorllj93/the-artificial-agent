
import os
from yaml import safe_load
from dotenv import load_dotenv

from core.utils import dict_utils

load_dotenv()

# os.environ['OBSIDIAN_VAULT_PATH']

config = {}


def from_env(key, default=None):
    if (key not in os.environ):
        return default
    return os.environ[key]


def get_value(path, default=None):
    return dict_utils.get_value_from_dict(config, path, default)


with open("config/config.yml", mode="rt", encoding="utf-8") as file:
    config = safe_load(file)

    dict_utils.set_value_into_dict(config, 'providers.openai.apiKey', from_env(
        'OPENAI_API_KEY', get_value('providers.openai.apiKey')))

    dict_utils.set_value_into_dict(config, 'providers.telegram.apiKey',
                                   from_env('TELEGRAM_BOT_API_KEY', get_value('providers.telegram.apiKey')))

    dict_utils.set_value_into_dict(config, 'providers.obsidian.vault',
                                   from_env('OBSIDIAN_VAULT_PATH', get_value('providers.obsidian.vault')))

    dict_utils.set_value_into_dict(config, 'providers.elevenlabs.apiKey',
                                   from_env('ELEVENLABS_API_KEY', get_value('providers.elevenlabs.apiKey')))

    dict_utils.set_value_into_dict(config, 'providers.openweathermap.apiKey',
                                   from_env('OPENWEATHERMAP_API_KEY', get_value('providers.openweathermap.apiKey')))

    dict_utils.set_value_into_dict(config, 'providers.openweathermap.location',
                                   from_env('OPENWEATHERMAP_LOCATION', get_value('providers.openweathermap.location')))

    dict_utils.set_value_into_dict(config, 'providers.news.apiKey',
                                   from_env('NEWS_API_KEY', get_value('providers.news.apiKey')))
