import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    GROQ_API_KEY: str = os.getenv("GROQ_API_WORD_MEANING")
    MODEL_NAME: str = "openai/gpt-oss-120b"

settings = Settings()