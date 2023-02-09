
from config import config

personalities = config['personalities']

defaultPersonality = next(
    (i for i in personalities if 'isDefault' in i and i['isDefault']), config['personalities'][0])


def getPersonalityNames():
    return [i['name'] for i in personalities]


def getPersonality(name=None):
    return next((i for i in personalities if i['name'] == name), defaultPersonality)


def getPersonalityPrompt(name=None):
    return getPersonality(name)['prompt']
