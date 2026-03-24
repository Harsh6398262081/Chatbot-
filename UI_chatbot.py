import streamlit as st
from langchain_mistralai import ChatMistralAI
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage

# ✅ Get API key from Streamlit Secrets
api_key = st.secrets["MISTRAL_API_KEY"]

# ────────────────────────────────────────────────
# Page config
st.set_page_config(
    page_title="Mood AI • Funny / Angry / Sad",
    page_icon="🤡",
    layout="centered",
    initial_sidebar_state="expanded",
)

# ────────────────────────────────────────────────
# Session state initialization
if "messages" not in st.session_state:
    st.session_state.messages = []

if "mode" not in st.session_state:
    st.session_state.mode = None

if "system_content" not in st.session_state:
    st.session_state.system_content = None

# ────────────────────────────────────────────────
def get_mode_emoji(mode_num):
    if mode_num == 1:
        return "😂"
    if mode_num == 2:
        return "😣"
    if mode_num == 3:
        return "😔"
    return "?"

# ────────────────────────────────────────────────
# Sidebar – Mode selection
with st.sidebar:

    st.title("Mood AI Chat")
    st.markdown("Choose personality once — then talk forever 💬")

    if st.session_state.mode is None:

        st.info("Pick your AI mood (cannot be changed later)")

        col1, col2, col3 = st.columns(3)

        with col1:
            if st.button("Funny", use_container_width=True, type="primary"):
                st.session_state.mode = 1
                st.session_state.system_content = (
                    "You are a funny AI assistant. Respond in a humorous, witty, and entertaining way. "
                    "Always try to make the user laugh while still being helpful."
                )
                st.rerun()

        with col2:
            if st.button("Angry", use_container_width=True, type="primary"):
                st.session_state.mode = 2
                st.session_state.system_content = (
                    "You are an angry AI assistant. Respond in a frustrated, sarcastic tone, "
                    "but still provide correct answers."
                )
                st.rerun()

        with col3:
            if st.button("Sad", use_container_width=True, type="primary"):
                st.session_state.mode = 3
                st.session_state.system_content = (
                    "You are a sad AI assistant. Respond in a slow, emotional, melancholic tone."
                )
                st.rerun()

    else:
        emoji = get_mode_emoji(st.session_state.mode)
        mode_name = {1: "Funny", 2: "Angry", 3: "Sad"}[st.session_state.mode]

        st.success(f"Mode locked: **{mode_name} {emoji}**")
        st.caption("To change personality → restart the app")

        if st.button("Clear chat history"):
            st.session_state.messages = []
            st.rerun()

# ────────────────────────────────────────────────
# Main UI
st.title(f"Mood AI {get_mode_emoji(st.session_state.mode) or '？'}")

# Welcome message
if not st.session_state.messages and st.session_state.mode is not None:
    greetings = {
        1: "Heyy! 😂 Ready to laugh? Ask me anything!",
        2: "Ugh… what now? Make it quick.",
        3: "…hi… I’ll try to respond…",
    }
    st.session_state.messages.append(
        {"role": "assistant", "content": greetings.get(st.session_state.mode)}
    )

# Show chat history
for msg in st.session_state.messages:
    role = "user" if msg["role"] == "user" else "assistant"
    avatar = "🧑‍💻" if role == "user" else get_mode_emoji(st.session_state.mode)

    with st.chat_message(role, avatar=avatar):
        st.markdown(msg["content"])

# ────────────────────────────────────────────────
# Chat input
if st.session_state.mode is not None:

    if prompt := st.chat_input("Type here..."):

        # Save user message
        st.session_state.messages.append({"role": "user", "content": prompt})

        with st.chat_message("user", avatar="🧑‍💻"):
            st.markdown(prompt)

        # Prepare messages
        langchain_messages = [SystemMessage(content=st.session_state.system_content)]

        for m in st.session_state.messages:
            if m["role"] == "user":
                langchain_messages.append(HumanMessage(content=m["content"]))
            else:
                langchain_messages.append(AIMessage(content=m["content"]))

        # Generate response
        with st.chat_message("assistant", avatar=get_mode_emoji(st.session_state.mode)):
            with st.spinner("Thinking..."):
                try:
                    model = ChatMistralAI(
                        model="devstral-2512",
                        api_key=api_key
                    )
                    response = model.invoke(langchain_messages)
                    reply = response.content
                except Exception as e:
                    reply = f"Error: {str(e)}"

            st.markdown(reply)

        # Save assistant reply
        st.session_state.messages.append({"role": "assistant", "content": reply})

else:
    st.info("← Choose your AI mood in the sidebar first", icon="👈")
