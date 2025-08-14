import sqlite3

conn = sqlite3.connect("prompt_feedback.db")
c = conn.cursor()

# 1. Create a new table with the desired schema
c.execute('''
    CREATE TABLE IF NOT EXISTS feedback_new (
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

# 2. Copy data from old table to new table (excluding 'visualization')
c.execute('''
    INSERT INTO feedback_new (id, prompt, visual_accuracy, visual_insightfulness, business_relevance, comment, timestamp, code)
    SELECT id, prompt, visual_accuracy, visual_insightfulness, business_relevance, comment, timestamp, code
    FROM feedback
''')

# 3. Drop the old table
c.execute('DROP TABLE feedback')

# 4. Rename the new table to the original name
c.execute('ALTER TABLE feedback_new RENAME TO feedback')

conn.commit()
conn.close()
print("Database schema cleaned up successfully.") 