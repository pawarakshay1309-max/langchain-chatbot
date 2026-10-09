import os

import streamlit as st
from dotenv import load_dotenv
from groq import Groq


load_dotenv(override=True)


class Chatbot:
    def __init__(self):
        # Read the API key from .env or Streamlit secrets
        api_key = os.getenv("GROQ_API_KEY")

        if not api_key:
            try:
                api_key = st.secrets.get("GROQ_API_KEY", "")
            except Exception:
                api_key = ""

        if not api_key or not api_key.strip():
            raise ValueError(
                "GROQ_API_KEY is missing or invalid. "
                "Add your Groq API key to the .env file."
            )

        self.client = Groq(api_key=api_key.strip())
        self.model = "openai/gpt-oss-120b"

        self.system_prompt = (
            "You are Akshay AI, a helpful, friendly, "
            "and intelligent AI assistant. "
            "Answer clearly and accurately."
        )

        self.history = []

    def chat(self, user_input):
        messages = [
            {
                "role": "system",
                "content": self.system_prompt,
            },
            *self.history,
            {
                "role": "user",
                "content": user_input,
            },
        ]

        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=0.7,
        )

        answer = response.choices[0].message.content

        # Save both messages for multi-turn conversation
        self.history.append({
            "role": "user",
            "content": user_input,
        })

        self.history.append({
            "role": "assistant",
            "content": answer,
        })

        return answer

    def get_history(self):
        # Return message objects compatible with app.py
        from langchain_core.messages import HumanMessage, AIMessage

        converted_history = []

        for message in self.history:
            if message["role"] == "user":
                converted_history.append(
                    HumanMessage(content=message["content"])
                )
            elif message["role"] == "assistant":
                converted_history.append(
                    AIMessage(content=message["content"])
                )

        return converted_history

    def clear_memory(self):
        self.history.clear()
