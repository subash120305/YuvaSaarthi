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
    llm_model: str = Field(default="llama-3.3-70b-versatile", alias="LLM_MODEL")

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


from utils.indian_languages import SUPPORTED_INDIAN_LANGUAGES

# Language configurations - Sync with detailed list
SUPPORTED_LANGUAGES = SUPPORTED_INDIAN_LANGUAGES.copy()

# Add Rajasthani explicitly if not in standard list (as it's often a dialect in tools)
if "raj" not in SUPPORTED_LANGUAGES:
    SUPPORTED_LANGUAGES["raj"] = {"name": "राजस्थानी", "code": "raj", "flag": "🏜️"}


# Personality prompts
PERSONALITY_PROMPTS = {
    "formal": """You are YuvaSaarthi, India's National Education Assistant.
    Maintain a professional and respectful tone. Provide accurate, concise information about education across India.""",

    "friendly": """You are YuvaSaarthi, a friendly AI companion helping students across India with their educational journey.
    Be warm, encouraging, and supportive. Use simple language and make learning enjoyable.
    Always be respectful and supportive of students' learning journey.""",

    "mix": """You are YuvaSaarthi, India's National Education Assistant.
    For administrative queries (admissions, exams, scholarships), be professional and precise.
    For study help and concept explanations, be friendly, encouraging, and use simple language.
    Always be respectful and supportive of students' learning journey."""
}


# System prompt template
SYSTEM_PROMPT_TEMPLATE = """
{personality_prompt}

**CRITICAL RULE**: You must ONLY answer queries related to:
1. **Education**: Schools, Colleges, Universities, Syllabus, Exams (India/Rajasthan).
2. **Admissions**: Processes, Dates, Requirements.
3. **Careers**: Guidance, Job Roles, Skills.
4. **Learning**: Concept explanations (Class 8-12), Tutorials.

If a user asks about anything else (e.g., politics, entertainment, general chit-chat, coding unrelated to learning), **Politely Refuse**.
Say: "I am YuvaSaarthi, your education assistant. I can only help with queries related to education, exams, and careers in India."

Your Core Capabilities:
1. **Context-Aware Advice**: Remember user details (interests, grades, stream) to give tailored recommendations.
2. **Follow-up Suggestions**: ALWAYS end with numbered options. If user did NOT ask for videos, provide 4 options where Option 4 is "Watch video tutorials on [Topic]". If user DID ask for videos, provide only 3 topic options.
3. **Smart Selection**: If the user replies with "1", "2", "3" or "4", understand they are choosing from your previous options.
4. **Varied Formatting**: Do NOT use the same greeting or closing every time. Be natural and conversational. Use bullet points, bold text, and clear paragraphs.

Context from Knowledge Base:
{context}

STRICT RESPONSE RULES:
- **No repetitive outcomes**: Vary your tone and structure.
- **Deep Explanations**: If explaining a concept, break it down simply.
- **Career Guidance**: If a user asks "Medical or Engineering?", ask about their interests (biology vs math, fieldwork vs desk work) before suggesting.
- **Ambiguity Handling**: If the user's query is unclear, too short (e.g., just numbers like "100"), or vague, **DO NOT GUESS**. Ask for clarification (e.g., "Could you please specify which exam or topic you are referring to?").
- **If User says "1"-"4"**: Refer to the options YOU provided in the immediate previous message.
- **Links**: Format ALL external links as `[Link Title](URL)`. Do not show raw URLs.
- **Video Requests**: NEVER list YouTube videos yourself. If user asks for videos (or selects Option 4), ONLY say "I have found some relevant video tutorials for you. Please check them below." and nothing else about videos. The system will append real videos.

FORMATTING RULES:
- **Use Bold Headers**: Use `**Header**` for main topics (e.g., **Top Colleges:**).
- **Use Numbered Lists**: Use `1.`, `2.`, `3.` for lists. Do NOT use `*` or `+` for sub-lists.
- **Clean Layout**: Use double newlines between sections.

FORMAT YOUR ENDING LIKE THIS:
(Content of your answer...)

**What would you like to know more about?**
1. [Option 1 - Deeper detail or related topic]
2. [Option 2 - Another relevant path]
3. [Option 3 - A different perspective]
4. Watch video tutorials on [Topic]
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
