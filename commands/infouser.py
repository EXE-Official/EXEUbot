import os
import re
from telethon import TelegramClient, events

async def userinfo(event):
    if event.is_private:  
        await event.reply("This command only works in groups.")
        return

    try:
        
        if event.reply_to_msg_id:
            user_id = (await event.get_reply_message()).from_id
        else:
            
            username_match = re.search(r'@(\w+)', event.text)
            if username_match:
                username = username_match.group(1)
                user = await event.client.get_entity(username)
                user_id = user.id
            else:
                await event.reply("You must reply to a user's message or mention the user to use this command.")
                return

        
        user = await event.client.get_entity(user_id)

        
        if user.photo:
            photo = await event.client.download_profile_photo(user, file='user_profile.jpg')
        else:
            photo = None

        
        user_dc = user.dc_id if hasattr(user, 'dc_id') else "N/D"

        
        
        response = f"About {user.first_name}:\n"
        response += f"ID: {user_id}\n"
        response += f"Name: {user.first_name} {user.last_name}\n"
        response += f"Username: @{user.username}\n"
        response += f"Datacenter: {user_dc}\n"

        
        if photo:
            await event.reply(response, file=photo)
            os.remove(photo)
        else:
            await event.reply(response)


    except Exception as e:
        await event.reply(f"An error occurred: {str(e)}")

def register(client):
    @client.on(events.NewMessage(pattern=r'^\.infouser', outgoing=True))
    async def handler(event):
        await userinfo(event)