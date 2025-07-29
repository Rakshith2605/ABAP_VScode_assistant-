"""
Configuration module for Local AI Code Completion
"""
import os
from typing import Optional
from pydantic import BaseModel, Field
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class ModelConfig(BaseModel):
    """Configuration for the AI model"""
    name: str = Field(default="qwen/qwen3-32b", description="Groq model name to use")
    temperature: float = Field(default=0.3, ge=0, le=2, description="Temperature for generation")
    top_p: float = Field(default=0.3, ge=0, le=1, description="Top-p for generation")
    timeout: int = Field(default=15000, description="Timeout in milliseconds")
    api_key: str = Field(default="", description="Groq API key")
    base_url: str = Field(default="https://api.groq.com", description="Groq API base URL")


class Config:
    """Main configuration class"""
    
    def __init__(self):
        self.model = ModelConfig(
            name=os.getenv("LACC_MODEL_NAME", "qwen/qwen3-32b"),
            temperature=float(os.getenv("LACC_TEMPERATURE", "0.3")),
            top_p=float(os.getenv("LACC_TOP_P", "0.3")),
            timeout=int(os.getenv("LACC_TIMEOUT", "15000")),
            api_key=os.getenv("GROQ_API_KEY", ""),
            base_url=os.getenv("GROQ_BASE_URL", "https://api.groq.com")
        )
    
    def get_model_config(self) -> ModelConfig:
        """Get the model configuration"""
        return self.model


# Global configuration instance
config = Config() 