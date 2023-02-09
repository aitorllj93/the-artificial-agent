
from config import config

commands = config['commands']

fallbackCommand = next(
    (i for i in commands if 'asFallback' in i and i['asFallback']), config['commands'][0])


def getCommandNames():
    return [i['name'] for i in commands]


def getCommand(name=None):
    return next((i for i in commands if i['name'] == name), fallbackCommand)


def getCommandHandler(name=None):
    handlerName = getCommand(name)['handler']
    return getattr(__import__(f'commandHandlers.{handlerName}'), handlerName)
