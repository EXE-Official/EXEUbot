from telethon import TelegramClient, events

async def test_command(event):
    await event.edit("Online!")

def register(client):
    @client.on(events.NewMessage(pattern=r'^\.test$', outgoing=True))
    async def handler(event):
        await test_command(event)