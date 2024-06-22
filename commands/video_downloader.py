import os
from telethon import TelegramClient, events
import yt_dlp as youtube_dl
from translations import translations

async def download_video(event, url):
    try:
        ydl_opts = {
            'outtmpl': 'downloads/%(title)s.%(ext)s',
            'format': 'best',
            'noplaylist': True,
        }

        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=True)
            video_title = info_dict.get('title', 'video')
            file_path = ydl.prepare_filename(info_dict)

        await event.reply(translations['video_downloaded_successfully'].format(video_title=video_title))
        
        
        await event.client.send_file(event.chat_id, file_path, caption=f"{translations['video'].format(video_title=video_title)}")
        
        
        os.remove(file_path)

    except Exception as e:
        await event.reply(translations['error_downloading_video'].format(error=str(e)))
        print(str(e))

def register(client):
    @client.on(events.NewMessage(pattern=r'^\.dlyt (.+)$', outgoing=True))
    async def handler(event):
        url = event.pattern_match.group(1)
        await download_video(event, url)