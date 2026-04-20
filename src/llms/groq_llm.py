"""
Groq LLM initialization and configuration (free tier).
"""

from langchain_groq import ChatGroq

from src.core.config import settings

llm = ChatGroq(
    model="llama3-70b-8192",
    api_key=settings.GROQ_API_KEY,
    temperature=0,
)
