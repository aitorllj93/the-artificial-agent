
from datetime import datetime
from core.adapters.telegram import Update

from core.config import config
from core.messages import get_last_messages


def get_hour_and_minute():
    return datetime.now().strftime("%H:%M")


def prompt(message, update: Update, personality):
    previousMessagesPrompt = ''

    for i in get_last_messages(5):
        print(i)
        previousMessagesPrompt += f'{i.toPrompt()}\n'

    # return f"""{personality} It's {get_hour_and_minute()}. My name is {config['common']['user']['name']}, and I'm the author of the document.

# # Previous Messages:
# # {previousMessagesPrompt}

# # Answer the following message from the author: {message}
#   """
    return message
