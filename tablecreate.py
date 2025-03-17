import os
import sqlite3

# Path to your existing SQLite database in the instance directory
DB_PATH = os.path.join(os.path.dirname(__file__), "instance", "test.db")

# Connect to the existing database
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# Create the 'summaries' table if it doesn't exist
cursor.execute("""
CREATE TABLE IF NOT EXISTS summaries (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    file_id INTEGER UNIQUE,
    summary TEXT,
    FOREIGN KEY (file_id) REFERENCES files(id)
)
""")

conn.commit()
conn.close()

print("Summaries table has been created successfully.")
