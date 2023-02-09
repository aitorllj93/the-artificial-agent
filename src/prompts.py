
from datetime import datetime
from telegram import Update

from config import config
from messages.get_messages import getLastMessages


def getHourAndMinute():
    return datetime.now().strftime("%H:%M")


def getChatPrompt(message, update: Update, personality):
    previousMessagesPrompt = ''

    for i in getLastMessages(5):
        print(i)
        previousMessagesPrompt += f'{i.toPrompt()}\n'

    return f"""{personality} It's {getHourAndMinute()}. My name is {config['common']['user']['name']}, and I'm the author of the document.

Previous Messages:
{previousMessagesPrompt}

Answer the following message from the author: {message}
  """
