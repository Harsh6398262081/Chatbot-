🤡 Mood AI Chatbot

A fun and interactive AI chatbot built using Streamlit and LangChain + Mistral AI that responds based on different emotional personalities.

Users can choose a mood once (Funny 😂, Angry 😣, or Sad 😔), and the chatbot will continue the conversation in that tone.

🚀 Features
🎭 Multiple AI Personalities
😂 Funny – witty, humorous, entertaining responses
😣 Angry – sarcastic, irritated but informative
😔 Sad – emotional, slow, melancholic replies
💬 Persistent Chat Session
Chat history maintained during session
🔒 Mode Lock System
Mood can only be selected once per session
🧠 Context-Aware Responses
Uses conversation history for better replies
🧹 Clear Chat Option
Reset conversation anytime
⚡ Real-time AI Responses
Powered by Mistral AI via LangChain
🛠️ Tech Stack
Frontend/UI: Streamlit
LLM Framework: LangChain
Model Provider: Mistral AI
Environment Management: Python Dotenv / Streamlit Secrets
📂 Project Structure
├── UI_chatbot.py      # Main Streamlit application
├── requirements.txt   # Dependencies
├── README.md          # Project documentation
⚙️ Installation (Local Setup)
1. Clone the repository
git clone https://github.com/your-username/mood-ai-chatbot.git
cd mood-ai-chatbot
2. Create virtual environment
python -m venv venv
3. Activate environment

Windows:

venv\Scripts\activate

Mac/Linux:

source venv/bin/activate
4. Install dependencies
pip install -r requirements.txt
5. Add API key

Create a .env file:

MISTRAL_API_KEY=your_api_key_here
▶️ Run the App Locally
streamlit run UI_chatbot.py
🌐 Deployment (Streamlit Cloud)
Push project to GitHub
Go to Streamlit Cloud
Deploy using:
Main file: UI_chatbot.py
Add secrets in Streamlit Cloud:
MISTRAL_API_KEY = "your_api_key_here"
🧠 How It Works
User selects a mood from sidebar
A system prompt is set based on selected personality
Chat history is stored in st.session_state
Messages are converted into LangChain format:
HumanMessage
AIMessage
SystemMessage
Sent to Mistral model for response generation
🎯 Example Personalities

Funny Mode 😂

"Oh wow, you asked THAT? Brace yourself, comedy incoming..."

Angry Mode 😣

"Seriously? You needed AI for this? Fine, here's your answer..."

Sad Mode 😔

"I guess… I can answer… even though nothing really matters…"

⚠️ Notes
Mood cannot be changed once selected (restart app to change)
API key must NOT be exposed publicly
.env file should not be pushed to GitHub
📌 Future Improvements
🌙 Dark/Light theme toggle
🎤 Voice input support
💾 Chat history download
🤖 More personality modes
⚡ Streaming responses
👨‍💻 Author

Harsh Kumar

⭐ If you like this project

Give it a ⭐ on GitHub and share it!
