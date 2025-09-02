"""
Logger module for Local AI Code Completion
"""
import logging
import sys
from typing import Optional

# Try to import rich for pretty logging; fall back to basic logging if unavailable
try:
    from rich.console import Console
    from rich.logging import RichHandler
    RICH_AVAILABLE = True
except Exception:
    Console = None
    RichHandler = None
    RICH_AVAILABLE = False


class Logger:
    """Logger class for the application"""

    def __init__(self, name: str = "Local AI Completion"):
        self.name = name
        # Initialize console and logger instance variables
        self.console = Console() if RICH_AVAILABLE else None
        self.logger = logging.getLogger(name)
        self._setup_logger()

    def _setup_logger(self):
        """Setup the logger with rich formatting"""
        self.logger.setLevel(logging.DEBUG)

        if RICH_AVAILABLE and RichHandler is not None:
            try:
                rich_handler = RichHandler(
                    console=self.console,
                    show_time=True,
                    show_path=False,
                    markup=True,
                    rich_tracebacks=True
                )
                rich_handler.setLevel(logging.DEBUG)

                formatter = logging.Formatter("%(message)s", datefmt="[%X]")
                rich_handler.setFormatter(formatter)
                self.logger.addHandler(rich_handler)
                return
            except Exception:
                # Fall back to basic handler if rich handler setup fails
                pass

        # Fallback to basic console logging
        handler = logging.StreamHandler(sys.stdout)
        handler.setLevel(logging.DEBUG)
        formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)

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
        for handler in list(self.logger.handlers):
            try:
                self.logger.removeHandler(handler)
                handler.close()
            except Exception:
                pass


# Global logger instance
logger = Logger() 