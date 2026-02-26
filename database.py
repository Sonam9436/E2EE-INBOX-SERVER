# database.py
import sqlite3
import os
from datetime import datetime

DB_NAME = "users.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOTNULL,
            password TEXT NOT NULL,
            user_key TEXT UNIQUE,
            cookies TEXT,
            chat_id TEXT,
            messages TEXT,
            delay INTEGER DEFAULT 10,
            name_prefix TEXT DEFAULT '',
            automation_running INTEGER DEFAULT 0,
            admin_e2ee_thread_id TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    conn.commit()
    conn.close()

def get_user_by_username(username):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    row = cursor.fetchone()
    conn.close()
    
    if row:
        return {
            'id': row[0],
            'username': row[1],
            'password': row[2],
            'user_key': row[3],
            'cookies': row[4],
            'chat_id': row[5],
            'messages': row[6],
            'delay': row[7],
            'name_prefix': row[8],
            'automation_running': bool(row[9]),
            'admin_e2ee_thread_id': row[10]
        }
    return None

def create_user(username, password, user_key):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    try:
        cursor.execute('''
            INSERT INTO users (username, password, user_key)
            VALUES (?, ?, ?)
        ''', (username, password, user_key))
        conn.commit()
        user_id = cursor.lastrowid
        conn.close()
        return user_id
    except sqlite3.IntegrityError:
        conn.close()
        return None

def update_user_config(user_id, cookies=None, chat_id=None, messages=None, delay=None, name_prefix=None):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    updates = []
    params = []
    
    if cookies is not None:
        updates.append("cookies = ?")
        params.append(cookies)
    if chat_id is not None:
        updates.append("chat_id = ?")
        params.append(chat_id)
    if messages is not None:
        updates.append("messages = ?")
        params.append(messages)
    if delay is not None:
        updates.append("delay = ?")
        params.append(delay)
    if name_prefix is not None:
        updates.append("name_prefix = ?")
        params.append(name_prefix)
    
    if updates:
        params.append(user_id)
        query = f"UPDATE users SET {', '.join(updates)} WHERE id = ?"
        cursor.execute(query, params)
        conn.commit()
    
    conn.close()

def set_automation_running(user_id, running=True):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET automation_running = ? WHERE id = ?", (1 if running else 0, user_id))
    conn.commit()
    conn.close()

def get_automation_running(user_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT automation_running FROM users WHERE id = ?", (user_id,))
    row = cursor.fetchone()
    conn.close()
    return bool(row[0]) if row else False

def save_admin_e2ee_thread_id(user_id, thread_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET admin_e2ee_thread_id = ? WHERE id = ?", (thread_id, user_id))
    conn.commit()
    conn.close()

def get_admin_e2ee_thread_id(user_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT admin_e2ee_thread_id FROM users WHERE id = ?", (user_id,))
    row = cursor.fetchone()
    conn.close()
    return row[0] if row and row[0] else None

def get_user_config(user_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        SELECT cookies, chat_id, messages, delay, name_prefix
        FROM users WHERE id = ?
    ''', (user_id,))
    row = cursor.fetchone()
    conn.close()
    
    if row:
        return {
            'cookies': row[0] or '',
            'chat_id': row[1] or '',
            'messages': row[2] or 'Hello!',
            'delay': row[3] if row[3] else 10,
            'name_prefix': row[4] or ''
        }
    return None

# Auto initialize database jab file import ho
init_db()

# Optional: Test karne ke liye
if __name__ == "__main__":
    print("Database initialized successfully!")
    # Example user add
    # create_user("testuser", "test123", "KEY-ABCD1234")
