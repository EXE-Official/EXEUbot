from telethon import TelegramClient, events
import os

async def delete_log(event):
    try:
        log_file_path = os.path.join(os.path.dirname(__file__), '..', 'userbot.log')
        if os.path.exists(log_file_path):
            os.remove(log_file_path)
            await event.respond("The userbot.log file was successfully deleted.")
        else:
            await event.respond("The userbot.log file is missing from the directory.")
    except Exception as e:
        await event.respond(f"An error occurred while deleting the userbot.log file: {str(e)}")

def register(client):
    @client.on(events.NewMessage(pattern=r'^\.dellog$', outgoing=True))
    async def handler(event):
        await delete_log(event)