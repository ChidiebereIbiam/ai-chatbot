# pages/chat_page.py
import streamlit as st
from utils.db_utils import get_user_profile
from backends.ai_backend import ChatAI
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

    # Custom CSS for message alignment
    st.markdown("""
    <style>
        section[data-testid="stSidebar"] div.st-emotion-cache-1cypcdb {
            display: none !important;
        }
        .assistant-message {
            background-color: #f0f2f6;
            border-radius: 15px;
            padding: 10px 15px;
            color: black;
            margin: 5px 0;
            max-width: 80%;
            float: left;
            clear: both;
        }
        .user-message {
            background-color: #1e88e5;
            color: white;
            border-radius: 15px;
            padding: 10px 15px;
            margin: 5px 0;
            max-width: 80%;
            float: right;
            clear: both;
        }
        .timestamp {
            font-size: 0.8em;
            opacity: 0.7;
            margin-bottom: 5px;
        }
        .message-container {
            display: flow-root;
            margin-bottom: 10px;
        }
    </style>
    """, unsafe_allow_html=True)

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
    st.title("CSC Department AI Assistant Chat")
    
    # Chat container with custom styling
    chat_container = st.container()
    
    # Message input area at the bottom (place it before displaying messages)
    st.markdown("---")
    prompt = st.chat_input("Ask me anything about CSC Department...")
    
    # Create a placeholder for the AI response
    if 'response_placeholder' not in st.session_state:
        st.session_state.response_placeholder = None
    
    # Process the user input
    if prompt:
        # Add user message to chat
        timestamp = datetime.datetime.now().strftime("%H:%M")
        st.session_state.messages.append({
            "role": "user",
            "content": prompt,
            "timestamp": timestamp
        })
        
        # Rerun to display the user message immediately
        st.rerun()
    
    # Display chat messages using custom HTML
    with chat_container:
        for i, message in enumerate(st.session_state.messages):
            role = message["role"]
            content = message["content"]
            timestamp = message["timestamp"]
            
            if role == "assistant":
                message_class = "assistant-message"
            else:
                message_class = "user-message"
            
            st.markdown(f"""
                <div class="message-container">
                    <div class="{message_class}">
                        <div class="timestamp">{timestamp}</div>
                        {content}
                    </div>
                </div>
            """, unsafe_allow_html=True)
    
    # Check if we need to generate an AI response
    # This happens after a user message has been added and the page has been rerun
    if st.session_state.messages and st.session_state.messages[-1]["role"] == "user":
        # Create placeholder for streaming response
        response_placeholder = st.empty()
        
        with response_placeholder:
            with st.spinner("AI is thinking..."):
                st.session_state.setdefault('ai_engine', ChatAI())
                
                # Implement streaming response
                full_response = ""
                timestamp = datetime.datetime.now().strftime("%H:%M")
                
                # Option 1: Using streaming if your ChatAI supports it
                try:
                    # If streaming is supported
                    message_placeholder = st.empty()
                    for chunk in st.session_state.ai_engine._stream_response(
                        st.session_state.ai_engine.setup_qa_chain(
                            st.session_state.ai_engine.create_vectorstore()
                        ), 
                        st.session_state.messages[-1]["content"]
                    ):
                        full_response += chunk
                        message_placeholder.markdown(f"""
                            <div class="message-container">
                                <div class="assistant-message">
                                    <div class="timestamp">{timestamp}</div>
                                    {full_response}
                                </div>
                            </div>
                        """, unsafe_allow_html=True)
                except Exception as e:
                    # Fall back to non-streaming if there's an error
                    print(f"Streaming not available: {e}")
                    full_response = st.session_state.ai_engine.ask_question(
                        st.session_state.messages[-1]["content"]
                    )
        
        # Add the complete AI response to the session state
        st.session_state.messages.append({
            "role": "assistant",
            "content": full_response,
            "timestamp": timestamp
        })
        
        # Rerun to update UI
        st.rerun()