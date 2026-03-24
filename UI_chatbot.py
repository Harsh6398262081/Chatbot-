# ────────────────────────────────────────────────
import streamlit as st
import requests

# ✅ Get API key from Streamlit Secrets
api_key = st.secrets["MISTRAL_API_KEY"]

# ────────────────────────────────────────────────
# Function to call Mistral API
def get_response(messages):
    url = "https://api.mistral.ai/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "mistral-small",
        "messages": messages
    }

    response = requests.post(url, headers=headers, json=data)

    if response.status_code != 200:
        return f"Error: {response.text}"

    return response.json()["choices"][0]["message"]["content"]

# ────────────────────────────────────────────────
# Page config
st.set_page_config(
    page_title="Mood AI • Funny / Angry / Sad",
    page_icon="🤡",
    layout="centered",
)

# ────────────────────────────────────────────────
# Session state
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
# Sidebar
with st.sidebar:

    st.title("Mood AI Chat")
    st.markdown("Choose personality once — then talk forever 💬")

    if st.session_state.mode is None:

        st.info("Pick your AI mood")

        col1, col2, col3 = st.columns(3)

        with col1:
            if st.button("Funny"):
                st.session_state.mode = 1
                st.session_state.system_content = (
                    "You are a funny AI assistant. Respond in a humorous and witty way."
                )
                st.rerun()

        with col2:
            if st.button("Angry"):
                st.session_state.mode = 2
                st.session_state.system_content = (
                    "You are an angry AI assistant. Respond in a sarcastic and irritated tone."
                )
                st.rerun()

        with col3:
            if st.button("Sad"):
                st.session_state.mode = 3
                st.session_state.system_content = (
                    "You are a sad AI assistant. Respond in a slow, emotional tone."
                )
                st.rerun()

    else:
        emoji = get_mode_emoji(st.session_state.mode)
        mode_name = {1: "Funny", 2: "Angry", 3: "Sad"}[st.session_state.mode]

        st.success(f"Mode locked: {mode_name} {emoji}")

        if st.button("Clear chat"):
            st.session_state.messages = []
            st.rerun()

# ────────────────────────────────────────────────
# Main UI
st.title(f"Mood AI {get_mode_emoji(st.session_state.mode) or ''}")

# Welcome message
if not st.session_state.messages and st.session_state.mode is not None:
    greetings = {
        1: "Hey 😂 Ask me anything!",
        2: "What now...?",
        3: "...hello..."
    }
    st.session_state.messages.append(
        {"role": "assistant", "content": greetings.get(st.session_state.mode)}
    )

# Show chat history
for msg in st.session_state.messages:
    role = msg["role"]
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

        # Prepare messages for API
        api_messages = [
            {"role": "system", "content": st.session_state.system_content}
        ]

        for m in st.session_state.messages:
            api_messages.append({
                "role": m["role"],
                "content": m["content"]
            })

        # Get response
        with st.chat_message("assistant", avatar=get_mode_emoji(st.session_state.mode)):
            with st.spinner("Thinking..."):
                reply = get_response(api_messages)

            st.markdown(reply)

        # Save reply
        st.session_state.messages.append({"role": "assistant", "content": reply})

else:
    st.info("← Choose your AI mood first", icon="👈")
