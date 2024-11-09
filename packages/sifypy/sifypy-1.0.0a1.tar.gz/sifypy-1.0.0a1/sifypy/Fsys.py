import os
from pathlib import Path

def getfilesize(base_dir = ".", filename = ""):
    file_path = Path(base_dir) / filename

    if not file_path.exists() or not file_path.is_file():
        raise FileNotFoundError(f"File '{filename}' not found in '{base_dir}'")
        return None

    file_size = os.path.getsize(file_path)
    return file_size

def getdir(base_dir = ".", filter_extension=None, filter_name=None):
    files = []
    for file_path in Path(base_dir).iterdir():
        if file_path.is_file():
            if filter_extension and not file_path.suffix == filter_extension:
                continue
            if filter_name and filter_name not in file_path.name:
                continue
            files.append(file_path.name)
    return files

