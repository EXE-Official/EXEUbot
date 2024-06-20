import sqlite3
import os

# REMOVING THIS FILE WILL CAUSE THE CRASH OF THE USERBOT!!!

DATABASE_PATH = os.path.join(os.path.dirname(__file__), '..', 'databases', 'whitelist.db')

def initialize_database():
    if not os.path.exists(os.path.join(os.path.dirname(__file__), '..', 'databases')):
        os.makedirs(os.path.join(os.path.dirname(__file__), '..', 'databases'))
    
    conn = sqlite3.connect(DATABASE_PATH)
    c = conn.cursor()
    
    # Create table if not exists
    c.execute('''CREATE TABLE IF NOT EXISTS whitelist
                 (user_id INTEGER PRIMARY KEY)''')
    
    # Create table for warning counts
    c.execute('''CREATE TABLE IF NOT EXISTS warnings
                 (user_id INTEGER PRIMARY KEY, count INTEGER)''')
    
    conn.commit()
    conn.close()

def add_to_whitelist(user_id):
    conn = sqlite3.connect(DATABASE_PATH)
    c = conn.cursor()
    c.execute('INSERT OR IGNORE INTO whitelist (user_id) VALUES (?)', (user_id,))
    conn.commit()
    conn.close()

def remove_from_whitelist(user_id):
    conn = sqlite3.connect(DATABASE_PATH)
    c = conn.cursor()
    c.execute('DELETE FROM whitelist WHERE user_id = ?', (user_id,))
    conn.commit()
    conn.close()

def is_whitelisted(user_id):
    conn = sqlite3.connect(DATABASE_PATH)
    c = conn.cursor()
    c.execute('SELECT 1 FROM whitelist WHERE user_id = ?', (user_id,))
    result = c.fetchone()
    conn.close()
    return result is not None

def get_warning_count(user_id):
    conn = sqlite3.connect(DATABASE_PATH)
    c = conn.cursor()
    c.execute('SELECT count FROM warnings WHERE user_id = ?', (user_id,))
    result = c.fetchone()
    conn.close()
    return result[0] if result else 0

def increment_warning_count(user_id):
    conn = sqlite3.connect(DATABASE_PATH)
    c = conn.cursor()
    current_count = get_warning_count(user_id)
    if current_count == 0:
        c.execute('INSERT INTO warnings (user_id, count) VALUES (?, ?)', (user_id, 1))
    else:
        c.execute('UPDATE warnings SET count = count + 1 WHERE user_id = ?', (user_id,))
    conn.commit()
    conn.close()

def reset_warning_count(user_id):
    conn = sqlite3.connect(DATABASE_PATH)
    c = conn.cursor()
    c.execute('DELETE FROM warnings WHERE user_id = ?', (user_id,))
    conn.commit()
    conn.close()