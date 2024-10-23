import sqlite3
from datetime import datetime

# Function to get a database connection
def get_db_connection():
    return sqlite3.connect('summaries.db', check_same_thread=False)

# Function to create the summaries table if not exists
def create_table():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS summaries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            video_id TEXT,
            video_title TEXT,
            transcript TEXT,
            summary TEXT,
            date_generated TEXT
        )
    ''')
    conn.commit()
    conn.close()

# Function to save summary details
def save_summary_to_db(video_id, title, transcript, summary):
    conn = get_db_connection()
    cursor = conn.cursor()
    generated_on = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    summary_data = (video_id, title, transcript, summary,generated_on )
    cursor.execute('''
        INSERT INTO summaries (video_id, title, transcript, summary, generated_on)
        VALUES (?, ?, ?, ?, ?)
    ''', summary_data)
    conn.commit()
    conn.close()

# Function to retrieve all summaries from the database
def get_summaries_from_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM summaries')
    summaries = cursor.fetchall()
    conn.close()
    return summaries

# Function to delete a specific summary from the database by id
def delete_summary_from_db(summary_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM summaries WHERE id = ?', (summary_id,))
    conn.commit()
    conn.close()

# Call create_table to ensure the table exists
create_table()
