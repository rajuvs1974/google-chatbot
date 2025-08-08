import streamlit as st
import google.generativeai as genai
from datetime import datetime
import os

# Configure the page
st.set_page_config(
    page_title="AI Chatbot",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        text-align: center;
        color: #1f77b4;
        margin-bottom: 2rem;
    }
    .chat-message {
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
        border-left: 4px solid;
    }
    .user-message {
        background-color: #e3f2fd;
        border-left-color: #2196f3;
    }
    .assistant-message {
        background-color: #f3e5f5;
        border-left-color: #9c27b0;
    }
    .sidebar-info {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

def initialize_session_state():
    """Initialize session state variables"""
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "api_key_configured" not in st.session_state:
        st.session_state.api_key_configured = False
    if "model" not in st.session_state:
        st.session_state.model = None

def configure_gemini_api(api_key):
    """Configure the Gemini API with the provided key"""
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-2.0-flash')
        return model, True
    except Exception as e:
        st.error(f"Error configuring API: {str(e)}")
        return None, False

def get_gemini_response(model, prompt, chat_history=None):
    """Get response from Gemini API"""
    try:
        # Create a chat session for better context handling
        chat = model.start_chat(history=[])
        
        # Add previous messages to context if available
        if chat_history:
            context = "\n".join([f"User: {msg['user']}\nAssistant: {msg['assistant']}" 
                               for msg in chat_history[-5:]])  # Last 5 exchanges
            full_prompt = f"Previous conversation:\n{context}\n\nCurrent question: {prompt}"
        else:
            full_prompt = prompt
            
        response = chat.send_message(full_prompt)
        return response.text
    except Exception as e:
        return f"Error generating response: {str(e)}"

def display_chat_message(role, content, timestamp=None):
    """Display a chat message with proper styling"""
    if timestamp:
        time_str = timestamp.strftime("%H:%M:%S")
    else:
        time_str = datetime.now().strftime("%H:%M:%S")
    
    if role == "user":
        st.markdown(f"""
        <div class="chat-message user-message">
            <strong>You ({time_str}):</strong><br>
            {content}
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="chat-message assistant-message">
            <strong>AI Assistant ({time_str}):</strong><br>
            {content}
        </div>
        """, unsafe_allow_html=True)

def main():
    # Initialize session state
    initialize_session_state()
    
    # Main header
    st.markdown('<h1 class="main-header">🤖 AI Chatbot with Google Gemini</h1>', 
                unsafe_allow_html=True)
    
    # Sidebar for configuration
    with st.sidebar:
        st.header("⚙️ Configuration")
        
        # API Key input
        api_key = st.text_input(
            "Google Gemini API Key",
            type="password",
            help="Enter your Google Gemini API key. Get it from: https://makersuite.google.com/app/apikey"
        )
        
        if api_key:
            if not st.session_state.api_key_configured or st.session_state.model is None:
                model, success = configure_gemini_api(api_key)
                if success:
                    st.session_state.model = model
                    st.session_state.api_key_configured = True
                    st.success("✅ API configured successfully!")
                else:
                    st.session_state.api_key_configured = False
        
        st.markdown("---")
        
        # Chat settings
        st.subheader("💬 Chat Settings")
        
        # Temperature setting
        temperature = st.slider(
            "Response Creativity",
            min_value=0.0,
            max_value=1.0,
            value=0.7,
            step=0.1,
            help="Higher values make responses more creative but less predictable"
        )
        
        # Max tokens
        max_tokens = st.slider(
            "Max Response Length",
            min_value=100,
            max_value=2000,
            value=500,
            step=100,
            help="Maximum length of AI responses"
        )
        
        st.markdown("---")
        
        # Chat history controls
        st.subheader("📝 Chat History")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Clear Chat", type="secondary"):
                st.session_state.messages = []
                st.rerun()
        
        with col2:
            if st.button("Export Chat"):
                if st.session_state.messages:
                    chat_export = []
                    for msg in st.session_state.messages:
                        chat_export.append(f"User: {msg['user']}")
                        chat_export.append(f"Assistant: {msg['assistant']}")
                        chat_export.append("---")
                    
                    st.download_button(
                        label="Download Chat History",
                        data="\n".join(chat_export),
                        file_name=f"chat_history_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                        mime="text/plain"
                    )
        
        # Info section
        st.markdown("---")
        st.markdown("""
        <div class="sidebar-info">
            <h4>ℹ️ About</h4>
            <p>This chatbot uses Google's Gemini 2.0 Flash model to provide intelligent responses to your questions.</p>
            <p><strong>Features:</strong></p>
            <ul>
                <li>Context-aware conversations</li>
                <li>Customizable response settings</li>
                <li>Chat history management</li>
                <li>Export functionality</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    # Main chat interface
    if not st.session_state.api_key_configured:
        st.warning("⚠️ Please enter your Google Gemini API key in the sidebar to start chatting.")
        st.info("You can get your free API key from: https://makersuite.google.com/app/apikey")
        
        # Example conversation
        st.markdown("### 💡 Example Conversation")
        display_chat_message("user", "What is artificial intelligence?")
        display_chat_message("assistant", "Artificial Intelligence (AI) is a branch of computer science that focuses on creating systems capable of performing tasks that typically require human intelligence. This includes learning, reasoning, problem-solving, perception, and language understanding. AI systems can analyze data, recognize patterns, and make decisions to solve complex problems across various domains like healthcare, finance, transportation, and more.")
        
    else:
        # Chat container
        chat_container = st.container()
        
        # Display chat history
        with chat_container:
            if st.session_state.messages:
                for message in st.session_state.messages:
                    display_chat_message("user", message["user"], message.get("timestamp"))
                    display_chat_message("assistant", message["assistant"], message.get("timestamp"))
            else:
                st.info("👋 Hi! I'm your AI assistant. Ask me anything to get started!")
        
        # Chat input
        with st.form(key="chat_form", clear_on_submit=True):
            col1, col2 = st.columns([4, 1])
            
            with col1:
                user_input = st.text_area(
                    "Your message:",
                    placeholder="Type your message here...",
                    height=100,
                    key="user_input"
                )
            
            with col2:
                submit_button = st.form_submit_button("Send 📤", type="primary", use_container_width=True)
                
                # Quick action buttons
                st.markdown("**Quick Actions:**")
                if st.form_submit_button("💡 Explain AI", use_container_width=True):
                    user_input = "What is artificial intelligence and how does it work?"
                    submit_button = True
                
                if st.form_submit_button("📚 Help with coding", use_container_width=True):
                    user_input = "Can you help me with a coding problem?"
                    submit_button = True
                
                if st.form_submit_button("🎨 Creative writing", use_container_width=True):
                    user_input = "Help me write a creative story or poem"
                    submit_button = True
        
        # Process user input
        if submit_button and user_input.strip():
            # Add user message to history
            timestamp = datetime.now()
            
            # Show user message immediately
            display_chat_message("user", user_input, timestamp)
            
            # Show loading spinner
            with st.spinner("🤔 Thinking..."):
                # Get AI response
                chat_history = [{"user": msg["user"], "assistant": msg["assistant"]} 
                              for msg in st.session_state.messages]
                
                ai_response = get_gemini_response(
                    st.session_state.model, 
                    user_input, 
                    chat_history
                )
            
            # Display AI response
            display_chat_message("assistant", ai_response, timestamp)
            
            # Save to session state
            st.session_state.messages.append({
                "user": user_input,
                "assistant": ai_response,
                "timestamp": timestamp
            })
            
            # Rerun to update the interface
            st.rerun()

if __name__ == "__main__":
    main()