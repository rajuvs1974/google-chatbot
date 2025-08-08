# Chatbot with Streamlit and Google APIs

A modern, interactive chatbot application built with Streamlit and powered by Google APIs for natural language processing and conversation capabilities.

## Features

- 🤖 **Intelligent Conversations**: Powered by Google's advanced AI models
- 🎨 **Modern UI**: Clean and responsive interface built with Streamlit
- 💬 **Real-time Chat**: Instant responses with typing indicators
- 🌐 **Multi-language Support**: Communicate in various languages
- 📱 **Mobile Friendly**: Responsive design that works on all devices
- 🔒 **Secure**: API key management and secure authentication
- 💾 **Chat History**: Persistent conversation storage
- ⚙️ **Customizable**: Configurable bot personality and responses

## Tech Stack

- **Frontend**: Streamlit
- **Backend**: Python 3.8+
- **AI/ML**: Google Cloud APIs (Dialogflow, Vertex AI, or PaLM API)

## Prerequisites

Before you begin, ensure you have the following installed:

- Python 3.8 or higher
- pip (Python package installer)
- A Google Cloud Platform account
- Google Cloud CLI (optional but recommended)

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/rajuvs1974/google-chatbot
cd google-chatbot
```

### 2. Create Virtual Environment

```bash
python -m venv chatbot_env
source chatbot_env/bin/activate  # On Windows: chatbot_env\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Set Up Google Cloud APIs

1. Go to the [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select an existing one
3. Enable the required APIs:
   - Dialogflow API
   - Cloud Natural Language API
   - Vertex AI API (if using)
4. Create service account credentials:
   - Go to IAM & Admin → Service Accounts
   - Create a new service account
   - Download the JSON key file
   - Rename it to `google-credentials.json`

### 5. Configure Environment Variables

Create a `.env` file in the project root:

```env
GOOGLE_APPLICATION_CREDENTIALS=google-credentials.json
GOOGLE_PROJECT_ID=your-project-id
DIALOGFLOW_SESSION_ID=default-session
STREAMLIT_SERVER_PORT=8501
```

## Project Structure

```
streamlit-google-chatbot/
├── app.py                 # Main Streamlit application
├── chatbot/
│   ├── __init__.py
│   ├── google_api.py      # Google APIs integration
│   ├── conversation.py    # Chat logic and state management
│   └── utils.py           # Helper functions
├── config/
│   ├── settings.py        # Configuration settings
│   └── prompts.py         # System prompts and templates
├── data/
│   └── chat_history.db    # SQLite database (auto-generated)
├── static/
│   ├── styles.css         # Custom CSS styles
│   └── images/            # Images and icons
├── tests/
│   ├── test_chatbot.py
│   └── test_api.py
├── requirements.txt       # Python dependencies
├── .env.example          # Environment variables template
├── .gitignore
└── README.md
```

## Usage

### 1. Start the Application

```bash
streamlit run app.py
```

The application will open in your default browser at `http://localhost:8501`

### 2. Chat with the Bot

- Type your message in the input field
- Press Enter or click Send
- View responses in the chat interface
- Access chat history from the sidebar

### 3. Configuration Options

Use the sidebar to:
- Adjust bot personality
- Change response length
- Select different AI models
- Clear chat history
- Export conversations


**Made with ❤️ using Streamlit and Google Cloud APIs**
