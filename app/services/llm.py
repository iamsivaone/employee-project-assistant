import os

from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chat_models import init_chat_model

load_dotenv()

google_llm = ChatGoogleGenerativeAI(
    model="gemini-3.6-flash", google_api_key=os.getenv("GOOGLE_API_KEY"), temperature=0
)


llm = init_chat_model(
            model="openai/gpt-oss-20b",
            model_provider="groq",
            temperature=0
        )