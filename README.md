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
- **Authentication**: Google OAuth 2.0
- **Database**: SQLite (or your preferred database)

## Prerequisites

Before you begin, ensure you have the following installed:

- Python 3.8 or higher
- pip (Python package installer)
- A Google Cloud Platform account
- Google Cloud CLI (optional but recommended)

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/streamlit-google-chatbot.git
cd streamlit-google-chatbot
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

## Configuration

### Google APIs Setup

#### Dialogflow Integration

```python
# In chatbot/google_api.py
from google.cloud import dialogflow

def detect_intent_texts(project_id, session_id, texts, language_code):
    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(project_id, session_id)
    
    for text in texts:
        text_input = dialogflow.TextInput(text=text, language_code=language_code)
        query_input = dialogflow.QueryInput(text=text_input)
        response = session_client.detect_intent(
            request={"session": session, "query_input": query_input}
        )
        return response
```

#### Vertex AI Integration

```python
# Alternative using Vertex AI
from google.cloud import aiplatform

def generate_response(prompt, model_name="text-bison"):
    aiplatform.init(project=PROJECT_ID, location="us-central1")
    model = aiplatform.gapic.PredictionServiceClient()
    # Implementation details...
```

### Streamlit Configuration

```toml
# .streamlit/config.toml
[server]
port = 8501
headless = true

[theme]
primaryColor = "#FF6B6B"
backgroundColor = "#FFFFFF"
secondaryBackgroundColor = "#F0F2F6"
textColor = "#262730"
```

## Customization

### Adding New Features

1. **Custom Intents**: Add new intents in Dialogflow Console
2. **Styling**: Modify `static/styles.css` for UI changes
3. **Functionality**: Extend `chatbot/conversation.py` for new features

### Environment-Specific Settings

```python
# config/settings.py
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    GOOGLE_PROJECT_ID = os.getenv('GOOGLE_PROJECT_ID')
    MODEL_NAME = os.getenv('MODEL_NAME', 'text-bison')
    MAX_TOKENS = int(os.getenv('MAX_TOKENS', '1024'))
    TEMPERATURE = float(os.getenv('TEMPERATURE', '0.7'))
```

## API Rate Limits and Costs

### Google Cloud Pricing

- **Dialogflow**: Free tier includes 1000 requests/month
- **Vertex AI**: Pay-per-use based on tokens processed
- **Natural Language API**: $1.00 per 1000 units

### Rate Limiting

```python
import time
from functools import wraps

def rate_limit(max_calls_per_second=1):
    def decorator(func):
        last_called = [0.0]
        
        @wraps(func)
        def wrapper(*args, **kwargs):
            elapsed = time.time() - last_called[0]
            left_to_wait = 1.0 / max_calls_per_second - elapsed
            if left_to_wait > 0:
                time.sleep(left_to_wait)
            ret = func(*args, **kwargs)
            last_called[0] = time.time()
            return ret
        return wrapper
    return decorator
```

## Testing

Run the test suite:

```bash
# Install test dependencies
pip install pytest pytest-streamlit

# Run tests
pytest tests/

# Run with coverage
pytest --cov=chatbot tests/
```

## Deployment

### Streamlit Cloud

1. Push your code to GitHub
2. Connect your repository to [Streamlit Cloud](https://streamlit.io/cloud)
3. Add secrets in the Streamlit Cloud dashboard
4. Deploy automatically

### Docker Deployment

```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8501

CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

### Google Cloud Run

```bash
# Build and deploy
gcloud builds submit --tag gcr.io/PROJECT_ID/chatbot
gcloud run deploy --image gcr.io/PROJECT_ID/chatbot --platform managed
```

## Troubleshooting

### Common Issues

1. **Authentication Errors**
   ```bash
   export GOOGLE_APPLICATION_CREDENTIALS="path/to/your/credentials.json"
   ```

2. **API Quota Exceeded**
   - Check your Google Cloud quotas
   - Implement proper rate limiting
   - Consider upgrading your plan

3. **Streamlit Performance**
   - Use `@st.cache_data` for expensive operations
   - Implement session state properly
   - Optimize API calls

### Debug Mode

```python
# Add to app.py for debugging
import logging
logging.basicConfig(level=logging.DEBUG)

if st.checkbox("Debug Mode"):
    st.write("Session State:", st.session_state)
```

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Setup

```bash
# Install development dependencies
pip install -r requirements-dev.txt

# Pre-commit hooks
pre-commit install

# Code formatting
black .
isort .
flake8 .
```

## Security Considerations

- Never commit API keys to version control
- Use environment variables for sensitive data
- Implement proper input validation
- Regular security audits of dependencies
- Use HTTPS in production

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

- 📧 **Email**: support@yourproject.com
- 🐛 **Issues**: [GitHub Issues](https://github.com/yourusername/streamlit-google-chatbot/issues)
- 📖 **Documentation**: [Project Wiki](https://github.com/yourusername/streamlit-google-chatbot/wiki)
- 💬 **Discussion**: [GitHub Discussions](https://github.com/yourusername/streamlit-google-chatbot/discussions)

## Acknowledgments

- [Streamlit](https://streamlit.io/) for the amazing web framework
- [Google Cloud](https://cloud.google.com/) for powerful AI APIs
- The open-source community for inspiration and contributions

---

**Made with ❤️ using Streamlit and Google Cloud APIs**
