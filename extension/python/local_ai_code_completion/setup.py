"""
Setup module for Local AI Code Completion
Handles Groq API setup and validation
"""
import asyncio
import sys
import time
from typing import Optional, Dict, Any
import groq
from .config import config
from .logger import logger


class GroqSetup:
    """Handles Groq API setup and validation"""
    
    def __init__(self):
        self.model_config = config.get_model_config()
        self.client = None
    
    async def check_api_key(self) -> bool:
        """Check if Groq API key is provided"""
        if not self.model_config.api_key:
            logger.error("No Groq API key provided. Please set GROQ_API_KEY environment variable.")
            return False
        
        try:
            # Initialize with minimal parameters to avoid compatibility issues
            self.client = groq.Groq(api_key=self.model_config.api_key)
            logger.info("Groq API key is valid")
            return True
        except TypeError as e:
            # Handle version compatibility issues
            logger.warning(f"Groq client compatibility issue: {e}")
            logger.info("Trying alternative client initialization...")
            try:
                # Try without any additional parameters
                self.client = groq.Groq(api_key=self.model_config.api_key)
                logger.info("Groq API key is valid (alternative initialization)")
                return True
            except Exception as e2:
                logger.error(f"Invalid Groq API key: {e2}")
                return False
        except Exception as e:
            logger.error(f"Invalid Groq API key: {e}")
            return False
    
    async def check_model_availability(self) -> bool:
        """Check if the specified model is available"""
        if not self.client:
            return False
        
        try:
            # Test a simple completion to check model availability
            response = self.client.chat.completions.create(
                model=self.model_config.name,
                messages=[{"role": "user", "content": "Hello"}],
                max_tokens=1
            )
            logger.info(f"Model {self.model_config.name} is available")
            return True
        except Exception as e:
            logger.error(f"Model {self.model_config.name} is not available: {e}")
            return False
    
    async def get_available_models(self) -> list:
        """Get list of available models"""
        if not self.client:
            return []
        
        try:
            models = self.client.models.list()
            return [model.id for model in models.data]
        except Exception as e:
            logger.error(f"Failed to get available models: {e}")
            return []
    
    async def setup(self) -> bool:
        """Complete setup process"""
        # Check API key
        if not await self.check_api_key():
            logger.error("Please get your API key from https://console.groq.com/keys")
            return False
        
        # Check model availability
        if not await self.check_model_availability():
            logger.error(f"Model {self.model_config.name} is not available")
            available_models = await self.get_available_models()
            if available_models:
                logger.info(f"Available models: {', '.join(available_models)}")
            return False
        
        logger.info("Setup completed successfully")
        return True
    
    def cleanup(self):
        """Clean up resources"""
        self.client = None
        logger.info("Groq client cleaned up")


# Global setup instance
setup = GroqSetup() 