import os
import shutil
from strands import tool

# Paths
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../'))
DOCS_DIR = os.path.join(BASE_DIR, 'docs')
SORTED_DIR = os.path.join(BASE_DIR, 'sorted')

def get_sorted_categories_query() -> list:
    """
    Returns a list of the existing folders within the 'sorted' directory.
    """
    if not os.path.exists(SORTED_DIR):
        return []
    return [d for d in os.listdir(SORTED_DIR) if os.path.isdir(os.path.join(SORTED_DIR, d))]

@tool
def list_sorted_categories() -> str:
    """
    This tool lists all the categories (folders) currently available in the 'sorted' directory.
    """
    print("\n[TOOL CALL] Running list_sorted_categories")
    try:
        categories = get_sorted_categories_query()
        if not categories:
            msg = "The 'sorted' directory is currently empty. No categories found."
        else:
            msg = f"Existing categories in 'sorted': {', '.join(categories)}"
        
        print(f"[TOOL OUTPUT] {msg}")
        return msg
    except Exception as e:
        err_msg = f"ERROR: Failed to list categories with exception {e}."
        print(f"[TOOL ERROR] {err_msg}")
        return err_msg

def copy_file_to_destination_query(source_filename: str, category: str, new_filename: str) -> bool:
    """
    Copies a file from the 'docs' folder to a subfolder in 'sorted'.
    Creates the category folder if it doesn't exist.
    """
    try:
        # Create category directory if it doesn't exist
        dest_dir = os.path.join(SORTED_DIR, category.lower())
        os.makedirs(dest_dir, exist_ok=True)

        source_path = os.path.join(DOCS_DIR, source_filename)
        dest_path = os.path.join(dest_dir, new_filename)

        if not os.path.exists(source_path):
            print(f"[FILE ERROR] Source file not found: {source_path}")
            return False

        shutil.copy2(source_path, dest_path)
        print(f"[FILE SUCCESS] Copied {source_filename} to {dest_path}")
        return True
    except Exception as e:
        print(f"[FILE ERROR] Error copying file: {e}")
        return False

@tool
def sort_file_to_category(source_filename: str, category: str, new_filename: str) -> str:
    """
    This tool copies a file from the 'docs' folder to a specific category folder in 'sorted'.
    It also renames the file to a representative name provided.
    
    Args:
        source_filename: The name of the file in the 'docs' folder (e.g., 'file_1.txt').
        category: The name of the category folder (e.g., 'finance', 'sports', 'tech').
        new_filename: A representative name for the file in the destination (e.g., 'finance_report_01.txt').
    """
    print(f"\n[TOOL CALL] Running sort_file_to_category: {source_filename} -> {category}/{new_filename}")
    try:
        success = copy_file_to_destination_query(source_filename, category, new_filename)
        if success:
            msg = f"Successfully copied '{source_filename}' to 'sorted/{category.lower()}/{new_filename}'."
        else:
            msg = f"ERROR: Could not copy '{source_filename}'. Please check if the source file exists."
        
        print(f"[TOOL OUTPUT] {msg}")
        return msg
    except Exception as e:
        err_msg = f"ERROR: Failed to sort file with exception {e}."
        print(f"[TOOL ERROR] {err_msg}")
        return err_msg
