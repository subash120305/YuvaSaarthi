"""
YuvaSaarthi - Main Chatbot Engine
Integrates RAG, LLM, Translation, and YouTube Search
"""

import re
from typing import Dict, List, Optional, Tuple
from loguru import logger

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

from backend.document_processor import DocumentProcessor
from backend.llm_handler import LLMHandler
from backend.google_translator import TranslationManager
from backend.youtube_search import YouTubeSearcher
from backend.syllabus_tracker import tracker as syllabus_tracker
from backend.vision_handler import vision_handler
from backend.teacher_assistant import teacher_assistant
from backend.spaced_repetition import spaced_repetition
from backend.exam_intelligence import exam_intelligence
from backend.schemes_client import schemes_client
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
        include_videos: bool = True,
        socratic_mode: bool = False,
        teach_back: bool = False,
        native_mnemonics: bool = False,
        image_path: Optional[str] = None
    ) -> Dict[str, any]:
        """
        Process user query and generate response
        """
        try:
            # Detect language if not specified
            if not language or language == "auto":
                language = self.language_detector.detect(query)
                logger.info(f"Detected language: {language}")

            if image_path:
                logger.info("Processing image input.")
                vision_resp = vision_handler.explain_image(image_path, query, language)
                self._update_history(user_id, "[Image Upload] " + query, vision_resp)
                return {
                    "response": vision_resp,
                    "videos": [],
                    "language": language,
                    "context_used": False,
                    "video_count": 0
                }

            # Feature 2: Distress Detection
            distress_keywords = ["want to die", "no point", "give up", "can't take it", "suicide", "end my life", "i want to die", "kill myself", "feeling hopeless", "depressed"]
            if any(k in query.lower() for k in distress_keywords):
                logger.info("Distress detected in query.")
                empathetic_response = "I can hear that you're going through a really tough time right now. Exam results or academic pressure don't define your worth or your future. If you're feeling overwhelmed, please reach out to someone who can help immediately:\n- **iCall**: 9152987821\n- **Vandrevala Foundation**: 1860-2662-345 (24/7)\n- **AASRA**: 9820466726\nWould you like to talk about what options are available to you?"
                try:
                    if language and language != "en":
                        empathetic_response = self.translator.translate(empathetic_response, "en", language)
                except Exception as e:
                    logger.warning(f"Failed to translate distress response: {e}")
                
                self._update_history(user_id, query, empathetic_response)
                return {
                    "response": empathetic_response,
                    "videos": [],
                    "language": language,
                    "context_used": False,
                    "video_count": 0
                }

            # Intercept intense queries
            q_lower = query.lower()
            if "lesson plan" in q_lower or "teacher mode" in q_lower:
                topic = query.replace("lesson plan", "").replace("for", "").strip() or "General Topic"
                resp = teacher_assistant.generate_lesson_plan(topic, language=language)
                self._update_history(user_id, query, resp)
                return {"response": resp, "videos": [], "language": language, "context_used": False, "video_count": 0}

            if "exam pattern" in q_lower or "strategy" in q_lower or "weightage" in q_lower:
                resp = exam_intelligence.provide_strategy(query)
                self._update_history(user_id, query, resp)
                return {"response": resp, "videos": [], "language": language, "context_used": False, "video_count": 0}

            if "scholarship" in q_lower or "scheme" in q_lower or "eligibility" in q_lower:
                resp = schemes_client.search_schemes(query)
                self._update_history(user_id, query, resp)
                return {"response": resp, "videos": [], "language": language, "context_used": False, "video_count": 0}

            # Get conversation history for context
            history = self.conversations.get(user_id, [])

            # Handle Option Selection (1, 2, 3)
            # If user sends a single digit, look up the option in the previous bot message
            if query.strip() in ["1", "2", "3"] and history:
                try:
                    last_bot_msg = history[-1]["content"] # Last message should be from Assistant
                    option_num = query.strip()
                    # Regex to find "1. Some text"
                    # Matches "1. Text..." until newline
                    match = re.search(rf"{option_num}\.\s*(.*?)(?:\n|$)", last_bot_msg)
                    if match:
                        extracted_option = match.group(1).strip()
                        logger.info(f"User selected Option {option_num}. Rewriting query to: '{extracted_option}'")
                        query = extracted_option
                        # Update language detection for the NEW query if needed (usually stays same)
                except Exception as e:
                    logger.warning(f"Failed to extract option context: {e}")

            # Handle Short Contextual Queries (e.g., "Strategy", "Syllabus", "Why")
            # If query is very short (< 3 words), append context from previous interaction
            if len(query.split()) <= 2 and len(history) >= 2:
                last_user_query = history[-2]["content"]
                # Avoid chaining if it's already long or disjoint
                if len(last_user_query.split()) < 20: 
                    logger.info(f"Short query detected. Appending context from: {last_user_query}")
                    query = f"{last_user_query} {query}"
                    logger.info(f"Contextualized query: {query}")

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
                conversation_history=history,
                socratic_mode=socratic_mode,
                teach_back=teach_back,
                native_mnemonics=native_mnemonics
            )

            # Feature 3 Gap Tracker & Feature 12 NEP Mapping
            classified_chapter = syllabus_tracker.classify_and_store(user_id, query)
            if classified_chapter and classified_chapter != "None":
                spaced_repetition.add_topic(user_id, classified_chapter) # Feature 8
                import json
                try:
                    with open("data/nep_mapping.json") as f:
                        nep_data = json.load(f)
                    if classified_chapter in nep_data:
                        n = nep_data[classified_chapter]
                        response += f"\n\n*NEP 2020: This topic aligns with {n['stage']}, Competency: {n['competency']}*"
                except Exception as e:
                    logger.warning(f"NEP tagging error: {e}")

            # Translate response back to user's language if needed
            if language != "en":
                response = self.translator.translate(response, "en", language)
                logger.debug(f"Translated response to {language}")

            # Feature 3 syllabus progress
            if "progress" in q_lower or "coverage" in q_lower:
                prog = syllabus_tracker.get_progress(user_id)
                response += f"\n\n**Syllabus Progress Tracker:**\nCoverage: {prog['percentage']}% ({prog['covered']}/{prog['total']} topics)"

            # Update conversation history
            self._update_history(user_id, query, response)

            # Check if this is a concept explanation query
            is_study_query = self._is_study_query(query)

            # Check for explicit video request
            explicit_video_request = "video" in query.lower() or query.strip() == "4"

            # Determine video search topic
            # Determine video search topic
            video_search_query = query
            if query.strip() == "4" and len(history) >= 2:
                # If user selects "4" (Video Option), context is in their PREVIOUS message
                # History structure: [User, Bot, User(current), Bot(current-being-built)]? 
                # No, history passed to this func is UP TO current.
                # Actually, 'history' passed here excludes current.
                # So if user sent "4", '4' is current query.
                # History[-1] is Bot Response. History[-2] is User's previous query.
                
                last_user_query = history[-2]["content"] if len(history) >= 2 else ""
                
                # Use the previous user query as the topic (e.g., "When is GATE 2026")
                # Clean it a bit
                clean_topic = last_user_query.lower().replace("explain", "").replace("tell me about", "").strip()
                if clean_topic:
                    video_search_query = clean_topic
                    logger.info(f"Extracted video topic from previous user query: {video_search_query}")
                else:
                    # Fallback to current query if extraction fails
                    pass

            # Search for YouTube videos ONLY if explicitly requested
            videos = []
            if include_videos and self.youtube.is_configured:
                if explicit_video_request:
                    videos = self.youtube.search_videos(video_search_query, language=language, max_results=3)
                    logger.info(f"Found {len(videos)} YouTube videos for topic: {video_search_query}")

            # Append videos to response text so they appear in all interfaces (Frontend/Telegram)
            if videos:
                video_text = self.youtube.format_videos_for_display(videos, language)
                response += f"\n\n{video_text}"

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
