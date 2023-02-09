import httpx

from config import config

voiceId = config['providers']['elevenlabs']['voiceId']

headers = {
    'accept': 'audio/mpeg',
    'xi-api-key': config['providers']['elevenlabs']['apiKey'],
    'Content-Type': 'application/json',
}


async def get_speech(text: str):
    async with httpx.AsyncClient() as client:
        json_data = {
            'text': text,
        }

        response = await client.post(f'https://api.elevenlabs.io/v1/text-to-speech/{voiceId}', headers=headers, json=json_data, timeout=None)

        return response.content
