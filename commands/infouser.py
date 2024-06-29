import os
import re
from telethon import TelegramClient, events
from translations import translations

async def userinfo(event):
    if event.is_private:  
        await event.reply(translations["command_in_groups_only"])
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
                await event.reply(translations["mention_or_reply_user"])
                return

        user = await event.client.get_entity(user_id)

        if user.photo:
            photo = await event.client.download_profile_photo(user, file='user_profile.jpg')
        else:
            photo = None

        user_dc = user.dc_id if hasattr(user, 'dc_id') else "N/D"

        response = translations["about_user"].format(first_name=user.first_name) + "\n"
        response += translations["user_id"].format(user_id=user_id) + "\n"
        response += translations["user_name"].format(first_name=user.first_name, last_name=user.last_name) + "\n"
        response += translations["user_username"].format(username=user.username) + "\n"
        response += translations["user_datacenter"].format(datacenter=user_dc) + "\n"

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
