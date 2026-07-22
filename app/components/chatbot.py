import html

import streamlit as st

try:
    from knowledge.cinemind_knowledge import WELCOME_MESSAGE
    from services.chatbot_engine import get_chatbot_response
except ModuleNotFoundError:
    from app.knowledge.cinemind_knowledge import WELCOME_MESSAGE
    from app.services.chatbot_engine import get_chatbot_response


def _initialize_chat_state():
    if "cinemind_chat_messages" not in st.session_state:
        st.session_state.cinemind_chat_messages = [
            {"role": "assistant", "content": WELCOME_MESSAGE, "topic": "application"}
        ]


def _render_message(role: str, content: str):
    alignment = "flex-end" if role == "user" else "flex-start"
    bubble_bg = "rgba(212, 175, 55, 0.95)" if role == "user" else "#151515"
    text_color = "#120A03" if role == "user" else "#FFFFFF"
    border = "1px solid rgba(212, 175, 55, 0.25)" if role == "assistant" else "1px solid rgba(212, 175, 55, 0.95)"
    escaped = html.escape(content).replace("\n", "<br>")

    st.markdown(
        f"""
        <div style="display:flex;justify-content:{alignment};margin:0.55rem 0;">
            <div style="max-width:78%;background:{bubble_bg};color:{text_color};border:{border};border-radius:18px;padding:0.85rem 1rem;line-height:1.6;box-shadow:0 10px 24px rgba(0,0,0,0.22);">
                {escaped}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_cinemind_assistant():
    _initialize_chat_state()

    st.markdown(
        """
        <style>
        .cinemind-chat-card {
            max-width: 1200px;
            margin: 0 auto 1.6rem;
            padding: 1.35rem;
            background: #1A1A1A;
            border: 1px solid rgba(212, 175, 55, 0.18);
            border-radius: 24px;
            box-shadow: 0 18px 42px rgba(0, 0, 0, 0.28);
        }
        .cinemind-chat-title {
            margin: 0;
            color: #FFFFFF;
            font-size: 1.35rem;
            font-weight: 800;
        }
        .cinemind-chat-subtitle {
            margin: 0.35rem 0 1rem;
            color: #CFC9B7;
            line-height: 1.55;
        }
        .cinemind-chat-window {
            max-height: 430px;
            overflow-y: auto;
            padding: 0.9rem;
            background: #0E0E0E;
            border: 1px solid rgba(212, 175, 55, 0.14);
            border-radius: 18px;
        }
        </style>
        <div class="cinemind-chat-card">
            <h2 class="cinemind-chat-title">🤖 CineMind AI Assistant</h2>
            <p class="cinemind-chat-subtitle">Ask focused questions about movie prediction, explainable AI, datasets, model evaluation, and this application.</p>
            <div class="cinemind-chat-window">
        """,
        unsafe_allow_html=True,
    )

    for message in st.session_state.cinemind_chat_messages:
        _render_message(message["role"], message["content"])

    st.markdown("</div>", unsafe_allow_html=True)

    with st.form("cinemind_assistant_form", clear_on_submit=True):
        input_col, button_col = st.columns([5, 1])
        with input_col:
            question = st.text_input(
                "Ask the CineMind AI Assistant",
                placeholder="Example: What is Random Forest?",
                label_visibility="collapsed",
            )
        with button_col:
            send = st.form_submit_button("Send", use_container_width=True)

    if send and question.strip():
        st.session_state.cinemind_chat_messages.append(
            {"role": "user", "content": question.strip(), "topic": None}
        )
        result = get_chatbot_response(
            question,
            messages=st.session_state.cinemind_chat_messages,
            latest_prediction=st.session_state.get("latest_prediction"),
        )
        st.session_state.cinemind_chat_messages.append(
            {"role": "assistant", "content": result["answer"], "topic": result["topic"]}
        )
        st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)
