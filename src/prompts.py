from telegram import Update

from messages.get_messages import getLastMessages


def getChatPrompt(message, update: Update, personality):
    previousMessagesPrompt = ''

    for i in getLastMessages(5):
        print(i)
        previousMessagesPrompt += f'{i.toPrompt()}\n'

    return f"""{personality}

Previous Messages:
{previousMessagesPrompt}

Answer the following message: {message}
  """
