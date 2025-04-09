#!/usr/bin/env python3
"""
Tool to analyze and report on Dart lint rules across a codebase.

This script identifies all analysis_options.yaml files in a directory,
compares their lint rules to a root configuration, and reports on duplications.
"""
import json
import logging
import os
import sys
from typing import Any

import yaml

from utils.cli import setup_basic_parser, validate_args
from utils.file import find_files, read_file

_LOGGER = logging.getLogger(__name__)


def find_analysis_options_files(directory: str) -> list[str]:
    """Find all analysis_options.yaml files in directory."""
    return list(find_files(directory, file_pattern="analysis_options.yaml"))


def print_tree(files: list[str]) -> None:
    """Print the directory tree of the given files."""
    for file in files:
        print(f"- {file}")


def load_yaml_rules(file_path: str) -> dict[str, Any]:
    """Load YAML file and convert it to a dictionary."""
    try:
        with open(file_path, "r") as f:
            return yaml.safe_load(f)
    except Exception as e:
        _LOGGER.error(f"Error loading {file_path}: {e}")
        return {}


def get_lint_rules(rules: dict[str, Any]) -> dict[str, Any]:
    """Extract lint rules from loaded YAML."""
    try:
        return rules.get("linter", {}).get("rules", {}) or {}
    except (AttributeError, KeyError):
        return {}


def analyze_lint_rules(directory: str, delete_duplicates: bool = False) -> tuple[int, int, int]:
    """
    Analyze lint rules across the codebase.
    
    Args:
        directory: Root directory to analyze
        delete_duplicates: Whether to delete files with duplicate rules
        
    Returns:
        Tuple of (empty_files, no_lint_rules, no_unique_lint_rules)
    """
    files = find_analysis_options_files(directory)
    if not files:
        _LOGGER.error(f"No analysis_options.yaml files found in {directory}")
        return 0, 0, 0
        
    print_tree(files)
    print(f"Gathered {len(files)} analysis_options.yaml")

    # Use first file as root
    root_file = files.pop(0)
    root_rules = load_yaml_rules(root_file)
    root_lint_rules = get_lint_rules(root_rules)

    # Export root rules for reference
    with open("root.json", "w") as f:
        json.dump(root_rules, f, indent=2)

    # Stats counters
    empty = 0
    no_lint_rules = 0
    no_unique_lint_rules = 0

    # Process each child file
    for child_path in files:
        rules_filename = child_path.replace("./", "").replace("/", "-")

        try:
            rules = load_yaml_rules(child_path)
            if not rules:
                _LOGGER.error(f"Analysis file is empty: {child_path}")
                empty += 1
                if delete_duplicates:
                    os.remove(child_path)
                continue
        except Exception as e:
            _LOGGER.error(f"Analyzing ({child_path}) failed: {e}")
            empty += 1
            if delete_duplicates:
                os.remove(child_path)
            continue

        lint_rules = get_lint_rules(rules)
        if not lint_rules:
            _LOGGER.warning(f"{child_path} has no lint rules")
            no_lint_rules += 1
            if delete_duplicates:
                os.remove(child_path)
            continue

        # Find duplicate rules
        duplicate_rules = []
        for rule, value in lint_rules.items():
            if rule in root_lint_rules and root_lint_rules[rule] == value:
                _LOGGER.debug(f"Found duplicate rule in {child_path}: {rule}:{value}")
                duplicate_rules.append(rule)

        # Remove duplicates from the child's rules
        for dupe in duplicate_rules:
            lint_rules.pop(dupe)

        # Check if any unique rules remain
        if len(lint_rules) < 1:
            _LOGGER.info(f"No unique rules found in {child_path}")
            no_unique_lint_rules += 1
            if delete_duplicates:
                os.remove(child_path)

    return empty, no_lint_rules, no_unique_lint_rules


def main() -> None:
    """Main entry point."""
    parser = setup_basic_parser("Analyze Dart lint rules across a codebase")
    parser.add_argument("--delete-duplicates", action="store_true", 
                       help="Delete files with no unique rules")
    parser.add_argument("--verbose", "-v", action="store_true",
                       help="Enable verbose logging")
    
    args = parser.parse_args()
    
    if not validate_args(args):
        sys.exit(1)
        
    # Setup logging
    log_level = logging.DEBUG if args.verbose else logging.INFO
    logging.basicConfig(level=log_level, 
                       format='%(levelname)s: %(message)s')
    
    try:
        empty, no_lint_rules, no_unique_lint_rules = analyze_lint_rules(
            args.directory, args.delete_duplicates
        )
        
        total_files = empty + no_lint_rules + no_unique_lint_rules
        
        print(f"Found {empty} empty analysis files")
        if total_files > 0:
            print(f"{(empty / total_files) * 100:.1f}% of all analysis files")
        
        print(f"Found {no_lint_rules} analysis files with no lint rules")
        if total_files > 0:
            print(f"{(no_lint_rules / total_files) * 100:.1f}% of all collected analysis files")
        
        print(f"{no_unique_lint_rules} files contained no unique lint rules")
        if total_files > 0:
            print(f"{(no_unique_lint_rules / total_files) * 100:.1f}% of all collected analysis files")
            
    except Exception as e:
        _LOGGER.error(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
