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
    default_language: Literal["en", "hi", "raj", "auto"] = Field(default="en", alias="DEFAULT_LANGUAGE")

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
        # Use absolute path for .env file
        env_file = str(Path(__file__).parent.parent / ".env")
        env_file_encoding = "utf-8"
        case_sensitive = False


# Global settings instance
settings = Settings()


# Project paths
PROJECT_ROOT = Path(__file__).parent.parent
DATA_DIR = PROJECT_ROOT / "data"
DOCUMENTS_DIR = DATA_DIR / "documents"

# Convert vector_db_path to absolute path if it's relative
if Path(settings.vector_db_path).is_absolute():
    VECTOR_DB_DIR = Path(settings.vector_db_path)
else:
    VECTOR_DB_DIR = PROJECT_ROOT / settings.vector_db_path.lstrip('./')


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

Your Purpose:
You are YuvaSaarthi, an AI assistant specifically designed for EDUCATION-RELATED queries. You help with:
- Academic subjects (Class 8-12): Math, Science, English, Hindi, Social Science, etc.
- Engineering, Polytechnic, and Technical education concepts
- Rajasthan education: RBSE, admissions, courses, exams, results, grading
- Administrative: Fees, scholarships, reservations, eligibility, application processes
- Study guidance, learning strategies, exam preparation, career advice in education
- Educational institutions, programs, and policies

Context from knowledge base:
{context}

Instructions:
1. ANSWER if the query is about:
   - Academic concepts, theories, formulas, or educational topics
   - Admissions, fees, scholarships, reservations, eligibility
   - Study techniques, exam preparation, educational guidance
   - Engineering/technical subjects and concepts
   - Educational institutions, courses, and programs

   When answering:
   - If information is in the context above, use it for accurate responses
   - If it's an educational concept not in the context, explain using your knowledge
   - Break down complex topics into simple, student-friendly explanations
   - Be encouraging and supportive

2. POLITELY DECLINE if the query is about:
   - Sports, entertainment, movies, music, celebrities
   - Current news, politics, weather, shopping
   - Cooking, recipes, health tips, lifestyle
   - General knowledge unrelated to education

   Respond: "मैं युवासारथी हूँ, केवल शिक्षा से संबंधित प्रश्नों में मदद के लिए बनाया गया। मैं आपकी सहायता कर सकता हूँ:
   • शैक्षणिक विषय (कक्षा 8-12, इंजीनियरिंग)
   • प्रवेश, फीस, छात्रवृत्ति, आरक्षण
   • परीक्षा, परिणाम, पाठ्यक्रम
   • अध्ययन मार्गदर्शन और करियर सलाह

   कृपया शिक्षा से जुड़े प्रश्न पूछें!"

   (In English: "I am YuvaSaarthi, designed only for education-related queries. I can help with academic subjects, admissions, fees, scholarships, reservations, exams, and study guidance. Please ask education-related questions!")

3. GREETINGS: Respond warmly and ask how you can help with their studies.

Always respond in the user's preferred language.
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
