import configparser
import importlib
from telethon import TelegramClient, events
import os
import traceback
import asyncio
import signal
import logging

logging.basicConfig(
    level=logging.WARN,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    filename="userbot.log",
    filemode="a"
)

def load_commands(client):
    commands_folder = os.path.join(os.path.dirname(__file__), 'commands')
    for filename in os.listdir(commands_folder):
        if filename.endswith('.py') and filename != '__init__.py':
            module_name = f'commands.{filename[:-3]}'
            module = importlib.import_module(module_name)
            if hasattr(module, 'register'):
                module.register(client)

async def main():
    # Read credentials from config.ini file
    config = configparser.ConfigParser()
    config.read('config.ini')
    api_id = config['telegram']['api_id']
    api_hash = config['telegram']['api_hash']
    backup_folder = config['var']['backup_dir']

    client = TelegramClient('session_name', api_id, api_hash)

    try:
        await client.start()
        load_commands(client)
        print("Userbot started!")
        await client.run_until_disconnected()
    except asyncio.CancelledError:
        print("Userbot disconnected due to a CancelledError exception.")
    except Exception as e:
        traceback.print_exc()
        print(f"An error occurred: {str(e)}")

def handle_signal(signum, frame):
    print("Abort signal received. closing the Userbot...")
    asyncio.get_event_loop().stop()

if __name__ == '__main__':
    signal.signal(signal.SIGINT, handle_signal)
    asyncio.run(main())