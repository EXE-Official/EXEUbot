from telethon import events

async def binary_to_text(event, client):
    binary_text = event.raw_text.split(" ", 1)[1]
    try:
        text = ''.join([chr(int(char, 2)) for char in binary_text.split(' ')])
        await event.edit(text)
    except Exception as e:
        await event.edit("Error converting binary to text.")

def register(client):
    @client.on(events.NewMessage(pattern=r'^\.sbin .+', outgoing=True))
    async def handler(event):
        await binary_to_text(event, client)