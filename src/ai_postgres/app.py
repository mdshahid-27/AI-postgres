import streamlit as st
import requests

# FastAPI backend endpoint
API_URL = "http://127.0.0.1:8000/chat"

# Page configuration
st.set_page_config(
    page_title="Library AI Assistant",
    page_icon="📚",
    layout="centered"
)

# Custom styling for a better chat interface
st.markdown("""
    <style>
    .stChatMessage {
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 0.5rem;
    }
    </style>
""", unsafe_allow_html=True)

st.title("📚 Library Assistant Chatbot")
st.caption("Powered by FastAPI, Google GenAI, and PostgreSQL tools")

# Initialize chat history in session state if it doesn't exist
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display prior chat messages when the page re-runs
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input via chat input box
if user_input := st.chat_input("Ask something about books, authors, users, or slots..."):
    # Add user message to session state and display it
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # Call the FastAPI backend
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                response = requests.post(API_URL, json={"message": user_input})
                
                if response.status_code == 200:
                    bot_reply = response.json().get("response", "No response content found.")
                else:
                    bot_reply = f"⚠️ Error from server: Status code {response.status_code}"
            except requests.exceptions.ConnectionError:
                bot_reply = "⚠️ Connection error: Could not connect to the FastAPI backend. Make sure it is running on port 8000."
            
            st.markdown(bot_reply)
            
    # Add assistant response to session state
    st.session_state.messages.append({"role": "assistant", "content": bot_reply})