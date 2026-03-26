import json
import os
from groq import Groq
from loguru import logger
from utils.config import settings

class ExamIntelligence:
    def __init__(self):
        self.api_key = settings.groq_api_key
        self.client = Groq(api_key=self.api_key) if self.api_key and self.api_key != "your_groq_api_key_here" else None
        
        self.patterns = {}
        patterns_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'exam_patterns')
        if os.path.exists(patterns_dir):
            for file in os.listdir(patterns_dir):
                if file.endswith('.json'):
                    with open(os.path.join(patterns_dir, file), 'r') as f:
                        data = json.load(f)
                        self.patterns[data['exam'].lower()] = data
                        
    def provide_strategy(self, user_query: str, exam: str = "jee mains"):
        exam_id = exam.lower()
        if exam_id not in self.patterns:
            return "Sorry, I don't have pattern data for this exam right now."
            
        if not self.client:
            return "Exam strategy service not configured."
            
        data = self.patterns[exam_id]
        
        prompt = f"""You are an expert Indian exam strategist. The student is asking: '{user_query}'
        
Here is the PYQ weightage data for {exam}:
{json.dumps(data, indent=2)}

Provide a concise, strategic 3-step action plan for the student based ONLY on this data. Highlight easy vs hard topics."""

        try:
            response = self.client.chat.completions.create(
                model=settings.llm_model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.2,
                max_tokens=500
            )
            return response.choices[0].message.content
        except Exception as e:
            logger.error(f"Strategy generation error: {e}")
            return "Error generating strategy."

exam_intelligence = ExamIntelligence()
