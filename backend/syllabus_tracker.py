import json
import sqlite3
import os
from groq import Groq
from loguru import logger
from utils.config import settings

DB_PATH = os.path.join(os.path.dirname(__file__), 'db', 'progress_store.db')

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS syllabus_progress (
            user_id TEXT,
            exam TEXT,
            subject TEXT,
            chapter TEXT,
            UNIQUE(user_id, exam, subject, chapter)
        )
    ''')
    conn.commit()
    conn.close()

class SyllabusTracker:
    def __init__(self):
        init_db()
        self.api_key = settings.groq_api_key
        self.client = Groq(api_key=self.api_key) if self.api_key and self.api_key != "your_groq_api_key_here" else None
        
        # Load syllabi
        self.syllabi = {}
        syllabi_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'syllabi')
        if os.path.exists(syllabi_dir):
            for file in os.listdir(syllabi_dir):
                if file.endswith('.json'):
                    with open(os.path.join(syllabi_dir, file), 'r') as f:
                        data = json.load(f)
                        key = f"{data['exam']}_{data['subject']}"
                        self.syllabi[key] = data['chapters']
    
    def classify_and_store(self, user_id: str, query: str):
        if not self.client or not self.syllabi:
            return None
        
        try:
            # Let's just use JEE Physics for demo
            exam = "JEE Mains"
            subject = "Physics"
            chapters = self.syllabi.get(f"{exam}_{subject}", [])
            
            prompt = f"Given the user query: '{query}', classify it into ONE of these syllabus chapters: {chapters}. Return ONLY the exact chapter name, or 'None' if it doesn't match any."
            
            response = self.client.chat.completions.create(
                model=settings.llm_model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.0,
                max_tokens=20
            )
            
            chapter = response.choices[0].message.content.strip()
            
            if chapter in chapters:
                conn = sqlite3.connect(DB_PATH)
                cursor = conn.cursor()
                cursor.execute('INSERT OR IGNORE INTO syllabus_progress (user_id, exam, subject, chapter) VALUES (?, ?, ?, ?)', 
                              (user_id, exam, subject, chapter))
                conn.commit()
                conn.close()
                return chapter
        except Exception as e:
            logger.error(f"Syllabus classification error: {e}")
        return None

    def get_progress(self, user_id: str, exam: str = "JEE Mains", subject: str = "Physics"):
        chapters = self.syllabi.get(f"{exam}_{subject}", [])
        if not chapters:
            return {"total": 0, "covered": 0, "percentage": 0, "chapters": []}
            
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute('SELECT chapter FROM syllabus_progress WHERE user_id=? AND exam=? AND subject=?', (user_id, exam, subject))
        covered_chapters = [row[0] for row in cursor.fetchall()]
        conn.close()
        
        return {
            "total": len(chapters),
            "covered": len(covered_chapters),
            "percentage": int((len(covered_chapters) / len(chapters)) * 100) if chapters else 0,
            "covered_chapters": covered_chapters,
            "all_chapters": chapters
        }

tracker = SyllabusTracker()
