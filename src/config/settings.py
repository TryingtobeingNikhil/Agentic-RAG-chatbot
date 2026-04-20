"""
Configuration settings for the application.
"""

import os
from pathlib import Path

import yaml
from dotenv import load_dotenv

load_dotenv()


class Config:
    """Load and manage configuration from YAML file."""

    # Free-tier API keys
    GROQ_API_KEY: str = os.getenv("GROQ_API_KEY", "")
    HUGGINGFACE_MODEL: str = os.getenv(
        "HUGGINGFACE_MODEL", "sentence-transformers/all-MiniLM-L6-v2"
    )
    TAVILY_API_KEY: str = os.getenv("TAVILY_API_KEY", "")

    # Optional database settings
    MONGODB_URL: str = os.getenv("MONGODB_URL", None)
    MONGODB_DB_NAME: str = os.getenv("MONGODB_DB_NAME", "adaptive_rag")

    def __init__(self, config_file: str = None):
        """
        Initialize configuration from YAML file.

        Args:
            config_file: Optional path to config file. Defaults to prompts.yaml.
        """
        base_path = Path(__file__).parent
        config_path = (
            base_path / "prompts.yaml"
            if config_file is None
            else Path(config_file)
        )
        with open(config_path, "r") as f:
            self.config = yaml.safe_load(f)

    def prompt(self, key: str) -> str:
        """
        Retrieve a prompt from configuration.

        Args:
            key: The prompt key.

        Returns:
            The prompt template string.
        """
        return self.config["prompts"][key]
