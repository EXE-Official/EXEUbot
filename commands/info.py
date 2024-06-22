import psutil
import speedtest
import platform
import humanize
from telethon import TelegramClient, events

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
            f"ℹ️ System info:\n"
            f"💻 OS: {system_info.system}\n"
            f"🔳 Kernel: {system_info.release}\n"
            f"🐍 Python version: {python_version}\n"
            f"🤖 Telethon version: {telethon_version}\n"
            f"⚙️ Userbot version: Beta 1.14\n"
            f"⚡ CPU usage: {cpu_usage}%\n"
            f"📈 RAM usage: {memory.percent}% ({humanize.naturalsize(memory.used)})\n"
            f"📉 RAM total: {humanize.naturalsize(memory.total)}\n"
            f"📶 Ping: {ping} ms\n"
            f"🤖 [Comandi Userbot](https://telegra.ph/Userbot-commands-09-11-46)\n"
            f"👤 Userbot created by Elxes ©️"
        )

        await event.edit(message)
    except Exception as e:
        await event.reply(f"An error occurred while reading system information: {str(e)}")
        print(str(e))

def register(client):
    @client.on(events.NewMessage(pattern=r'^\.info$', outgoing=True))
    async def handler(event):
        await system_info(event)