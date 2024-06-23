from telethon import events
from translations import translations

async def leave_group(event, client):
    try:
        if event.is_group:
            chat_id = event.chat_id
            
            await event.respond(translations['left_group'])
            
            
            await client.delete_dialog(chat_id)
        else:
            await event.respond(translations['command_groups_only'])
    except Exception as e:
        await event.respond(translations['error_occurred'].format(error=str(e)))

def register(client):
    @client.on(events.NewMessage(pattern=r'^\.leave$', outgoing=True))
    async def handler(event):
        await leave_group(event, client)