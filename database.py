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
            video_id TEXT UNIQUE,
            video_title TEXT,
            transcript TEXT,
            summary TEXT,
            generated_on TEXT
        )
    ''')
    conn.commit()
    conn.close()

def save_summary_to_db(video_id, title, transcript_text, summary):
    conn = get_db_connection()
    cursor = conn.cursor()
    generated_on = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Check if the video_id already exists
    cursor.execute("SELECT * FROM summaries WHERE video_id = ?", (video_id,))
    result = cursor.fetchone()

    if result:
        # Update the existing record
        cursor.execute('''
            UPDATE summaries
            SET title = ?, transcript = ?, summary = ?, generated_on = ?
            WHERE video_id = ?
        ''', (title, transcript_text, summary, generated_on, video_id))
        conn.commit()
        print(f"Summary for video_id {video_id} updated.")
    else:
        # Insert a new record
        cursor.execute('''
            INSERT INTO summaries (video_id, title, transcript, summary, generated_on)
            VALUES (?, ?, ?, ?, ?)
        ''', (video_id, title, transcript_text, summary, generated_on))
        conn.commit()
        print(f"Summary for video_id {video_id} saved.")

    conn.close()
    conn = get_db_connection()
    cursor = conn.cursor()
    generated_on = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Check if the video_id already exists
    cursor.execute("SELECT * FROM summaries WHERE video_id = ?", (video_id,))
    result = cursor.fetchone()

    if result:
        # Update the existing record
        cursor.execute('''
            UPDATE summaries
            SET title = ?, transcript = ?, summary = ?, generated_on = ?
            WHERE video_id = ?
        ''', (title, transcript_text, summary, generated_on,  video_id))
        conn.commit()
        print(f"Summary for video_id {video_id} updated.")
    else:
        # Insert a new record
        cursor.execute('''
            INSERT INTO summaries (video_id, title, transcript, summary)
            VALUES (?, ?, ?, ?, ?)
        ''', (video_id, title, transcript_text, summary))
        conn.commit()
        print(f"Summary for video_id {video_id} saved.")

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
