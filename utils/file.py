"""File utility functions for directory traversal and file operations."""
import os
from typing import Generator


def find_files(
    directory: str,
    file_pattern: str|None = None,
    file_extension: str|None = None,
    exclude_dirs: list[str]|None = None,
    include_dirs: list[str]|None = None,
) -> Generator[str, None, None]:
    """
    Find files in directory matching the given criteria.
    
    Args:
        directory: Root directory to search
        file_pattern: Specific filename to search for
        file_extension: File extension to filter by
        exclude_dirs: Directories to exclude
        include_dirs: Only include these directories if specified
        
    Yields:
        File paths matching criteria
    """
    if exclude_dirs is None:
        exclude_dirs = [".git", "__pycache__", ".mypy_cache"]
    
    for root, dirs, files in os.walk(directory):
        # Apply directory filters
        if exclude_dirs:
            dirs[:] = [d for d in dirs if d not in exclude_dirs]
        
        if include_dirs:
            rel_path = os.path.relpath(root, directory)
            if not any(rel_path.startswith(d) for d in include_dirs) and rel_path != ".":
                continue
        
        for file in files:
            if file_pattern and file != file_pattern:
                continue
            if file_extension and not file.endswith(file_extension):
                continue
            
            yield os.path.join(root, file)


def count_lines(file_path: str) -> int:
    """Count lines in a file."""
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
        return sum(1 for _ in f)


def read_file(file_path: str) -> str:
    """Read file contents as string."""
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
        return f.read()