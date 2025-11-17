"""
Translation System using Bhashini API
Supports English, Hindi, and Rajasthani
"""

import requests
from typing import Literal, Optional
from loguru import logger

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))
from utils.config import settings


LanguageCode = Literal["en", "hi", "raj"]


class BhashiniTranslator:
    """Translator using Government of India's Bhashini API"""

    # Bhashini language codes
    LANGUAGE_CODES = {
        "en": "en",
        "hi": "hi",
        "raj": "hi"  # Rajasthani uses Hindi as base
    }

    def __init__(self):
        self.user_id = settings.bhashini_user_id
        self.api_key = settings.bhashini_api_key
        self.pipeline_id = settings.bhashini_pipeline_id
        self.base_url = "https://meity-auth.ulcacontrib.org/ulca/apis/v0/model/getModelsPipeline"

        self.is_configured = bool(
            self.api_key and
            self.api_key != "your_bhashini_api_key" and
            self.user_id
        )

    def translate(
        self,
        text: str,
        source_lang: LanguageCode,
        target_lang: LanguageCode
    ) -> str:
        """
        Translate text between languages

        Args:
            text: Text to translate
            source_lang: Source language code
            target_lang: Target language code

        Returns:
            Translated text
        """
        # If same language, return original
        if source_lang == target_lang:
            return text

        # If Bhashini is not configured, return original with warning
        if not self.is_configured:
            logger.warning("Bhashini API not configured. Translation disabled.")
            return text

        # Handle Rajasthani as Hindi variant
        bhashini_source = self.LANGUAGE_CODES.get(source_lang, "hi")
        bhashini_target = self.LANGUAGE_CODES.get(target_lang, "hi")

        try:
            # Call Bhashini API
            translated = self._call_bhashini_api(
                text,
                bhashini_source,
                bhashini_target
            )

            # If translating to Rajasthani, apply dialect conversion
            if target_lang == "raj" and translated:
                translated = self._apply_rajasthani_style(translated)

            return translated if translated else text

        except Exception as e:
            logger.error(f"Translation error: {e}")
            return text  # Return original on error

    def _call_bhashini_api(
        self,
        text: str,
        source_lang: str,
        target_lang: str
    ) -> Optional[str]:
        """
        Call Bhashini translation API

        Args:
            text: Text to translate
            source_lang: Source language code
            target_lang: Target language code

        Returns:
            Translated text or None on error
        """
        try:
            # Bhashini API payload
            payload = {
                "pipelineTasks": [
                    {
                        "taskType": "translation",
                        "config": {
                            "language": {
                                "sourceLanguage": source_lang,
                                "targetLanguage": target_lang
                            }
                        }
                    }
                ],
                "inputData": {
                    "input": [{"source": text}]
                }
            }

            headers = {
                "userID": self.user_id,
                "ulcaApiKey": self.api_key,
                "Content-Type": "application/json"
            }

            response = requests.post(
                self.base_url,
                json=payload,
                headers=headers,
                timeout=10
            )

            if response.status_code == 200:
                result = response.json()
                translated_text = result["pipelineResponse"][0]["output"][0]["target"]
                logger.debug(f"Translation successful: {source_lang} -> {target_lang}")
                return translated_text
            else:
                logger.error(f"Bhashini API error: {response.status_code}")
                return None

        except Exception as e:
            logger.error(f"Bhashini API call failed: {e}")
            return None

    def _apply_rajasthani_style(self, hindi_text: str) -> str:
        """
        Convert standard Hindi to Rajasthani dialect style

        This is a basic conversion for demonstration.
        Real Rajasthani would require more sophisticated NLP.

        Args:
            hindi_text: Text in Hindi

        Returns:
            Text with Rajasthani flavor
        """
        # Basic substitutions for common words
        replacements = {
            "मैं": "म्है",
            "तुम": "थे",
            "आप": "थे",
            "आपका": "थारो",
            "मेरा": "म्हारो",
            "बहुत": "घणो",
            "कब": "कद",
            "कहाँ": "कठै",
            "क्या": "कांई",
            "है": "सै",
            "हैं": "सै",
            "होगा": "होसी",
            "था": "हतो",
            "करना": "करणो"
        }

        result = hindi_text
        for hindi, rajasthani in replacements.items():
            result = result.replace(hindi, rajasthani)

        return result


class FallbackTranslator:
    """Fallback translator when Bhashini is not available"""

    def translate(
        self,
        text: str,
        source_lang: LanguageCode,
        target_lang: LanguageCode
    ) -> str:
        """
        Simple fallback - returns original text
        In production, this could use another translation service
        """
        if source_lang == target_lang:
            return text

        logger.warning(
            f"Fallback translator: Cannot translate {source_lang} -> {target_lang}. "
            "Returning original text."
        )
        return text


class TranslationManager:
    """Manages translation with fallback options"""

    def __init__(self):
        # Try Bhashini first
        self.bhashini = BhashiniTranslator()

        if self.bhashini.is_configured:
            self.translator = self.bhashini
            logger.info("Using Bhashini translator")
        else:
            self.translator = FallbackTranslator()
            logger.warning("Bhashini not configured. Using fallback translator.")

    def translate(
        self,
        text: str,
        source_lang: LanguageCode,
        target_lang: LanguageCode
    ) -> str:
        """Translate text using configured translator"""
        return self.translator.translate(text, source_lang, target_lang)

    def is_translation_available(self) -> bool:
        """Check if translation is available"""
        return isinstance(self.translator, BhashiniTranslator)


# Global translator instance
translator = TranslationManager()


if __name__ == "__main__":
    # Test translation
    print("YuvaSaarthi - Translation System Test")
    print("=" * 60)

    test_cases = [
        ("Hello, how are you?", "en", "hi"),
        ("नमस्ते, आप कैसे हैं?", "hi", "en"),
        ("What is your name?", "en", "raj"),
    ]

    trans = TranslationManager()
    print(f"Translation Available: {trans.is_translation_available()}\n")

    for text, source, target in test_cases:
        print(f"Original ({source}): {text}")
        translated = trans.translate(text, source, target)
        print(f"Translated ({target}): {translated}")
        print("-" * 60)
