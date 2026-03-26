"""
YuvaSaarthi - Telegram Bot Interface
"""

import asyncio
import requests
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ContextTypes,
    filters
)
from loguru import logger
import sys

from utils.config import settings, SUPPORTED_LANGUAGES
from backend.voice_handler import voice_handler


class TelegramBot:
    """Telegram bot interface for YuvaSaarthi (API Client Mode)"""

    def __init__(self):
        self.bot_token = settings.telegram_bot_token
        self.api_base_url = "http://localhost:8000/api"
        
        # User preferences (in-memory storage)
        self.user_preferences = {}

        logger.info("Telegram bot initialized in API Client Mode")

    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /start command"""
        user = update.effective_user
        user_id = str(user.id)

        # Initialize user preferences
        if user_id not in self.user_preferences:
            self.user_preferences[user_id] = {
                "language": settings.default_language,
                "include_videos": True,
                "socratic_mode": False,
                "teach_back": False,
                "native_mnemonics": False
            }

        welcome_messages = {
            "en": f"""
🎓 **Welcome to YuvaSaarthi!**

Hello {user.first_name}! I'm your AI educational assistant.

**I can help you with:**
• Admissions & Course Information
• Exam Schedules & Results
• Concept Explanations (Class 8-12)
• Study Guidance & Tips
• YouTube Video Recommendations

**Commands:**
/help - Show all commands
/language - Change language
/videos - Toggle video recommendations
/clear - Clear conversation history

Ask me anything! 📚
""",
            "hi": f"""
🎓 **युवासारथी में आपका स्वागत है!**

नमस्ते {user.first_name}! मैं आपका AI शैक्षिक सहायक हूं।

**मैं आपकी मदद कर सकता हूं:**
• प्रवेश और पाठ्यक्रम की जानकारी
• परीक्षा कार्यक्रम और परिणाम
• अवधारणाओं की व्याख्या (कक्षा 8-12)
• अध्ययन मार्गदर्शन और सुझाव
• YouTube वीडियो सिफारिशें

**कमांड:**
/help - सभी कमांड देखें
/language - भाषा बदलें
/videos - वीडियो सिफारिशें टॉगल करें
/clear - वार्तालाप इतिहास साफ़ करें

मुझसे कुछ भी पूछें! 📚
""",
            "raj": f"""
🎓 **युवासारथी में थारो स्वागत है!**

नमस्कार {user.first_name}! म्हैं थारी मदद कर सकूं:
• दाखिलो अर पाठ्यक्रम री जाणकारी
• परीक्षा री तारीख अर नतीजा
• अवधारणा री समझावण (कक्षा 8-12)
• पढ़ाई री मार्गदर्शन
• YouTube वीडियो री सलाह

**कमांड:**
/help - सारा कमांड देखो
/language - भाषा बदलो
/videos - वीडियो टॉगल करो
/clear - बातचीत साफ करो

महानै कांई भी पूछो! 📚
"""
        }

        lang = self.user_preferences[user_id]["language"]
        await update.message.reply_text(
            welcome_messages.get(lang, welcome_messages["hi"]),
            parse_mode="Markdown"
        )

    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /help command"""
        user_id = str(update.effective_user.id)
        lang = self.user_preferences.get(user_id, {}).get("language", "hi")
        
        help_texts = {
            "en": """
**YuvaSaarthi Commands:**

/start - Start the bot
/help - Show this help message
/language - Change language
/videos - Toggle video recommendations
/clear - Clear history
/health - Check system status
""",
            "hi": """
**युवासारथी कमांड:**

/start - बॉट शुरू करें
/help - सहायता संदेश
/language - भाषा बदलें
/videos - वीडियो टॉगल
/clear - इतिहास साफ़ करें
/health - सिस्टम स्थिति
""",
             "raj": """
**युvaसारथी कमांड:**

/start - बॉट सुरु करो
/help - मदद
/language - भाषा बदलो
/videos - वीडियो टॉगल
/clear - बातचीत साफ
/health - सिस्टम हालत
"""
        }
        await update.message.reply_text(help_texts.get(lang, help_texts["hi"]), parse_mode="Markdown")

    async def language_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /language command"""
        
        # Create keyboard from SUPPORTED_LANGUAGES dynamically
        # Layout: 2 buttons per row
        keyboard = []
        row = []
        
        for code, info in SUPPORTED_LANGUAGES.items():
            # User requested clean names without emojis
            # info is a dictionary: {"name": "English", ...}
            # We use the English name for clarity, or could use native
            label = info.get("name", code)
            
            row.append(InlineKeyboardButton(label, callback_data=f"lang_{code}"))
            
            if len(row) == 2:
                keyboard.append(row)
                row = []
        
        if row: # Add remaining
            keyboard.append(row)

        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text("Choose your language / अपनी भाषा चुनें:", reply_markup=reply_markup)

    async def language_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle language selection"""
        query = update.callback_query
        await query.answer()
        user_id = str(query.from_user.id)
        lang_code = query.data.split("_")[1]
        
        if user_id not in self.user_preferences:
            self.user_preferences[user_id] = {}
        self.user_preferences[user_id]["language"] = lang_code
        
        # Get language name for confirmation message
        lang_name = SUPPORTED_LANGUAGES.get(lang_code, {}).get("name", lang_code)
        
        # Confirmation message
        if lang_code == "en":
            msg = f"✅ Language set to {lang_name}"
        elif lang_code == "hi":
            msg = f"✅ भाषा {lang_name} में सेट की गई"
        elif lang_code == "raj":
            msg = f"✅ भाषा {lang_name} में सेट"
        else:
            # Generic fallback for other languages (English text + Native Name)
            msg = f"✅ Language set to {lang_name}"

        await query.edit_message_text(msg)

    async def videos_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Toggle videos"""
        user_id = str(update.effective_user.id)

        if user_id not in self.user_preferences:
            self.user_preferences[user_id] = {"include_videos": True}

        curr = self.user_preferences[user_id].get("include_videos", True)
        self.user_preferences[user_id]["include_videos"] = not curr
        status = "enabled" if not curr else "disabled"
        await update.message.reply_text(f"✅ Video recommendations {status}")

    async def clear_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Clear history"""
        user_id = str(update.effective_user.id)
        try:
            response = requests.post(f"{self.api_base_url}/clear-history?conversation_id={user_id}")
            response.raise_for_status()
            await update.message.reply_text("✅ Conversation history cleared!")
        except Exception as e:
            await update.message.reply_text(f"❌ Error clearing history: {e}")

    async def health_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Check health"""
        try:
            resp = requests.get(f"{self.api_base_url}/health")
            resp.raise_for_status() # Raise HTTPError for bad responses (4xx or 5xx)
            data = resp.json()
            await update.message.reply_text(f"✅ System Healthy\nAPI Status: {data.get('status')}")
        except requests.exceptions.RequestException as e:
            await update.message.reply_text(f"❌ System Unhealthy\nError connecting to API: {e}")
        except Exception as e:
            await update.message.reply_text(f"❌ System Unhealthy\nError: {e}")

    async def socratic_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        user_id = str(update.effective_user.id)
        if user_id not in self.user_preferences:
            self.user_preferences[user_id] = {"socratic_mode": False}
        curr = self.user_preferences[user_id].get("socratic_mode", False)
        self.user_preferences[user_id]["socratic_mode"] = not curr
        status = "enabled" if not curr else "disabled"
        await update.message.reply_text(f"✅ Socratic Mode {status}")

    async def teachback_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        user_id = str(update.effective_user.id)
        if user_id not in self.user_preferences:
            self.user_preferences[user_id] = {"teach_back": False}
        curr = self.user_preferences[user_id].get("teach_back", False)
        self.user_preferences[user_id]["teach_back"] = not curr
        status = "enabled" if not curr else "disabled"
        await update.message.reply_text(f"✅ Teach-Back {status}")

    async def mnemonics_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        user_id = str(update.effective_user.id)
        if user_id not in self.user_preferences:
            self.user_preferences[user_id] = {"native_mnemonics": False}
        curr = self.user_preferences[user_id].get("native_mnemonics", False)
        self.user_preferences[user_id]["native_mnemonics"] = not curr
        status = "enabled" if not curr else "disabled"
        await update.message.reply_text(f"✅ Native Mnemonics {status}")

    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle user messages via API"""
        user_id = str(update.effective_user.id)
        query = update.message.text
        
        prefs = self.user_preferences.get(user_id, {"language": "auto", "include_videos": True})
        
        await update.message.chat.send_action("typing")
        
        try:
            payload = {
                "message": query,
                "language": prefs.get("language", "auto"),
                "conversation_id": user_id,
                "include_videos": prefs.get("include_videos", True),
                "socratic_mode": prefs.get("socratic_mode", False),
                "teach_back": prefs.get("teach_back", False),
                "native_mnemonics": prefs.get("native_mnemonics", False)
            }
            
            response = requests.post(f"{self.api_base_url}/chat", json=payload)
            response.raise_for_status()
            data = response.json()
            
            # Response text already includes appended video links if any
            try:
                await update.message.reply_text(data["response"], parse_mode="Markdown")
            except Exception as e:
                logger.warning(f"Markdown parsing failed, falling back to plain text: {e}")
                await update.message.reply_text(data["response"])
        
        except Exception as e:
            logger.error(f"Error communicating with backend: {e}")
            await update.message.reply_text("❌ Sorry, I couldn't reach the backend server. Please try again later.")

    def run(self):
        """Run the bot"""
        if not self.bot_token or self.bot_token == "your_telegram_bot_token":
            logger.error("Telegram bot token not configured!")
            print("\n❌ Error: Telegram bot token not configured")
            print("Please set TELEGRAM_BOT_TOKEN in your .env file")
            print("Get token from @BotFather on Telegram")
            return

        logger.info("Starting Telegram bot...")

        # Create application
        application = Application.builder().token(self.bot_token).build()

        # Add handlers
        application.add_handler(CommandHandler("start", self.start_command))
        application.add_handler(CommandHandler("help", self.help_command))
        application.add_handler(CommandHandler("language", self.language_command))
        application.add_handler(CommandHandler("videos", self.videos_command))
        application.add_handler(CommandHandler("clear", self.clear_command))
        application.add_handler(CommandHandler("health", self.health_command))
        application.add_handler(CommandHandler("socratic", self.socratic_command))
        application.add_handler(CommandHandler("teachback", self.teachback_command))
        application.add_handler(CommandHandler("mnemonics", self.mnemonics_command))
        application.add_handler(CallbackQueryHandler(self.language_callback, pattern="^lang_"))
        application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_message))
        application.add_handler(MessageHandler(filters.VOICE, self.handle_voice_message))
        
        # Handle unsupported content types 
        unsupported_filters = ~filters.TEXT & ~filters.COMMAND & ~filters.VOICE
        application.add_handler(MessageHandler(unsupported_filters, self.handle_unsupported_content))

        # Start bot
        print("\n" + "=" * 60)
        print("🎓 YuvaSaarthi Telegram Bot Started (API Client Mode)")
        print("=" * 60)
        print("\nBot is running... Press Ctrl+C to stop")
        print("=" * 60 + "\n")

        application.run_polling(allowed_updates=Update.ALL_TYPES)

    async def handle_voice_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle voice messages via Groq STT and return via gTTS"""
        user_id = str(update.effective_user.id)
        prefs = self.user_preferences.get(user_id, {"language": "auto", "include_videos": True})
        
        await update.message.chat.send_action("record_voice")
        
        try:
            # Download audio
            voice_file = await context.bot.get_file(update.message.voice.file_id)
            audio_bytes = await voice_file.download_as_bytearray()
            
            # Convert to text
            query = voice_handler.speech_to_text(bytes(audio_bytes))
            if not query:
                await update.message.reply_text("❌ Sorry, I couldn't understand the audio. Please try again.")
                return
            
            # Send to backend
            payload = {
                "message": query,
                "language": prefs.get("language", "auto"),
                "conversation_id": user_id,
                "include_videos": prefs.get("include_videos", True),
                "socratic_mode": prefs.get("socratic_mode", False),
                "teach_back": prefs.get("teach_back", False),
                "native_mnemonics": prefs.get("native_mnemonics", False)
            }
            
            response = requests.post(f"{self.api_base_url}/chat", json=payload)
            response.raise_for_status()
            data = response.json()
            reply_text = data["response"]
            
            # Fallback for overly long logs
            clean_reply = reply_text[:1020] + "..." if len(reply_text) > 1024 else reply_text
            
            # TTS
            audio_response = voice_handler.text_to_speech(reply_text, data.get("language", "hi"))
            
            if audio_response:
                await update.message.reply_voice(voice=audio_response, caption=f"🗣️ You said: {query}\n\n{clean_reply}")
            else:
                await update.message.reply_text(reply_text, parse_mode="Markdown")
                
        except Exception as e:
            logger.error(f"Error handling voice message: {e}")
            await update.message.reply_text("❌ Sorry, an error occurred while processing your voice.")

    async def handle_unsupported_content(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Inform user that non-text content is not supported yet"""
        msg = "⚠️ Sorry, I currently only support text and voice messages.\nPhotos and documents are coming in a future update! 📝"
        await update.message.reply_text(msg)




if __name__ == "__main__":
    try:
        bot = TelegramBot()
        bot.run()
    except KeyboardInterrupt:
        logger.info("Bot stopped by user")
        print("\n\n👋 Bot stopped.")
    except Exception as e:
        logger.error(f"Bot crashed: {e}")
        print(f"\n\n❌ Error: {e}")
