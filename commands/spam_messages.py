from telethon import events
from telethon.errors import FloodError
import asyncio

async def spam_messages(event, client):
    try:
        command = event.raw_text.split()
        if len(command) >= 3:
            num_messages = int(command[1])
            spam_message = ' '.join(command[2:])
            for _ in range(num_messages):
                try:
                    await client.send_message(event.chat_id, spam_message)
                except FloodError as e:
                    wait_time = e.seconds
                    print(f"Account is in floodwait. Waiting for {wait_time} seconds...")
                    await asyncio.sleep(wait_time)
                except Exception as e:
                    print(f"An error occurred: {str(e)}")
            
            await event.delete()
        else:
            await event.respond("Invalid command format. Usage: .spam <num_messages> <spam_message>")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

def register(client):
    @client.on(events.NewMessage(pattern=r'^\.spam\s+\d+\s+.+$', outgoing=True))
    async def handler(event):
        await spam_messages(event, client)