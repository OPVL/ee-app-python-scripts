"""Configuration settings for the codebase."""
import os
from typing import Any

# Default configuration
DEFAULT_CONFIG: dict[str, Any] = {
    "ignore_dirs": [".git", "__pycache__", ".mypy_cache", ".vscode"],
    "python_extensions": [".py"],
    "output_directory": "output",
}


def get_config() -> dict[str, Any]:
    """
    Get configuration with environment variable overrides.
    
    Returns:
        Configuration dictionary
    """
    config = DEFAULT_CONFIG.copy()
    
    # Override from environment variables if present
    if os.environ.get("IGNORE_DIRS"):
        config["ignore_dirs"] = os.environ.get("IGNORE_DIRS", '').split(",")
    
    return config