"""
YuvaSaarthi - Streamlit Web Interface
"""

import streamlit as st
from datetime import datetime
from loguru import logger
import uuid

from backend.chatbot_engine import get_chatbot
from utils.config import settings, SUPPORTED_LANGUAGES


# Page configuration
st.set_page_config(
    page_title="YuvaSaarthi - National Education Assistant",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 1rem;
    }
    .sub-header {
        text-align: center;
        color: #666;
        margin-bottom: 2rem;
    }
    .chat-message {
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
    }
    .user-message {
        background-color: #e3f2fd;
        border-left: 4px solid #1f77b4;
    }
    .assistant-message {
        background-color: #f5f5f5;
        border-left: 4px solid #4caf50;
    }
    .video-card {
        border: 1px solid #ddd;
        border-radius: 0.5rem;
        padding: 1rem;
        margin-bottom: 0.5rem;
    }
    .stat-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1rem;
        border-radius: 0.5rem;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)


# Initialize session state
if 'chatbot' not in st.session_state:
    st.session_state.chatbot = get_chatbot()

if 'messages' not in st.session_state:
    st.session_state.messages = []

if 'user_id' not in st.session_state:
    st.session_state.user_id = str(uuid.uuid4())

if 'language' not in st.session_state:
    st.session_state.language = settings.default_language

if 'include_videos' not in st.session_state:
    st.session_state.include_videos = True


def display_message(role: str, content: str):
    """Display a chat message"""
    css_class = "user-message" if role == "user" else "assistant-message"
    icon = "👤" if role == "user" else "🤖"

    st.markdown(f"""
    <div class="chat-message {css_class}">
        <strong>{icon} {role.title()}:</strong><br>
        {content}
    </div>
    """, unsafe_allow_html=True)


def display_video(video: dict):
    """Display a YouTube video card"""
    st.markdown(f"""
    <div class="video-card">
        <strong>📺 {video['title']}</strong><br>
        <small>Channel: {video['channel']}</small><br>
        <a href="{video['url']}" target="_blank">Watch Video</a>
    </div>
    """, unsafe_allow_html=True)


def main():
    """Main Streamlit app"""

    # Header
    st.markdown('<h1 class="main-header">🎓 YuvaSaarthi - National Education Assistant</h1>', unsafe_allow_html=True)
    st.markdown(
        '<p class="sub-header">AI-Powered Educational Assistant for Students of India 🇮🇳</p>',
        unsafe_allow_html=True
    )

    # Sidebar
    with st.sidebar:
        st.header("⚙️ Settings")

        # Language selection with all Indian languages
        from utils.indian_languages import (
            SUPPORTED_INDIAN_LANGUAGES,
            get_language_display_name,
            get_popular_languages
        )
        
        popular_langs = get_popular_languages()
        all_langs = list(SUPPORTED_INDIAN_LANGUAGES.keys())
        
        st.write("**Popular Languages:**")
        popular_options = {lang: get_language_display_name(lang) for lang in popular_langs}
        
        selected_lang = st.selectbox(
            "भाषा चुनें / Select Language",
            options=popular_langs,
            format_func=lambda x: popular_options[x],
            index=popular_langs.index(st.session_state.language) if st.session_state.language in popular_langs else 0
        )

        # Show all languages in expander
        with st.expander("🌏 All 22 Indian Languages"):
            st.write("**Complete List:**")
            for lang_code in sorted(all_langs, key=lambda x: SUPPORTED_INDIAN_LANGUAGES[x]['name']):
                if st.button(
                    get_language_display_name(lang_code),
                    key=f"lang_{lang_code}",
                    use_container_width=True
                ):
                    selected_lang = lang_code
                    st.rerun()

        if selected_lang != st.session_state.language:
            st.session_state.language = selected_lang
            st.success(f"Language changed to {SUPPORTED_INDIAN_LANGUAGES[selected_lang]['name']}")
            st.rerun()

        # Video recommendations toggle
        st.session_state.include_videos = st.checkbox(
            "📺 Include YouTube Videos",
            value=st.session_state.include_videos
        )

        st.divider()

        # System health
        st.header("🏥 System Health")
        if st.button("Check Status"):
            with st.spinner("Checking..."):
                health = st.session_state.chatbot.get_system_health()

                st.write("**Components:**")
                st.write(f"🤖 LLM: {health['llm']['status']}")
                st.write(f"📺 YouTube: {health['youtube']['status']}")
                st.write(f"🌐 Translation: {health['translation']['status']}")
                st.write(f"📚 Knowledge Base: {health['vector_store']['status']}")

        st.divider()

        # Clear chat
        if st.button("🗑️ Clear Chat"):
            st.session_state.messages = []
            st.session_state.chatbot.clear_history(st.session_state.user_id)
            st.success("Chat cleared!")
            st.rerun()

        st.divider()

        # Quick actions with language-specific queries
        st.header("⚡ Quick Actions")
        
        from utils.indian_languages import get_sample_queries
        sample_queries = get_sample_queries(st.session_state.language)

        st.write("**Sample Questions:**")
        for idx, query in enumerate(sample_queries[:3]):
            if st.button(query, key=f"sample_{idx}_{st.session_state.language}"):
                st.session_state.messages.append({"role": "user", "content": query})
                st.rerun()

        st.divider()

        # About
        st.header("ℹ️ About")
        st.write(f"**{settings.bot_name}**")
        st.write(f"{settings.organization}")
        st.write(f"Version: 1.0.0")

    # Main chat area
    chat_container = st.container()

    # Display chat history
    with chat_container:
        for message in st.session_state.messages:
            if message["role"] in ["user", "assistant"]:
                display_message(message["role"], message["content"])

            # Display videos if present
            if message["role"] == "assistant" and "videos" in message:
                if message["videos"]:
                    st.markdown("---")
                    st.markdown("### 📺 Recommended Videos")
                    cols = st.columns(len(message["videos"]))
                    for idx, video in enumerate(message["videos"]):
                        with cols[idx]:
                            display_video(video)

    # Chat input
    if prompt := st.chat_input("Ask me anything... / मुझसे कुछ भी पूछें..."):
        # Add user message
        st.session_state.messages.append({"role": "user", "content": prompt})

        # Display user message
        with chat_container:
            display_message("user", prompt)

        # Generate response
        with st.spinner("Thinking... / सोच रहा हूँ..."):
            try:
                result = st.session_state.chatbot.process_query(
                    query=prompt,
                    user_id=st.session_state.user_id,
                    language=st.session_state.language,
                    include_videos=st.session_state.include_videos
                )

                # Add assistant message
                assistant_message = {
                    "role": "assistant",
                    "content": result["response"],
                    "videos": result.get("videos", [])
                }
                st.session_state.messages.append(assistant_message)

                # Rerun to display new messages
                st.rerun()

            except Exception as e:
                logger.error(f"Error processing query: {e}")
                st.error(f"Sorry, I encountered an error: {str(e)}")

    # Footer
    st.divider()
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("**📚 Available Topics**")
        st.markdown("• Admissions")
        st.markdown("• Course Information")
        st.markdown("• Exam Schedules")

    with col2:
        st.markdown("**🎯 Features**")
        st.markdown("• Multilingual Support")
        st.markdown("• Video Recommendations")
        st.markdown("• Concept Explanations")

    with col3:
        st.markdown("**💡 Tips**")
        st.markdown("• Ask specific questions")
        st.markdown("• Mention your class/grade")
        st.markdown("• Use your preferred language")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        logger.error(f"App error: {e}")
        st.error(f"Application error: {e}")
