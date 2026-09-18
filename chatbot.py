import os

from dotenv import load_dotenv
from google.genai.types import AutomaticFunctionCallingConfig

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage, AIMessage


# ============================================================
# Load environment variables from .env
# ============================================================

load_dotenv()


class Chatbot:
    """
    LangChain conversational chatbot using Google Gemini.

    Features:
    - Gemini LLM integration
    - LangChain prompt template
    - System prompt
    - Conversation memory
    - Multi-turn conversation
    - Error handling
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
        # Initialize Gemini LLM
        # ====================================================

        self.llm = ChatGoogleGenerativeAI(
            model="gemini-3.6-flash",
            google_api_key=api_key,
            max_retries=2,
            timeout=60,
        ).bind(
            automatic_function_calling=AutomaticFunctionCallingConfig(
                disable=True
            )
        )

        # ====================================================
        # Conversation Memory
        # ====================================================

        self.chat_history = []

        # ====================================================
        # Prompt Template
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

                # Previous conversation
                MessagesPlaceholder(
                    variable_name="chat_history"
                ),

                # Current user message
                (
                    "human",
                    "{user_input}"
                ),
            ]
        )

    # ========================================================
    # Chat Function
    # ========================================================

    def chat(self, user_input: str) -> str:
        """
        Send user message to Gemini
        and return AI response.
        """

        # ----------------------------------------------------
        # Validate user input
        # ----------------------------------------------------

        if not user_input or not user_input.strip():
            return "Please enter a valid message."

        try:

            # ------------------------------------------------
            # Create messages using prompt template
            # ------------------------------------------------

            messages = self.prompt.format_messages(
                chat_history=self.chat_history,
                user_input=user_input
            )

            # ------------------------------------------------
            # Send request to Gemini
            # ------------------------------------------------

            response = self.llm.invoke(messages)

            # ------------------------------------------------
            # Extract response text
            # ------------------------------------------------

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

            # ------------------------------------------------
            # Empty response protection
            # ------------------------------------------------

            if not answer.strip():
                answer = "I couldn't generate a response."

            # ------------------------------------------------
            # Save user message to memory
            # ------------------------------------------------

            self.chat_history.append(
                HumanMessage(
                    content=user_input
                )
            )

            # ------------------------------------------------
            # Save AI response to memory
            # ------------------------------------------------

            self.chat_history.append(
                AIMessage(
                    content=answer
                )
            )

            # ------------------------------------------------
            # Return response
            # ------------------------------------------------

            return answer

        except Exception as e:

            # ------------------------------------------------
            # Print actual error for debugging
            # ------------------------------------------------

            print(f"\nError: {e}")

            # ------------------------------------------------
            # Friendly error for user
            # ------------------------------------------------

            error_message = str(e).lower()

            if "quota" in error_message or "resource_exhausted" in error_message:
                return (
                    "Gemini API quota has been exceeded. "
                    "Please try again after the quota resets "
                    "or check your Gemini API billing/quota."
                )

            if "api key" in error_message:
                return (
                    "Gemini API key is missing or invalid. "
                    "Please check your .env file."
                )

            return (
                "Sorry, I couldn't process your request. "
                "Please try again."
            )

    # ========================================================
    # Clear Conversation Memory
    # ========================================================

    def clear_memory(self):
        """
        Clear conversation history.
        """

        self.chat_history = []

    # ========================================================
    # Get Conversation History
    # ========================================================

    def get_history(self):
        """
        Return conversation history.
        """

        return self.chat_history