"""
Local AI Code Completion - Python Version

A Python implementation of the Local AI Code Completion tool, providing AI-assisted 
code completion that runs entirely on your local machine using Ollama.
"""

__version__ = "1.0.0"
__author__ = "Python Migration"
__email__ = "python@example.com"

from .config import config
from .logger import logger
from .setup import setup
from .ai_completion import ai_completion

__all__ = ["config", "logger", "setup", "ai_completion"] 