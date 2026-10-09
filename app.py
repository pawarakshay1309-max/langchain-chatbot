import streamlit as st
from chatbot import Chatbot


# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="Akshay AI Assistant",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)


# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown("""
<style>
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 1200px;
    }

    div[data-testid="metric-container"] {
        background-color: white;
        border: 1px solid #e5e7eb;
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
    }

    div[data-testid="stChatInput"] {
        margin-bottom: 20px;
    }

    section[data-testid="stSidebar"] {
        border-right: 1px solid #e5e7eb;
    }
</style>
""", unsafe_allow_html=True)


# =========================================================
# INITIALIZE CHATBOT
# =========================================================

if "chatbot" not in st.session_state:
    try:
        st.session_state.chatbot = Chatbot()
    except ValueError as e:
        st.error(str(e))
        st.info(
            "Check that your .env file contains "
            "GROQ_API_KEY=your_actual_api_key"
        )
        st.stop()


chatbot = st.session_state.chatbot


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:
    st.title("🤖 Akshay AI")
    st.caption("Your Personal AI Assistant")
    st.divider()

    st.subheader("Navigation")

    page = st.radio(
        "Select Page",
        ["💬 Chat", "📊 Dashboard", "ℹ️ About"],
        label_visibility="collapsed",
    )

    st.divider()
    st.subheader("⚙️ Chat Settings")

    if st.button("🗑️ Clear Conversation", use_container_width=True):
        chatbot.clear_memory()
        st.rerun()

    st.divider()
    st.subheader("✨ Features")

    st.write("⚡ Groq Cloud LLM")
    st.write("🔗 Python SDK")
    st.write("💭 Conversation Memory")
    st.write("🔄 Multi-turn Chat")
    st.write("⚙️ System Prompt")


# =========================================================
# CONVERSATION STATISTICS
# =========================================================

history = chatbot.get_history()

total_messages = len(history)

user_messages = sum(
    1 for message in history
    if message.type == "human"
)

ai_messages = sum(
    1 for message in history
    if message.type == "ai"
)


# =========================================================
# CHAT PAGE
# =========================================================

if page == "💬 Chat":

    st.title("🤖 Akshay AI Assistant")

    st.write(
        "Your intelligent AI assistant powered by "
        "Groq Cloud and Python."
    )

    st.divider()

    col1, col2, col3 = st.columns(3)

    with col1:
        st.info("⚡ **Groq LLM**\n\nAI-powered responses")

    with col2:
        st.success("🔗 **Groq API**\n\nCloud AI inference")

    with col3:
        st.warning("💭 **Memory**\n\nMulti-turn conversation")

    st.divider()

    if not history:
        st.markdown("## 👋 Welcome to Akshay AI!")
        st.write(
            "Start a conversation by typing your question below."
        )
        st.write("### 💡 Try asking:")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.caption("🐍 Explain Python")

        with col2:
            st.caption("🤖 What is AI?")

        with col3:
            st.caption("📚 Explain Machine Learning")

    # Display previous messages
    for message in history:
        if message.type == "human":
            with st.chat_message("user", avatar="👤"):
                st.write(message.content)

        elif message.type == "ai":
            with st.chat_message("assistant", avatar="🤖"):
                st.write(message.content)

    # Chat input
    user_input = st.chat_input("💬 Type your message here...")

    if user_input:
        with st.chat_message("user", avatar="👤"):
            st.write(user_input)

        with st.chat_message("assistant", avatar="🤖"):
            with st.spinner("🤔 Akshay AI is thinking..."):
                try:
                    response = chatbot.chat(user_input)
                    st.write(response)

                except Exception as e:
                    st.error(f"Groq API error: {e}")


# =========================================================
# DASHBOARD PAGE
# =========================================================

elif page == "📊 Dashboard":

    st.title("📊 AI Dashboard")
    st.write("Overview of your current chatbot session.")
    st.divider()

    st.subheader("📈 Conversation Statistics")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("💬 Total Messages", total_messages)

    with col2:
        st.metric("👤 Your Questions", user_messages)

    with col3:
        st.metric("🤖 AI Responses", ai_messages)

    st.divider()
    st.subheader("🚀 AI Capabilities")

    col1, col2 = st.columns(2)

    with col1:
        with st.container(border=True):
            st.subheader("⚡ Groq LLM")
            st.write(
                "Generates responses using the Groq Cloud API."
            )
            st.success("Configured")

    with col2:
        with st.container(border=True):
            st.subheader("💭 Conversation Memory")
            st.write(
                "Keeps previous messages during the current session."
            )
            st.success("Active")

    col1, col2 = st.columns(2)

    with col1:
        with st.container(border=True):
            st.subheader("🔄 Multi-turn Chat")
            st.write(
                "Uses conversation history to support follow-up questions."
            )
            st.success("Active")

    with col2:
        with st.container(border=True):
            st.subheader("⚙️ System Prompt")
            st.write(
                "Sets the assistant's behavior and response style."
            )
            st.success("Active")

    st.divider()
    st.subheader("🕒 Recent Conversation")

    if history:
        for message in history[-6:]:
            if message.type == "human":
                st.write(f"👤 **You:** {message.content}")
            else:
                st.write(f"🤖 **Akshay AI:** {message.content}")
    else:
        st.info(
            "No conversation yet. Go to Chat and start talking."
        )


# =========================================================
# ABOUT PAGE
# =========================================================

elif page == "ℹ️ About":

    st.title("ℹ️ About Akshay AI")

    st.write(
        "Akshay AI is a conversational AI application "
        "built using Python, Streamlit and Groq Cloud."
    )

    st.divider()
    st.subheader("🛠️ Technology Stack")

    col1, col2 = st.columns(2)

    with col1:
        st.write("🐍 Python")
        st.write("🎈 Streamlit")
        st.write("⚡ Groq API")

    with col2:
        st.write("🧠 Llama model")
        st.write("💭 Conversation Memory")
        st.write("⚙️ System Prompt")

    st.divider()
    st.subheader("✨ Features")

    st.write("✅ Interactive Chat Interface")
    st.write("✅ Multi-turn Conversation")
    st.write("✅ Conversation Memory")
    st.write("✅ Groq Cloud Integration")
    st.write("✅ Clear Conversation")
    st.write("✅ Interactive Dashboard")
