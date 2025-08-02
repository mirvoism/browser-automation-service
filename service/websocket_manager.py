"""
WebSocket Manager - Handles real-time progress updates and client connections
"""

import asyncio
import json
import logging
from typing import Set, Dict, Any, Optional
from datetime import datetime
import structlog

from fastapi import WebSocket

logger = structlog.get_logger(__name__)

class WebSocketManager:
    """Manages WebSocket connections and broadcasts real-time updates"""
    
    def __init__(self):
        self.active_connections: Set[WebSocket] = set()
        self.task_subscribers: Dict[str, Set[WebSocket]] = {}
        
    async def connect(self, websocket: WebSocket, task_id: Optional[str] = None):
        """Accept a new WebSocket connection"""
        await websocket.accept()
        self.active_connections.add(websocket)
        
        # Subscribe to specific task updates if task_id provided
        if task_id:
            if task_id not in self.task_subscribers:
                self.task_subscribers[task_id] = set()
            self.task_subscribers[task_id].add(websocket)
            
            logger.info("WebSocket connected", task_id=task_id, total_connections=len(self.active_connections))
        else:
            logger.info("WebSocket connected", total_connections=len(self.active_connections))
    
    def disconnect(self, websocket: WebSocket):
        """Remove a WebSocket connection"""
        self.active_connections.discard(websocket)
        
        # Remove from task subscriptions
        for task_id, subscribers in list(self.task_subscribers.items()):
            subscribers.discard(websocket)
            if not subscribers:
                del self.task_subscribers[task_id]
                
        logger.info("WebSocket disconnected", total_connections=len(self.active_connections))
    
    async def send_to_all(self, message: Dict[str, Any]):
        """Send message to all connected clients"""
        if not self.active_connections:
            return
            
        # Add timestamp
        message["timestamp"] = datetime.utcnow().isoformat()
        message_json = json.dumps(message)
        
        # Send to all connections
        disconnected = set()
        for websocket in self.active_connections:
            try:
                await websocket.send_text(message_json)
            except Exception as e:
                logger.warning("Failed to send to websocket", error=str(e))
                disconnected.add(websocket)
        
        # Clean up disconnected clients
        for websocket in disconnected:
            self.disconnect(websocket)
    
    async def send_to_task_subscribers(self, task_id: str, message: Dict[str, Any]):
        """Send message to clients subscribed to a specific task"""
        if task_id not in self.task_subscribers:
            return
            
        # Add task context
        message["task_id"] = task_id
        message["timestamp"] = datetime.utcnow().isoformat()
        message_json = json.dumps(message)
        
        subscribers = self.task_subscribers[task_id].copy()
        disconnected = set()
        
        for websocket in subscribers:
            try:
                await websocket.send_text(message_json)
            except Exception as e:
                logger.warning("Failed to send to task subscriber", task_id=task_id, error=str(e))
                disconnected.add(websocket)
        
        # Clean up disconnected clients
        for websocket in disconnected:
            self.disconnect(websocket)
    
    async def broadcast_task_update(self, task_id: str, update_type: str, data: Dict[str, Any]):
        """Broadcast a task update to relevant subscribers"""
        message = {
            "type": "task_update",
            "update_type": update_type,
            "data": data
        }
        
        # Send to task-specific subscribers
        await self.send_to_task_subscribers(task_id, message)
    
    async def broadcast_system_message(self, message_type: str, data: Dict[str, Any]):
        """Broadcast a system-wide message"""
        message = {
            "type": "system",
            "message_type": message_type,
            "data": data
        }
        
        await self.send_to_all(message)
    
    async def broadcast_agent_step(self, task_id: str, step_data: Dict[str, Any]):
        """Broadcast browser agent step progress"""
        await self.broadcast_task_update(task_id, "agent_step", step_data)
    
    async def broadcast_task_started(self, task_id: str, task_data: Dict[str, Any]):
        """Broadcast that a task has started"""
        await self.broadcast_task_update(task_id, "task_started", task_data)
    
    async def broadcast_task_completed(self, task_id: str, result: Dict[str, Any]):
        """Broadcast that a task has completed"""
        await self.broadcast_task_update(task_id, "task_completed", result)
    
    async def broadcast_task_failed(self, task_id: str, error: Dict[str, Any]):
        """Broadcast that a task has failed"""
        await self.broadcast_task_update(task_id, "task_failed", error)
    
    async def broadcast_browser_action(self, task_id: str, action: str, details: Dict[str, Any]):
        """Broadcast browser action details"""
        action_data = {
            "action": action,
            "details": details
        }
        await self.broadcast_task_update(task_id, "browser_action", action_data)
    
    def get_connection_stats(self) -> Dict[str, Any]:
        """Get WebSocket connection statistics"""
        return {
            "total_connections": len(self.active_connections),
            "task_subscriptions": {
                task_id: len(subscribers) 
                for task_id, subscribers in self.task_subscribers.items()
            },
            "total_task_subscribers": sum(len(subscribers) for subscribers in self.task_subscribers.values())
        }

# Global WebSocket manager instance
websocket_manager = WebSocketManager()