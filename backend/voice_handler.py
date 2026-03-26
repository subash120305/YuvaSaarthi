import os
import io
from gtts import gTTS
from groq import Groq
from loguru import logger
from utils.config import settings

class VoiceHandler:
    def __init__(self):
        self.api_key = settings.groq_api_key
        self.client = Groq(api_key=self.api_key) if self.api_key and self.api_key != "your_groq_api_key_here" else None

    def speech_to_text(self, audio_bytes: bytes) -> str:
        """Convert speech to text using Groq Whisper API"""
        if not self.client:
            logger.error("Groq client not configured for Voice STT")
            return ""
        
        try:
            # We need to save the bytes to a temporary file since groq's python client expects a file object
            temp_path = "/tmp/temp_voice_input.m4a"
            with open(temp_path, "wb") as f:
                f.write(audio_bytes)
                
            with open(temp_path, "rb") as file:
                transcription = self.client.audio.transcriptions.create(
                    file=(temp_path, file.read()),
                    model="whisper-large-v3",
                    response_format="text",
                )
            
            # Clean up
            if os.path.exists(temp_path):
                os.remove(temp_path)
                
            return transcription.strip()
        except Exception as e:
            logger.error(f"STT Error: {e}")
            return ""

    def text_to_speech(self, text: str, language: str = "en") -> bytes:
        """Convert text to speech using gTTS"""
        try:
            # Map common languages to gTTS codes if needed
            lang_map = {
                "en": "en",
                "hi": "hi",
                "ta": "ta",
                "te": "te",
                "mr": "mr",
                "bn": "bn",
            }
            # Fallback to current language or default to hindi if language not supported
            gtts_lang = lang_map.get(language, "hi")
            
            tts = gTTS(text=text, lang=gtts_lang, slow=False)
            fp = io.BytesIO()
            tts.write_to_fp(fp)
            fp.seek(0)
            return fp.read()
        except Exception as e:
            logger.error(f"TTS Error: {e}")
            return b""

voice_handler = VoiceHandler()
