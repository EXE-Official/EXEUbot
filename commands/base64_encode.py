import base64
from telethon import events

async def base64_encode(event, client):
    text = event.raw_text.split(" ", 1)[1]
    encoded_text = base64.b64encode(text.encode()).decode()
    await event.edit(encoded_text)

def register(client):
    @client.on(events.NewMessage(pattern=r'^\.base .+', outgoing=True))
    async def handler(event):
        await base64_encode(event, client)