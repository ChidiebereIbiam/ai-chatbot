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
    
    c.execute('''CREATE TABLE IF NOT EXISTS messages
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  username TEXT NOT NULL,
                  role TEXT NOT NULL,
                  content TEXT NOT NULL,
                  timestamp TEXT NOT NULL,
                  FOREIGN KEY (username) REFERENCES users(username))''')
                  
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

def save_message(username, role, content, timestamp):
    """Save a message to the database."""
    conn = sqlite3.connect('ai_chat.db')
    c = conn.cursor()
    c.execute('INSERT INTO messages (username, role, content, timestamp) VALUES (?, ?, ?, ?)',
              (username, role, content, timestamp))
    conn.commit()
    conn.close()


def get_user_messages(username):
    """Get all messages for a specific user."""
    conn = sqlite3.connect('ai_chat.db')
    c = conn.cursor()
    c.execute('SELECT role, content, timestamp FROM messages WHERE username = ? ORDER BY id ASC', (username,))
    messages = c.fetchall()
    conn.close()
    
    # Convert to list of dictionaries
    message_list = []
    for msg in messages:
        message_list.append({
            "role": msg[0],
            "content": msg[1],
            "timestamp": msg[2]
        })
    
    return message_list


def clear_user_messages(username):
    """Clear all messages for a user."""
    conn = sqlite3.connect('ai_chat.db')
    c = conn.cursor()
    c.execute('DELETE FROM messages WHERE username = ?', (username,))
    conn.commit()
    conn.close()