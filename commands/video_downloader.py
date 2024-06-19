import os
from telethon import TelegramClient, events
import yt_dlp as youtube_dl


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

        await event.reply(f"Video '{video_title}' downloaded successfully! Sending...")
        
        
        await event.client.send_file(event.chat_id, file_path, caption=f"Video: {video_title}")
        
        
        os.remove(file_path)

    except Exception as e:
        await event.reply(f"Error downloading video: {str(e)}")
        print(str(e))

def register(client):
    @client.on(events.NewMessage(pattern=r'^\.dlyt (.+)$', outgoing=True))
    async def handler(event):
        url = event.pattern_match.group(1)
        await download_video(event, url)