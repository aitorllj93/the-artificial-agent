# read messages from a text file and parses them into a list of messages.

from os.path import exists
from os import mkdir
import json

from core.messages.message import Message

_dataFolder = 'data'
_dataPath = f'{_dataFolder}/messages.txt'
_jsonPath = f'{_dataFolder}/messages.json'

messages = []
messagesJSON = []

if not exists(_dataFolder):
    mkdir(_dataFolder)

if not exists(_dataPath):
    with open(_dataPath, 'w') as f:
        f.write('')
        
if not exists(_jsonPath):
    with open(_jsonPath, 'w') as f:
        f.write('[]')

with open(_dataPath, 'r') as f:
    lines = f.readlines()

    for line in lines:
        message = Message().fromString(line)
        messages.append(message)

with open(_jsonPath, 'r') as f:
    messagesJSON = json.load(f)

def get_last_messages(n: int):
    return messages[-n:]


def add_message(message: Message):
    messages.append(message)
    with open(_dataPath, 'a') as f:
        f.write(f'{message}\n')

def get_last_messages_json(n: int):
    return messagesJSON[-n:]

def add_message_json(prompt: str, response: str):
    messagesJSON.append({
        "prompt": prompt,
        "response": response
    })
    with open(_jsonPath, 'w') as f:
        json.dump(messagesJSON, f)