
from notes.task import Task


def prompt(tasks: list, text: str):
    tasksStr = ''

    for index, task in enumerate(tasks):
        tasksStr += f'{index + 1}. {task.text}\n'

    return f"""Answer only with the number of the task to be completed. There's only one correct answer:

{tasksStr}

message: {text}
"""
