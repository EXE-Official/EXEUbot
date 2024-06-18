from telethon import events

async def text_to_binary(event, client):
    text = event.raw_text.split(" ", 1)[1]
    binary_text = ' '.join(format(ord(char), '08b') for char in text)
    await event.edit(binary_text)

def register(client):
    @client.on(events.NewMessage(pattern=r'^\.bin .+', outgoing=True))
    async def handler(event):
        await text_to_binary(event, client)