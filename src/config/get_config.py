
import os
from yaml import safe_load
from dotenv import load_dotenv

load_dotenv()

# os.environ['OBSIDIAN_VAULT_PATH']

with open("config/config.yml", mode="rt", encoding="utf-8") as file:
    config = safe_load(file)

    config['providers']['openai'] = config['providers']['openai'] or {}
    config['providers']['telegram'] = config['providers']['telegram'] or {}
    config['providers']['obsidian'] = config['providers']['obsidian'] or {}
    config['providers']['elevenlabs'] = config['providers']['elevenlabs'] or {}

    config['providers']['openai']['apiKey'] = os.environ['OPENAI_API_KEY'] or config['providers']['openai']['apiKey']
    config['providers']['telegram']['apiKey'] = os.environ['TELEGRAM_BOT_API_KEY'] or config['providers']['telegram']['apiKey']
    config['providers']['obsidian']['vault'] = os.environ['OBSIDIAN_VAULT_PATH'] or config['providers']['obsidian']['vault']
    config['providers']['elevenlabs']['apiKey'] = os.environ['ELEVENLABS_API_KEY'] or config['providers']['elevenlabs']['apiKey']
