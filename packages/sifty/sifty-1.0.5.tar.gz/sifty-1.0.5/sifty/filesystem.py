import os
from pathlib import Path

def getfilesize(base_dir = ".", filename = ""):
    """Get the size of a file in bytes."""
    file_path = Path(base_dir) / filename
    
    if not file_path.exists() or not file_path.is_file():
        print(f"File '{filename}' not found in '{base_dir}'.")
        return None
    
    file_size = os.path.getsize(file_path)
    return file_size


def search_files(base_dir, search_term):
    base_path = Path(base_dir)

    if not base_path.exists() or not base_path.is_dir():
        print(f"Directory '{base_dir}' does not exist or is not a valid directory.")
        return []

    matching_files = []
    for root, dirs, files in os.walk(base_dir):
        for file in files:
            if search_term.lower() in file.lower():
                matching_files.append(os.path.join(root, file))
    return matching_files
