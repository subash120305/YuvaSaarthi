"""
LLM Handler using Groq API
"""

from typing import Optional, List
from loguru import logger
from groq import Groq

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))
from utils.config import settings, get_personality_prompt, SYSTEM_PROMPT_TEMPLATE


class LLMHandler:
    """Handle LLM interactions using Groq"""

    def __init__(self):
        self.api_key = settings.groq_api_key
        self.model = settings.llm_model
        self.temperature = settings.temperature
        self.max_tokens = settings.max_tokens

        # Check if API key is configured
        self.is_configured = bool(
            self.api_key and
            self.api_key != "your_groq_api_key_here"
        )

        if self.is_configured:
            self.client = Groq(api_key=self.api_key)
            logger.info(f"Groq LLM initialized with model: {self.model}")
        else:
            self.client = None
            logger.warning("Groq API key not configured")

    def generate_response(
        self,
        query: str,
        context: str = "",
        language: str = "en",
        conversation_history: Optional[List[dict]] = None,
        socratic_mode: bool = False,
        teach_back: bool = False,
        native_mnemonics: bool = False
    ) -> str:
        """
        Generate response using LLM

        Args:
            query: User's question
            context: Retrieved context from RAG
            language: Response language (en, hi, raj)
            conversation_history: Previous conversation messages

        Returns:
            Generated response
        """
        if not self.is_configured:
            return "I apologize, but the AI service is not configured. Please contact the administrator."

        try:
            # Build system prompt
            personality = get_personality_prompt()
            system_prompt = SYSTEM_PROMPT_TEMPLATE.format(
                personality_prompt=personality,
                context=context if context else "No specific context available."
            )

            # Feature additions based on args:
            if socratic_mode:
                system_prompt += "\n\n[SOCRATIC MODE ACTIVE]: DO NOT give direct answers. Instead, act as a Socratic tutor. Ask a guiding question to help the student discover the answer themselves."
            if teach_back:
                system_prompt += "\n\n[TEACH-BACK ACTIVE]: After explaining the concept, ask the student to explain it back to you in their own words to verify their understanding."
            if native_mnemonics:
                system_prompt += f"\n\n[NATIVE MNEMONICS ACTIVE]: When generating memory aids or mnemonics, use cultural references from {language} culture (like local food, festivals, movies, cricket) to make it memorable."

            # Add language instruction
            language_instructions = {
                "en": "Respond in English.",
                "hi": "हिंदी में उत्तर दें।",
                "raj": "राजस्थानी शैली में हिंदी में उत्तर दें।"
            }
            system_prompt += f"\n\n{language_instructions.get(language, language_instructions['en'])}"

            # Build messages
            messages = [{"role": "system", "content": system_prompt}]

            # Add conversation history if provided
            if conversation_history:
                messages.extend(conversation_history[-6:])  # Last 3 exchanges

            # Add current query
            messages.append({"role": "user", "content": query})

            # Call Groq API
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=self.temperature,
                max_tokens=self.max_tokens,
            )

            answer = response.choices[0].message.content
            logger.debug(f"Generated response ({len(answer)} chars)")
            return answer

        except Exception as e:
            logger.error(f"LLM generation error: {e}")
            return f"I apologize, but I encountered an error: {str(e)}"

    def generate_simple_explanation(
        self,
        topic: str,
        grade_level: str = "class_10",
        language: str = "hi"
    ) -> str:
        """
        Generate a simple explanation for a difficult concept

        Args:
            topic: Topic to explain
            grade_level: Student's grade level
            language: Language for explanation

        Returns:
            Simple explanation
        """
        prompt = f"""
Explain the concept of "{topic}" in very simple terms for a {grade_level} student.

Requirements:
1. Use everyday examples and analogies
2. Break down complex ideas into simple steps
3. Be encouraging and supportive
4. Keep the explanation concise (2-3 paragraphs)
5. End with a practical tip for understanding better

Make it easy to understand and remember!
"""

        return self.generate_response(
            query=prompt,
            context="",
            language=language
        )

    def check_health(self) -> dict:
        """Check if LLM service is working"""
        if not self.is_configured:
            return {
                "status": "not_configured",
                "message": "Groq API key not configured"
            }

        try:
            # Try a simple completion
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": "Hello"}],
                max_tokens=10
            )

            return {
                "status": "healthy",
                "message": "Groq API is working",
                "model": self.model
            }

        except Exception as e:
            return {
                "status": "error",
                "message": str(e)
            }


# Global LLM instance
llm_handler = LLMHandler()


if __name__ == "__main__":
    # Test LLM handler
    print("YuvaSaarthi - LLM Handler Test")
    print("=" * 60)

    llm = LLMHandler()

    # Health check
    health = llm.check_health()
    print(f"Health Status: {health['status']}")
    print(f"Message: {health['message']}\n")

    if health['status'] == 'healthy':
        # Test query
        test_query = "What is Pythagoras theorem?"
        print(f"Test Query: {test_query}\n")

        response = llm.generate_response(
            query=test_query,
            context="Pythagoras theorem states that in a right triangle, the square of the hypotenuse equals the sum of squares of the other two sides.",
            language="en"
        )

        print(f"Response:\n{response}")
