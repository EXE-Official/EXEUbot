from telethon import events

async def leave_group(event, client):
    try:
        if event.is_group:
            chat_id = event.chat_id
            
            await event.respond("I left the group.")
            
            # Lascia il gruppo
            await client.delete_dialog(chat_id)
        else:
            await event.respond("This command can only be used in groups.")
    except Exception as e:
        await event.respond(f"An error occurred: {str(e)}")

def register(client):
    @client.on(events.NewMessage(pattern=r'^\.leave$', outgoing=True))
    async def handler(event):
        await leave_group(event, client)