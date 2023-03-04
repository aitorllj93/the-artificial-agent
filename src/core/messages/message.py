# the message

class Message:

    text: str
    author: str
    date: str

    def __init__(self,  text: str = '', author: str = '', date: str = ''):
        self.text = text
        self.author = author
        self.date = date

    def __str__(self):
        return f'{self.date} | {self.author} | {self.text.strip()}'

    def fromString(self, string: str):
        self.date, self.author, self.text = string.split(' | ')
        return self

    def toPrompt(self):
        return f'{self.author}: {self.text}'

    def toChatGPT(self):
        return {
            "role": self.author,
            "content": self.text.replace('\n', '')
        }
