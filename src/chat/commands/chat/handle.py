
from core.adapters import telegram, openai

from core.messages import add_message, Message
from chat.commands.chat.prompt import prompt


async def handle(
    params: dict,
    command: dict,
    update: telegram.Update,
    context: telegram.ContextTypes.DEFAULT_TYPE
):
    prompt_text = prompt(params['message'], update, command['personality'])

    print(prompt_text)

    text = await openai.generate_text_from_prompt(prompt_text)

    print('completed')

    print(text)

    message = Message(
        text or 'I don\'t know what to say', 'bot', update.message.date
    )

    add_message(message)

    await telegram.send_text_message(update, context, message.text)
