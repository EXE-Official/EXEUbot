import os
from telethon import TelegramClient, events
from translations import translations

async def delete_log(event):
    try:
        log_file_path = os.path.join(os.path.dirname(__file__), '..', 'userbot.log')
        if os.path.exists(log_file_path):
            os.remove(log_file_path)
            await event.respond(translations['dellog_successfully"'])
        else:
            await event.respond(translations['dellog_missing'])
    except Exception as e:
        await event.respond(translations['error_occurred'].format(error=str(e)))

def register(client):
    @client.on(events.NewMessage(pattern=r'^\.dellog$', outgoing=True))
    async def handler(event):
        await delete_log(event)