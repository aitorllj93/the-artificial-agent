
from telegram import Update
from telegram.ext import ContextTypes

class ChatContext:
  
  text: str
  author: str
  date: str
  update: Update or None # type: ignore
  context: ContextTypes.DEFAULT_TYPE or None # type: ignore
  telegram: ContextTypes.DEFAULT_TYPE or None # type: ignore
  
  def __init__(self,  text: str = '', author: str = '', date: str = '', update: Update = None, telegram: ContextTypes.DEFAULT_TYPE = None): # type: ignore
      self.text = text
      self.author = author
      self.date = date
      self.update = update
      self.context = telegram
      self.telegram = telegram