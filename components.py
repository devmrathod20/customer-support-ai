"""
=========================================================
components.py
Premium UI Components
Customer Support AI
=========================================================
"""

import streamlit as st
from pathlib import Path
from datetime import datetime


# ==========================================================
# LOAD CSS
# ==========================================================

def load_css(css_file="styles.css"):
    """
    Load external CSS.
    """

    css_path = Path(css_file)

    if css_path.exists():

        with open(css_path, "r", encoding="utf-8") as f:

            st.markdown(
                f"<style>{f.read()}</style>",
                unsafe_allow_html=True
            )

    else:

        st.warning(f"CSS file not found : {css_file}")


# ==========================================================
# HERO SECTION
# ==========================================================

def hero():

    st.markdown(
        """
<div class="hero fade">

<h1>
🤖 Customer Support AI
</h1>

<p>

AI-powered customer support using
Amazon Bedrock + n8n + Streamlit

</p>

<div class="status">

AI Online

</div>

</div>
""",
        unsafe_allow_html=True,
    )


# ==========================================================
# PAGE TITLE
# ==========================================================

def page_title(title, subtitle=""):

    st.markdown(
        f"""
<h2 style="
margin-top:20px;
margin-bottom:5px;
color:white;
font-weight:700;
">

{title}

</h2>

<p style="
color:#94A3B8;
margin-bottom:25px;
">

{subtitle}

</p>
""",
        unsafe_allow_html=True,
    )


# ==========================================================
# GLASS CARD
# ==========================================================

def glass_card(title, body):

    st.markdown(
        f"""
<div class="glass-card">

<h3>

{title}

</h3>

<p>

{body}

</p>

</div>
""",
        unsafe_allow_html=True,
    )


# ==========================================================
# BADGE
# ==========================================================

def badge(text):

    st.markdown(
        f"""
<div class="badge">

{text}

</div>
""",
        unsafe_allow_html=True,
    )


# ==========================================================
# SECTION DIVIDER
# ==========================================================

def divider():

    st.markdown(
        "<hr>",
        unsafe_allow_html=True
    )


# ==========================================================
# SPACER
# ==========================================================

def spacer(height=20):

    st.markdown(

        f"<div style='height:{height}px'></div>",

        unsafe_allow_html=True

    )


# ==========================================================
# CURRENT TIME
# ==========================================================

def current_time():

    return datetime.now().strftime("%I:%M %p")
# ==========================================================
# CHAT MESSAGE COMPONENTS
# ==========================================================

def user_message(message: str, time: str = ""):
    """
    Render a user message.
    """

    with st.chat_message("user"):

        st.markdown(
            f"""
<div class="message-row user">

<div class="user-message">

{message}

</div>

</div>

<p style="
text-align:right;
font-size:12px;
color:#94A3B8;
margin-top:6px;
">

{time}

</p>
""",
            unsafe_allow_html=True,
        )


def assistant_message(message: str, time: str = ""):
    """
    Render an assistant message.
    """

    with st.chat_message("assistant"):

        st.markdown(
            f"""
<div class="message-row">

<div class="avatar">

🤖

</div>

<div class="bot-message">

{message}

</div>

</div>

<p style="
margin-left:58px;
font-size:12px;
color:#94A3B8;
margin-top:6px;
">

{time}

</p>
""",
            unsafe_allow_html=True,
        )


# ==========================================================
# CHAT HISTORY
# ==========================================================

def render_chat_history(messages):
    """
    Display all messages.
    """

    for msg in messages:

        role = msg.get("role", "assistant")

        content = msg.get("content", "")

        timestamp = msg.get("time", "")

        if role == "user":

            user_message(content, timestamp)

        else:

            assistant_message(content, timestamp)


# ==========================================================
# TYPING INDICATOR
# ==========================================================

def typing_indicator():
    """
    Animated typing indicator.
    """

    st.markdown(
        """
<div class="message-row">

<div class="avatar">

🤖

</div>

<div class="bot-message">

<div class="typing">

<span></span>
<span></span>
<span></span>

</div>

</div>

</div>
""",
        unsafe_allow_html=True,
    )


# ==========================================================
# STREAM RESPONSE
# ==========================================================

def stream_response(text: str, speed: float = 0.015):
    """
    Stream text with a typing effect.
    """

    import time

    placeholder = st.empty()

    output = ""

    for ch in text:

        output += ch

        placeholder.markdown(output + "▌")

        time.sleep(speed)

    placeholder.markdown(output)

    return output


# ==========================================================
# WELCOME CARD
# ==========================================================

def welcome_card():

    st.markdown(
        """
<div class="glass-card fade">

<h2>

👋 Welcome

</h2>

<p>

I'm your AI Customer Support Assistant.

I can help you with:

</p>

<ul>

<li>📦 Track Orders</li>

<li>💰 Refund Status</li>

<li>↩️ Return Policy</li>

<li>📞 Customer Support</li>

</ul>

</div>
""",
        unsafe_allow_html=True,
    )
# ==========================================================
# QUICK ACTION CARD
# ==========================================================

def quick_action_card(icon, title, description):

    st.markdown(
        f"""
<div class="quick-card">

<div class="quick-icon">
{icon}
</div>

<div class="quick-text">

<div class="quick-title">
{title}
</div>

<div class="quick-desc">
{description}
</div>

</div>

</div>
""",
        unsafe_allow_html=True,
    )


# ==========================================================
# METRIC CARD
# ==========================================================

def metric_card(title, value, icon):

    st.markdown(
        f"""
<div class="metric-card">

<div>

<div class="metric-title">

{title}

</div>

<div class="metric-value">

{value}

</div>

</div>

<div class="metric-icon">

{icon}

</div>

</div>
""",
        unsafe_allow_html=True,
    )


# ==========================================================
# METRICS ROW
# ==========================================================

def metrics_row():

    col1, col2, col3 = st.columns(3)

    with col1:

        metric_card(
            "Orders",
            "24K+",
            "📦"
        )

    with col2:

        metric_card(
            "Accuracy",
            "99.2%",
            "🎯"
        )

    with col3:

        metric_card(
            "Support",
            "24/7",
            "🤖"
        )


# ==========================================================
# SESSION CARD
# ==========================================================

def session_card(session_id):

    short_id = session_id[:8]

    st.markdown(
        f"""
<div class="glass-card">

<h4>

🆔 Session

</h4>

<p>

{short_id}

</p>

</div>
""",
        unsafe_allow_html=True,
    )


# ==========================================================
# CHAT HEADER
# ==========================================================

def chat_header():

    st.markdown(
        """
<div style="margin-bottom:20px;">

<h2 style="color:white;">

💬 Conversation

</h2>

<p style="color:#94A3B8;">

Start chatting with your AI assistant.

</p>

</div>
""",
        unsafe_allow_html=True,
    )


# ==========================================================
# FEATURE GRID
# ==========================================================

def feature_grid():

    col1, col2, col3 = st.columns(3)

    with col1:

        glass_card(
            "📦 Order Tracking",
            "Track customer orders instantly using AI."
        )

    with col2:

        glass_card(
            "💰 Refunds",
            "Provide refund information automatically."
        )

    with col3:

        glass_card(
            "📞 Customer Support",
            "24×7 AI-powered assistance."
        )


# ==========================================================
# FOOTER
# ==========================================================

def footer():

    st.markdown(
        """
<div class="footer">

<p>

Built with ❤️ using

<strong>Python</strong> •

<strong>Streamlit</strong> •

<strong>n8n</strong> •

<strong>Amazon Bedrock</strong>

</p>

</div>
""",
        unsafe_allow_html=True,
    )


# ==========================================================
# END OF FILE
# ==========================================================