import streamlit as st
import sqlite3
import bcrypt
import os
from datetime import datetime

# Database setup
def init_db():
    conn = sqlite3.connect('users.db')
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

init_db()

def hash_password(password):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

def verify_password(input_password, hashed_password):
    return bcrypt.checkpw(input_password.encode('utf-8'), hashed_password)

# Authentication functions
def register_user(name, email, phone, username, password):
    try:
        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        hashed_pw = hash_password(password)
        c.execute('INSERT INTO users (name, email, phone, username, password) VALUES (?, ?, ?, ?, ?)',
                  (name, email, phone, username, hashed_pw))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

def authenticate_user(username, password):
    try:
        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        c.execute('SELECT password FROM users WHERE username = ?', (username,))
        result = c.fetchone()
        if result and verify_password(password, result[0]):
            return True
        return False
    finally:
        conn.close()

# Page configurations
def login_page():
    st.title("Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    
    if st.button("Login"):
        if authenticate_user(username, password):
            st.session_state['authenticated'] = True
            st.session_state['username'] = username
            st.rerun() 
        else:
            st.error("Invalid username or password")
    
    if st.button("Create New Account"):
        st.session_state['page'] = 'register'

def register_page():
    st.title("Register")
    with st.form("registration_form"):
        name = st.text_input("Full Name")
        email = st.text_input("Email")
        phone = st.text_input("Phone Number")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        
        if st.form_submit_button("Register"):
            if not all([name, email, username, password]):
                st.error("Please fill all required fields")
            else:
                if register_user(name, email, phone, username, password):
                    st.success("Registration successful! Please login")
                    st.session_state['page'] = 'login'
                else:
                    st.error("Username or email already exists")

def main_chat_page():
    st.title(f"Welcome {st.session_state['username']}")
    st.subheader("AI Chatbot Interface")
    
    # Simple chat interface
    if 'messages' not in st.session_state:
        st.session_state.messages = []
    
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    if prompt := st.chat_input("Ask me anything"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Add simple AI response (replace with actual model)
        ai_response = f"Echo: {prompt}"
        with st.chat_message("assistant"):
            st.markdown(ai_response)
        st.session_state.messages.append({"role": "assistant", "content": ai_response})
    
    if st.button("Logout"):
        st.session_state.clear()
        st.rerun() 

# Main app logic
def main():
    if 'page' not in st.session_state:
        st.session_state.page = 'login'
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False
    
    if not st.session_state.authenticated:
        if st.session_state.page == 'login':
            login_page()
        elif st.session_state.page == 'register':
            register_page()
    else:
        main_chat_page()

if __name__ == "__main__":
    main()