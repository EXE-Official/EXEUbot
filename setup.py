import subprocess
import sys
import os
import configparser
import json

CONFIG_FILE = 'config.ini'
TRANSLATIONS_DIR = 'setup/bin/translations'

def load_translations(language):
    translations_path = os.path.join(TRANSLATIONS_DIR, f"{language}.json")
    with open(translations_path, 'r', encoding='utf-8') as file:
        return json.load(file)

def get_user_input(prompt):
    return input(prompt).strip()

def create_virtual_environment():
    print(translations["creating_venv"])
    subprocess.check_call([sys.executable, '-m', 'venv', 'env'])
    print(translations["venv_created"])

def install_dependencies(venv=False):
    if venv:
        pip_executable = os.path.join('env', 'Scripts', 'pip') if sys.platform.startswith('win') else os.path.join('env', 'bin', 'pip')
    else:
        pip_executable = sys.executable

    print(translations["installing_deps"].format(pip=pip_executable))
    if venv:
        subprocess.check_call([pip_executable, 'install', '-r', 'requirements.txt'])
    else:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'])
    print(translations["deps_installed"])

def create_config_file():
    config = configparser.ConfigParser()

    print(translations["config_telegram"])
    api_id = get_user_input(translations["enter_api_id"])
    api_hash = get_user_input(translations["enter_api_hash"])

    print(translations["config_backup"])
    backup_dir = get_user_input(translations["enter_backup_dir"])

    print(translations["config_language"])
    lang = get_user_input(translations["enter_language"])

    print(translations["ask_whitelist_enabled"])
    whitelist_enabled = get_user_input(translations["ask_whitelist_enabled"]).lower()

    if whitelist_enabled == 'yes':
        whitelist_enabled = True
        message_limit = get_user_input(translations["ask_message_limit"])
    else:
        whitelist_enabled = False
        message_limit = 3

    config['telegram'] = {'api_id': api_id, 'api_hash': api_hash}
    config['var'] = {'backup_dir': backup_dir}
    config['language'] = {'lang': lang}
    config['whitelist'] = {'enabled': str(whitelist_enabled), 'message_limit': str(message_limit)}

    with open(CONFIG_FILE, 'w') as configfile:
        config.write(configfile)

    print(translations["config_created"].format(config=CONFIG_FILE))

def main():
    global translations

    lang = get_user_input("Select language (en, it, ru, pl, de, fr, es): ").lower()
    translations = load_translations(lang)

    setup_venv = get_user_input(translations["create_venv"]).lower()

    if setup_venv == 'yes':
        create_virtual_environment()
        install_dependencies(venv=True)
    elif setup_venv == 'no':
        install_dependencies()
    else:
        print(translations["invalid_input"])
        return

    create_config_file()
    print(translations["config_completed"])

    if sys.platform.startswith('win'):
        print(translations["start_main_windows"])
    elif sys.platform.startswith('linux') or sys.platform.startswith('darwin'):
        print(translations["start_main_unix"])
    else:
        print(translations["start_main_generic"])

if __name__ == '__main__':
    main()
