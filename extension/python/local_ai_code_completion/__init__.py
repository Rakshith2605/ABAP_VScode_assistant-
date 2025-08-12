"""
Local AI Code Completion - Python Version

A Python implementation of the Local AI Code Completion tool, providing AI-assisted 
code completion using Groq API.
"""

__version__ = "1.0.0"
__author__ = "Python Migration"
__email__ = "python@example.com"

# Import with error handling for missing dependencies
try:
    from .config import config
    from .logger import logger
    from .setup import setup
    from .ai_completion import ai_completion
    
    __all__ = ["config", "logger", "setup", "ai_completion"]
except ImportError as e:
    # If dependencies are missing, create placeholder objects
    print(f"Warning: Some dependencies are missing: {e}")
    print("Please run the setup command to install dependencies.")
    
    # Create placeholder objects
    class PlaceholderConfig:
        def __init__(self):
            self.model = type('obj', (object,), {
                'name': 'llama-3.3-70b-versatile',
                'temperature': 0.3,
                'top_p': 0.3,
                'timeout': 15000,
                'api_key': 'Not set',
                'base_url': 'https://api.groq.com'
            })()
    
    config = PlaceholderConfig()
    logger = None
    setup = None
    ai_completion = None
    
    __all__ = ["config", "logger", "setup", "ai_completion"] 