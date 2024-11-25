import os
import sys
import configparser
import json

# Constants
CONFIG_FILE = 'config.ini'
TRANSLATIONS_DIR = 'setup/bin/translations'

def load_translations(language):
    """
    Load translations for the selected language.
    """
    translations_path = os.path.join(TRANSLATIONS_DIR, f"{language}.json")
    if not os.path.exists(translations_path):
        print(f"Translation file for '{language}' not found. Defaulting to English.")
        translations_path = os.path.join(TRANSLATIONS_DIR, "en.json")
    
    with open(translations_path, 'r', encoding='utf-8') as file:
        return json.load(file)

def get_user_input(prompt, default=None):
    """
    Get input from the user with an optional default value.
    """
    user_input = input(f"{prompt} {f'[{default}]' if default else ''}: ").strip()
    return user_input if user_input else default

def create_config_file():
    """
    Create the config.ini file with user-provided inputs.
    """
    config = configparser.ConfigParser()

    print(translations["config_telegram"])
    api_id = get_user_input(translations["enter_api_id"])
    api_hash = get_user_input(translations["enter_api_hash"])

    print(translations["config_backup"])
    backup_dir = get_user_input(translations["enter_backup_dir"], default="./backup")

    print(translations["config_language"])
    lang = get_user_input(translations["enter_language"], default="en")

    print(translations["ask_whitelist_enabled"])
    whitelist_enabled = get_user_input(translations["ask_whitelist_enabled"], default="no").lower() in ['yes', 'y']
    
    if whitelist_enabled:
        message_limit = get_user_input(translations["ask_message_limit"], default="3")
    else:
        message_limit = "3"

    # Populate the config file
    config['telegram'] = {'api_id': api_id, 'api_hash': api_hash}
    config['var'] = {'backup_dir': backup_dir}
    config['language'] = {'lang': lang}
    config['whitelist'] = {'enabled': str(whitelist_enabled), 'message_limit': str(message_limit)}
    config['plugins'] = {'OpenWeatherMapKey': 'XXXXXXXXX'}  # Placeholder for the API key

    # Write the config to a file
    with open(CONFIG_FILE, 'w') as configfile:
        config.write(configfile)

    print(translations["config_created"].format(config=CONFIG_FILE))

def main():
    """
    Main function for the setup process.
    """
    global translations

    # Prompt user to select a language
    lang = get_user_input("Select language (en, it, ru, pl, de, fr, es): ", default="en").lower()
    translations = load_translations(lang)

    # Create the configuration file
    create_config_file()
    print(translations["config_completed"])

    # Provide instructions to the user based on their platform
    if sys.platform.startswith('win'):
        print(translations["start_main_windows"])
    elif sys.platform.startswith(('linux', 'darwin')):
        print(translations["start_main_unix"])
    else:
        print(translations["start_main_generic"])

if __name__ == '__main__':
    main()
