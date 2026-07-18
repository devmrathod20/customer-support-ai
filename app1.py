"""
=========================================================
Customer Support AI
Streamlit + n8n + Amazon Bedrock
=========================================================
"""

# ==========================================================
# IMPORTS
# ==========================================================

import streamlit as st
from PIL import Image

from components import (
    load_css,
    hero,
    metrics_row,
    feature_grid,
    chat_header,
    welcome_card,
    render_chat_history,
    spacer,
    divider,
    quick_action_card,
    session_card,
    footer,
    badge,
)

from utils import (
    initialize_session,
    get_chat_history,
    add_user_message,
    add_assistant_message,
    send_to_n8n,
    clean_message,
    is_valid_message,
    conversation_stats,
    export_chat,
    reset_chat,
    get_session_id,
    check_webhook,
)

# ==========================================================
# PAGE CONFIG
# ==========================================================

try:
    logo = Image.open("assets/chatbot.png")
except Exception:
    logo = None

st.set_page_config(
    page_title="Customer Support AI",
    page_icon=logo,
    layout="wide",
    initial_sidebar_state="expanded",
)

# ==========================================================
# LOAD CSS
# ==========================================================

load_css("styles.css")

# ==========================================================
# INITIALIZE SESSION
# ==========================================================

initialize_session()

# ==========================================================
# HERO
# ==========================================================

hero()

spacer(20)

# ==========================================================
# METRICS
# ==========================================================

metrics_row()

spacer(25)

# ==========================================================
# FEATURES
# ==========================================================

feature_grid()

spacer(25)

# ==========================================================
# CHAT HEADER
# ==========================================================

chat_header()

# ==========================================================
# WELCOME CARD
# ==========================================================

if len(get_chat_history()) <= 1:

    welcome_card()

spacer(15)

# ==========================================================
# SIDEBAR
# ==========================================================

with st.sidebar:

    st.markdown("## 🚀 Quick Support")

    divider()

    quick_action_card(
        "📦",
        "Track Order",
        "Track any customer order",
    )

    if st.button(
        "Track Order",
        use_container_width=True,
        key="track_btn",
    ):
        st.session_state.quick_message = (
            "Track my order"
        )

    spacer(10)

    quick_action_card(
        "💰",
        "Refund",
        "Refund information",
    )

    if st.button(
        "Refund",
        use_container_width=True,
        key="refund_btn",
    ):
        st.session_state.quick_message = (
            "Refund status"
        )

    spacer(10)

    quick_action_card(
        "↩️",
        "Return",
        "Return policy",
    )

    if st.button(
        "Return",
        use_container_width=True,
        key="return_btn",
    ):
        st.session_state.quick_message = (
            "Return policy"
        )

    spacer(10)

    quick_action_card(
        "📞",
        "Contact",
        "Talk to support",
    )

    if st.button(
        "Contact Support",
        use_container_width=True,
        key="contact_btn",
    ):
        st.session_state.quick_message = (
            "Contact support"
        )

    divider()

    st.markdown("### ⚡ AI Status")

    if check_webhook():

        badge("🟢 n8n Connected")

    else:

        st.error("Webhook Offline")

    divider()

    stats = conversation_stats()

    st.metric(
        "Messages",
        stats["total"],
    )

    session_card(
        get_session_id()
    )

    divider()

    st.download_button(
        "📄 Export Chat",
        export_chat(),
        "conversation.txt",
        "text/plain",
        use_container_width=True,
    )

    if st.button(
        "🗑 Clear Chat",
        use_container_width=True,
    ):

        reset_chat()

        st.rerun()

# ==========================================================
# CHAT CONTAINER
# ==========================================================

chat_container = st.container()

with chat_container:

    render_chat_history(
        get_chat_history()
    )
# ==========================================================
# QUICK ACTION HANDLER
# ==========================================================

if "quick_message" in st.session_state:

    prompt = st.session_state.pop("quick_message")

    prompt = clean_message(prompt)

    if is_valid_message(prompt):

        add_user_message(prompt)

        with st.spinner("🤖 AI is thinking..."):

            try:

                response = send_to_n8n(prompt)

            except Exception as e:

                response = f"❌ Error:\n\n{e}"

        add_assistant_message(response)

        st.rerun()


# ==========================================================
# CHAT INPUT
# ==========================================================

prompt = st.chat_input(
    "💬 Ask about orders, refunds, returns..."
)

if prompt:

    prompt = clean_message(prompt)

    if is_valid_message(prompt):

        add_user_message(prompt)

        with st.spinner("🤖 AI is thinking..."):

            try:

                response = send_to_n8n(prompt)

            except Exception as e:

                response = (
                    "❌ Unable to contact AI service.\n\n"
                    f"{e}"
                )

        add_assistant_message(response)

        st.rerun()


# ==========================================================
# FOOTER
# ==========================================================

spacer(40)

footer()


# ==========================================================
# AUTO SCROLL
# ==========================================================

st.markdown(
    """
<script>
const chat=document.querySelector('section.main');
if(chat){
    window.scrollTo({
        top:document.body.scrollHeight,
        behavior:'smooth'
    });
}
</script>
""",
    unsafe_allow_html=True,
)


# ==========================================================
# CONNECTION WARNING
# ==========================================================

if not check_webhook():

    st.warning(
        """
⚠️ n8n webhook is currently offline.

Please start your n8n server before sending
messages.

Example:

http://localhost:5678
"""
    )


# ==========================================================
# END OF APP
# ==========================================================