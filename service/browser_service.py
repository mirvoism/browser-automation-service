"""
Browser Service - Core automation service that integrates browser-use with our components
"""

import asyncio
import logging
from typing import Dict, Any, Optional, Callable
import structlog

from browser_use import Agent
from .browser_manager import browser_manager
from .llm_client import LLMClient, LLMProvider
from .prompt_manager import prompt_manager

logger = structlog.get_logger(__name__)

class BrowserAutomationService:
    """Core service that coordinates browser automation using browser-use library"""
    
    def __init__(self):
        self.current_agent = None
        
    async def execute_command(
        self,
        command: str,
        llm_provider: str = "mac_studio",
        llm_model: str = "llama4:scout",
        browser_profile: str = "anti_bot",
        progress_callback: Optional[Callable] = None
    ) -> Dict[str, Any]:
        """Execute a browser automation command"""
        
        try:
            # Create progress callback wrapper
            async def progress_handler(step: str, details: Dict[str, Any] = None):
                if progress_callback:
                    await progress_callback(step, details or {})
            
            await progress_handler("Initializing LLM client")
            
            # Create LLM client
            if llm_provider == "mac_studio":
                llm_client = LLMClient(LLMProvider.MAC_STUDIO, llm_model)
            elif llm_provider == "gemini":
                llm_client = LLMClient(LLMProvider.GEMINI, llm_model)
            else:
                raise ValueError(f"Unsupported LLM provider: {llm_provider}")
            
            # Test LLM connection
            await progress_handler("Testing LLM connection")
            connection_test = await llm_client.test_connection()
            if connection_test["status"] != "connected":
                raise RuntimeError(f"LLM connection failed: {connection_test.get('error', 'Unknown error')}")
            
            # Ensure browser is started with correct profile
            await progress_handler("Starting browser")
            browser_status = await browser_manager.get_status()
            if not browser_status["is_running"]:
                await browser_manager.start(browser_profile)
            
            # Create browser-use agent
            await progress_handler("Creating automation agent")
            
            # Get browser page for browser-use
            page = await browser_manager.get_page()
            
            # Determine task type for prompt optimization
            task_type = self._determine_task_type(command)
            
            # Build optimized system prompt
            system_prompt = prompt_manager.build_system_prompt(task_type)
            
            # Create browser-use agent with our LLM and optimized prompts
            self.current_agent = Agent(
                task=command,
                llm=llm_client.get_llm(),
                browser=page,  # Pass our managed browser page
                use_vision=True,  # Enable visual navigation
                step_timeout=90,  # Longer timeout for reliability
                retry_delay=5,    # Human-like delays
                max_actions_per_step=5,  # More thorough actions
                system_prompt_suffix=system_prompt,  # Add our optimized prompts
            )
            
            await progress_handler("Starting task execution")
            
            # Execute the task
            result = await self.current_agent.run()
            
            await progress_handler("Task completed successfully")
            
            # Take final screenshot
            screenshot_data = await browser_manager.screenshot()
            
            # Return structured result
            return {
                "success": True,
                "result": str(result),
                "llm_provider": llm_provider,
                "llm_model": llm_model,
                "browser_profile": browser_profile,
                "final_url": await page.url(),
                "screenshot_size": len(screenshot_data),
                "model_info": llm_client.get_model_info()
            }
            
        except Exception as e:
            error_msg = f"Automation failed: {str(e)}"
            logger.error("Browser automation failed", command=command, error=error_msg)
            
            if progress_callback:
                await progress_callback("Task failed", {"error": error_msg})
            
            # Return error result
            return {
                "success": False,
                "error": error_msg,
                "llm_provider": llm_provider,
                "llm_model": llm_model,
                "browser_profile": browser_profile
            }
        
        finally:
            self.current_agent = None
    
    def _determine_task_type(self, command: str) -> str:
        """Determine the task type based on command content for prompt optimization"""
        command_lower = command.lower()
        
        # E-commerce keywords
        ecommerce_keywords = ["amazon", "ebay", "shop", "buy", "product", "price", "cart", "checkout"]
        if any(keyword in command_lower for keyword in ecommerce_keywords):
            return "ecommerce"
        
        # Financial keywords
        financial_keywords = ["stock", "price", "fund", "etf", "finance", "market", "trading", "investment"]
        if any(keyword in command_lower for keyword in financial_keywords):
            return "financial"
        
        # Search keywords
        search_keywords = ["search", "find", "look for", "google", "bing"]
        if any(keyword in command_lower for keyword in search_keywords):
            return "search"
        
        # Default to navigation
        return "navigation"
    
    async def cancel_current_task(self):
        """Cancel currently running task"""
        if self.current_agent:
            # browser-use doesn't have explicit cancellation, but we can try to stop
            self.current_agent = None
            logger.info("Current task cancelled")
    
    def get_status(self) -> Dict[str, Any]:
        """Get service status"""
        return {
            "has_active_task": self.current_agent is not None,
            "service_ready": True
        }