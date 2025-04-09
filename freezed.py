#!/usr/bin/env python3
"""
Tool to analyze Dart freezed files in a codebase.

This script counts files and lines of code for freezed.dart, cubit, and aem files.
"""
import os
import sys
from typing import Tuple

from utils.cli import setup_basic_parser, validate_args
from utils.file import find_files, count_lines


def gather_freezed_files_info(directory: str) -> Tuple[int, int, int, int, int, int]:
    """
    Gather information about freezed files in the given directory.
    
    Args:
        directory: Root directory to search
        
    Returns:
        Tuple of (freezed_files, freezed_lines, cubit_files, cubit_lines, aem_files, aem_lines)
    """
    # Stats counters
    total_files_freezed = 0
    total_lines_freezed = 0
    total_files_cubit = 0
    total_lines_cubit = 0
    total_files_aem = 0
    total_lines_aem = 0
    
    # Find and count freezed.dart files
    for file_path in find_files(directory, file_extension=".freezed.dart"):
        total_files_freezed += 1
        total_lines_freezed += count_lines(file_path)
    
    # Find and count cubit files
    for file_path in find_files(directory, file_extension="_cubit.dart"):
        total_files_cubit += 1
        total_lines_cubit += count_lines(file_path)
    
    # Find and count aem files
    for file_path in find_files(directory, file_extension="_aem.dart"):
        total_files_aem += 1
        total_lines_aem += count_lines(file_path)
        
    return (
        total_files_freezed,
        total_lines_freezed,
        total_files_cubit,
        total_lines_cubit,
        total_files_aem,
        total_lines_aem,
    )


def main() -> None:
    """Main entry point."""
    parser = setup_basic_parser("Analyze Dart freezed files in a codebase")
    args = parser.parse_args()
    
    if not validate_args(args):
        sys.exit(1)
    
    try:
        stats = gather_freezed_files_info(args.directory)
        
        # Unpack stats
        (
            total_files_freezed,
            total_lines_freezed,
            total_files_cubit,
            total_lines_cubit,
            total_files_aem,
            total_lines_aem,
        ) = stats
        
        # Display results
        print(f"Total number of .freezed.dart files: {total_files_freezed}")
        print(f"Total number of lines of code in .freezed.dart files: {total_lines_freezed}")
        print(f"Total number of cubit files: {total_files_cubit}")
        print(f"Total number of lines of code in cubit files: {total_lines_cubit}")
        print(f"Total number of aem files: {total_files_aem}")
        print(f"Total number of lines of code in aem files: {total_lines_aem}")
        
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
