"""
YuvaSaarthi - Configuration Management
"""

import os
from pathlib import Path
from typing import Literal
from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    """Application settings with environment variable support"""

    # API Keys
    groq_api_key: str = Field(default="", alias="GROQ_API_KEY")
    bhashini_user_id: str = Field(default="", alias="BHASHINI_USER_ID")
    bhashini_api_key: str = Field(default="", alias="BHASHINI_API_KEY")
    bhashini_pipeline_id: str = Field(default="", alias="BHASHINI_PIPELINE_ID")
    youtube_api_key: str = Field(default="", alias="YOUTUBE_API_KEY")
    telegram_bot_token: str = Field(default="", alias="TELEGRAM_BOT_TOKEN")

    # Bot Configuration
    bot_name: str = Field(default="YuvaSaarthi", alias="BOT_NAME")
    bot_personality: Literal["formal", "friendly", "mix"] = Field(default="mix", alias="BOT_PERSONALITY")
    default_language: Literal["en", "hi", "raj", "auto"] = Field(default="hi", alias="DEFAULT_LANGUAGE")

    # Organization Details
    department_name: str = Field(default="Department of Technical Education", alias="DEPARTMENT_NAME")
    organization: str = Field(default="Government of Rajasthan", alias="ORGANIZATION")
    location: str = Field(default="Rajasthan, India", alias="LOCATION")
    website: str = Field(default="https://dte.rajasthan.gov.in", alias="WEBSITE")

    # System Configuration
    vector_db_path: str = Field(default="./data/vectorstore", alias="VECTOR_DB_PATH")
    chunk_size: int = Field(default=1000, alias="CHUNK_SIZE")
    chunk_overlap: int = Field(default=200, alias="CHUNK_OVERLAP")
    max_context_length: int = Field(default=4000, alias="MAX_CONTEXT_LENGTH")
    temperature: float = Field(default=0.7, alias="TEMPERATURE")

    # Models
    embedding_model: str = Field(
        default="sentence-transformers/paraphrase-multilingual-mpnet-base-v2",
        alias="EMBEDDING_MODEL"
    )
    llm_model: str = Field(default="llama-3.1-70b-versatile", alias="LLM_MODEL")

    # Advanced Settings
    debug: bool = Field(default=False, alias="DEBUG")
    log_level: str = Field(default="INFO", alias="LOG_LEVEL")
    max_tokens: int = Field(default=2048, alias="MAX_TOKENS")
    top_k_results: int = Field(default=4, alias="TOP_K_RESULTS")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False


# Global settings instance
settings = Settings()


# Project paths
PROJECT_ROOT = Path(__file__).parent.parent
DATA_DIR = PROJECT_ROOT / "data"
DOCUMENTS_DIR = DATA_DIR / "documents"
VECTOR_DB_DIR = Path(settings.vector_db_path)


# Language configurations
SUPPORTED_LANGUAGES = {
    "en": {"name": "English", "code": "en", "flag": "🇬🇧"},
    "hi": {"name": "हिंदी", "code": "hi", "flag": "🇮🇳"},
    "raj": {"name": "राजस्थानी", "code": "raj", "flag": "🏜️"}
}


# Personality prompts
PERSONALITY_PROMPTS = {
    "formal": """You are YuvaSaarthi, an official AI assistant for the Department of Technical Education,
    Government of Rajasthan. Maintain a professional and respectful tone. Provide accurate, concise information.""",

    "friendly": """You are YuvaSaarthi, a friendly AI companion helping students with their educational journey.
    Be warm, encouraging, and supportive. Use simple language and make learning enjoyable.""",

    "mix": """You are YuvaSaarthi, an AI assistant for the Department of Technical Education, Government of Rajasthan.
    For administrative queries (admissions, fees, schedules), be professional and precise.
    For study help and concept explanations, be friendly, encouraging, and use simple language.
    Always be respectful and supportive of students' learning journey."""
}


# System prompt template
SYSTEM_PROMPT_TEMPLATE = """
{personality_prompt}

Your capabilities:
- Answer questions about admissions, courses, exams, fees, and administrative processes
- Explain difficult concepts in simple terms for students from Class 8 to 12
- Provide study guidance and learning resources
- Recommend relevant YouTube videos for better understanding
- Support English, Hindi, and Rajasthani languages

Context from knowledge base:
{context}

Instructions:
- If the answer is in the context, use it to provide accurate information
- If you're explaining a concept, break it down into simple steps
- For study-related queries, be encouraging and suggest learning strategies
- If you don't know something, be honest and guide them to the right resource
- Always respond in the user's preferred language
"""


# Document categories and their metadata
DOCUMENT_CATEGORIES = {
    "textbooks": {
        "description": "Class 8-12 textbooks and study materials",
        "priority": 1,
        "tags": ["education", "study", "curriculum"]
    },
    "polytechnic": {
        "description": "Polytechnic and diploma course materials",
        "priority": 2,
        "tags": ["technical", "diploma", "vocational"]
    },
    "engineering": {
        "description": "Engineering degree programs and courses",
        "priority": 2,
        "tags": ["engineering", "degree", "btech"]
    },
    "admissions": {
        "description": "Admission processes, eligibility, and notifications",
        "priority": 3,
        "tags": ["admission", "enrollment", "eligibility"]
    },
    "administrative": {
        "description": "Fees, scholarships, facilities, and administration",
        "priority": 3,
        "tags": ["fees", "scholarship", "administration"]
    },
    "general": {
        "description": "FAQs, guides, and general information",
        "priority": 4,
        "tags": ["faq", "guide", "support"]
    }
}


def get_personality_prompt() -> str:
    """Get the configured personality prompt"""
    return PERSONALITY_PROMPTS.get(settings.bot_personality, PERSONALITY_PROMPTS["mix"])


def validate_api_keys() -> dict:
    """Validate which API keys are configured"""
    return {
        "groq": bool(settings.groq_api_key and settings.groq_api_key != "your_groq_api_key_here"),
        "bhashini": bool(settings.bhashini_api_key and settings.bhashini_api_key != "your_bhashini_api_key"),
        "youtube": bool(settings.youtube_api_key and settings.youtube_api_key != "your_youtube_api_key"),
        "telegram": bool(settings.telegram_bot_token and settings.telegram_bot_token != "your_telegram_bot_token")
    }


if __name__ == "__main__":
    # Test configuration
    print("YuvaSaarthi Configuration")
    print("=" * 50)
    print(f"Bot Name: {settings.bot_name}")
    print(f"Personality: {settings.bot_personality}")
    print(f"Default Language: {settings.default_language}")
    print(f"Department: {settings.department_name}")
    print("\nAPI Keys Status:")
    for service, status in validate_api_keys().items():
        status_icon = "✓" if status else "✗"
        print(f"  {status_icon} {service.upper()}")
