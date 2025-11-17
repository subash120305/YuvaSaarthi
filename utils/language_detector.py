"""
Language Detection and Handling
"""

from typing import Literal, Optional
from langdetect import detect, LangDetectException
from loguru import logger


LanguageCode = Literal["en", "hi", "raj"]


class LanguageDetector:
    """Detect and manage language for user queries"""

    # Language mappings
    LANGUAGE_MAP = {
        "en": "en",  # English
        "hi": "hi",  # Hindi
        "mr": "hi",  # Marathi -> Hindi (similar script)
        "ne": "hi",  # Nepali -> Hindi (similar script)
    }

    # Rajasthani detection keywords (common Rajasthani words)
    RAJASTHANI_KEYWORDS = [
        "थारो", "म्हारो", "घणो", "माईत", "कद", "कठै", "कांई",
        "थानै", "म्हानै", "होसी", "हुवैगो", "रो", "री", "रै"
    ]

    def __init__(self):
        self.default_language = "hi"

    def detect(self, text: str) -> LanguageCode:
        """
        Detect language of the input text

        Args:
            text: Input text to detect language

        Returns:
            Language code: 'en', 'hi', or 'raj'
        """
        if not text or not text.strip():
            return self.default_language

        try:
            # Check for Rajasthani keywords first
            if self._is_rajasthani(text):
                logger.debug(f"Detected Rajasthani based on keywords")
                return "raj"

            # Use langdetect for other languages
            detected = detect(text)
            language = self.LANGUAGE_MAP.get(detected, "en")

            logger.debug(f"Detected language: {language} (raw: {detected})")
            return language

        except LangDetectException as e:
            logger.warning(f"Language detection failed: {e}. Using default: {self.default_language}")
            return self.default_language

    def _is_rajasthani(self, text: str) -> bool:
        """
        Check if text contains Rajasthani keywords

        Args:
            text: Input text

        Returns:
            True if Rajasthani keywords found
        """
        return any(keyword in text for keyword in self.RAJASTHANI_KEYWORDS)

    def get_language_name(self, code: LanguageCode) -> str:
        """Get full language name from code"""
        names = {
            "en": "English",
            "hi": "हिंदी",
            "raj": "राजस्थानी"
        }
        return names.get(code, "English")

    def get_language_flag(self, code: LanguageCode) -> str:
        """Get emoji flag for language"""
        flags = {
            "en": "🇬🇧",
            "hi": "🇮🇳",
            "raj": "🏜️"
        }
        return flags.get(code, "🌐")


# Global instance
language_detector = LanguageDetector()


if __name__ == "__main__":
    # Test language detection
    detector = LanguageDetector()

    test_cases = [
        ("What are the admission requirements?", "en"),
        ("प्रवेश की आवश्यकताएं क्या हैं?", "hi"),
        ("परीक्षा कद होसी?", "raj"),
        ("How much is the fee?", "en"),
        ("फीस कितनी है?", "hi"),
        ("म्हारो नाम राज है", "raj"),
    ]

    print("Language Detection Tests")
    print("=" * 60)
    for text, expected in test_cases:
        detected = detector.detect(text)
        status = "✓" if detected == expected else "✗"
        print(f"{status} Text: {text}")
        print(f"  Expected: {expected}, Detected: {detected}")
        print()
