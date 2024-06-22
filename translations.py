import json
import os
import configparser

def load_language():
    config = configparser.ConfigParser()
    config.read('config.ini')
    return config['language']['lang']

def load_translations(lang):
    translations_folder = os.path.join(os.path.dirname(__file__), 'translations')
    translations_file = os.path.join(translations_folder, f'{lang}.json')
    
    if not os.path.exists(translations_file):
        raise FileNotFoundError(f"No translation file found for language: {lang}")
    
    with open(translations_file, 'r', encoding='utf-8') as f:
        translations = json.load(f)
    
    return translations

def get_translations():
    lang = load_language()
    return load_translations(lang)

translations = get_translations()
