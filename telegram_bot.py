"""
YuvaSaarthi - Telegram Bot Interface
"""

import asyncio
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

from backend.chatbot_engine import get_chatbot
from utils.config import settings, SUPPORTED_LANGUAGES


class TelegramBot:
    """Telegram bot interface for YuvaSaarthi"""

    def __init__(self):
        self.bot_token = settings.telegram_bot_token
        self.chatbot = get_chatbot()

        # User preferences (in-memory storage)
        self.user_preferences = {}

        logger.info("Telegram bot initialized")

    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /start command"""
        user = update.effective_user
        user_id = str(user.id)

        # Initialize user preferences
        if user_id not in self.user_preferences:
            self.user_preferences[user_id] = {
                "language": settings.default_language,
                "include_videos": True
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

नमस्कार {user.first_name}! म्हैं थारो AI शिक्षा सहायक हूं।

**म्हैं थारी मदद कर सकूं:**
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

म्हानै कांई भी पूछो! 📚
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
/language - Change language (English/Hindi/Rajasthani)
/videos - Toggle YouTube video recommendations
/clear - Clear conversation history
/health - Check system status

**How to use:**
Just send me your questions directly! For example:
• "What are the admission requirements?"
• "Explain Pythagoras theorem"
• "When are the exams?"
""",
            "hi": """
**युवासारथी कमांड:**

/start - बॉट शुरू करें
/help - यह सहायता संदेश दिखाएं
/language - भाषा बदलें (अंग्रेज़ी/हिंदी/राजस्थानी)
/videos - YouTube वीडियो सिफारिशें टॉगल करें
/clear - वार्तालाप इतिहास साफ़ करें
/health - सिस्टम स्थिति जांचें

**उपयोग कैसे करें:**
बस मुझे सीधे अपने सवाल भेजें! उदाहरण के लिए:
• "प्रवेश की आवश्यकताएं क्या हैं?"
• "पाइथागोरस प्रमेय समझाओ"
• "परीक्षाएं कब हैं?"
""",
            "raj": """
**युवासारथी कमांड:**

/start - बॉट सुरु करो
/help - यो मदद संदेश देखो
/language - भाषा बदलो (अंग्रेजी/हिंदी/राजस्थानी)
/videos - YouTube वीडियो टॉगल करो
/clear - बातचीत साफ करो
/health - सिस्टम री हालत देखो

**कैस्यां इस्तेमाल करो:**
सीधो म्हानै आपरा सवाल भेजो! जैस्या:
• "दाखिलो री जरूरत कांई है?"
• "पाइथागोरस थ्योरम समझावो"
• "परीक्षा कद है?"
"""
        }

        await update.message.reply_text(
            help_texts.get(lang, help_texts["hi"]),
            parse_mode="Markdown"
        )

    async def language_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /language command - show language selection"""
        keyboard = [
            [
                InlineKeyboardButton("🇬🇧 English", callback_data="lang_en"),
                InlineKeyboardButton("🇮🇳 हिंदी", callback_data="lang_hi")
            ],
            [
                InlineKeyboardButton("🏜️ राजस्थानी", callback_data="lang_raj")
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        await update.message.reply_text(
            "Choose your language / अपनी भाषा चुनें / आपरी भाषा चुणो:",
            reply_markup=reply_markup
        )

    async def language_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle language selection callback"""
        query = update.callback_query
        await query.answer()

        user_id = str(query.from_user.id)
        lang_code = query.data.split("_")[1]

        # Update user preference
        if user_id not in self.user_preferences:
            self.user_preferences[user_id] = {}
        self.user_preferences[user_id]["language"] = lang_code

        confirmations = {
            "en": "✅ Language set to English",
            "hi": "✅ भाषा हिंदी में सेट की गई",
            "raj": "✅ भाषा राजस्थानी में सेट होगी"
        }

        await query.edit_message_text(confirmations.get(lang_code, confirmations["hi"]))

    async def videos_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Toggle YouTube video recommendations"""
        user_id = str(update.effective_user.id)

        if user_id not in self.user_preferences:
            self.user_preferences[user_id] = {"include_videos": True}

        current = self.user_preferences[user_id].get("include_videos", True)
        self.user_preferences[user_id]["include_videos"] = not current

        lang = self.user_preferences[user_id].get("language", "hi")
        status = "enabled" if not current else "disabled"

        messages = {
            "en": f"✅ YouTube video recommendations {status}",
            "hi": f"✅ YouTube वीडियो सिफारिशें {'सक्षम' if not current else 'अक्षम'}",
            "raj": f"✅ YouTube वीडियो {'चालू' if not current else 'बंद'}"
        }

        await update.message.reply_text(messages.get(lang, messages["hi"]))

    async def clear_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Clear conversation history"""
        user_id = str(update.effective_user.id)
        self.chatbot.clear_history(user_id)

        lang = self.user_preferences.get(user_id, {}).get("language", "hi")

        messages = {
            "en": "✅ Conversation history cleared!",
            "hi": "✅ वार्तालाप इतिहास साफ़ हो गया!",
            "raj": "✅ बातचीत री हिस्ट्री साफ होगी!"
        }

        await update.message.reply_text(messages.get(lang, messages["hi"]))

    async def health_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Show system health status"""
        health = self.chatbot.get_system_health()

        status_text = f"""
**System Health Status**

🤖 LLM: {health['llm']['status']}
📺 YouTube: {health['youtube']['status']}
🌐 Translation: {health['translation']['status']}
📚 Vector Store: {health['vector_store']['status']}

Version: {health['version']}
"""

        await update.message.reply_text(status_text, parse_mode="Markdown")

    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle user messages"""
        user_id = str(update.effective_user.id)
        query = update.message.text

        # Get user preferences
        prefs = self.user_preferences.get(user_id, {
            "language": "auto",
            "include_videos": True
        })

        # Show typing indicator
        await update.message.chat.send_action("typing")

        try:
            # Process query
            result = self.chatbot.process_query(
                query=query,
                user_id=user_id,
                language=prefs.get("language", "auto"),
                include_videos=prefs.get("include_videos", True)
            )

            # Send response
            response_text = result["response"]

            # Add videos if available
            if result["videos"]:
                video_text = self.chatbot.youtube.format_videos_for_display(
                    result["videos"],
                    result["language"]
                )
                response_text += f"\n\n{video_text}"

            await update.message.reply_text(response_text, parse_mode="Markdown")

        except Exception as e:
            logger.error(f"Error handling message: {e}")
            await update.message.reply_text(
                "Sorry, I encountered an error. Please try again."
            )

    def run(self):
        """Run the Telegram bot"""
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
        application.add_handler(CallbackQueryHandler(self.language_callback, pattern="^lang_"))
        application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_message))

        # Start bot
        print("\n" + "=" * 60)
        print("🎓 YuvaSaarthi Telegram Bot Started!")
        print("=" * 60)
        print(f"Bot Name: {settings.bot_name}")
        print(f"Department: {settings.department_name}")
        print("\nBot is running... Press Ctrl+C to stop")
        print("=" * 60 + "\n")

        application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    try:
        bot = TelegramBot()
        bot.run()
    except KeyboardInterrupt:
        logger.info("Bot stopped by user")
        print("\n\n👋 Bot stopped. Goodbye!")
    except Exception as e:
        logger.error(f"Bot crashed: {e}")
        print(f"\n\n❌ Error: {e}")
