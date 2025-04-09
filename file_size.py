#!/usr/bin/env python3
"""
Tool to find the largest files in a directory.

This script traverses a directory structure and reports on the largest files
found, with options to include or exclude specific directories or file types.
"""
import os
import sys

from utils.cli import setup_basic_parser, validate_args, parse_list_arg
from utils.file import find_files


def get_file_sizes(
    directory: str, 
    include_dirs: list[str]|None = None, 
    exclude_dirs: list[str]|None = None,
    exclude_extensions: list[str]|None = None
) -> list[tuple[str, int]]:
    """
    Get sizes of all files in the directory.
    
    Args:
        directory: Root directory to search
        include_dirs: Only include these directories if specified
        exclude_dirs: Directories to exclude
        exclude_extensions: File extensions to exclude
        
    Returns:
        list of (file_path, size) tuples
    """
    file_sizes = []
    
    # Default excludes if none provided
    if exclude_dirs is None:
        exclude_dirs = [".git", "build", "__pycache__", ".mypy_cache"]
        
    # Find all files matching criteria
    for file_path in find_files(
        directory, 
        exclude_dirs=exclude_dirs,
        include_dirs=include_dirs
    ):
        # Skip excluded extensions
        if exclude_extensions and any(file_path.endswith(ext) for ext in exclude_extensions):
            continue
            
        try:
            size = os.path.getsize(file_path)
            file_sizes.append((file_path, size))
        except (OSError, IOError) as e:
            print(f"Error reading {file_path}: {e}", file=sys.stderr)
            
    return file_sizes


def format_size(size_bytes: int|float) -> str:
    """Format file size in human-readable format."""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.2f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.2f} TB"


def main() -> None:
    """Main entry point."""
    parser = setup_basic_parser("Find largest files in a directory")
    parser.add_argument("--exclude", help="Comma-separated list of directories or extensions to exclude")
    parser.add_argument("--include", help="Comma-separated list of directories to include")
    parser.add_argument("--limit", type=int, default=25, help="Number of files to display (default: 25)")
    
    args = parser.parse_args()
    
    if not validate_args(args):
        sys.exit(1)
        
    # Parse include/exclude lists
    excludes = parse_list_arg(args.exclude) if args.exclude else None
    includes = parse_list_arg(args.include) if args.include else None
    
    # Separate directory excludes from extension excludes
    exclude_dirs = []
    exclude_extensions = []
    if excludes:
        for item in excludes:
            if item.startswith('.'):
                exclude_extensions.append(item)
            else:
                exclude_dirs.append(item)
    
    try:
        file_sizes = get_file_sizes(
            args.directory,
            include_dirs=includes,
            exclude_dirs=exclude_dirs,
            exclude_extensions=exclude_extensions
        )
        
        # Sort by size (largest first)
        file_sizes.sort(key=lambda x: x[1], reverse=True)
        
        # Display results
        print(f"Largest {min(args.limit, len(file_sizes))} files in {args.directory}:")
        for i, (file_path, size) in enumerate(file_sizes[:args.limit], 1):
            print(f"{i}. {file_path} - {format_size(size)}")
            
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
