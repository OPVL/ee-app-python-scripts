"""Common CLI argument parsing utilities."""

import argparse


def setup_basic_parser(description: str) -> argparse.ArgumentParser:
    """Create a basic argument parser with common options."""
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument("directory", help="Target directory to analyze")
    return parser


def validate_args(args: argparse.Namespace) -> bool:
    """Validate common argument patterns."""
    if not hasattr(args, "directory") or not args.directory:
        print("Error: Directory argument is required")
        return False
    return True


def parse_list_arg(arg_value: str) -> list[str]:
    """Parse comma-separated argument into list."""
    return arg_value.split(",") if arg_value else []
