from groq import Groq
from utils.config import settings
from .prompts.teacher import TEACHER_PROMPT

class TeacherAssistant:
    def __init__(self):
        self.api_key = settings.groq_api_key
        self.client = Groq(api_key=self.api_key) if self.api_key and self.api_key != "your_groq_api_key_here" else None

    def generate_lesson_plan(self, topic: str, duration: str = "40 min", language: str = "Hindi") -> str:
        if not self.client:
            return "Teacher Assist service is not configured."
        
        prompt = TEACHER_PROMPT.format(plan_type="Lesson Plan", topic=topic, duration=duration, language=language)
        
        response = self.client.chat.completions.create(
            model=settings.llm_model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=1000
        )
        return response.choices[0].message.content

teacher_assistant = TeacherAssistant()
