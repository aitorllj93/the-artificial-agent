# read messages from a text file and parses them into a list of messages.

from os.path import exists
from os import mkdir

from messages.message import Message

_dataFolder = 'data'
_dataPath = f'{_dataFolder}/messages.txt'

messages = []

if not exists(_dataFolder):
    mkdir(_dataFolder)

if not exists(_dataPath):
    with open(_dataPath, 'w') as f:
        f.write('')

with open(_dataPath, 'r') as f:
    lines = f.readlines()

    for line in lines:
        message = Message().fromString(line)
        messages.append(message)


def get_last_messages(n: int):
    return messages[-n:]


def add_message(message: Message):
    messages.append(message)
    with open(_dataPath, 'a') as f:
        f.write(f'{message}\n')
