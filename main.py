import configparser
import importlib
from telethon import TelegramClient, events
import os
import traceback
import asyncio
import signal
import logging
from translations import translations

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
    # Leggi le credenziali dal file config.ini
    config = configparser.ConfigParser()
    config.read('config.ini')
    api_id = config['telegram']['api_id']
    api_hash = config['telegram']['api_hash']
    backup_folder = config['var']['backup_dir']

    client = TelegramClient('session_name', api_id, api_hash)

    try:
        await client.start()
        load_commands(client)
        print(translations['userbot_started'])
        await client.run_until_disconnected()
    except asyncio.CancelledError:
        print(translations['userbot_disconnected_cancelled_error'])
    except Exception as e:
        traceback.print_exc()
        print(translations['error_occurred'].format(error=str(e)))

def handle_signal(signum, frame):
    print(translations['abort_signal_received'])
    asyncio.get_event_loop().stop()

if __name__ == '__main__':
    signal.signal(signal.SIGINT, handle_signal)
    asyncio.run(main())
