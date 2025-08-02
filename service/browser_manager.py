"""
Browser Manager - Handles Chrome instance management and browser profiles
"""

import asyncio
import logging
from typing import Optional, Dict, Any
from playwright.async_api import async_playwright, Browser, BrowserContext, Page
import structlog

logger = structlog.get_logger(__name__)

class BrowserProfile:
    """Browser configuration profile for different use cases"""
    
    STANDARD = {
        "viewport": {"width": 1280, "height": 720},
        "user_agent": None,  # Use default
        "extensions": [],
        "disable_web_security": False,
        "headless": False
    }
    
    ANTI_BOT = {
        "viewport": {"width": 1280, "height": 720},
        "user_agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "extensions": [],  # No extensions for stealth
        "disable_web_security": False,
        "headless": False,  # Visible for human-like behavior
        "extra_args": [
            "--no-first-run",
            "--disable-blink-features=AutomationControlled",
            "--disable-features=VizDisplayCompositor"
        ]
    }

class BrowserManager:
    """Manages Chrome browser instances for the automation service"""
    
    def __init__(self):
        self.playwright = None
        self.browser: Optional[Browser] = None
        self.context: Optional[BrowserContext] = None
        self.page: Optional[Page] = None
        self.is_running = False
        
    async def start(self, profile: str = "anti_bot") -> None:
        """Start browser instance with specified profile"""
        try:
            logger.info("Starting browser manager", profile=profile)
            
            # Get profile configuration
            config = getattr(BrowserProfile, profile.upper(), BrowserProfile.ANTI_BOT)
            
            # Initialize Playwright
            self.playwright = await async_playwright().start()
            
            # Launch browser
            launch_args = {
                "headless": config.get("headless", False),
                "viewport": config.get("viewport"),
            }
            
            # Add extra arguments for anti-bot profile
            if "extra_args" in config:
                launch_args["args"] = config["extra_args"]
                
            self.browser = await self.playwright.chromium.launch(**launch_args)
            
            # Create context with profile settings
            context_args = {}
            if config.get("user_agent"):
                context_args["user_agent"] = config["user_agent"]
                
            self.context = await self.browser.new_context(**context_args)
            
            # Create initial page
            self.page = await self.context.new_page()
            
            self.is_running = True
            logger.info("Browser manager started successfully")
            
        except Exception as e:
            logger.error("Failed to start browser manager", error=str(e))
            await self.stop()
            raise
    
    async def stop(self) -> None:
        """Stop browser instance and cleanup"""
        try:
            logger.info("Stopping browser manager")
            
            if self.page:
                await self.page.close()
                self.page = None
                
            if self.context:
                await self.context.close()
                self.context = None
                
            if self.browser:
                await self.browser.close()
                self.browser = None
                
            if self.playwright:
                await self.playwright.stop()
                self.playwright = None
                
            self.is_running = False
            logger.info("Browser manager stopped")
            
        except Exception as e:
            logger.error("Error stopping browser manager", error=str(e))
    
    async def get_page(self) -> Page:
        """Get the current page instance"""
        if not self.is_running or not self.page:
            raise RuntimeError("Browser manager not running. Call start() first.")
        return self.page
    
    async def new_page(self) -> Page:
        """Create a new page in the current context"""
        if not self.is_running or not self.context:
            raise RuntimeError("Browser manager not running. Call start() first.")
            
        self.page = await self.context.new_page()
        return self.page
    
    async def screenshot(self, path: Optional[str] = None) -> bytes:
        """Take screenshot of current page"""
        if not self.page:
            raise RuntimeError("No active page")
            
        screenshot_args = {"full_page": True}
        if path:
            screenshot_args["path"] = path
            
        return await self.page.screenshot(**screenshot_args)
    
    async def get_status(self) -> Dict[str, Any]:
        """Get browser manager status"""
        return {
            "is_running": self.is_running,
            "has_browser": self.browser is not None,
            "has_context": self.context is not None,
            "has_page": self.page is not None,
            "current_url": await self.page.url() if self.page else None
        }

# Global browser manager instance
browser_manager = BrowserManager()