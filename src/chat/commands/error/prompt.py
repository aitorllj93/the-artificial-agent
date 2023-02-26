
def prompt(text: str, personality: str):
    return f"""{personality} Tell me that you failed running the following command:
  
Example: Note "Hello World" added to daily notes
Failed to add "Hello World" into your daily notes!


Command: {text}

"""
