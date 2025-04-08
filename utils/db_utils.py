import sqlite3
from datetime import datetime

def init_db():
    """Initialize the database and create tables if they don't exist."""
    conn = sqlite3.connect('ai_chat.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  name TEXT NOT NULL,
                  email TEXT UNIQUE NOT NULL,
                  phone TEXT,
                  username TEXT UNIQUE NOT NULL,
                  password TEXT NOT NULL,
                  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
    conn.commit()
    conn.close()

def add_user(name, email, phone, username, password_hash):
    """Add a new user to the database."""
    try:
        conn = sqlite3.connect('ai_chat.db')
        c = conn.cursor()
        c.execute('INSERT INTO users (name, email, phone, username, password) VALUES (?, ?, ?, ?, ?)',
                  (name, email, phone, username, password_hash))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

def get_user_password(username):
    """Get a user's password hash from the database."""
    conn = sqlite3.connect('ai_chat.db')
    c = conn.cursor()
    c.execute('SELECT password FROM users WHERE username = ?', (username,))
    result = c.fetchone()
    conn.close()
    return result[0] if result else None

def get_user_profile(username):
    """Get user profile information."""
    conn = sqlite3.connect('ai_chat.db')
    c = conn.cursor()
    c.execute('SELECT name, email, phone FROM users WHERE username = ?', (username,))
    result = c.fetchone()
    conn.close()
    return result if result else None
