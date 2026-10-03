import os

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

load_dotenv()


def get_llm():

    return ChatOpenAI(
        api_key=os.getenv("GROQ_API_KEY"),
        model="openai/gpt-oss-20b",
        base_url="https://api.groq.com/openai/v1",
        temperature=0,
        max_tokens=4096,
        reasoning_effort="low"
    )