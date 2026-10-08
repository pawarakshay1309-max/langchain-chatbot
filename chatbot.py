import os

from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage, AIMessage


# ============================================================
# Load environment variables
# ============================================================

load_dotenv()


class Chatbot:
    """
    LangChain conversational chatbot using Google Gemini.
    """

    def __init__(self):

        # ====================================================
        # Get Gemini API key
        # ====================================================

        api_key = os.getenv("GEMINI_API_KEY")

        if not api_key:
            raise ValueError(
                "GEMINI_API_KEY is missing. "
                "Please add it to the .env file."
            )

        # ====================================================
        # Initialize Gemini
        # ====================================================

        self.llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            google_api_key=api_key,
            temperature=0.7,
            max_retries=2,
            timeout=60,
        )

        # ====================================================
        # Conversation memory
        # ====================================================

        self.chat_history = []

        # ====================================================
        # Prompt
        # ====================================================

        self.prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    """
You are a helpful AI assistant.

Follow these rules:

1. Answer clearly and simply.
2. Be polite and professional.
3. Use previous conversation when relevant.
4. If you don't know something, say you don't know.
5. Keep answers easy to understand.
6. Do not make up information.
"""
                ),

                MessagesPlaceholder(
                    variable_name="chat_history"
                ),

                (
                    "human",
                    "{user_input}"
                ),
            ]
        )

    # ========================================================
    # Chat
    # ========================================================

    def chat(self, user_input: str) -> str:

        if not user_input or not user_input.strip():
            return "Please enter a valid message."

        try:

            # Create prompt messages
            messages = self.prompt.format_messages(
                chat_history=self.chat_history,
                user_input=user_input
            )

            # Send request to Gemini
            response = self.llm.invoke(messages)

            # =================================================
            # Extract response
            # =================================================

            if isinstance(response.content, list):

                text_parts = []

                for item in response.content:

                    if isinstance(item, dict):

                        if item.get("type") == "text":
                            text_parts.append(
                                item.get("text", "")
                            )

                    elif isinstance(item, str):
                        text_parts.append(item)

                answer = "".join(text_parts)

            else:

                answer = str(response.content)

            # =================================================
            # Empty response protection
            # =================================================

            if not answer.strip():
                answer = "I couldn't generate a response."

            # =================================================
            # Save conversation
            # =================================================

            self.chat_history.append(
                HumanMessage(
                    content=user_input
                )
            )

            self.chat_history.append(
                AIMessage(
                    content=answer
                )
            )

            return answer

        except Exception as e:

            print(f"\nGemini Error: {e}")

            error_message = str(e).lower()

            if (
                "quota" in error_message
                or "resource_exhausted" in error_message
            ):
                return (
                    "Gemini API quota has been exceeded. "
                    "Please check your Gemini API quota."
                )

            if (
                "api key" in error_message
                or "authentication" in error_message
                or "unauthorized" in error_message
                or "401" in error_message
                or "403" in error_message
            ):
                return (
                    "Gemini API key is invalid. "
                    "Please check your GEMINI_API_KEY."
                )

            return (
                "Sorry, I couldn't process your request.\n\n"
                f"Error: {e}"
            )

    # ========================================================
    # Clear memory
    # ========================================================

    def clear_memory(self):

        self.chat_history = []

    # ========================================================
    # Get history
    # ========================================================

    def get_history(self):

        return self.chat_history

        return self.chat_history
