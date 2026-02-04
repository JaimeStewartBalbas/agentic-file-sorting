import sqlite3
import os
from strands import tool

# Path to the database file
DB_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '../database/files_metadata.db'))

def get_file_sorted_query(filename: str = "file_1.txt") -> int:
    """
    This function queries the database to check the is_sorted status of a file.
    Returns: 0 if not sorted, 1 if sorted, -1 if not found.
    """
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT is_sorted FROM files WHERE filename = ?", (filename,))
        row = cursor.fetchone()
        conn.close()
        
        if row is not None:
            return int(row[0])
        return -1  
    except Exception as e:
        print(f"[DB QUERY ERROR] {e}")
        return -2 

@tool
def is_file_sorted(filename: str = "file_1.txt") -> str:
    """
    This tool queries the filename in the SQL-Lite database and checks if has or not sorted already.
    """
    print(f"\n[TOOL CALL] Running is_file_sorted for: {filename}")
    try:
        result = get_file_sorted_query(filename)

        if result == 0:
            msg = f"The file {filename} is not sorted yet."
        elif result == 1:
            msg = f"The file {filename} is already sorted."
        elif result == -1:
            msg = f"The file {filename} was not found in the database."
        else:
            msg = f"ERROR: Unexpected result value: {result} when querying database."
        
        print(f"[TOOL OUTPUT] {msg}")
        return msg

    except Exception as e:
        err_msg = f"ERROR: There has been an error processing {filename} with exception {e}."
        print(f"[TOOL ERROR] {err_msg}")
        return err_msg

def set_file_sorted_query(filename: str) -> bool:
    """
    Updates the is_sorted field to 1 for the given filename.
    Returns True if the update was successful, False otherwise.
    """
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("UPDATE files SET is_sorted = 1 WHERE filename = ?", (filename,))
        updated_rows = cursor.rowcount
        conn.commit()
        conn.close()
        return updated_rows > 0
    except Exception as e:
        print(f"[DB UPDATE ERROR] {e}")
        return False

@tool
def mark_file_as_sorted(filename: str) -> str:
    """
    This tool updates the status of a file in the database to 'sorted'.
    """
    print(f"\n[TOOL CALL] Running mark_file_as_sorted for: {filename}")
    try:
        success = set_file_sorted_query(filename)
        if success:
            msg = f"The file {filename} has been successfully marked as sorted in the database."
        else:
            msg = f"The file {filename} could not be marked as sorted (it might not exist in the database)."
        
        print(f"[TOOL OUTPUT] {msg}")
        return msg
    except Exception as e:
        err_msg = f"ERROR: Failed to mark {filename} as sorted with exception {e}."
        print(f"[TOOL ERROR] {err_msg}")
        return err_msg
