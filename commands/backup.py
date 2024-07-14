import os
import configparser
import json
from telethon import TelegramClient, events
from telethon.tl.functions.users import GetFullUserRequest
from telethon.tl.functions.account import UpdateProfileRequest
from telethon.tl.functions.photos import UploadProfilePhotoRequest
from translations import translations


config_path = os.path.join(os.path.dirname(__file__), '..', 'config.ini')
config_path = os.path.abspath(config_path)

config = configparser.ConfigParser()
config.read(config_path)
backup_folder = config['var']['backup_dir']


# Restore and backup functions

async def backup_info(event, client, backup_folder):
    try:
        me = await client.get_me()
        my_info = await client(GetFullUserRequest(me))

        data = {
            "first_name": me.first_name,
            "last_name": me.last_name,
            "bio": my_info.full_user.about,
        }

        info_file_path = os.path.join(backup_folder, 'userbot_info.json')
        with open(info_file_path, 'w') as json_file:
            json.dump(data, json_file, indent=4)

        profile_photo = await client.download_profile_photo(me, file=os.path.join(backup_folder, 'profile_photo.jpg'))

        await event.reply(translations["backup_complete"])

    except Exception as e:
        await event.reply(translations["backup_error"].format(error=str(e)))

async def check_files_in_backup_folder(backup_folder):
    required_files = ['userbot_info.json', 'profile_photo.jpg']
    for file in required_files:
        if not os.path.exists(os.path.join(backup_folder, file)):
            return False
    return True

async def revert_info(event, client, backup_folder):
    try:
        backup_folder = os.path.abspath(backup_folder)

        if not await check_files_in_backup_folder(backup_folder):
            await event.reply(translations["no_backup_files"])
            return

        info_file_path = os.path.join(backup_folder, 'userbot_info.json')
        with open(info_file_path, 'r') as json_file:
            data = json.load(json_file)

        await client(UpdateProfileRequest(
            first_name=data.get("first_name", ""),
            last_name=data.get("last_name", ""),
            about=data.get("bio", ""),
        ))

        profile_photo_path = os.path.join(backup_folder, 'profile_photo.jpg')
        if os.path.exists(profile_photo_path):
            await client(UploadProfilePhotoRequest(
                file=await client.upload_file(profile_photo_path)
            ))

        await event.reply(translations["restore_complete"])

    except Exception as e:
        await event.reply(translations["restore_error"].format(error=str(e)))


def register(client, backup_folder):
    @client.on(events.NewMessage(pattern=r'^\.revert$', outgoing=True))
    async def handler(event):
        await revert_info(event, client, backup_folder)


def register(client):
    @client.on(events.NewMessage(pattern=r'^\.backup$', outgoing=True))
    async def handler(event):
        await backup_info(event, client, backup_folder)