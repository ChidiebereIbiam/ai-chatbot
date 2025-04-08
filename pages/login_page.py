# pages/login_page.py
import streamlit as st
from utils.auth_utils import authenticate_user

def show():
    """Display the login page."""
    st.title("Welcome to AI Assistant")
    
    with st.container():
        st.markdown("### Login")
        with st.form("login_form"):
            username = st.text_input("Username", key="login_username")
            password = st.text_input("Password", type="password", key="login_password")
            
            col1, col2 = st.columns([1, 1])
            with col1:
                submit = st.form_submit_button("Login", use_container_width=True)
            with col2:
                register_button = st.form_submit_button("Create Account", use_container_width=True)
        
        if submit:
            if authenticate_user(username, password):
                st.session_state['authenticated'] = True
                st.session_state['username'] = username
                # Authentication saved in main app.py
                st.rerun()
            else:
                st.error("Invalid username or password")
        
        if register_button:
            st.session_state['page'] = 'register'
            st.rerun()
    
    # Add some nice styling and information
    st.markdown("---")
    st.markdown("### About this App")
    st.write("This is an AI assistant chatbot application. Log in to start chatting with our AI!")
    with st.expander("Features"):
        st.markdown("""
        - Chat with an AI assistant
        - Get quick responses to your questions
        - Secure authentication system
        - User-friendly interface
        """)