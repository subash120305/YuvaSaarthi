import sqlite3
import os
import requests
from loguru import logger

DB_PATH = os.path.join(os.path.dirname(__file__), 'db', 'progress_store.db')

def init_schemes_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS schemes (
            id TEXT PRIMARY KEY,
            title TEXT,
            description TEXT,
            eligibility TEXT,
            link TEXT
        )
    ''')
    conn.commit()
    conn.close()

class SchemesClient:
    def __init__(self):
        init_schemes_db()
        self.sync_dummy_data()  # Fallback to local data
        
    def sync_dummy_data(self):
        # A simple fallback sync to local DB for reliability as suggested
        dummy_schemes = [
            ("post-matric-obc", "Post-Matric Scholarship for OBC", "Up to Rs 10,000/year for OBC students.", "OBC, Income < 2.5L", "scholarships.gov.in"),
            ("up-merit", "UP State Merit Scholarship", "Rs 5,000 one-time for meritorious students.", "12th Pass UP", "scholarship.up.gov.in"),
            ("pm-ssy", "PM YASASVI Scholarship", "Award for brilliant students.", "Class 9 to 12. Income < 2.5L", "yet.nta.ac.in")
        ]
        
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        for s in dummy_schemes:
            cursor.execute('''
                INSERT OR IGNORE INTO schemes (id, title, description, eligibility, link) 
                VALUES (?, ?, ?, ?, ?)
            ''', s)
        conn.commit()
        conn.close()

    def search_schemes(self, query: str):
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        # Simple local search
        q = f"%{query.lower()}%"
        cursor.execute("SELECT title, description, link FROM schemes WHERE LOWER(title) LIKE ? OR LOWER(description) LIKE ? OR LOWER(eligibility) LIKE ?", (q, q, q))
        results = cursor.fetchall()
        conn.close()
        
        if not results:
            return "No matching schemes found right now based on your query."
            
        formatted = "Here are the eligible schemes I found:\n"
        for idx, r in enumerate(results, 1):
            formatted += f"{idx}. **{r[0]}**: {r[1]} (Apply at {r[2]})\n"
        return formatted

schemes_client = SchemesClient()
