"""
API Server - FastAPI application with REST endpoints and WebSocket support
"""

import asyncio
import logging
from typing import Dict, Any, Optional, List
from datetime import datetime
import structlog

from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# Import our service components
from .browser_manager import browser_manager
from .llm_client import LLMClient, LLMProvider
from .websocket_manager import websocket_manager
from .task_queue import task_queue, TaskStatus
from .browser_service import BrowserAutomationService
from .prompt_manager import prompt_manager

logger = structlog.get_logger(__name__)

# Pydantic models for API
class ExecuteCommandRequest(BaseModel):
    command: str
    llm_provider: Optional[str] = "mac_studio"
    llm_model: Optional[str] = "llama4:scout"
    browser_profile: Optional[str] = "anti_bot"

class ExecuteCommandResponse(BaseModel):
    task_id: str
    status: str
    message: str

class TaskStatusResponse(BaseModel):
    id: str
    status: str
    created_at: str
    started_at: Optional[str]
    completed_at: Optional[str]
    command: str
    progress_steps: int
    has_result: bool
    error: Optional[str]

class HealthResponse(BaseModel):
    status: str
    timestamp: str
    browser_status: Dict[str, Any]
    queue_stats: Dict[str, Any]
    websocket_stats: Dict[str, Any]

# Create FastAPI app
app = FastAPI(
    title="Browser Automation Service",
    description="AI-powered browser automation with visual navigation",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global service instance
automation_service = None

@app.on_event("startup")
async def startup_event():
    """Initialize services on startup"""
    global automation_service
    try:
        logger.info("Starting Browser Automation Service...")
        
        # Initialize browser manager
        await browser_manager.start()
        
        # Initialize automation service
        automation_service = BrowserAutomationService()
        
        # Start task processor
        asyncio.create_task(task_processor())
        
        logger.info("Browser Automation Service started successfully")
        
    except Exception as e:
        logger.error("Failed to start service", error=str(e))
        raise

@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown"""
    try:
        logger.info("Shutting down Browser Automation Service...")
        await browser_manager.stop()
        logger.info("Service shutdown complete")
    except Exception as e:
        logger.error("Error during shutdown", error=str(e))

# REST API Endpoints

@app.post("/api/execute", response_model=ExecuteCommandResponse)
async def execute_command(request: ExecuteCommandRequest, background_tasks: BackgroundTasks):
    """Execute a browser automation command"""
    try:
        # Create task
        task_id = task_queue.create_task(
            command=request.command,
            llm_provider=request.llm_provider,
            llm_model=request.llm_model,
            browser_profile=request.browser_profile
        )
        
        # Broadcast task creation
        await websocket_manager.broadcast_task_started(task_id, {
            "command": request.command,
            "llm_provider": request.llm_provider,
            "llm_model": request.llm_model
        })
        
        logger.info("Command queued for execution", task_id=task_id, command=request.command[:100])
        
        return ExecuteCommandResponse(
            task_id=task_id,
            status="queued",
            message="Task created and queued for execution"
        )
        
    except Exception as e:
        logger.error("Failed to execute command", error=str(e))
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/tasks/{task_id}", response_model=TaskStatusResponse)
async def get_task_status(task_id: str):
    """Get status of a specific task"""
    task_status = task_queue.get_task_status(task_id)
    if not task_status:
        raise HTTPException(status_code=404, detail="Task not found")
    
    return TaskStatusResponse(**task_status)

@app.get("/api/tasks/{task_id}/result")
async def get_task_result(task_id: str):
    """Get detailed result of a completed task"""
    task = task_queue.get_task(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    if task.status != TaskStatus.COMPLETED:
        raise HTTPException(status_code=400, detail=f"Task not completed (status: {task.status.value})")
    
    return {
        "task_id": task_id,
        "result": task.result,
        "progress": task.progress,
        "completed_at": task.completed_at.isoformat()
    }

@app.get("/api/tasks")
async def list_tasks(limit: int = 20):
    """List all tasks (most recent first)"""
    return {
        "tasks": task_queue.get_all_tasks(limit=limit),
        "queue_stats": task_queue.get_queue_stats()
    }

@app.delete("/api/tasks/{task_id}")
async def cancel_task(task_id: str):
    """Cancel a task"""
    success = task_queue.cancel_task(task_id)
    if not success:
        raise HTTPException(status_code=404, detail="Task not found")
    
    await websocket_manager.broadcast_task_update(task_id, "task_cancelled", {})
    
    return {"message": "Task cancelled"}

@app.get("/api/health", response_model=HealthResponse)
async def health_check():
    """Get service health status"""
    browser_status = await browser_manager.get_status()
    queue_stats = task_queue.get_queue_stats()
    websocket_stats = websocket_manager.get_connection_stats()
    
    return HealthResponse(
        status="healthy" if browser_status["is_running"] else "degraded",
        timestamp=datetime.utcnow().isoformat(),
        browser_status=browser_status,
        queue_stats=queue_stats,
        websocket_stats=websocket_stats
    )

@app.get("/api/models")
async def list_available_models():
    """List available LLM models and their descriptions"""
    from .llm_client import ModelConfig
    
    return {
        "mac_studio_models": ModelConfig.MAC_STUDIO_MODELS,
        "gemini_models": ModelConfig.GEMINI_MODELS
    }

@app.get("/api/prompts")
async def list_prompts(version: Optional[str] = None, category: Optional[str] = None):
    """List available prompt templates"""
    prompts = prompt_manager.list_prompts(version, category)
    
    return {
        "prompts": [
            {
                "key": key,
                "name": prompt.name,
                "description": prompt.description,
                "use_case": prompt.use_case,
                "category": prompt.category,
                "version": prompt.version
            }
            for key, prompt in enumerate(prompts)
        ],
        "stats": prompt_manager.get_prompt_stats()
    }

@app.get("/api/prompts/versions")
async def list_prompt_versions():
    """List available prompt versions"""
    return {
        "versions": prompt_manager.get_versions(),
        "current_version": prompt_manager.current_version,
        "stats": prompt_manager.get_prompt_stats()
    }

# WebSocket endpoint

@app.websocket("/ws/updates")
async def websocket_endpoint(websocket: WebSocket, task_id: Optional[str] = None):
    """WebSocket endpoint for real-time updates"""
    await websocket_manager.connect(websocket, task_id)
    
    try:
        # Send initial connection message
        await websocket.send_json({
            "type": "connection",
            "message": "Connected to Browser Automation Service",
            "task_id": task_id,
            "timestamp": datetime.utcnow().isoformat()
        })
        
        # Keep connection alive
        while True:
            # Wait for messages from client (ping/pong, etc.)
            data = await websocket.receive_text()
            
            # Echo back for keep-alive
            await websocket.send_json({
                "type": "ping_response",
                "timestamp": datetime.utcnow().isoformat()
            })
            
    except WebSocketDisconnect:
        pass
    except Exception as e:
        logger.error("WebSocket error", error=str(e))
    finally:
        websocket_manager.disconnect(websocket)

# Background task processor

async def task_processor():
    """Background task processor that executes queued tasks"""
    logger.info("Task processor started")
    
    while True:
        try:
            # Get next task from queue
            task_id = await task_queue.get_next_task()
            if not task_id:
                continue
            
            # Check if we can run more tasks
            queue_stats = task_queue.get_queue_stats()
            if queue_stats["running_tasks"] >= task_queue.max_concurrent_tasks:
                # Put task back in queue
                await task_queue.pending_queue.put(task_id)
                await asyncio.sleep(1)
                continue
            
            # Execute task in background
            async_task = asyncio.create_task(execute_task(task_id))
            task_queue.mark_task_running(task_id, async_task)
            
        except Exception as e:
            logger.error("Error in task processor", error=str(e))
            await asyncio.sleep(5)

async def execute_task(task_id: str):
    """Execute a single automation task"""
    task = task_queue.get_task(task_id)
    if not task:
        return
    
    try:
        logger.info("Executing task", task_id=task_id, command=task.command[:100])
        
        # Update progress
        task_queue.add_task_progress(task_id, "Starting execution")
        await websocket_manager.broadcast_agent_step(task_id, {
            "step": "Starting execution",
            "status": "running"
        })
        
        # Execute using automation service
        result = await automation_service.execute_command(
            task.command,
            llm_provider=task.llm_provider,
            llm_model=task.llm_model,
            browser_profile=task.browser_profile,
            progress_callback=lambda step, details: handle_task_progress(task_id, step, details)
        )
        
        # Mark as completed
        task_queue.mark_task_completed(task_id, result)
        await websocket_manager.broadcast_task_completed(task_id, result)
        
        logger.info("Task completed successfully", task_id=task_id)
        
    except Exception as e:
        error_msg = str(e)
        logger.error("Task execution failed", task_id=task_id, error=error_msg)
        
        task_queue.mark_task_failed(task_id, error_msg)
        await websocket_manager.broadcast_task_failed(task_id, {"error": error_msg})

async def handle_task_progress(task_id: str, step: str, details: Dict[str, Any]):
    """Handle progress updates from automation service"""
    task_queue.add_task_progress(task_id, step, details)
    await websocket_manager.broadcast_agent_step(task_id, {
        "step": step,
        "details": details
    })

# Export the app
__all__ = ["app"]