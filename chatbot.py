import os

from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, AIMessage


load_dotenv()


class Chatbot:

    def __init__(self):

        api_key = os.getenv("GEMINI_API_KEY")

        if not api_key:
            raise ValueError(
                "GEMINI_API_KEY is missing. "
                "Please add GEMINI_API_KEY to your .env file."
            )

        self.llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            google_api_key=api_key,
            temperature=0.7,
        )

        self.chat_history = []

    def chat(self, user_input):

        if not user_input.strip():
            return "Please enter a message."

        try:

            messages = [
                (
                    "system",
                    "You are a helpful AI assistant. "
                    "Answer clearly and accurately. "
                    "Keep answers easy to understand."
                )
            ]

            messages.extend(self.chat_history)

            messages.append(
                HumanMessage(content=user_input)
            )

            response = self.llm.invoke(messages)

            answer = response.content

            if isinstance(answer, list):

                answer = "".join(
                    item.get("text", "")
                    for item in answer
                    if isinstance(item, dict)
                )

            answer = str(answer)

            self.chat_history.append(
                HumanMessage(content=user_input)
            )

            self.chat_history.append(
                AIMessage(content=answer)
            )

            return answer

        except Exception as e:

            print("ERROR:", e)

            return f"Error: {e}"

    def clear_memory(self):

        self.chat_history = []
