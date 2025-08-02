"""
LLM Client - Unified interface for Mac Studio and Google Gemini LLMs
"""

import os
import logging
from typing import Optional, Dict, Any
from enum import Enum
import structlog

# LLM imports
from browser_use.llm.openai.chat import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI

logger = structlog.get_logger(__name__)

class LLMProvider(Enum):
    MAC_STUDIO = "mac_studio"
    GEMINI = "gemini"

class ModelConfig:
    """Configuration for different LLM models"""
    
    # Mac Studio models
    MAC_STUDIO_MODELS = {
        "llama4:scout": {
            "description": "Best for browser navigation and search tasks",
            "recommended_temperature": 0.3,
            "use_case": "navigation"
        },
        "maverick": {
            "description": "Best for complex reasoning and analysis",
            "recommended_temperature": 0.7,
            "use_case": "analysis"
        },
        "deepseek-r1": {
            "description": "Good for logical tasks and reasoning",
            "recommended_temperature": 0.5,
            "use_case": "reasoning"
        },
        "qwen3:32b": {
            "description": "Large context, detailed extraction",
            "recommended_temperature": 0.4,
            "use_case": "extraction"
        },
        "qwen25": {
            "description": "Balanced performance",
            "recommended_temperature": 0.6,
            "use_case": "general"
        }
    }
    
    # Gemini models
    GEMINI_MODELS = {
        "gemini-1.5-flash": {
            "description": "Fast and efficient for most tasks",
            "recommended_temperature": 0.7,
            "use_case": "general"
        },
        "gemini-1.5-pro": {
            "description": "More capable but slower",
            "recommended_temperature": 0.7,
            "use_case": "complex"
        }
    }

class LLMClient:
    """Unified LLM client supporting both Mac Studio and Gemini"""
    
    def __init__(self, provider: LLMProvider = LLMProvider.MAC_STUDIO, model: Optional[str] = None):
        self.provider = provider
        self.model = model or self._get_default_model()
        self.llm = None
        self._initialize_llm()
    
    def _get_default_model(self) -> str:
        """Get default model for the provider"""
        if self.provider == LLMProvider.MAC_STUDIO:
            return "llama4:scout"  # Best for browser automation
        else:
            return "gemini-1.5-flash"
    
    def _initialize_llm(self):
        """Initialize the LLM based on provider and model"""
        try:
            if self.provider == LLMProvider.MAC_STUDIO:
                self._initialize_mac_studio()
            elif self.provider == LLMProvider.GEMINI:
                self._initialize_gemini()
            else:
                raise ValueError(f"Unsupported provider: {self.provider}")
                
            logger.info("LLM client initialized", provider=self.provider.value, model=self.model)
            
        except Exception as e:
            logger.error("Failed to initialize LLM", provider=self.provider.value, model=self.model, error=str(e))
            raise
    
    def _initialize_mac_studio(self):
        """Initialize Mac Studio LLM client"""
        base_url = "https://matiass-mac-studio.tail174e9b.ts.net/v1"
        
        # Get model config
        model_config = ModelConfig.MAC_STUDIO_MODELS.get(self.model, {})
        temperature = model_config.get("recommended_temperature", 0.7)
        
        self.llm = ChatOpenAI(
            base_url=base_url,
            api_key="ollama",  # Placeholder - Ollama ignores this
            model=self.model,
            temperature=temperature,
        )
    
    def _initialize_gemini(self):
        """Initialize Google Gemini LLM client"""
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            raise ValueError("GOOGLE_API_KEY environment variable required for Gemini")
        
        # Get model config
        model_config = ModelConfig.GEMINI_MODELS.get(self.model, {})
        temperature = model_config.get("recommended_temperature", 0.7)
        
        self.llm = ChatGoogleGenerativeAI(
            model=self.model,
            temperature=temperature,
            google_api_key=api_key
        )
    
    def get_llm(self):
        """Get the initialized LLM instance"""
        if not self.llm:
            raise RuntimeError("LLM not initialized")
        return self.llm
    
    def switch_model(self, new_model: str):
        """Switch to a different model within the same provider"""
        logger.info("Switching model", old_model=self.model, new_model=new_model)
        self.model = new_model
        self._initialize_llm()
    
    def get_model_info(self) -> Dict[str, Any]:
        """Get information about the current model"""
        if self.provider == LLMProvider.MAC_STUDIO:
            model_config = ModelConfig.MAC_STUDIO_MODELS.get(self.model, {})
        else:
            model_config = ModelConfig.GEMINI_MODELS.get(self.model, {})
        
        return {
            "provider": self.provider.value,
            "model": self.model,
            "description": model_config.get("description", "Unknown model"),
            "use_case": model_config.get("use_case", "general"),
            "temperature": model_config.get("recommended_temperature", 0.7)
        }
    
    @classmethod
    def create_for_task(cls, task_type: str = "navigation") -> "LLMClient":
        """Create LLM client optimized for specific task type"""
        if task_type == "navigation":
            return cls(LLMProvider.MAC_STUDIO, "llama4:scout")
        elif task_type == "analysis":
            return cls(LLMProvider.MAC_STUDIO, "maverick")
        elif task_type == "reasoning":
            return cls(LLMProvider.MAC_STUDIO, "deepseek-r1")
        elif task_type == "extraction":
            return cls(LLMProvider.MAC_STUDIO, "qwen3:32b")
        else:
            # Default to general purpose
            return cls(LLMProvider.MAC_STUDIO, "llama4:scout")
    
    async def test_connection(self) -> Dict[str, Any]:
        """Test LLM connection and get status"""
        try:
            # Simple test message
            if hasattr(self.llm, 'ainvoke'):
                response = await self.llm.ainvoke("Hello")
            else:
                response = self.llm.invoke("Hello")
            
            return {
                "status": "connected",
                "provider": self.provider.value,
                "model": self.model,
                "response_preview": str(response)[:100]
            }
        except Exception as e:
            return {
                "status": "failed",
                "provider": self.provider.value,
                "model": self.model,
                "error": str(e)
            }

# Factory functions for easy creation
def create_mac_studio_client(model: str = "llama4:scout") -> LLMClient:
    """Create Mac Studio LLM client"""
    return LLMClient(LLMProvider.MAC_STUDIO, model)

def create_gemini_client(model: str = "gemini-1.5-flash") -> LLMClient:
    """Create Gemini LLM client"""
    return LLMClient(LLMProvider.GEMINI, model)