from telethon import TelegramClient, events
import requests
import re

async def shorten_url(event):
    # Estrai l'URL dal messaggio usando una regex migliorata
    message = event.message.message
    match = re.search(r'\.short\s+(\S+)', message)
    if match:
        url_to_shorten = match.group(1)
        try:
            # Utilizza il servizio TinyURL per abbreviare l'URL
            api_url = "https://tinyurl.com/api-create.php?url=" + url_to_shorten
            response = requests.get(api_url)
            if response.status_code == 200:
                shortened_url = response.text
                await event.edit(f"URL shortened with TinyURL: {shortened_url}")
            else:
                await event.reply("An error occurred while shortening the URL.")
        except Exception as e:
            await event.reply(f"An error occurred: {str(e)}")
    else:
        await event.reply("Please provide a URL to shorten.")

def register(client):
    @client.on(events.NewMessage(pattern=r'^\.short\s+\S+', outgoing=True))
    async def handler(event):
        await shorten_url(event)