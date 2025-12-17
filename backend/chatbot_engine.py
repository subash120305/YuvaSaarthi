"""
YuvaSaarthi - Main Chatbot Engine
Integrates RAG, LLM, Translation, and YouTube Search
"""

from typing import Dict, List, Optional, Tuple
from loguru import logger

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

from backend.document_processor import DocumentProcessor
from backend.llm_handler import LLMHandler
from backend.google_translator import TranslationManager  # Changed to Google Translator
from backend.youtube_search import YouTubeSearcher
from utils.language_detector import LanguageDetector
from utils.config import settings


class ChatbotEngine:
    """Main chatbot engine integrating all components"""

    def __init__(self):
        logger.info("Initializing YuvaSaarthi Chatbot Engine...")

        # Initialize components
        self.doc_processor = DocumentProcessor()
        self.llm = LLMHandler()
        self.translator = TranslationManager()
        self.youtube = YouTubeSearcher()
        self.language_detector = LanguageDetector()

        # Conversation history storage (in-memory for now)
        self.conversations: Dict[str, List[dict]] = {}

        # Load vector store
        self.vector_store = self.doc_processor.load_vector_store()
        if not self.vector_store:
            logger.warning("Vector store not found. Documents need to be ingested first.")

        logger.info("Chatbot engine initialized successfully")

    def process_query(
        self,
        query: str,
        user_id: str,
        language: Optional[str] = None,
        include_videos: bool = True
    ) -> Dict[str, any]:
        """
        Process user query and generate response

        Args:
            query: User's question
            user_id: Unique user identifier
            language: Preferred language (en, hi, raj) or None for auto-detect
            include_videos: Whether to include YouTube video recommendations

        Returns:
            Dict with response, videos, language info
        """
        try:
            # Detect language if not specified
            if not language or language == "auto":
                language = self.language_detector.detect(query)
                logger.info(f"Detected language: {language}")

            # Translate query to English for RAG (if needed)
            query_for_rag = query
            if language != "en":
                query_for_rag = self.translator.translate(query, language, "en")
                logger.debug(f"Translated query for RAG: {query_for_rag}")

            # Retrieve relevant context from documents
            context = self._retrieve_context(query_for_rag)

            # Get conversation history
            history = self.conversations.get(user_id, [])

            # Generate response using LLM
            response = self.llm.generate_response(
                query=query,
                context=context,
                language=language,
                conversation_history=history
            )

            # Translate response back to user's language if needed
            if language != "en":
                response = self.translator.translate(response, "en", language)
                logger.debug(f"Translated response to {language}")

            # Update conversation history
            self._update_history(user_id, query, response)

            # Check if this is a concept explanation query
            is_study_query = self._is_study_query(query)

            # Search for YouTube videos if appropriate
            videos = []
            if include_videos and is_study_query and self.youtube.is_configured:
                videos = self.youtube.search_videos(query, language=language, max_results=3)
                logger.info(f"Found {len(videos)} YouTube videos")

            return {
                "response": response,
                "videos": videos,
                "language": language,
                "context_used": bool(context),
                "video_count": len(videos)
            }

        except Exception as e:
            logger.error(f"Error processing query: {e}")
            return {
                "response": "I apologize, but I encountered an error processing your query. Please try again.",
                "videos": [],
                "language": language or "en",
                "context_used": False,
                "video_count": 0,
                "error": str(e)
            }

    def _retrieve_context(self, query: str) -> str:
        """
        Retrieve relevant context from vector store

        Args:
            query: Search query

        Returns:
            Formatted context string
        """
        if not self.vector_store:
            return ""

        try:
            # Search for relevant documents
            results = self.doc_processor.search(query, k=settings.top_k_results)

            if not results:
                return ""

            # Format context
            context_parts = []
            for i, doc in enumerate(results, 1):
                source = doc.metadata.get('source', 'Unknown')
                content = doc.page_content.strip()

                # Add metadata if available
                metadata_str = ""
                if 'class' in doc.metadata:
                    metadata_str += f"[{doc.metadata['class']}]"
                if 'subject' in doc.metadata:
                    metadata_str += f"[{doc.metadata['subject']}]"

                context_parts.append(f"Source {i} {metadata_str}: {content}")

            context = "\n\n".join(context_parts)
            logger.debug(f"Retrieved context from {len(results)} documents")
            return context

        except Exception as e:
            logger.error(f"Context retrieval error: {e}")
            return ""

    def _is_study_query(self, query: str) -> bool:
        """
        Determine if query is about studying/learning concepts

        Args:
            query: User query

        Returns:
            True if it's a study-related query
        """
        study_keywords = [
            # English
            'explain', 'understand', 'learn', 'how', 'what', 'why',
            'theorem', 'concept', 'formula', 'solve', 'calculate',
            'definition', 'meaning', 'example', 'tutorial',

            # Hindi
            'समझाओ', 'समझना', 'सीखना', 'कैसे', 'क्या', 'क्यों',
            'सिद्धांत', 'अवधारणा', 'सूत्र', 'हल', 'परिभाषा',
            'उदाहरण', 'मतलब',

            # Rajasthani
            'समझावो', 'सीखणो', 'कांई', 'कैस्याँ', 'क्यूँ'
        ]

        query_lower = query.lower()
        return any(keyword in query_lower for keyword in study_keywords)

    def _update_history(self, user_id: str, query: str, response: str):
        """
        Update conversation history for a user

        Args:
            user_id: User identifier
            query: User's query
            response: Bot's response
        """
        if user_id not in self.conversations:
            self.conversations[user_id] = []

        self.conversations[user_id].append({
            "role": "user",
            "content": query
        })
        self.conversations[user_id].append({
            "role": "assistant",
            "content": response
        })

        # Keep only last 10 messages (5 exchanges)
        if len(self.conversations[user_id]) > 10:
            self.conversations[user_id] = self.conversations[user_id][-10:]

    def clear_history(self, user_id: str):
        """Clear conversation history for a user"""
        if user_id in self.conversations:
            del self.conversations[user_id]
            logger.info(f"Cleared history for user: {user_id}")

    def explain_concept(
        self,
        topic: str,
        language: str = "hi",
        grade_level: str = "class_10"
    ) -> Dict[str, any]:
        """
        Provide a simple explanation of a concept

        Args:
            topic: Topic to explain
            language: Language for explanation
            grade_level: Student's grade level

        Returns:
            Dict with explanation and videos
        """
        try:
            # Generate simple explanation
            explanation = self.llm.generate_simple_explanation(
                topic=topic,
                grade_level=grade_level,
                language=language
            )

            # Get YouTube videos
            videos = []
            if self.youtube.is_configured:
                videos = self.youtube.search_videos(topic, language=language, max_results=3)

            return {
                "explanation": explanation,
                "videos": videos,
                "topic": topic,
                "language": language
            }

        except Exception as e:
            logger.error(f"Error explaining concept: {e}")
            return {
                "explanation": f"Sorry, I couldn't explain this topic: {str(e)}",
                "videos": [],
                "topic": topic,
                "language": language
            }

    def ingest_new_documents(self, force_refresh: bool = False) -> bool:
        """
        Ingest or refresh documents in vector store

        Args:
            force_refresh: Force recreation of vector store

        Returns:
            True if successful
        """
        try:
            logger.info("Starting document ingestion...")
            self.vector_store = self.doc_processor.ingest_documents(force_refresh)
            return self.vector_store is not None
        except Exception as e:
            logger.error(f"Document ingestion failed: {e}")
            return False

    def get_system_health(self) -> Dict[str, any]:
        """Get health status of all components"""
        return {
            "llm": self.llm.check_health(),
            "youtube": self.youtube.check_health(),
            "translation": {"status": "healthy" if self.translator.is_translation_available() else "fallback"},
            "vector_store": {"status": "healthy" if self.vector_store else "not_initialized"},
            "bot_name": settings.bot_name,
            "version": "1.0.0"
        }


# Global chatbot instance
chatbot = None


def get_chatbot() -> ChatbotEngine:
    """Get or create global chatbot instance"""
    global chatbot
    if chatbot is None:
        chatbot = ChatbotEngine()
    return chatbot


if __name__ == "__main__":
    # Test chatbot engine
    print("YuvaSaarthi - Chatbot Engine Test")
    print("=" * 60)

    bot = ChatbotEngine()

    # System health check
    print("\nSystem Health Check:")
    health = bot.get_system_health()
    for component, status in health.items():
        if isinstance(status, dict):
            print(f"  {component}: {status.get('status', 'unknown')}")
        else:
            print(f"  {component}: {status}")

    print("\n" + "=" * 60)

    # Test query
    test_query = "पाइथागोरस प्रमेय क्या है?"
    print(f"\nTest Query: {test_query}\n")

    result = bot.process_query(
        query=test_query,
        user_id="test_user",
        language="auto",
        include_videos=True
    )

    print(f"Language Detected: {result['language']}")
    print(f"Context Used: {result['context_used']}")
    print(f"\nResponse:\n{result['response']}")

    if result['videos']:
        print(f"\n{bot.youtube.format_videos_for_display(result['videos'], result['language'])}")
