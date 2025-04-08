# app.py
import streamlit as st
import os
from utils.db_utils import init_db
from pages import login_page, register_page, chat_page

# Initialize the database
init_db()

# Set page configuration
st.set_page_config(
    page_title="CSC Dept. AI Chat Assistant",
    page_icon="💬",
    layout="wide",
    initial_sidebar_state="collapsed" 
)

# Function to hide sidebar for login and register pages
def manage_sidebar_visibility():
    if not st.session_state.get('authenticated', False):
        # Hide sidebar on login and registration pages
        st.markdown(
            """
            <style>
            [data-testid="stSidebar"][aria-expanded="true"]{
                visibility: hidden;
                width: 0px;
            }
            [data-testid="stSidebar"][aria-expanded="false"]{
                visibility: hidden;
            }
            </style>
            """,
            unsafe_allow_html=True,
        )

# Session management
def check_authentication_from_cookie():
    """Check if user session exists in cookie and restore session if it does"""
    # Use Streamlit's session state as a simple persistence mechanism
    if os.path.exists(".session_cookie"):
        try:
            with open(".session_cookie", "r") as f:
                username = f.read().strip()
                if username:
                    st.session_state['authenticated'] = True
                    st.session_state['username'] = username
        except:
            pass  # If there's any error, just proceed without authentication

def save_authentication_to_cookie():
    """Save authentication status to a cookie"""
    if st.session_state.get('authenticated', False):
        with open(".session_cookie", "w") as f:
            f.write(st.session_state['username'])

# Main app logic
def main():
    # Initialize session state variables
    if 'page' not in st.session_state:
        st.session_state.page = 'login'
    
    # Check if user has a valid session
    check_authentication_from_cookie()
    
    # Manage sidebar visibility (hide on login/register)
    manage_sidebar_visibility()
    
    # Route to the appropriate page
    if not st.session_state.get('authenticated', False):
        if st.session_state.page == 'login':
            login_page.show()
        elif st.session_state.page == 'register':
            register_page.show()
    else:
        chat_page.show()
    
    # Save authentication status after rendering
    save_authentication_to_cookie()

if __name__ == "__main__":
    # Add custom CSS
    try:
        with open("style.css") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    except FileNotFoundError:
        pass  # If style.css doesn't exist, continue without it
    
    main()