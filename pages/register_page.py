# pages/register_page.py
import streamlit as st
from utils.auth_utils import register_user

def show():
    """Display the registration page."""
    st.title("Create New Account")
    
    with st.container():
        with st.form("registration_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                name = st.text_input("Full Name*")
                email = st.text_input("Email Address*")
                phone = st.text_input("Phone Number")
            
            with col2:
                username = st.text_input("Username*")
                password = st.text_input("Password*", type="password")
                password_confirm = st.text_input("Confirm Password*", type="password")
            
            st.markdown("*Required fields")
            
            col1, col2 = st.columns([1, 1])
            with col1:
                back_button = st.form_submit_button("Back to Login", use_container_width=True)
            with col2:
                submit_button = st.form_submit_button("Register", use_container_width=True)
        
        # Handle form submission
        if submit_button:
            if not all([name, email, username, password]):
                st.error("Please fill all required fields")
            elif password != password_confirm:
                st.error("Passwords do not match")
            else:
                if register_user(name, email, phone, username, password):
                    st.success("Registration successful! Please login")
                    st.session_state['page'] = 'login'
                    st.rerun()
                else:
                    st.error("Username or email already exists")
        
        # Handle back button
        if back_button:
            st.session_state['page'] = 'login'
            st.rerun()
