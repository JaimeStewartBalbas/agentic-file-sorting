import os
import sys

# Add the project root to sys.path BEFORE other local imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

from strands import Agent
from strands.models.ollama import OllamaModel
from strands_tools import file_read
from src.tools.database import is_file_sorted, mark_file_as_sorted
from src.tools.files import list_sorted_categories, sort_file_to_category
from strands.tools.executors import SequentialToolExecutor

# Create an Ollama model instance
ollama_model = OllamaModel(
    host="http://localhost:11434",  # Ollama server address
    model_id="qwen3:1.7b"              
)

SYSTEM_PROMPT = """You are an Intelligent File Organizer.
Your task is to sort .txt files from the 'docs' folder into 'sorted' subfolders.

Workflow:
1. Check if the file is already sorted using `is_file_sorted`.
2. If NOT sorted:
   - Read the file content with `file_read` (files are in the 'docs' folder).
   - Check existing categories with `list_sorted_categories`.
   - Determine the correct category or add a new one if needed.
   - Choose a descriptive new filename.
   - Move/Rename the file using `sort_file_to_category`.
   - Mark the file as sorted in the database using `mark_file_as_sorted`.

Guidelines:
- If a category doesn't exist, create it via `sort_file_to_category`.
- Be concise. Use tools exactly as described.
"""

agent = Agent(
    model=ollama_model,
    system_prompt=SYSTEM_PROMPT,
    tool_executor=SequentialToolExecutor(),
    callback_handler=None,
    tools=[is_file_sorted,
           mark_file_as_sorted,
           list_sorted_categories,
           sort_file_to_category,
           file_read]
)

if __name__ == "__main__":
    # Example usage:
    result = agent("Please sort this file: file_1.txt")
    
    # Save the output to a file
    output_path = os.path.join(os.path.dirname(__file__), "output.txt")
    with open(output_path, "w", encoding="utf-8") as f:
        # result is likely a response object, we access the content or str()
        f.write(str(result))
    
    print(f"\n[INFO] Agent response saved to {output_path}")
