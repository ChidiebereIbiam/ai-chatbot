# pages/chat_page.py
import streamlit as st
from utils.db_utils import get_user_profile
from backends import ai_backend
import datetime
import os

def logout():
    """Log out user and clear session cookie"""
    st.session_state.clear()
    # Remove session cookie file
    if os.path.exists(".session_cookie"):
        try:
            os.remove(".session_cookie")
        except:
            pass  # If there's any error, just proceed with logout
    st.rerun()

def show():
    """Display the chat interface with improved UI."""
    # Now the sidebar will only show on this page
    
    if 'messages' not in st.session_state:
        st.session_state.messages = []
        # Add initial welcome message
        st.session_state.messages.append({
            "role": "assistant", 
            "content": f"Hello {st.session_state['username']}! How can I help you today?",
            "timestamp": datetime.datetime.now().strftime("%H:%M")
        })
    
    # Sidebar with user profile and settings
    with st.sidebar:
        st.title("User Profile")
        profile = get_user_profile(st.session_state['username'])
        
        if profile:
            name, email, phone = profile
            st.write(f"**Name:** {name}")
            st.write(f"**Email:** {email}")
            if phone:
                st.write(f"**Phone:** {phone}")
        
        st.markdown("---")
        st.subheader("Settings")
        theme = st.selectbox("Chat Theme", ["Light", "Dark", "Auto"])
        
        st.markdown("---")
        if st.button("Logout", use_container_width=True):
            logout()  # Use the improved logout function
    
    # Main chat area
    st.title("AI Assistant Chat")
    
    # Chat container with custom styling
    chat_container = st.container()
    with chat_container:
        # Display all messages
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.write(f"**{message['timestamp']}**")
                st.markdown(message["content"])
    
    # Input area at the bottom
    st.markdown("---")
    
    # Chat controls
    col1, col2 = st.columns([4, 1])
    with col1:
        prompt = st.chat_input("Ask me anything...")
    
    # Process the user input
    if prompt:
        # Add user message to chat
        timestamp = datetime.datetime.now().strftime("%H:%M")
        st.session_state.messages.append({
            "role": "user", 
            "content": prompt,
            "timestamp": timestamp
        })
        
        # Get AI response
        ai_response = ai_backend.process_message(prompt)
        
        # Add AI response to chat
        st.session_state.messages.append({
            "role": "assistant", 
            "content": ai_response,
            "timestamp": timestamp
        })
        
        # Rerun to update UI
        st.rerun()