
import streamlit as st
import requests
import uuid
import base64
from PIL import Image

# ==============================
# PAGE CONFIG
# ==============================
logo = Image.open("chatbot.png")

st.set_page_config(
    page_title="Customer Support Chatbot",
    page_icon=logo,
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==============================
# BACKGROUND IMAGE
# ==============================
def get_base64(file_path):
    with open(file_path, "rb") as f:
        return base64.b64encode(f.read()).decode()

try:
    bg_image = get_base64("background.jpg")

    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("data:image/jpg;base64,{bg_image}");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            background-attachment: fixed;
        }}

        [data-testid="stSidebar"] {{
            background-color: rgba(255,255,255,0.95);
        }}

        [data-testid="stChatMessage"] {{
            background-color: rgba(255,255,255,0.92);
            border-radius: 12px;
            padding: 10px;
            margin-bottom: 8px;
        }}

        .header-container {{
            background: rgba(255,255,255,0.90);
            padding: 15px;
            border-radius: 15px;
            margin-bottom: 15px;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

except Exception:
    pass

# ==============================
# SESSION
# ==============================
if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())

if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "Hello 👋 Welcome to Customer Support. How can I help you today?"
        }
    ]

# ==============================
# WEBHOOK
# ==============================
WEBHOOK_URL = "http://localhost:5678/webhook/chatbot"

# ==============================
# HEADER
# ==============================
st.markdown('<div class="header-container">', unsafe_allow_html=True)

col1, col2 = st.columns([1, 8])

with col1:
    try:
        st.image("chatbot.png", width=130)
    except:
        pass

with col2:
    st.markdown(
        """
        <h1 style="
            color:white;
            margin-bottom:0px;
            font-size:42px;
            font-weight:700;
            text-shadow:2px 2px 8px rgba(0,0,0,0.6);
        ">
            Customer Support Chatbot
        </h1>

        <p style="
            color:white;
            font-size:18px;
            margin-top:0px;
            text-shadow:1px 1px 6px rgba(0,0,0,0.6);
        ">
            Track Orders • Refunds • Returns • Support
        </p>
        """,
        unsafe_allow_html=True
    )
st.markdown('</div>', unsafe_allow_html=True)

# ==============================
# RESPONSE PARSER
# ==============================
def parse_response(data):

    if isinstance(data, list):
        if len(data) > 0 and isinstance(data[0], dict):
            return (
                data[0].get("text")
                or data[0].get("output")
                or str(data[0])
            )
        return str(data)

    if isinstance(data, dict):
        return (
            data.get("text")
            or data.get("output")
            or data.get("message")
            or str(data)
        )

    return str(data)

# ==============================
# N8N CALL
# ==============================
def send_to_n8n(message):

    try:

        response = requests.post(
            WEBHOOK_URL,
            json={
                "message": message,
                "session_id": st.session_state.session_id
            },
            timeout=30
        )

        if response.status_code != 200:
            return f"Server Error: {response.status_code}"

        try:
            data = response.json()
            return parse_response(data)

        except:
            return response.text

    except Exception as e:
        return f"Connection Error: {e}"

# ==============================
# PROCESS MESSAGE
# ==============================
def process_message(prompt):

    st.session_state.messages.append(
        {
            "role": "user",
            "content": prompt
        }
    )

    reply = send_to_n8n(prompt)

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": reply
        }
    )

# ==============================
# CHAT HISTORY
# ==============================
for msg in st.session_state.messages:

    with st.chat_message(msg["role"]):

        if msg["role"] == "assistant":
            st.text(msg["content"])
        else:
            st.markdown(msg["content"])

# ==============================
# SIDEBAR
# ==============================
with st.sidebar:

    st.title("🛠 Quick Support")

    if st.button("📦 Track Order"):
        st.session_state["quick_message"] = "Where is my order?"

    if st.button("↩️ Return Policy"):
        st.session_state["quick_message"] = "What is your return policy?"

    if st.button("💰 Refund Policy"):
        st.session_state["quick_message"] = "What is your refund policy?"

    if st.button("📞 Contact Support"):
        st.session_state["quick_message"] = "How can I contact support?"

    st.markdown("---")

    st.subheader("Example Queries")

    st.code("Where is my order 22345?")
    st.code("Track order 22345")
    st.code("What is your return policy?")
    st.code("How can I contact support?")

    st.markdown("---")

    if st.button("🗑 Clear Chat"):

        st.session_state.messages = [
            {
                "role": "assistant",
                "content": "Hello 👋 Welcome to Customer Support. How can I help you today?"
            }
        ]

        st.rerun()

# ==============================
# QUICK ACTION HANDLER
# ==============================
if "quick_message" in st.session_state:

    prompt = st.session_state.pop("quick_message")

    process_message(prompt)

    st.rerun()

# ==============================
# CHAT INPUT
# ==============================
prompt = st.chat_input("Type your message...")

if prompt:

    process_message(prompt)

    st.rerun()
