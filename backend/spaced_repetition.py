import sqlite3
import os
import datetime

DB_PATH = os.path.join(os.path.dirname(__file__), 'db', 'progress_store.db')

def init_srs_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS flashcards (
            user_id TEXT,
            topic TEXT,
            ease_factor REAL,
            interval INTEGER,
            next_review DATE,
            UNIQUE(user_id, topic)
        )
    ''')
    conn.commit()
    conn.close()

class SpacedRepetition:
    def __init__(self):
        init_srs_db()
        
    def add_topic(self, user_id: str, topic: str):
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        next_review = datetime.date.today() + datetime.timedelta(days=1)
        cursor.execute('''
            INSERT OR IGNORE INTO flashcards (user_id, topic, ease_factor, interval, next_review) 
            VALUES (?, ?, 2.5, 1, ?)
        ''', (user_id, topic, next_review))
        conn.commit()
        conn.close()
        
    def get_due_reviews(self, user_id: str):
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        today = datetime.date.today()
        cursor.execute("SELECT topic FROM flashcards WHERE user_id=? AND next_review <= ?", (user_id, today))
        topics = [row[0] for row in cursor.fetchall()]
        conn.close()
        return topics
        
    def review_topic(self, user_id: str, topic: str, quality: int):
        '''quality: 0-5. 5 is perfect, 0 is complete blackout.'''
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute('''SELECT ease_factor, interval FROM flashcards WHERE user_id=? AND topic=?''', (user_id, topic))
        row = cursor.fetchone()
        if not row:
            conn.close()
            return
            
        ease_factor, interval = row
        
        if quality < 3:
            interval = 1
        else:
            if interval == 1:
                interval = 6
            else:
                interval = round(interval * ease_factor)
                
        ease_factor = ease_factor + (0.1 - (5 - quality) * (0.08 + (5 - quality) * 0.02))
        ease_factor = max(1.3, ease_factor)
        
        next_review = datetime.date.today() + datetime.timedelta(days=interval)
        
        cursor.execute('''
            UPDATE flashcards SET ease_factor=?, interval=?, next_review=? WHERE user_id=? AND topic=?
        ''', (ease_factor, interval, next_review, user_id, topic))
        conn.commit()
        conn.close()

spaced_repetition = SpacedRepetition()
