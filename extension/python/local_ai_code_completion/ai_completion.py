"""
AI Code Completion module
Handles code generation using Groq API
"""
import asyncio
import json
import time
from typing import AsyncGenerator, Optional, Dict, Any
import groq
from .config import config
from .logger import logger


class AICodeCompletion:
    """Handles AI code completion using Groq API"""
    
    def __init__(self):
        self.model_config = config.get_model_config()
        self.is_generating = False
        self.is_aborted = False
        self.client = None  # Initialize client lazily
    
    def _get_client(self):
        """Get or initialize the Groq client"""
        if self.client is not None:
            return self.client
        
        if not self.model_config.api_key:
            logger.warning("No Groq API key provided. Set GROQ_API_KEY environment variable.")
            return None
        
        try:
            # Initialize with minimal parameters to avoid compatibility issues
            self.client = groq.Groq(api_key=self.model_config.api_key)
            return self.client
        except TypeError as e:
            # Handle version compatibility issues
            logger.warning(f"Groq client initialization issue: {e}")
            logger.info("Trying alternative initialization...")
            try:
                # Try without any additional parameters
                self.client = groq.Groq(api_key=self.model_config.api_key)
                return self.client
            except Exception as e2:
                logger.error(f"Failed to initialize Groq client: {e2}")
                return None
        except Exception as e:
            logger.error(f"Failed to initialize Groq client: {e}")
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
        client = self._get_client()
        if not client:
            logger.error("Groq client not initialized. Please set GROQ_API_KEY environment variable.")
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
                    logger.info("Code generation aborted")
                    break
                
                if chunk.choices[0].delta.content:
                    content = chunk.choices[0].delta.content
                    # Remove end of sequence token and trailing spaces
                    stripped_content = content.replace("<EOT>", "").rstrip()
                    if stripped_content:
                        yield stripped_content
                        
        except Exception as e:
            logger.error(f"Error during code generation: {e}")
    
    async def generate_code(self, prefix: str, suffix: str) -> str:
        """Generate complete code (non-streaming)"""
        client = self._get_client()
        if not client:
            logger.error("Groq client not initialized. Please set GROQ_API_KEY environment variable.")
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
            logger.error(f"Error during code generation: {e}")
            return ""
    
    def abort_generation(self):
        """Abort current generation"""
        self.is_aborted = True
        logger.info("Code generation aborted")
    
    def reset_state(self):
        """Reset generation state"""
        self.is_generating = False
        self.is_aborted = False
    
    async def generate_code_with_prompt(self, prompt: str) -> str:
        """Generate code using a custom prompt"""
        client = self._get_client()
        if not client:
            logger.error("Groq client not initialized. Please set GROQ_API_KEY environment variable.")
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
            logger.error(f"Error during code generation: {e}")
            return ""


# Global AI completion instance
ai_completion = AICodeCompletion() 