#!/usr/bin/env python3
"""
Tool to analyze Dart freezed files in a codebase.

This script counts files and lines of code for freezed.dart, cubit, and aem files.
Results are stored in JSON files under the report/<normalized_file_path>/ directory.
"""
import sys

from utils.cli import setup_basic_parser, validate_args
from utils.file import count_lines, find_files
import json
from pathlib import Path


def gather_freezed_files_info(directory: str) -> tuple[list[str], int, list[str], int, list[str], int]:
    """
    Gather information about freezed files in the given directory.

    Args:
        directory: Root directory to search

    Returns:
        Tuple of (freezed_files, freezed_lines, cubit_files, cubit_lines, aem_files, aem_lines)
    """
    # Stats counters
    total_files_freezed = []
    total_lines_freezed = 0
    total_files_cubit = []
    total_lines_cubit = 0
    total_files_aem = []
    total_lines_aem = 0

    # Find and count freezed.dart files
    for file_path in find_files(directory, file_extension=".freezed.dart"):
        total_files_freezed.append(file_path)
        total_lines_freezed += count_lines(file_path)

    # Find and count cubit files
    for file_path in find_files(directory, file_pattern="cubit", file_extension=".freezed.dart"):
        total_files_cubit.append(file_path)
        total_lines_cubit += count_lines(file_path)

    # Find and count aem files
    for file_path in find_files(directory, file_pattern="aem", file_extension=".freezed.dart"):
        total_files_aem.append(file_path)
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
        print(f"Total number of .freezed.dart files: {len(total_files_freezed)}")
        print(
            f"Total number of lines of code in .freezed.dart files: {total_lines_freezed}"
        )
        print(f"Total number of cubit files: {len(total_files_cubit)}")
        print(f"Total number of lines of code in cubit files: {total_lines_cubit}")
        print(f"Total number of aem files: {len(total_files_aem)}")
        print(f"Total number of lines of code in aem files: {total_lines_aem}")    

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

    def write_to_json_file(data: dict, file_path: str) -> None:
        """
        Write the given data to a JSON file.

        Args:
            data: Data to write
            file_path: Path to the JSON file
        """
        with open(file_path, "w") as json_file:
            json.dump(data, json_file, indent=4)

    # Create report directory
    report_dir = Path("report")
    report_dir.mkdir(exist_ok=True)

    # Normalize directory path to create a subdirectory
    norm_dir = Path(args.directory).name
    report_subdir = report_dir / norm_dir
    report_subdir.mkdir(exist_ok=True, parents=True)

    # Create data structures for each file type
    freezed_data = {
        "files": total_files_freezed,
        "lines": total_lines_freezed
    }

    cubit_data = {
        "files": total_files_cubit,
        "lines": total_lines_cubit
    }

    aem_data = {
        "files": total_files_aem,
        "lines": total_lines_aem
    }

    # Write data to JSON files
    write_to_json_file(freezed_data, str(report_subdir / "freezed_stats.json"))
    write_to_json_file(cubit_data, str(report_subdir / "cubit_stats.json"))
    write_to_json_file(aem_data, str(report_subdir / "aem_stats.json"))


if __name__ == "__main__":
    main()
