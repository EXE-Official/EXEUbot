from telethon import events
from translations import translations

async def send_dm(event, client):
    text = event.text.split(maxsplit=2)
    if len(text) < 3:
        await event.respond(translations['provide_username_dm'])
        return

    username = text[1].replace("@", "")  
    dm_message = text[2]

    try:
        user = await client.get_entity(username)
    except Exception:
        await event.respond(translations['user_not_found'])
        return

    try:
        await client.send_message(user, dm_message)  
        await event.respond(translations['message_sent'])
    except Exception as e:
        await event.respond(translations['error_occurred'].format(error=str(e)))

def register(client):
    @client.on(events.NewMessage(pattern=r'^\.dm\s+\S+\s+.+$', outgoing=True))
    async def handler(event):
        await send_dm(event, client)