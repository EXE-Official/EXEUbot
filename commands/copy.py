import os
from telethon import events
from telethon.tl.functions.users import GetFullUserRequest
from telethon.tl.functions.account import UpdateProfileRequest
from telethon.tl.functions.photos import UploadProfilePhotoRequest
from translations import translations

async def copy_info(event, client):
    try:
        username = event.pattern_match.group(1)
        
        user = await client.get_entity(username)
        
        user_info = await client(GetFullUserRequest(user))

        first_name = user.first_name
        last_name = user.last_name
        bio = user_info.full_user.about
        
        
        await client(UpdateProfileRequest(
            first_name=first_name,
            last_name=last_name,
            about=bio,
        ))

        
        profile_photo = await client.download_profile_photo(user, file='profile_photo.jpg')
        
        
        await client(UploadProfilePhotoRequest(
            file=await client.upload_file(profile_photo)
        ))

        os.remove(profile_photo)
        
        await event.reply(translations['copy_successfully'])

    except Exception as e:
        await event.reply(translations['error_occurred'].format(error=str(e)))

def register(client):
    @client.on(events.NewMessage(pattern=r'^\.copy\s+(\S+)$', outgoing=True))
    async def handler(event):
        await copy_info(event, client)