
class Task:

    def __init__(self, text: str = '', completed: bool = False, scheduled: str = None, raw: str = None):

        self.text = text
        self.completed = completed
        self.scheduled = scheduled
        self.raw = raw
        self.childContent = ''

    def from_md(self, raw: str) -> 'Task':
        lines = raw.splitlines()

        task = None

        children = []
        for (i, line) in enumerate(lines):
            if i == 0:
                task = self.from_line(line)
            else:
                children.append(line)

        task.raw = raw
        task.childContent = '\n'.join(children)

        return task

    def from_line(self, task: str) -> 'Task':
        if task.startswith("- ["):
            completed = task.startswith("- [x]")
            body = task[5:].strip()
        else:
            completed = False
            body = task[2:].strip()

        if (body[2] == ":"):
            scheduled = body[:5]
            text = body[6:]
        else:
            scheduled = None
            text = body

        return Task(text, completed, scheduled)

    def to_md(self) -> str:
        return ' '.join(
            filter(lambda x: x != '',
                   [
                       '-',
                       '[x]' if self.completed else '[ ]',
                       self.scheduled if self.scheduled else '',
                       self.text
                   ])
        )

    def __str__(self):
        return self.to_md()
