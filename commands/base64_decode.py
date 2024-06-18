import base64
from telethon import events

async def base64_decode(event, client):
    text = event.raw_text.split(" ", 1)[1]
    try:
        decoded_text = base64.b64decode(text).decode()
        await event.edit(decoded_text)
    except Exception as e:
        await event.edit("Decoding error. Make sure the text is in valid base64 format.")

def register(client):
    @client.on(events.NewMessage(pattern=r'^\.sbase .+', outgoing=True))
    async def handler(event):
        await base64_decode(event, client)