"""Streamlit Web Interface"""
import streamlit as st
import sys
import os
from datetime import datetime
from indic_transliteration import sanscript
from indic_transliteration.sanscript import transliterate
import io

sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

try:
    from src.chatbot import SimpleAITeacher
except ImportError:
    st.error("Please install requirements: pip install -r requirements.txt")
    st.stop()

st.set_page_config(page_title="🤖📚 AI Teacher", page_icon="🤖", layout="wide")

if 'teacher' not in st.session_state:
    st.session_state.teacher = SimpleAITeacher()
if 'messages' not in st.session_state:
    st.session_state.messages = []

st.title("🤖📚 AI Teacher Chatbot")
st.markdown("**Ask questions in English, Hindi (हिंदी), or Telugu (తెలుగు)!**")

with st.sidebar:
    st.header("📊 Features")
    st.markdown("""
    - 🌐 **3 Languages**: English, Hindi, Telugu
    - 🎓 **Educational AI**: Math, Science, General
    - 🤖 **AI Powered**: Groq API

    """)

    stats = st.session_state.teacher.get_stats()
    if stats['total_messages'] > 0:
        st.header("📈 Session Stats")
        st.metric("Messages", stats['total_messages'])
        st.write(f"**Languages**: {', '.join(stats['languages_used'])}")
        st.write(f"**Subjects**: {', '.join(stats['subjects_discussed'])}")

    if st.button("🗑️ Clear Chat"):
        st.session_state.messages = []
        st.session_state.teacher.clear_history()
        st.rerun()

    # Download chat history button
    if st.session_state.messages:
        chat_text = ""
        for msg in st.session_state.messages:
            timestamp = msg.get('timestamp', '')
            chat_text += f"[{timestamp}] You: {msg['user_input']}\n"
            chat_text += f"[{timestamp}] Teacher ({msg['language_name']} | {msg['category'].title()}): {msg['response']}\n\n"

        bio = io.BytesIO()
        bio.write(chat_text.encode('utf-8'))
        bio.seek(0)

        st.download_button(
            label="📥 Download Chat History",
            data=bio,
            file_name="chat_history.txt",
            mime="text/plain"
        )

chat_container = st.container()

with chat_container:
    for msg in st.session_state.messages:
        timestamp = msg.get('timestamp', '')
        with st.chat_message("user"):
            st.markdown(f"<small style='color:gray'>{timestamp}</small>", unsafe_allow_html=True)
            st.write(msg['user_input'])
        with st.chat_message("assistant"):
            st.markdown(f"<small style='color:gray'>{timestamp}</small>", unsafe_allow_html=True)
            st.write(f"**{msg['language_name']} | {msg['category'].title()}**")
            st.write(msg['response'])

if user_input := st.chat_input("Ask me anything..."):
    with st.spinner("🤔 Thinking..."):
        response = st.session_state.teacher.chat(user_input)
    st.session_state.messages.append(response)
    st.rerun()

if len(st.session_state.messages) == 0:
    st.header("💡 Try These Examples")
    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("What is algebra?"):
            response = st.session_state.teacher.chat("What is algebra?")
            st.session_state.messages.append(response)
            st.rerun()

    with col2:
        if st.button("Supervised Learning vs Unsupervised Learning"):
            response = st.session_state.teacher.chat("పర్యవేక్షించబడిన మరియు వివేకం లేని యంత్ర అభ్యాస అల్గోరిథం మధ్య తేడాను గుర్తించండి?")
            st.session_state.messages.append(response)
            st.rerun()

    with col3:
        if st.button("गणित क्या है?"):
            response = st.session_state.teacher.chat("गणित क्या है?")
            st.session_state.messages.append(response)
            st.rerun()