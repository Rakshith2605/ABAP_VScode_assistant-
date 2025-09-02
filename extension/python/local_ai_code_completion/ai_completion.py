"""
AI Code Completion module
Handles code generation using Groq API
"""
import asyncio
import json
import time
from typing import AsyncGenerator, Optional, Dict, Any
import os

# Conditional import to handle missing dependencies
try:
    import groq
    GROQ_AVAILABLE = True
except ImportError:
    GROQ_AVAILABLE = False
    print("Warning: groq package not available. Please install dependencies.")

try:
    from .config import config
    from .logger import logger
except ImportError as e:
    print(f"Warning: Could not import config or logger: {e}")
    config = None
    logger = None


class AICodeCompletion:
    """Handles AI code completion using Groq API"""
    
    def __init__(self):
        if not GROQ_AVAILABLE:
            print("Error: groq package not available. Please install dependencies.")
            self.model_config = None
            self.is_generating = False
            self.is_aborted = False
            self.client = None
            return

        if config:
            self.model_config = config.get_model_config()
        else:
            self.model_config = None
        self.is_generating = False
        self.is_aborted = False
        self.client = None  # Initialize client lazily
    
    def _get_client(self):
        """Get or initialize the Groq client"""
        if not GROQ_AVAILABLE:
            print("Error: groq package not available. Please install dependencies.")
            return None
            
        if self.client is not None:
            return self.client
        
        # Allow fallback to environment variable if config doesn't provide api_key
        api_key = None
        try:
            api_key = self.model_config.api_key if self.model_config and getattr(self.model_config, 'api_key', None) else os.getenv('GROQ_API_KEY', None)
        except Exception:
            api_key = os.getenv('GROQ_API_KEY', None)

        if not api_key:
            print("No Groq API key provided. Set GROQ_API_KEY environment variable or update config.")
            return None
        
        try:
            # Initialize with minimal parameters to avoid compatibility issues
            self.client = groq.Groq(api_key=api_key)
            return self.client
        except TypeError as e:
            # Handle version compatibility issues
            print(f"Groq client initialization issue: {e}")
            print("Trying alternative initialization...")
            try:
                # Try without any additional parameters
                self.client = groq.Groq(api_key=api_key)
                return self.client
            except Exception as e2:
                print(f"Failed to initialize Groq client: {e2}")
                return None
        except Exception as e:
            print(f"Failed to initialize Groq client: {e}")
            return None
    
    def create_prompt(self, prefix: str, suffix: str) -> str:
        """Create the prompt for code completion"""
        return f"<PRE>{prefix} <SUF>{suffix} <MID>"
    
    def line_count(self, text: str) -> int:
        """Count the number of lines in text"""
        return len(text.split('\n')) - 1
    
    def find_line(self, text: str, end_line: int, start_line: int) -> str:
        """Find the line at the specified position"""
        text_lines = text.split('\n')
        index = end_line - start_line
        return text_lines[index] if index < len(text_lines) else ""
    
    async def generate_code_stream(self, prefix: str, suffix: str) -> AsyncGenerator[str, None]:
        """Generate code using streaming API"""
        if not GROQ_AVAILABLE:
            print("Error: groq package not available. Please install dependencies.")
            return
            
        client = self._get_client()
        if not client:
            print("Groq client not initialized. Please set GROQ_API_KEY environment variable.")
            return
        
        prompt = self.create_prompt(prefix, suffix)
        
        try:
            stream = client.chat.completions.create(
                model=self.model_config.name,
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=self.model_config.temperature,
                top_p=self.model_config.top_p,
                max_tokens=1000,
                stream=True
            )
            
            for chunk in stream:
                if self.is_aborted:
                    print("Code generation aborted")
                    break
                
                if chunk.choices[0].delta.content:
                    content = chunk.choices[0].delta.content
                    # Remove end of sequence token and trailing spaces
                    stripped_content = content.replace("<EOT>", "").rstrip()
                    if stripped_content:
                        yield stripped_content
                        
        except Exception as e:
            print(f"Error during code generation: {e}")
    
    async def generate_code(self, prefix: str, suffix: str) -> str:
        """Generate complete code (non-streaming)"""
        if not GROQ_AVAILABLE:
            print("Error: groq package not available. Please install dependencies.")
            return ""
            
        client = self._get_client()
        if not client:
            print("Groq client not initialized. Please set GROQ_API_KEY environment variable.")
            return ""
        
        prompt = self.create_prompt(prefix, suffix)
        
        try:
            response = client.chat.completions.create(
                model=self.model_config.name,
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=self.model_config.temperature,
                top_p=self.model_config.top_p,
                max_tokens=1000
            )
            
            content = response.choices[0].message.content
            return content.replace("<EOT>", "").rstrip() if content else ""
                
        except Exception as e:
            print(f"Error during code generation: {e}")
            return ""
    
    def abort_generation(self):
        """Abort current generation"""
        self.is_aborted = True
        print("Code generation aborted")
    
    def reset_state(self):
        """Reset generation state"""
        self.is_generating = False
        self.is_aborted = False
    
    async def generate_code_with_prompt(self, prompt: str) -> str:
        """Generate code using a custom prompt"""
        if not GROQ_AVAILABLE:
            print("Error: groq package not available. Please install dependencies.")
            return ""
            
        client = self._get_client()
        if not client:
            print("Groq client not initialized. Please set GROQ_API_KEY environment variable.")
            return ""

        try:
            response = client.chat.completions.create(
                model=self.model_config.name,
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=self.model_config.temperature,
                top_p=self.model_config.top_p,
                max_tokens=1000
            )

            content = response.choices[0].message.content
            return content.replace("<EOT>", "").rstrip() if content else ""

        except Exception as e:
            print(f"Error during code generation: {e}")
            return ""


# Global AI completion instance
ai_completion = AICodeCompletion() 