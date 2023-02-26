
import openai

from core.config import get_value
from core.utils.dict import get_value_from_dict

openai.api_key = get_value('providers.openai.apiKey')


def remove_prefix(text, prefix):
    if text.strip().startswith(prefix):
        return text[len(prefix):]
    return text


async def generate_text_from_prompt(prompt: str, params: dict = {}):
    completion = await openai.Completion.acreate(
        engine=get_value_from_dict(params, 'engine', 'text-davinci-003'),
        prompt=prompt,
        temperature=get_value_from_dict(params, 'temperature', 0.7),
        max_tokens=get_value_from_dict(params, 'max_tokens', 256),
        top_p=get_value_from_dict(params, 'top_p', 1),
        frequency_penalty=get_value_from_dict(params, 'frequency_penalty', 0),
        presence_penalty=get_value_from_dict(params, 'presence_penalty', 0),
    )

    text: str = remove_prefix(completion.choices[0].text, 'bot:').strip()

    return text.strip()
