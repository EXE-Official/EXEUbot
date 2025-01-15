from telethon import TelegramClient, events
import requests
import re
import json
import os
from translations import translations

async def shorten_url(event):
    
    message = event.message.message
    match = re.search(r'\.short\s+(\S+)', message)
    if match:
        url_to_shorten = match.group(1)
        try:
            
            api_url = "https://tinyurl.com/api-create.php?url=" + url_to_shorten
            response = requests.get(api_url)
            if response.status_code == 200:
                shortened_url = response.text
                await event.edit(translations["url_shortened"].format(shortened_url=shortened_url))
            else:
                await event.reply(translations["error_shortening_url"])
        except Exception as e:
            await event.reply(translations["error_occurred"].format(error=str(e)))
    else:
        await event.reply(translations["provide_url_to_shorten"])

def register(client):
    @client.on(events.NewMessage(pattern=r'^\.short\s+\S+', outgoing=True))
    async def handler(event):
        await shorten_url(event)