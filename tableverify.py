import sqlite3

# Connect to your SQLite database
conn = sqlite3.connect(
    "instance/test.db"
)  # Update with the correct path if needed
cursor = conn.cursor()

# Execute the query to check if the 'summaries' table exists
cursor.execute(
    "SELECT name FROM sqlite_master WHERE type='table' AND name='summaries';"
)

# Fetch the result
table_exists = cursor.fetchone()

if table_exists:
    print("Table 'summaries' exists.")
else:
    print("Table 'summaries' does NOT exist.")

conn.close()
