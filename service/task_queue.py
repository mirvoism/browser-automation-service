"""
Task Queue - Manages automation task scheduling and execution
"""

import asyncio
import uuid
import logging
from datetime import datetime
from typing import Dict, Any, Optional, List
from enum import Enum
from dataclasses import dataclass, asdict
import structlog

logger = structlog.get_logger(__name__)

class TaskStatus(Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"

@dataclass
class Task:
    """Represents an automation task"""
    id: str
    command: str
    status: TaskStatus
    created_at: datetime
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    result: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    progress: List[Dict[str, Any]] = None
    llm_provider: str = "mac_studio"
    llm_model: str = "llama4:scout"
    browser_profile: str = "anti_bot"
    
    def __post_init__(self):
        if self.progress is None:
            self.progress = []
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert task to dictionary for JSON serialization"""
        data = asdict(self)
        # Convert datetime objects to ISO strings
        for field in ["created_at", "started_at", "completed_at"]:
            if data[field]:
                data[field] = data[field].isoformat()
        # Convert enum to value
        data["status"] = data["status"].value
        return data
    
    def add_progress(self, step: str, details: Dict[str, Any] = None):
        """Add progress update to task"""
        progress_entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "step": step,
            "details": details or {}
        }
        self.progress.append(progress_entry)

class TaskQueue:
    """Manages task queue and execution"""
    
    def __init__(self):
        self.tasks: Dict[str, Task] = {}
        self.pending_queue: asyncio.Queue = asyncio.Queue()
        self.max_concurrent_tasks = 3  # Limit concurrent executions
        self.running_tasks: Dict[str, asyncio.Task] = {}
        
    def create_task(self, command: str, **kwargs) -> str:
        """Create a new automation task"""
        task_id = str(uuid.uuid4())
        
        task = Task(
            id=task_id,
            command=command,
            status=TaskStatus.PENDING,
            created_at=datetime.utcnow(),
            llm_provider=kwargs.get("llm_provider", "mac_studio"),
            llm_model=kwargs.get("llm_model", "llama4:scout"),
            browser_profile=kwargs.get("browser_profile", "anti_bot")
        )
        
        self.tasks[task_id] = task
        
        # Add to pending queue
        asyncio.create_task(self.pending_queue.put(task_id))
        
        logger.info("Task created", task_id=task_id, command=command[:100])
        return task_id
    
    def get_task(self, task_id: str) -> Optional[Task]:
        """Get task by ID"""
        return self.tasks.get(task_id)
    
    def get_task_status(self, task_id: str) -> Optional[Dict[str, Any]]:
        """Get task status and basic info"""
        task = self.get_task(task_id)
        if not task:
            return None
        
        return {
            "id": task.id,
            "status": task.status.value,
            "created_at": task.created_at.isoformat(),
            "started_at": task.started_at.isoformat() if task.started_at else None,
            "completed_at": task.completed_at.isoformat() if task.completed_at else None,
            "command": task.command,
            "progress_steps": len(task.progress),
            "has_result": task.result is not None,
            "error": task.error
        }
    
    def get_all_tasks(self, limit: int = 50) -> List[Dict[str, Any]]:
        """Get all tasks (most recent first)"""
        sorted_tasks = sorted(
            self.tasks.values(), 
            key=lambda t: t.created_at, 
            reverse=True
        )
        return [task.to_dict() for task in sorted_tasks[:limit]]
    
    def update_task_status(self, task_id: str, status: TaskStatus, **kwargs):
        """Update task status and optional fields"""
        task = self.get_task(task_id)
        if not task:
            return
        
        old_status = task.status
        task.status = status
        
        # Update timestamps
        if status == TaskStatus.RUNNING and not task.started_at:
            task.started_at = datetime.utcnow()
        elif status in [TaskStatus.COMPLETED, TaskStatus.FAILED, TaskStatus.CANCELLED]:
            task.completed_at = datetime.utcnow()
        
        # Update optional fields
        if "result" in kwargs:
            task.result = kwargs["result"]
        if "error" in kwargs:
            task.error = kwargs["error"]
        
        logger.info("Task status updated", 
                   task_id=task_id, 
                   old_status=old_status.value, 
                   new_status=status.value)
    
    def add_task_progress(self, task_id: str, step: str, details: Dict[str, Any] = None):
        """Add progress update to task"""
        task = self.get_task(task_id)
        if task:
            task.add_progress(step, details)
            logger.debug("Task progress added", task_id=task_id, step=step)
    
    def cancel_task(self, task_id: str) -> bool:
        """Cancel a task"""
        task = self.get_task(task_id)
        if not task:
            return False
        
        # Cancel if running
        if task_id in self.running_tasks:
            running_task = self.running_tasks[task_id]
            running_task.cancel()
            del self.running_tasks[task_id]
        
        self.update_task_status(task_id, TaskStatus.CANCELLED)
        logger.info("Task cancelled", task_id=task_id)
        return True
    
    def get_queue_stats(self) -> Dict[str, Any]:
        """Get queue statistics"""
        status_counts = {}
        for status in TaskStatus:
            status_counts[status.value] = sum(
                1 for task in self.tasks.values() 
                if task.status == status
            )
        
        return {
            "total_tasks": len(self.tasks),
            "pending_queue_size": self.pending_queue.qsize(),
            "running_tasks": len(self.running_tasks),
            "max_concurrent": self.max_concurrent_tasks,
            "status_breakdown": status_counts
        }
    
    async def get_next_task(self) -> Optional[str]:
        """Get next task from queue (blocking)"""
        try:
            task_id = await self.pending_queue.get()
            return task_id
        except asyncio.CancelledError:
            return None
    
    def mark_task_running(self, task_id: str, async_task: asyncio.Task):
        """Mark task as running and track the async task"""
        self.running_tasks[task_id] = async_task
        self.update_task_status(task_id, TaskStatus.RUNNING)
    
    def mark_task_completed(self, task_id: str, result: Dict[str, Any]):
        """Mark task as completed with result"""
        if task_id in self.running_tasks:
            del self.running_tasks[task_id]
        self.update_task_status(task_id, TaskStatus.COMPLETED, result=result)
    
    def mark_task_failed(self, task_id: str, error: str):
        """Mark task as failed with error"""
        if task_id in self.running_tasks:
            del self.running_tasks[task_id]
        self.update_task_status(task_id, TaskStatus.FAILED, error=error)

# Global task queue instance
task_queue = TaskQueue()