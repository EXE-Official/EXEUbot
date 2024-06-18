from telethon import events

async def send_dm(event, client):
    text = event.text.split(maxsplit=2)
    if len(text) < 3:
        await event.respond("Please provide a username and a message.")
        return

    username = text[1].replace("@", "")  # Rimuovi il simbolo '@' se presente
    dm_message = text[2]

    try:
        user = await client.get_entity(username)
    except Exception:
        await event.respond("Failed to find the user. Please provide a valid username.")
        return

    try:
        await client.send_message(user, dm_message)  # Passa direttamente l'entità dell'utente
        await event.respond(f"Message sent to @{username}!")
    except Exception as e:
        print(e)
        await event.respond("Failed to send the DM. Apologies!")

def register(client):
    @client.on(events.NewMessage(pattern=r'^\.dm\s+\S+\s+.+$', outgoing=True))
    async def handler(event):
        await send_dm(event, client)