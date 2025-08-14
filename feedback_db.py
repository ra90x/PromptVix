import sqlite3

def init_db():
    conn = sqlite3.connect("prompt_feedback.db")
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS feedback (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            prompt TEXT,
            visual_accuracy INTEGER,
            visual_insightfulness INTEGER,
            business_relevance INTEGER,
            comment TEXT,
            timestamp TEXT,
            code TEXT
        )
    ''')
    conn.commit()
    conn.close()

def save_feedback(prompt, visual_accuracy, insightfulness, relevance, comment, timestamp, code):
    try:
        conn = sqlite3.connect("prompt_feedback.db")
        c = conn.cursor()
        c.execute('''
            INSERT INTO feedback (prompt, visual_accuracy, visual_insightfulness,
            business_relevance, comment, timestamp, code)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (prompt, visual_accuracy, insightfulness, relevance, comment, timestamp, code))
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        return str(e)
