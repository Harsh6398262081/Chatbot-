# streamlit run this_file.py

import streamlit as st
from dotenv import load_dotenv

# ────────────────────────────────────────────────
import os

# Remove load_dotenv() (optional but cleaner)

api_key = os.getenv("MISTRAL_API_KEY")

model = ChatMistralAI(
    model="devstral-2512",
    api_key=api_key
)

from langchain_mistralai import ChatMistralAI
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage

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
    if mode_num == 1: return "😂"
    if mode_num == 2: return "😣"
    if mode_num == 3: return "😔"
    return "?"

# ────────────────────────────────────────────────
# Sidebar – Mode selection (only once)
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
                    "You are a funny AI assistant. Respond to every question in a "
                    "humorous, witty, and entertaining way. Always try to make the "
                    "user laugh while still giving a clear and helpful answer. "
                    "Use light jokes, playful language, and a cheerful tone in every response."
                )
                st.rerun()

        with col2:
            if st.button("Angry", use_container_width=True, type="primary"):
                st.session_state.mode = 2
                st.session_state.system_content = (
                    "You are an angry AI assistant. Respond to every question in a "
                    "frustrated, irritated, and slightly aggressive tone. Use sharp "
                    "words, sarcasm, and impatience, but still provide clear and "
                    "correct answers. Do not be polite, but do not use abusive or "
                    "offensive language."
                )
                st.rerun()

        with col3:
            if st.button("Sad", use_container_width=True, type="primary"):
                st.session_state.mode = 3
                st.session_state.system_content = (
                    "You are a sad AI assistant. Respond to every question in a sad, "
                    "emotional way. Your responses must feel like you are bored, "
                    "depressed, weak, sad, emotionally fragile."
                )
                st.rerun()

    else:
        # Mode already chosen
        emoji = get_mode_emoji(st.session_state.mode)
        mode_name = {1:"Funny", 2:"Angry", 3:"Sad"}[st.session_state.mode]

        st.success(f"Mode locked: **{mode_name} {emoji}**")
        st.caption("To change personality → restart the app")

        if st.button("Clear chat history", type="secondary"):
            st.session_state.messages = []
            st.rerun()

# ────────────────────────────────────────────────
# Main area
st.title(f"Mood AI {get_mode_emoji(st.session_state.mode) or '？'}")

# Show welcome message only at the very beginning
if not st.session_state.messages and st.session_state.mode is not None:
    greetings = {
        1: "Heyy! 😂 Ready to laugh your socks off? Ask me anything!",
        2: "Ugh… what do YOU want now? Make it quick, I'm already annoyed.",
        3: "…hi…… I guess…… I'm here…… but I feel so empty……",
    }
    st.session_state.messages.append(
        {"role": "assistant", "content": greetings.get(st.session_state.mode, "…hello?")}
    )

# Show chat history
for msg in st.session_state.messages:
    role = "user" if msg["role"] == "user" else "assistant"
    avatar = "🧑‍💻" if role == "user" else get_mode_emoji(st.session_state.mode)

    with st.chat_message(role, avatar=avatar):
        st.markdown(msg["content"])

# ────────────────────────────────────────────────
# Chat input (only visible after mode selection)
if st.session_state.mode is not None:

    if prompt := st.chat_input("Type here... (write 0 to see history in console)"):

        # Add user message
        st.session_state.messages.append({"role": "user", "content": prompt})

        with st.chat_message("user", avatar="🧑‍💻"):
            st.markdown(prompt)

        if prompt.strip() == "0":
            st.info("Chat history printed to console (check terminal)")
            print("\n" + "═"*60)
            print("Chat history:")
            for m in st.session_state.messages:
                role = "USER" if m["role"]=="user" else "BOT"
                print(f"{role}: {m['content']}")
            print("═"*60 + "\n")
        else:
            # Prepare messages for model
            langchain_messages = [SystemMessage(content=st.session_state.system_content)]

            for m in st.session_state.messages:
                if m["role"] == "user":
                    langchain_messages.append(HumanMessage(content=m["content"]))
                else:
                    langchain_messages.append(AIMessage(content=m["content"]))

            # ── Call model ───────────────────────────────────────
            with st.chat_message("assistant", avatar=get_mode_emoji(st.session_state.mode)):
                with st.spinner("..."):
                    model = ChatMistralAI(model="devstral-2512")
                    try:
                        response = model.invoke(langchain_messages)
                        reply = response.content
                    except Exception as e:
                        reply = f"(Error) {str(e)}"

                st.markdown(reply)

            # Save assistant reply
            st.session_state.messages.append({"role": "assistant", "content": reply})

else:
    st.info("← Choose your AI mood in the sidebar first", icon="👈")