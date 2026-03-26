"""
Google Translate Integration for YuvaSaarthi using deep-translator
Supports all 22 official Indian languages + English
"""

from typing import Optional
from loguru import logger
from deep_translator import GoogleTranslator
import time

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))
from utils.config import settings


from utils.indian_languages import SUPPORTED_INDIAN_LANGUAGES

# Sync with official full list
INDIAN_LANGUAGES = {code: info["name"] for code, info in SUPPORTED_INDIAN_LANGUAGES.items()}


class GoogleTranslatorService:
    """
    Google Translate service for multilingual support
    Free and supports all Indian languages
    """
    
    def __init__(self):
        self.supported_languages = INDIAN_LANGUAGES
        logger.info(f"Google Translator initialized with {len(self.supported_languages)} Indian languages")
    
    def translate(
        self,
        text: str,
        source_lang: str = 'auto',
        target_lang: str = 'en'
    ) -> str:
        """
        Translate text from source language to target language
        
        Args:
            text: Text to translate
            source_lang: Source language code ('auto' for auto-detect)
            target_lang: Target language code
            
        Returns:
            Translated text
        """
        # If same language, return original
        if source_lang == target_lang and source_lang != 'auto':
            return text
        
        # If text is empty, return empty
        if not text or not text.strip():
            return text
        
        try:
            # Translate using deep-translator
            translator = GoogleTranslator(source=source_lang, target=target_lang)
            result = translator.translate(text)
            
            logger.debug(f"Translated: {source_lang} → {target_lang}")
            
            return result
            
        except Exception as e:
            logger.error(f"Translation error: {e}")
            return text  # Return original on error
    
    def detect_language(self, text: str) -> Optional[str]:
        """
        Detect language of given text using deep-translator
        
        Args:
            text: Text to detect language for
            
        Returns:
            Language code or None
        """
        try:
            from langdetect import detect
            detected = detect(text)
            logger.debug(f"Detected language: {detected}")
            return detected
        except Exception as e:
            logger.error(f"Language detection error: {e}")
            return None
    
    def batch_translate(
        self,
        texts: list[str],
        source_lang: str = 'auto',
        target_lang: str = 'en'
    ) -> list[str]:
        """
        Translate multiple texts
        
        Args:
            texts: List of texts to translate
            source_lang: Source language code
            target_lang: Target language code
            
        Returns:
            List of translated texts
        """
        translated = []
        for text in texts:
            translated_text = self.translate(text, source_lang, target_lang)
            translated.append(translated_text)
            # Small delay to avoid rate limiting
            time.sleep(0.1)
        
        return translated
    
    def is_indian_language(self, lang_code: str) -> bool:
        """Check if language code is an Indian language"""
        return lang_code in self.supported_languages
    
    def get_language_name(self, lang_code: str) -> str:
        """Get language name from code"""
        return self.supported_languages.get(lang_code, lang_code.upper())


class TranslationManager:
    """
    Manages translation with Google Translate via deep-translator
    """
    
    def __init__(self):
        self.translator = GoogleTranslatorService()
        logger.info("Translation Manager initialized with deep-translator")
    
    def translate(
        self,
        text: str,
        source_lang: str = 'auto',
        target_lang: str = 'en'
    ) -> str:
        """Translate text using Google Translate"""
        return self.translator.translate(text, source_lang, target_lang)
    
    def detect_language(self, text: str) -> Optional[str]:
        """Detect language of text"""
        return self.translator.detect_language(text)
    
    def is_translation_available(self) -> bool:
        """Check if translation is available"""
        return True  # Google Translate is always available
    
    def get_supported_languages(self) -> dict:
        """Get all supported Indian languages"""
        return self.translator.supported_languages


# Global translator instance
translator = TranslationManager()


if __name__ == "__main__":
    # Test translation
    print("YuvaSaarthi - Google Translation System Test")
    print("=" * 60)
    
    test_cases = [
        ("Hello, how are you?", "en", "hi"),
        ("नमस्ते, आप कैसे हैं?", "hi", "en"),
        ("Hello", "en", "ta"),  # Tamil
        ("Hello", "en", "te"),  # Telugu
        ("Hello", "en", "bn"),  # Bengali
        ("Hello", "en", "mr"),  # Marathi
    ]
    
    trans = TranslationManager()
    print(f"Translation Available: {trans.is_translation_available()}")
    print(f"Supported Languages: {len(trans.get_supported_languages())}\n")
    
    for text, source, target in test_cases:
        lang_name = trans.translator.get_language_name(target)
        print(f"Original ({source}): {text}")
        try:
            translated = trans.translate(text, source, target)
            print(f"Translated ({target} - {lang_name}): {translated}")
        except Exception as e:
            print(f"Error: {e}")
        print("-" * 60)
    
    # Test language detection
    print("\nLanguage Detection Test:")
    detect_texts = [
        "Hello, how are you?",
        "नमस्ते",
        "வணக்கம்",
        "నమస్తే",
        "নমস্কার"
    ]
    
    for text in detect_texts:
        detected = trans.detect_language(text)
        lang_name = trans.translator.get_language_name(detected) if detected else "Unknown"
        print(f"Text: {text} → Detected: {lang_name} ({detected})")
