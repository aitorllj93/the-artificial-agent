
import os
from yaml import safe_load
from dotenv import load_dotenv

from utils import get_value_from_dict, set_value_into_dict

load_dotenv()

# os.environ['OBSIDIAN_VAULT_PATH']

config = {}


def get_value(path, default=None):
    return get_value_from_dict(config, path, default)


with open("config/config.yml", mode="rt", encoding="utf-8") as file:
    config = safe_load(file)

    set_value_into_dict(config, 'providers.openai.apiKey',
                        os.environ['OPENAI_API_KEY'] or get_value('providers.openai.apiKey'))

    set_value_into_dict(config, 'providers.telegram.apiKey',
                        os.environ['TELEGRAM_BOT_API_KEY'] or get_value('providers.telegram.apiKey'))

    set_value_into_dict(config, 'providers.obsidian.vault',
                        os.environ['OBSIDIAN_VAULT_PATH'] or get_value('providers.obsidian.vault'))

    set_value_into_dict(config, 'providers.elevenlabs.apiKey',
                        os.environ['ELEVENLABS_API_KEY'] or get_value('providers.elevenlabs.apiKey'))

    set_value_into_dict(config, 'providers.openweathermap.apiKey',
                        os.environ['OPENWEATHERMAP_API_KEY'] or get_value('providers.openweathermap.apiKey'))

    set_value_into_dict(config, 'providers.openweathermap.location',
                        os.environ['OPENWEATHERMAP_LOCATION'] or get_value('providers.openweathermap.location'))
