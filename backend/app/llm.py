import os
from langchain_google_genai import ChatGoogleGenerativeAI

def get_llm():
    return ChatGoogleGenerativeAI(
        model="gemini-pro",
        temperature=0.3,
        google_api_key=os.getenv("GEMINI_API_KEY")
    )
