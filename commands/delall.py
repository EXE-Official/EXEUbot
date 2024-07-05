import asyncio
from telethon import events
from telethon.errors import FloodWaitError
from translations import translations

async def delete_all_messages(event, client):
    chat_id = event.chat_id
    message_ids = []
    
    async for msg in client.iter_messages(chat_id):
        message_ids.append(msg.id)
        
        if len(message_ids) >= 100:
            try:
                await client.delete_messages(chat_id, message_ids)
                message_ids = []
                await asyncio.sleep(1)  # Add a 1 second delay between deletes
            except FloodWaitError as e:
                wait_time = e.seconds
                print(translations['floodwait_error'].format(waitingtime=str(wait_time)))
                await asyncio.sleep(wait_time)
            except Exception as e:
                print(translations['error_occurred'].format(error=str(e)))
    
    # Delete any remaining messages
    if message_ids:
        try:
            await client.delete_messages(chat_id, message_ids)
        except Exception as e:
            print(translations['error_occurred'].format(error=str(e)))

def register(client):
    @client.on(events.NewMessage(pattern=r'^\.delall$', outgoing=True))
    async def handler(event):
        await delete_all_messages(event, client)
