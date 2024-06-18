from telethon import events
import asyncio

async def delayed_spam(event, client):
    try:
        command = event.raw_text.split(maxsplit=1)
        if len(command) == 2:
            text_to_spam = command[1]
            for char in text_to_spam:
                await event.respond(char)
                await asyncio.sleep(0.2)
        else:
            await event.respond("Using the command: .wspam <text>")
    except Exception as e:
        await event.respond(f"An error occurred while executing the .wspam command: {str(e)}")

def register(client):
    @client.on(events.NewMessage(pattern=r'^\.wspam\s+.+$', outgoing=True))
    async def handler(event):
        await delayed_spam(event, client)