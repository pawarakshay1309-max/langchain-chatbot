import streamlit as st
from chatbot import Chatbot


# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="Akshay AI Assistant",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)


# =========================================================
# SIMPLE CUSTOM STYLE
# =========================================================

st.markdown("""
<style>

    /* Main page */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 1200px;
    }

    /* Metric cards */
    div[data-testid="metric-container"] {
        background-color: white;
        border: 1px solid #e5e7eb;
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
    }

    /* Chat input */
    div[data-testid="stChatInput"] {
        margin-bottom: 20px;
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        border-right: 1px solid #e5e7eb;
    }

</style>
""", unsafe_allow_html=True)


# =========================================================
# CREATE CHATBOT
# =========================================================

if "chatbot" not in st.session_state:

    try:
        st.session_state.chatbot = Chatbot()

    except ValueError as e:
        st.error(str(e))
        st.stop()


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
        [
            "💬 Chat",
            "📊 Dashboard",
            "ℹ️ About"
        ],
        label_visibility="collapsed"
    )

    st.divider()

    st.subheader("⚙️ Chat Settings")

    if st.button(
        "🗑️ Clear Conversation",
        use_container_width=True
    ):

        st.session_state.chatbot.clear_memory()

        st.rerun()

    st.divider()

    st.subheader("✨ Features")

    st.write("🧠 Gemini LLM")
    st.write("🔗 LangChain")
    st.write("💭 Conversation Memory")
    st.write("🔄 Multi-turn Chat")
    st.write("⚙️ System Prompt")


# =========================================================
# GET CHAT HISTORY
# =========================================================

history = st.session_state.chatbot.get_history()

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

    # Header
    st.title("🤖 Akshay AI Assistant")

    st.write(
        "Your intelligent AI assistant powered by LangChain and Gemini."
    )

    st.divider()

    # Quick information
    col1, col2, col3 = st.columns(3)

    with col1:
        st.info("🧠 **Gemini LLM**\n\nAI-powered responses")

    with col2:
        st.success("🔗 **LangChain**\n\nConversation framework")

    with col3:
        st.warning("💭 **Memory**\n\nMulti-turn conversation")

    st.divider()

    # Welcome message
    if not history:

        st.markdown("## 👋 Welcome to Akshay AI!")

        st.write(
            "Start a conversation by typing your question below."
        )

        st.write("### 💡 Try asking:")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.button(
                "🐍 Explain Python",
                use_container_width=True
            )

        with col2:
            st.button(
                "🤖 What is AI?",
                use_container_width=True
            )

        with col3:
            st.button(
                "📚 Explain Machine Learning",
                use_container_width=True
            )

    # -----------------------------------------------------
    # CHAT HISTORY
    # -----------------------------------------------------

    for message in history:

        if message.type == "human":

            with st.chat_message(
                "user",
                avatar="👤"
            ):
                st.write(message.content)

        elif message.type == "ai":

            with st.chat_message(
                "assistant",
                avatar="🤖"
            ):
                st.write(message.content)

    # -----------------------------------------------------
    # CHAT INPUT
    # -----------------------------------------------------

    user_input = st.chat_input(
        "💬 Type your message here..."
    )

    if user_input:

        with st.chat_message(
            "user",
            avatar="👤"
        ):
            st.write(user_input)

        with st.chat_message(
            "assistant",
            avatar="🤖"
        ):

            with st.spinner("🤔 Akshay AI is thinking..."):

                try:

                    response = (
                        st.session_state
                        .chatbot
                        .chat(user_input)
                    )

                    st.write(response)

                except Exception as e:

                    st.error(
                        f"❌ Error: {e}"
                    )


# =========================================================
# DASHBOARD PAGE
# =========================================================

elif page == "📊 Dashboard":

    st.title("📊 AI Dashboard")

    st.write(
        "Overview of your current chatbot session."
    )

    st.divider()

    # -----------------------------------------------------
    # STATISTICS
    # -----------------------------------------------------

    st.subheader("📈 Conversation Statistics")

    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric(
            label="💬 Total Messages",
            value=total_messages
        )

    with col2:

        st.metric(
            label="👤 Your Questions",
            value=user_messages
        )

    with col3:

        st.metric(
            label="🤖 AI Responses",
            value=ai_messages
        )

    st.divider()

    # -----------------------------------------------------
    # AI FEATURES
    # -----------------------------------------------------

    st.subheader("🚀 AI Capabilities")

    col1, col2 = st.columns(2)

    with col1:

        with st.container(border=True):

            st.subheader("🧠 Gemini LLM")

            st.write(
                "Generates intelligent responses "
                "to user questions."
            )

            st.success("Active")

    with col2:

        with st.container(border=True):

            st.subheader("🔗 LangChain")

            st.write(
                "Connects the chatbot with the "
                "language model and conversation logic."
            )

            st.success("Active")

    col1, col2 = st.columns(2)

    with col1:

        with st.container(border=True):

            st.subheader("💭 Conversation Memory")

            st.write(
                "Maintains previous messages for "
                "multi-turn conversations."
            )

            st.success("Active")

    with col2:

        with st.container(border=True):

            st.subheader("⚙️ System Prompt")

            st.write(
                "Controls the assistant's behavior "
                "and response style."
            )

            st.success("Active")

    st.divider()

    # -----------------------------------------------------
    # RECENT ACTIVITY
    # -----------------------------------------------------

    st.subheader("🕒 Recent Conversation")

    if history:

        for message in history[-6:]:

            if message.type == "human":

                st.write(
                    f"👤 **You:** {message.content}"
                )

            else:

                st.write(
                    f"🤖 **Akshay AI:** {message.content}"
                )

    else:

        st.info(
            "No conversation yet. Go to Chat and start talking with Akshay AI."
        )


# =========================================================
# ABOUT PAGE
# =========================================================

elif page == "ℹ️ About":

    st.title("ℹ️ About Akshay AI")

    st.write(
        "Akshay AI is a conversational AI application "
        "built using Python, Streamlit and LangChain."
    )

    st.divider()

    st.subheader("🛠️ Technology Stack")

    col1, col2 = st.columns(2)

    with col1:

        st.write("🐍 Python")
        st.write("🎈 Streamlit")
        st.write("🔗 LangChain")

    with col2:

        st.write("🧠 Gemini LLM")
        st.write("💭 Conversation Memory")
        st.write("⚙️ System Prompt")

    st.divider()

    st.subheader("✨ Features")

    st.write("✅ Interactive Chat Interface")
    st.write("✅ Multi-turn Conversation")
    st.write("✅ Conversation Memory")
    st.write("✅ Gemini LLM")
    st.write("✅ LangChain Integration")
    st.write("✅ Clear Conversation")
    st.write("✅ Interactive Dashboard")