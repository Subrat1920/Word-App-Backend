from langchain_groq import ChatGroq
from app.core.config import settings

# Singleton LLM instance
llm = ChatGroq(
    model=settings.MODEL_NAME,
    temperature=0.3,
    api_key=settings.GROQ_API_KEY
)