import psutil
import speedtest
import platform
import humanize
from telethon import TelegramClient, events
from translations import translations

async def system_info(event):
    try:
        cpu_usage = psutil.cpu_percent()
        memory = psutil.virtual_memory()

        st = speedtest.Speedtest(secure=True)
        server = st.get_best_server()
        ping = server['latency']

        system_info = platform.uname()
        python_version = platform.python_version()
        telethon_version = TelegramClient.__version__

        message = (
            f"{translations.get('system_info_title')}\n"
            f"{translations.get('os')}: {system_info.system}\n"
            f"{translations.get('kernel')}: {system_info.release}\n"
            f"{translations.get('python_version')}: {python_version}\n"
            f"{translations.get('telethon_version')}: {telethon_version}\n"
            f"{translations.get('userbot_version')}: Beta 1.20\n"
            f"{translations.get('cpu_usage')}: {cpu_usage}%\n"
            f"{translations.get('ram_usage')}: {memory.percent}% ({humanize.naturalsize(memory.used)})\n"
            f"{translations.get('ram_total')}: {humanize.naturalsize(memory.total)}\n"
            f"{translations.get('ping')}: {ping} ms\n"
            f"{translations.get('userbot_commands_link')}\n"
            f"{translations.get('userbot_created_by')}"
        )

        await event.edit(message)
    except Exception as e:
        await event.reply(translations.get('error_occurred', error=str(e)))
        print(str(e))

def register(client):
    @client.on(events.NewMessage(pattern=r'^\.info$', outgoing=True))
    async def handler(event):
        await system_info(event)
