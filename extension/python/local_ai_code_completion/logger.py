"""
Logger module for Local AI Code Completion
"""
import logging
import sys
from typing import Optional
from rich.console import Console
from rich.logging import RichHandler


class Logger:
    """Logger class for the application"""
    
    def __init__(self, name: str = "Local AI Completion"):
        self.name = name
        self.console = Console()
        self.logger = logging.getLogger(name)
        self._setup_logger()
    
    def _setup_logger(self):
        """Setup the logger with rich formatting"""
        self.logger.setLevel(logging.DEBUG)
        
        # Create rich handler
        rich_handler = RichHandler(
            console=self.console,
            show_time=True,
            show_path=False,
            markup=True,
            rich_tracebacks=True
        )
        rich_handler.setLevel(logging.DEBUG)
        
        # Create formatter
        formatter = logging.Formatter(
            "%(message)s",
            datefmt="[%X]"
        )
        rich_handler.setFormatter(formatter)
        
        # Add handler to logger
        self.logger.addHandler(rich_handler)
    
    def info(self, message: str, *args, **kwargs):
        """Log info message"""
        self.logger.info(message, *args, **kwargs)
    
    def debug(self, message: str, *args, **kwargs):
        """Log debug message"""
        self.logger.debug(message, *args, **kwargs)
    
    def warning(self, message: str, *args, **kwargs):
        """Log warning message"""
        self.logger.warning(message, *args, **kwargs)
    
    def error(self, message: str, *args, **kwargs):
        """Log error message"""
        self.logger.error(message, *args, **kwargs)
    
    def critical(self, message: str, *args, **kwargs):
        """Log critical message"""
        self.logger.critical(message, *args, **kwargs)
    
    def dispose(self):
        """Clean up logger resources"""
        for handler in self.logger.handlers[:]:
            self.logger.removeHandler(handler)
            handler.close()


# Global logger instance
logger = Logger() 