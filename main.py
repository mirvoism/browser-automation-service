"""
Browser Automation Service - Main Entry Point
"""

import os
import asyncio
import logging
from pathlib import Path
import structlog
import uvicorn
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure structured logging
structlog.configure(
    processors=[
        structlog.stdlib.filter_by_level,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.TimeStamper(fmt="ISO"),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.processors.UnicodeDecoder(),
        structlog.processors.JSONRenderer()
    ],
    context_class=dict,
    logger_factory=structlog.stdlib.LoggerFactory(),
    wrapper_class=structlog.stdlib.BoundLogger,
    cache_logger_on_first_use=True,
)

logger = structlog.get_logger(__name__)

def get_config():
    """Get service configuration from environment variables"""
    return {
        "host": os.getenv("HOST", "0.0.0.0"),
        "port": int(os.getenv("PORT", "8000")),
        "reload": os.getenv("RELOAD", "true").lower() == "true",
        "log_level": os.getenv("LOG_LEVEL", "info"),
        "workers": int(os.getenv("WORKERS", "1")),
        
        # LLM Configuration
        "default_llm_provider": os.getenv("DEFAULT_LLM_PROVIDER", "mac_studio"),
        "default_llm_model": os.getenv("DEFAULT_LLM_MODEL", "llama4:scout"),
        "google_api_key": os.getenv("GOOGLE_API_KEY"),
        "mac_studio_url": os.getenv("MAC_STUDIO_URL", "https://matiass-mac-studio.tail174e9b.ts.net/v1"),
        
        # Browser Configuration  
        "default_browser_profile": os.getenv("DEFAULT_BROWSER_PROFILE", "anti_bot"),
        "max_concurrent_tasks": int(os.getenv("MAX_CONCURRENT_TASKS", "3")),
        
        # Service Configuration
        "enable_cors": os.getenv("ENABLE_CORS", "true").lower() == "true",
        "cors_origins": os.getenv("CORS_ORIGINS", "*").split(","),
    }

def validate_config(config):
    """Validate configuration and check requirements"""
    issues = []
    
    # Check LLM configuration
    if config["default_llm_provider"] == "gemini" and not config["google_api_key"]:
        issues.append("GOOGLE_API_KEY required for Gemini provider")
    
    # Check port availability
    if not (1000 <= config["port"] <= 65535):
        issues.append(f"Invalid port: {config['port']}")
    
    if issues:
        for issue in issues:
            logger.error("Configuration issue", issue=issue)
        raise ValueError(f"Configuration errors: {', '.join(issues)}")
    
    logger.info("Configuration validated", 
                llm_provider=config["default_llm_provider"],
                port=config["port"])

async def check_dependencies():
    """Check that required dependencies are available"""
    try:
        # Test imports
        import playwright
        import browser_use
        import fastapi
        
        # Test browser installation
        from playwright.async_api import async_playwright
        playwright_instance = await async_playwright().start()
        browser = await playwright_instance.chromium.launch(headless=True)
        await browser.close()
        await playwright_instance.stop()
        
        logger.info("Dependencies check passed")
        
    except ImportError as e:
        logger.error("Missing dependency", error=str(e))
        raise RuntimeError(f"Missing dependency: {e}")
    except Exception as e:
        logger.error("Browser check failed", error=str(e))
        raise RuntimeError(f"Browser setup failed: {e}")

def main():
    """Main entry point"""
    try:
        print("🚀 Starting Browser Automation Service...")
        
        # Get and validate configuration
        config = get_config()
        validate_config(config)
        
        # Check dependencies
        asyncio.run(check_dependencies())
        
        # Import the FastAPI app
        from service.api_server import app
        
        # Configure task queue limits
        from service.task_queue import task_queue
        task_queue.max_concurrent_tasks = config["max_concurrent_tasks"]
        
        print(f"🌐 Starting server on http://{config['host']}:{config['port']}")
        print(f"🧠 Default LLM: {config['default_llm_provider']} ({config['default_llm_model']})")
        print(f"🔧 Max concurrent tasks: {config['max_concurrent_tasks']}")
        print(f"📡 WebSocket endpoint: ws://{config['host']}:{config['port']}/ws/updates")
        print()
        
        # Start the server
        uvicorn.run(
            "service.api_server:app",
            host=config["host"],
            port=config["port"],
            reload=config["reload"],
            log_level=config["log_level"],
            workers=config["workers"] if not config["reload"] else 1
        )
        
    except KeyboardInterrupt:
        print("\n👋 Shutting down gracefully...")
    except Exception as e:
        logger.error("Service startup failed", error=str(e))
        print(f"❌ Failed to start service: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())