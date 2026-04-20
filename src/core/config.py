"""
Core configuration and environment settings.
"""

import os

from dotenv import load_dotenv

load_dotenv()


class Settings:
    """Application settings loaded from environment variables."""

    GROQ_API_KEY: str = os.getenv("GROQ_API_KEY", "")
    HUGGINGFACE_MODEL: str = os.getenv(
        "HUGGINGFACE_MODEL", "sentence-transformers/all-MiniLM-L6-v2"
    )
    TAVILY_API_KEY: str = os.getenv("TAVILY_API_KEY", "")
    MONGODB_URL: str = os.getenv("MONGODB_URL", None)
    MONGODB_DB_NAME: str = os.getenv("MONGODB_DB_NAME", "adaptive_rag")


settings = Settings()

# Set env variables for LangChain integrations
os.environ["GROQ_API_KEY"] = settings.GROQ_API_KEY
os.environ["TAVILY_API_KEY"] = settings.TAVILY_API_KEY
