import sqlite3
import os

def load_database():
    # Path to the database file in the current directory
    db_path = os.path.join(os.path.dirname(__file__), 'files_metadata.db')
    
    # Path to the docs directory (relative to this script)
    docs_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../docs'))
    
    # Connect to SQLite database (it will be created if it doesn't exist)
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Create the files table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS files (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            filename TEXT NOT NULL UNIQUE,
            is_sorted BOOLEAN DEFAULT 0
        )
    ''')
    
    # Check if docs directory exists
    if not os.path.exists(docs_dir):
        print(f"Error: Directory {docs_dir} not found.")
        return

    # List all files in the docs directory
    files = [f for f in os.listdir(docs_dir) if os.path.isfile(os.path.join(docs_dir, f))]
    
    # Populate the table with filenames
    count = 0
    for filename in files:
        try:
            cursor.execute('INSERT INTO files (filename, is_sorted) VALUES (?, ?)', (filename, 0))
            print(f"Added to database: {filename}")
            count += 1
        except sqlite3.IntegrityError:
            # If the file is already in the DB, we skip it
            print(f"Skipping {filename} already in DB.")
            pass
            
    conn.commit()
    conn.close()
    print(f"Process finished. {count} new files added to the database.")

if __name__ == "__main__":
    load_database()
