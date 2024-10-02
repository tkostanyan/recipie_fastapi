import os

from pathlib import Path
from dotenv import load_dotenv

from pydantic_settings import BaseSettings

BASE_DIR = Path(__file__).parent.resolve()


class Settings(BaseSettings):
    """Application settings."""

    WORKERS_COUNT: int = 1
    OPENAI_KEY: str
    OPENAI_LLM: str

    class Config:
        env_file = f"{BASE_DIR}/.env"
        env_file_encoding = "utf-8"

    @classmethod
    def load_from_env(cls):
        load_dotenv()
        return cls(
            OPENAI_KEY=os.getenv('OPENAI_KEY'),
            OPENAI_LLM=os.getenv('OPENAI_LLM', "gpt-3.5-turbo"),

        )


settings = Settings.load_from_env()
