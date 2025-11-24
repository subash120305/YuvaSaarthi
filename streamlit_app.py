"""
YuvaSaarthi - Streamlit Web Interface
Modern UI without sidebar
"""

import streamlit as st
from datetime import datetime
from loguru import logger
import uuid

from backend.chatbot_engine import get_chatbot
from utils.config import settings, SUPPORTED_LANGUAGES


# Page configuration
st.set_page_config(
    page_title="YuvaSaarthi - AI Educational Assistant",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for modern UI
st.markdown("""
<style>
    /* Hide sidebar */
    [data-testid="stSidebar"] {
        display: none;
    }

    /* Main container */
    .main-header {
        font-size: 2.5rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 0.5rem;
    }

    .sub-header {
        text-align: center;
        color: #666;
        margin-bottom: 2rem;
    }

    /* Chat messages */
    .chat-message {
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
    }

    .user-message {
        background-color: #e3f2fd;
        border-left: 4px solid #1f77b4;
        margin-left: auto;
        margin-right: 0;
        max-width: 70%;
        text-align: right;
    }

    .assistant-message {
        background-color: #f5f5f5;
        border-left: 4px solid #4caf50;
        margin-left: 0;
        margin-right: auto;
        max-width: 70%;
    }

    /* Suggestion chips */
    .suggestion-container {
        position: fixed;
        bottom: 120px;
        left: 50%;
        transform: translateX(-50%);
        z-index: 999;
        display: flex;
        gap: 10px;
        flex-wrap: wrap;
        justify-content: center;
        max-width: 800px;
    }

    .suggestion-chip {
        background: white;
        border: 1px solid #ddd;
        border-radius: 20px;
        padding: 8px 16px;
        cursor: pointer;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        transition: all 0.2s;
        font-size: 14px;
    }

    .suggestion-chip:hover {
        background: #e3f2fd;
        border-color: #1f77b4;
        box-shadow: 0 4px 8px rgba(0,0,0,0.15);
    }

    /* Dropdown menus */
    .dropdown-container {
        position: relative;
        display: inline-block;
    }

    .dropdown-btn {
        background: white;
        border: 1px solid #ddd;
        border-radius: 4px;
        padding: 8px 12px;
        cursor: pointer;
        font-size: 14px;
        min-width: 80px;
    }

    .dropdown-menu {
        position: absolute;
        bottom: 100%;
        right: 0;
        background: white;
        border: 1px solid #ddd;
        border-radius: 4px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.15);
        margin-bottom: 5px;
        z-index: 1000;
        min-width: 150px;
    }

    .dropdown-item {
        padding: 10px 15px;
        cursor: pointer;
        border-bottom: 1px solid #f0f0f0;
    }

    .dropdown-item:hover {
        background: #f5f5f5;
    }

    .dropdown-item:last-child {
        border-bottom: none;
    }

    /* Input area container */
    .input-controls {
        position: fixed;
        bottom: 20px;
        left: 50%;
        transform: translateX(-50%);
        width: 90%;
        max-width: 800px;
        display: flex;
        gap: 10px;
        align-items: center;
        background: white;
        padding: 10px;
        border-radius: 10px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        z-index: 998;
    }

    /* Resource cards */
    .video-card {
        border: 1px solid #ddd;
        border-radius: 0.5rem;
        padding: 1rem;
        margin-bottom: 0.5rem;
    }

    /* Force selectbox dropdown to open upwards */
    div[data-baseweb="select"] > div[role="listbox"] {
        bottom: 100% !important;
        top: auto !important;
        margin-bottom: 5px !important;
    }

    /* Hide dropdown arrow on selectbox */
    div[data-baseweb="select"] svg {
        display: none !important;
    }

    /* Ensure language dropdown opens upward */
    div[data-testid="stSelectbox"] div[data-baseweb="select"] > div {
        bottom: 100% !important;
        top: auto !important;
        margin-bottom: 5px !important;
    }

    /* Force popover to open upwards and left */
    div[data-testid="stPopover"] > div {
        bottom: 100% !important;
        top: auto !important;
        right: 0 !important;
        left: auto !important;
        margin-bottom: 5px !important;
    }

    /* Simplify popover button styles */
    div[data-testid="stPopover"] button[kind="secondary"] {
        width: 100%;
        text-align: left;
        padding: 10px 15px !important;
        border: none !important;
        background: white !important;
        margin: 0 !important;
    }

    div[data-testid="stPopover"] button[kind="secondary"]:hover {
        background: #f5f5f5 !important;
    }

    /* Hide popover arrow */
    div[data-testid="stPopover"] button[kind="header"] svg {
        display: none !important;
    }

    /* Footer styling */
    .footer {
        position: fixed;
        bottom: 0;
        left: 0;
        width: 100%;
        background-color: #f5f5f5;
        color: #666;
        text-align: center;
        padding: 10px 0;
        font-size: 12px;
        border-top: 1px solid #ddd;
        z-index: 1000;
    }
</style>
""", unsafe_allow_html=True)


# Initialize session state
if 'chatbot' not in st.session_state:
    st.session_state.chatbot = get_chatbot()

if 'messages' not in st.session_state:
    st.session_state.messages = []
    # Add welcome message on first load
    welcome_msg = {
        "role": "assistant",
        "content": """नमस्ते! 🙏 मैं युवासारथी हूँ, राजस्थान तकनीकी शिक्षा विभाग का AI शिक्षा सहायक।

मैं आपकी इन सभी चीज़ों में मदद कर सकता हूँ:

📚 **शैक्षणिक विषय:**
• कक्षा 8-12: गणित, विज्ञान, अंग्रेजी, हिंदी, सामाजिक विज्ञान
• इंजीनियरिंग, पॉलिटेक्निक, तकनीकी शिक्षा

🎓 **प्रवेश और परीक्षाएं:**
• RBSE परीक्षा, परिणाम, ग्रेडिंग
• कॉलेज प्रवेश, पात्रता, आवेदन प्रक्रिया
• फीस, छात्रवृत्ति, आरक्षण जानकारी

📖 **अध्ययन मार्गदर्शन:**
• परीक्षा की तैयारी और अध्ययन तकनीक
• करियर सलाह और शिक्षा योजना

मुझसे कोई भी शिक्षा संबंधी सवाल पूछें! 😊

---

Hello! 🙏 I'm YuvaSaarthi, AI Education Assistant for Rajasthan Department of Technical Education.

I can help you with:

📚 **Academic Subjects:** Class 8-12, Engineering, Polytechnic
🎓 **Admissions & Exams:** RBSE, College admissions, Scholarships
📖 **Study Guidance:** Exam preparation, Career advice

Ask me any education-related question! 😊""",
        "videos": [],
        "articles": []
    }
    st.session_state.messages.append(welcome_msg)

if 'user_id' not in st.session_state:
    st.session_state.user_id = str(uuid.uuid4())

if 'language' not in st.session_state:
    st.session_state.language = "en"  # Default to English

if 'include_resources' not in st.session_state:
    st.session_state.include_resources = True

if 'current_input' not in st.session_state:
    st.session_state.current_input = ""

if 'text_input_value' not in st.session_state:
    st.session_state.text_input_value = ""


# Sample questions in all languages
SAMPLE_QUESTIONS = {
    "en": [
        "What is SC reservation in Rajasthan?",
        "Explain Pythagoras theorem",
        "What are the admission requirements?"
    ],
    "hi": [
        "राजस्थान में SC आरक्षण क्या है?",
        "पाइथागोरस प्रमेय समझाओ",
        "प्रवेश की आवश्यकताएं क्या हैं?"
    ],
    "raj": [
        "राजस्थान में SC आरक्षण कांई है?",
        "पाइथागोरस थ्योरम समझावो",
        "दाखिलो री जरूरत कांई है?"
    ]
}


def display_message(role: str, content: str, message_id: str = ""):
    """Display a chat message with action buttons for assistant"""
    css_class = "user-message" if role == "user" else "assistant-message"

    st.markdown(f"""
    <div class="chat-message {css_class}">
        {content}
    </div>
    """, unsafe_allow_html=True)

    # Add action buttons for assistant messages
    if role == "assistant":
        # Custom CSS for plain icon buttons with no borders
        st.markdown("""
        <style>
        div[data-testid="column"] button {
            border: none !important;
            background: transparent !important;
            padding: 4px 8px !important;
            min-height: 24px !important;
            height: 24px !important;
            font-size: 14px !important;
            color: #666 !important;
            cursor: pointer !important;
        }
        div[data-testid="column"] button:hover {
            color: #1f77b4 !important;
            background: transparent !important;
        }
        div[data-testid="column"] button p {
            margin: 0 !important;
            padding: 0 !important;
        }
        </style>
        """, unsafe_allow_html=True)

        col1, col2, col3, col4, col5, col6 = st.columns([0.3, 0.3, 0.3, 0.3, 0.3, 10])

        with col1:
            if st.button("📋", key=f"copy_{message_id}", help="Copy", type="secondary"):
                st.session_state.clipboard = content
                st.success("Copied!")

        with col2:
            if st.button("👍", key=f"like_{message_id}", help="Good response", type="secondary"):
                st.success("Thanks for feedback!")

        with col3:
            if st.button("👎", key=f"dislike_{message_id}", help="Bad response", type="secondary"):
                st.info("Feedback noted")

        with col4:
            if st.button("🔄", key=f"regen_{message_id}", help="Regenerate", type="secondary"):
                # Get the last user query
                user_messages = [m for m in st.session_state.messages if m["role"] == "user"]
                if user_messages:
                    last_query = user_messages[-1]["content"]
                    # Remove last assistant response
                    st.session_state.messages = st.session_state.messages[:-1]
                    process_query(last_query)
                    st.rerun()

        with col5:
            if st.button("↗", key=f"share_{message_id}", help="Share", type="secondary"):
                st.warning("Deploy app to enable sharing")


def display_video(video: dict):
    """Display a YouTube video card"""
    st.markdown(f"""
    <div class="video-card">
        <strong>📺 {video['title']}</strong><br>
        <small>Channel: {video['channel']}</small><br>
        <a href="{video['url']}" target="_blank">Watch Video</a>
    </div>
    """, unsafe_allow_html=True)


def display_article(article: dict):
    """Display a web article card"""
    st.markdown(f"""
    <div class="video-card">
        <strong>📚 {article['title']}</strong><br>
        <small>Source: {article['source']}</small><br>
        <a href="{article['url']}" target="_blank">Read Article</a>
    </div>
    """, unsafe_allow_html=True)


def main():
    """Main Streamlit app"""

    # Header
    st.markdown('<h1 class="main-header">🎓 YuvaSaarthi</h1>', unsafe_allow_html=True)
    st.markdown(
        f'<p class="sub-header">AI Educational Assistant - {settings.department_name}, Rajasthan</p>',
        unsafe_allow_html=True
    )

    # Main chat area
    chat_container = st.container()

    # Display chat history
    with chat_container:
        for idx, message in enumerate(st.session_state.messages):
            if message["role"] in ["user", "assistant"]:
                display_message(message["role"], message["content"], message_id=str(idx))

            # Display learning resources if present
            if message["role"] == "assistant":
                # Display videos
                if "videos" in message and message["videos"]:
                    st.markdown("---")
                    st.markdown("### 📺 Recommended Videos")
                    cols = st.columns(min(len(message["videos"]), 2))
                    for idx, video in enumerate(message["videos"]):
                        with cols[idx]:
                            display_video(video)

                # Display articles
                if "articles" in message and message["articles"]:
                    st.markdown("### 📚 Recommended Articles")
                    cols = st.columns(min(len(message["articles"]), 3))
                    for idx, article in enumerate(message["articles"]):
                        with cols[idx]:
                            display_article(article)

    # Add spacing for fixed input area
    st.markdown("<div style='height: 80px;'></div>", unsafe_allow_html=True)

    # Show quick suggestions with filtering based on input
    suggestions = SAMPLE_QUESTIONS.get(st.session_state.language, SAMPLE_QUESTIONS["en"])

    # Filter suggestions based on what user is typing
    if st.session_state.text_input_value:
        user_input_lower = st.session_state.text_input_value.lower()
        filtered_suggestions = [s for s in suggestions if s.lower().startswith(user_input_lower)]
    else:
        filtered_suggestions = suggestions

    if filtered_suggestions:
        st.markdown("**💡 Quick Suggestions:**")
        for idx, suggestion in enumerate(filtered_suggestions):
            if st.button(
                suggestion,
                key=f"sugg_{idx}",
                type="secondary"
            ):
                process_query(suggestion)
                st.session_state.text_input_value = ""  # Clear input
                st.rerun()

    # Input row: Chat box + Language dropdown + Settings gear
    input_col, lang_col, settings_col = st.columns([10, 1, 1])

    with input_col:
        # Use text_input with on_change callback to track real-time typing
        prompt = st.text_input(
            "Ask me anything... / मुझसे कुछ भी पूछें...",
            value=st.session_state.text_input_value,
            key="user_input_box",
            label_visibility="collapsed",
            on_change=lambda: setattr(st.session_state, 'text_input_value', st.session_state.user_input_box)
        )

    with lang_col:
        language_options = {
            "en": "English",
            "hi": "हिंदी",
            "raj": "राजस्थानी"
        }
        selected_lang = st.selectbox(
            "🌐",
            options=list(language_options.keys()),
            format_func=lambda x: language_options[x],
            index=list(language_options.keys()).index(st.session_state.language),
            label_visibility="collapsed",
            key="lang_selector"
        )
        if selected_lang != st.session_state.language:
            st.session_state.language = selected_lang
            st.rerun()

    with settings_col:
        with st.popover("⚙"):
            if st.button("🏥 Check Status", use_container_width=True):
                with st.spinner("Checking..."):
                    health = st.session_state.chatbot.get_system_health()
                    st.write("**System Health:**")
                    st.write(f"🤖 LLM: {health['llm']['status']}")
                    st.write(f"📺 YouTube: {health['youtube']['status']}")
                    st.write(f"🌐 Web: {health['web_search']['status']}")
                    st.write(f"💬 Translation: {health['translation']['status']}")
                    st.write(f"📚 KB: {health['vector_store']['status']}")

            if st.button("🗑️ Clear Chat", use_container_width=True):
                st.session_state.messages = []
                st.session_state.chatbot.clear_history(st.session_state.user_id)
                st.success("Chat cleared!")
                st.rerun()

    # Handle text input submission (when user presses Enter)
    if prompt and prompt != st.session_state.get('last_processed_query', ''):
        st.session_state.last_processed_query = prompt
        st.session_state.text_input_value = ""  # Clear for next query
        process_query(prompt)
        st.rerun()

    # Footer
    st.markdown("""
    <div class="footer">
        © 2025 YuvaSaarthi. All rights reserved. | Developed by Subash S, Yashas P, Shanjith SA, Harshith P
    </div>
    """, unsafe_allow_html=True)


def process_query(prompt: str):
    """Process user query"""
    # Add user message
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Generate response
    try:
        result = st.session_state.chatbot.process_query(
            query=prompt,
            user_id=st.session_state.user_id,
            language=st.session_state.language,
            include_resources=st.session_state.include_resources
        )

        # Add assistant message
        assistant_message = {
            "role": "assistant",
            "content": result["response"],
            "videos": result.get("videos", []),
            "articles": result.get("articles", [])
        }
        st.session_state.messages.append(assistant_message)

        # Clear current input
        st.session_state.current_input = ""

    except Exception as e:
        logger.error(f"Error processing query: {e}")
        st.error(f"Sorry, I encountered an error: {str(e)}")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        logger.error(f"App error: {e}")
        st.error(f"Application error: {e}")
