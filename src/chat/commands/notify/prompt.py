
def prompt(text: str, personality: str):
    return f"""{personality} Tell me that you successfully ran the following command:
  
Example: Note "Hello World" added to daily notes
Added "Hello World" into your daily notes!


Command: {text}
"""
