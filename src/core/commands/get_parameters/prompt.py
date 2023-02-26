def prompt(msg: str, command: dict):
    """ Description: Prompts the AI for the JSON representation of a message given a list of properties"""

    examplesStr = ""

    for example in command["examples"]:
        examplesStr += f"""
{example["in"]}
{example["out"]}\n"""

    parametersStr = ", ".join(map(lambda x: f'"{x}"', command["parameters"]))

    return f"""What's the JSON representation for the following message given this list of properties?

Examples:
{examplesStr}

Properties: {parametersStr}

Message: ${msg}"""
