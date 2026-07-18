"""
=========================================================
utils.py
Backend Utilities
=========================================================
"""

import uuid
from datetime import datetime
import requests
import streamlit as st

# ==========================================================
# CONFIGURATION
# ==========================================================

# Change this when deploying
WEBHOOK_URL = "http://localhost:5678/webhook/chatbot"

REQUEST_TIMEOUT = 30

WELCOME_MESSAGE = (
    "👋 Hello! Welcome to Customer Support AI.\n\n"
    "How can I help you today?"
)

# ==========================================================
# SESSION INITIALIZATION
# ==========================================================

def initialize_session():
    """
    Initialize Streamlit session state.
    """

    if "session_id" not in st.session_state:
        st.session_state.session_id = str(uuid.uuid4())

    if "messages" not in st.session_state:
        st.session_state.messages = [
            {
                "role": "assistant",
                "content": WELCOME_MESSAGE,
                "time": current_time(),
            }
        ]

# ==========================================================
# CURRENT TIME
# ==========================================================

def current_time():
    """
    Return formatted current time.
    """

    return datetime.now().strftime("%I:%M %p")

# ==========================================================
# CHAT HISTORY
# ==========================================================

def get_chat_history():
    """
    Return complete conversation.
    """

    return st.session_state.messages

# ==========================================================
# USER MESSAGE
# ==========================================================

def add_user_message(message: str):
    """
    Store user message.
    """

    st.session_state.messages.append(
        {
            "role": "user",
            "content": message,
            "time": current_time(),
        }
    )

# ==========================================================
# ASSISTANT MESSAGE
# ==========================================================

def add_assistant_message(message: str):
    """
    Store assistant message.
    """

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": message,
            "time": current_time(),
        }
    )

# ==========================================================
# RESET CHAT
# ==========================================================

def reset_chat():
    """
    Clear conversation while keeping session ID.
    """

    st.session_state.messages = [
        {
            "role": "assistant",
            "content": WELCOME_MESSAGE,
            "time": current_time(),
        }
    ]
# ==========================================================
# RESPONSE PARSER
# ==========================================================

def parse_response(data):
    """
    Parse different response formats returned by n8n.
    """

    # Plain string
    if isinstance(data, str):
        return data.strip()

    # List response
    if isinstance(data, list):

        if len(data) == 0:
            return "No response received."

        first = data[0]

        if isinstance(first, dict):

            for key in [
                "text",
                "response",
                "answer",
                "output",
                "message",
                "content",
            ]:
                if key in first:
                    return str(first[key])

            return str(first)

        return str(first)

    # Dictionary response
    if isinstance(data, dict):

        for key in [
            "text",
            "response",
            "answer",
            "output",
            "message",
            "content",
        ]:

            if key in data:
                return str(data[key])

        return str(data)

    return str(data)


# ==========================================================
# SEND REQUEST TO N8N
# ==========================================================

def send_to_n8n(message: str):
    """
    Send user message to the n8n webhook and return the parsed reply.
    """

    payload = {
        "message": message,
        "session_id": st.session_state.session_id,
    }

    try:

        response = requests.post(
            WEBHOOK_URL,
            json=payload,
            timeout=REQUEST_TIMEOUT,
        )

    except requests.exceptions.Timeout:

        return (
            "⏳ The request timed out. "
            "Please try again."
        )

    except requests.exceptions.ConnectionError:

        return (
            "❌ Unable to connect to the n8n server.\n\n"
            "Make sure:\n"
            "- n8n is running\n"
            "- The webhook is active\n"
            "- The WEBHOOK_URL is correct"
        )

    except requests.exceptions.RequestException as e:

        return f"Network Error:\n{e}"


    # ======================================================
    # HTTP STATUS
    # ======================================================

    if response.status_code != 200:

        return (
            f"Server Error ({response.status_code})"
        )


    # ======================================================
    # TRY JSON
    # ======================================================

    try:

        data = response.json()

        return parse_response(data)

    except ValueError:

        if response.text.strip():

            return response.text.strip()

        return "Empty response received from server."
# ==========================================================
# EXPORT CONVERSATION
# ==========================================================

def export_chat():
    """
    Export the conversation as plain text.
    """

    conversation = []

    for message in st.session_state.messages:

        role = (
            "You"
            if message["role"] == "user"
            else "AI"
        )

        time = message.get("time", "")

        conversation.append(
            f"[{time}] {role}: {message['content']}"
        )

    return "\n\n".join(conversation)


# ==========================================================
# CONVERSATION STATISTICS
# ==========================================================

def conversation_stats():
    """
    Return conversation statistics.
    """

    messages = st.session_state.messages

    user_count = sum(
        1
        for msg in messages
        if msg["role"] == "user"
    )

    assistant_count = sum(
        1
        for msg in messages
        if msg["role"] == "assistant"
    )

    return {
        "total": len(messages),
        "user": user_count,
        "assistant": assistant_count,
    }


# ==========================================================
# CHECK WEBHOOK STATUS
# ==========================================================

def check_webhook():
    """
    Check whether the webhook is reachable.
    """

    try:

        response = requests.get(
            WEBHOOK_URL,
            timeout=5,
        )

        return response.status_code in (200, 404, 405)

    except Exception:

        return False


# ==========================================================
# FORMAT USER INPUT
# ==========================================================

def clean_message(message: str):
    """
    Clean user input before sending.
    """

    if not message:
        return ""

    return message.strip()


# ==========================================================
# VALIDATE MESSAGE
# ==========================================================

def is_valid_message(message: str):
    """
    Validate user input.
    """

    if message is None:
        return False

    if len(message.strip()) == 0:
        return False

    return True


# ==========================================================
# NEW SESSION
# ==========================================================

def new_session():
    """
    Create a brand-new session.
    """

    st.session_state.session_id = str(uuid.uuid4())

    reset_chat()


# ==========================================================
# GET SESSION ID
# ==========================================================

def get_session_id():

    return st.session_state.session_id


# ==========================================================
# SAVE MESSAGE
# ==========================================================

def save_message(role, content):

    st.session_state.messages.append(
        {
            "role": role,
            "content": content,
            "time": current_time(),
        }
    )


# ==========================================================
# LAST MESSAGE
# ==========================================================

def last_message():

    if len(st.session_state.messages) == 0:

        return None

    return st.session_state.messages[-1]


# ==========================================================
# CLEAR ONLY USER MESSAGES
# ==========================================================

def clear_user_messages():

    st.session_state.messages = [

        msg

        for msg in st.session_state.messages

        if msg["role"] == "assistant"

    ]


# ==========================================================
# APP INFORMATION
# ==========================================================

APP_NAME = "Customer Support AI"

APP_VERSION = "1.0.0"

AUTHOR = "Dev Rathod"


def app_info():

    return {

        "name": APP_NAME,

        "version": APP_VERSION,

        "author": AUTHOR,

    }


# ==========================================================
# END OF FILE
# ==========================================================