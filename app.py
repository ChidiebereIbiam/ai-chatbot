# app.py
import streamlit as st
from utils.db_utils import init_db
from pages import login_page, register_page, chat_page

# Initialize the database
init_db()

# Set page configuration
st.set_page_config(
    page_title="AI Chat Assistant",
    page_icon="💬",
    layout="wide",
    initial_sidebar_state="auto"
)

# Main app logic
def main():
    # Initialize session state variables
    if 'page' not in st.session_state:
        st.session_state.page = 'login'
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False
    
    # Route to the appropriate page
    if not st.session_state.authenticated:
        if st.session_state.page == 'login':
            login_page.show()
        elif st.session_state.page == 'register':
            register_page.show()
    else:
        chat_page.show()

if __name__ == "__main__":
    # Add custom CSS
    with open("style.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    main()
