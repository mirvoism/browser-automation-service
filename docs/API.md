# 🌐 Browser Automation Service API Documentation

**Version**: 1.0.0  
**Base URL**: `http://localhost:8000`  
**WebSocket**: `ws://localhost:8000/ws/updates`

---

## 📋 **Quick Reference**

| Endpoint | Method | Purpose | Port |
|----------|--------|---------|------|
| `/api/execute` | POST | Execute automation command | 8000 |
| `/api/tasks/{id}` | GET | Get task status | 8000 |
| `/api/tasks/{id}/result` | GET | Get task result | 8000 |
| `/api/tasks` | GET | List all tasks | 8000 |
| `/api/tasks/{id}` | DELETE | Cancel task | 8000 |
| `/api/health` | GET | Service health check | 8000 |
| `/api/models` | GET | Available LLM models | 8000 |
| `/ws/updates` | WebSocket | Real-time progress | 8000 |
| `/docs` | GET | Interactive API docs | 8000 |

---

## 🚀 **Getting Started**

### **Docker Setup (Recommended)**
```bash
# Start the service
docker compose up browser-automation-service

# Service will be available at:
# API: http://localhost:8000
# WebSocket: ws://localhost:8000/ws/updates
# Docs: http://localhost:8000/docs
```

### **Quick Test**
```bash
# Test service health
curl http://localhost:8000/api/health

# Execute a simple automation
curl -X POST http://localhost:8000/api/execute \
  -H "Content-Type: application/json" \
  -d '{"command": "Search Google for Tesla stock price"}'
```

---

## 🎯 **Core Endpoints**

### **POST /api/execute**
Execute a browser automation command using natural language.

**Request Body:**
```json
{
  "command": "Search Google for Tesla stock price and return the current value",
  "llm_provider": "mac_studio",
  "llm_model": "llama4:scout", 
  "browser_profile": "anti_bot"
}
```

**Request Fields:**
- `command` (required): Natural language description of the automation task
- `llm_provider` (optional): `"mac_studio"` or `"gemini"` (default: `"mac_studio"`)
- `llm_model` (optional): Model name (default: `"llama4:scout"`)
- `browser_profile` (optional): `"anti_bot"` or `"standard"` (default: `"anti_bot"`)

**Response:**
```json
{
  "task_id": "550e8400-e29b-41d4-a716-446655440000",
  "status": "queued",
  "message": "Task created and queued for execution"
}
```

**Example cURL:**
```bash
curl -X POST http://localhost:8000/api/execute \
  -H "Content-Type: application/json" \
  -d '{
    "command": "Go to Amazon and search for gaming laptops under $1000, return top 3 results",
    "llm_provider": "mac_studio",
    "llm_model": "llama4:scout"
  }'
```

**Example Python:**
```python
import requests

response = requests.post("http://localhost:8000/api/execute", json={
    "command": "Search Yahoo Finance for Apple stock price and recent news",
    "llm_provider": "mac_studio",
    "llm_model": "llama4:scout"
})

task_data = response.json()
task_id = task_data["task_id"]
print(f"Task started: {task_id}")
```

---

### **GET /api/tasks/{task_id}**
Get the status and progress of a specific task.

**Response:**
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "status": "running",
  "created_at": "2025-01-20T10:30:00.000Z",
  "started_at": "2025-01-20T10:30:05.000Z",
  "completed_at": null,
  "command": "Search Google for Tesla stock price",
  "progress_steps": 3,
  "has_result": false,
  "error": null
}
```

**Status Values:**
- `pending`: Task is queued for execution
- `running`: Task is currently being executed
- `completed`: Task finished successfully
- `failed`: Task failed with an error
- `cancelled`: Task was cancelled

**Example:**
```bash
curl http://localhost:8000/api/tasks/550e8400-e29b-41d4-a716-446655440000
```

---

### **GET /api/tasks/{task_id}/result**
Get the detailed result of a completed task.

**Response:**
```json
{
  "task_id": "550e8400-e29b-41d4-a716-446655440000",
  "result": {
    "success": true,
    "result": "Tesla (TSLA) current stock price: $248.42, up 2.1% today...",
    "llm_provider": "mac_studio",
    "llm_model": "llama4:scout",
    "browser_profile": "anti_bot",
    "final_url": "https://finance.yahoo.com/quote/TSLA",
    "screenshot_size": 1024000,
    "model_info": {
      "provider": "mac_studio",
      "model": "llama4:scout",
      "description": "Best for browser navigation and search tasks"
    }
  },
  "progress": [
    {
      "timestamp": "2025-01-20T10:30:05.000Z",
      "step": "Starting execution",
      "details": {}
    },
    {
      "timestamp": "2025-01-20T10:30:08.000Z", 
      "step": "Opening browser",
      "details": {"url": "https://google.com"}
    }
  ],
  "completed_at": "2025-01-20T10:31:22.000Z"
}
```

---

### **GET /api/health**
Get service health status and system information.

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2025-01-20T10:30:00.000Z",
  "browser_status": {
    "is_running": true,
    "has_browser": true,
    "has_context": true,
    "has_page": true,
    "current_url": "about:blank"
  },
  "queue_stats": {
    "total_tasks": 5,
    "pending_queue_size": 0,
    "running_tasks": 1,
    "max_concurrent": 3,
    "status_breakdown": {
      "pending": 0,
      "running": 1,
      "completed": 3,
      "failed": 1,
      "cancelled": 0
    }
  },
  "websocket_stats": {
    "total_connections": 2,
    "task_subscriptions": {
      "550e8400-e29b-41d4-a716-446655440000": 1
    },
    "total_task_subscribers": 1
  }
}
```

---

## 📡 **WebSocket Real-Time Updates**

### **Connection**
```javascript
const ws = new WebSocket('ws://localhost:8000/ws/updates');

// Subscribe to specific task
const ws = new WebSocket('ws://localhost:8000/ws/updates?task_id=550e8400-e29b-41d4-a716-446655440000');
```

### **Message Types**

**Connection Confirmation:**
```json
{
  "type": "connection",
  "message": "Connected to Browser Automation Service",
  "task_id": null,
  "timestamp": "2025-01-20T10:30:00.000Z"
}
```

**Task Started:**
```json
{
  "type": "task_update",
  "update_type": "task_started",
  "task_id": "550e8400-e29b-41d4-a716-446655440000",
  "data": {
    "command": "Search Google for Tesla stock price",
    "llm_provider": "mac_studio",
    "llm_model": "llama4:scout"
  },
  "timestamp": "2025-01-20T10:30:05.000Z"
}
```

**Agent Step Progress:**
```json
{
  "type": "task_update",
  "update_type": "agent_step",
  "task_id": "550e8400-e29b-41d4-a716-446655440000",
  "data": {
    "step": "Navigating to Google",
    "details": {
      "url": "https://google.com",
      "action": "navigate"
    }
  },
  "timestamp": "2025-01-20T10:30:08.000Z"
}
```

**Task Completed:**
```json
{
  "type": "task_update",
  "update_type": "task_completed",
  "task_id": "550e8400-e29b-41d4-a716-446655440000",
  "data": {
    "success": true,
    "result": "Tesla (TSLA) current stock price: $248.42...",
    "execution_time": 45.2
  },
  "timestamp": "2025-01-20T10:31:22.000Z"
}
```

### **JavaScript Example**
```javascript
const ws = new WebSocket('ws://localhost:8000/ws/updates');

ws.onmessage = function(event) {
  const message = JSON.parse(event.data);
  
  switch(message.type) {
    case 'connection':
      console.log('Connected to automation service');
      break;
      
    case 'task_update':
      if (message.update_type === 'agent_step') {
        console.log(`Step: ${message.data.step}`);
      } else if (message.update_type === 'task_completed') {
        console.log('Task completed:', message.data.result);
      }
      break;
  }
};
```

---

## 🤖 **LLM Models & Configuration**

### **Mac Studio Models (Local)**
| Model | Best For | Speed | Cost |
|-------|----------|-------|------|
| `llama4:scout` | Navigation, search, general automation | Fast | Free |
| `maverick` | Complex reasoning, data analysis | Medium | Free |
| `deepseek-r1` | Logical tasks, problem solving | Medium | Free |
| `qwen3:32b` | Large context, detailed extraction | Slow | Free |
| `qwen25` | Balanced performance | Fast | Free |

### **Google Gemini Models (Cloud)**
| Model | Best For | Speed | Cost |
|-------|----------|-------|------|
| `gemini-1.5-flash` | General automation, fast responses | Very Fast | $$ |
| `gemini-1.5-pro` | Complex tasks, detailed analysis | Fast | $$$ |

### **Model Selection Examples**
```bash
# For navigation and search
curl -X POST http://localhost:8000/api/execute \
  -H "Content-Type: application/json" \
  -d '{"command": "...", "llm_model": "llama4:scout"}'

# For complex data analysis  
curl -X POST http://localhost:8000/api/execute \
  -H "Content-Type: application/json" \
  -d '{"command": "...", "llm_model": "maverick"}'

# Using Google Gemini
curl -X POST http://localhost:8000/api/execute \
  -H "Content-Type: application/json" \
  -d '{"command": "...", "llm_provider": "gemini", "llm_model": "gemini-1.5-flash"}'
```

---

## 🛡️ **Browser Profiles**

### **Anti-Bot Profile (Recommended)**
- **Use Case**: Bypassing anti-bot protection
- **Features**: Human-like user agent, natural timing, visual navigation
- **Best For**: E-commerce, protected sites, real-world automation

### **Standard Profile**
- **Use Case**: Simple automation tasks
- **Features**: Faster execution, less stealth optimization
- **Best For**: Internal tools, testing, development

---

## 🔧 **Integration Examples**

### **Python Client**
```python
import requests
import websocket
import json
import time

class BrowserAutomationClient:
    def __init__(self, base_url="http://localhost:8000"):
        self.base_url = base_url
        
    def execute_task(self, command, **kwargs):
        """Execute automation task and return task ID"""
        response = requests.post(f"{self.base_url}/api/execute", json={
            "command": command,
            **kwargs
        })
        return response.json()["task_id"]
    
    def wait_for_completion(self, task_id, timeout=300):
        """Wait for task completion and return result"""
        start_time = time.time()
        
        while time.time() - start_time < timeout:
            status = requests.get(f"{self.base_url}/api/tasks/{task_id}").json()
            
            if status["status"] == "completed":
                result = requests.get(f"{self.base_url}/api/tasks/{task_id}/result").json()
                return result["result"]
            elif status["status"] == "failed":
                raise Exception(f"Task failed: {status['error']}")
            
            time.sleep(2)
        
        raise TimeoutError("Task did not complete within timeout")

# Usage
client = BrowserAutomationClient()
task_id = client.execute_task("Find Tesla stock price on Yahoo Finance")
result = client.wait_for_completion(task_id)
print(result)
```

### **Node.js Client**
```javascript
const axios = require('axios');
const WebSocket = require('ws');

class BrowserAutomationClient {
  constructor(baseUrl = 'http://localhost:8000') {
    this.baseUrl = baseUrl;
  }
  
  async executeTask(command, options = {}) {
    const response = await axios.post(`${this.baseUrl}/api/execute`, {
      command,
      ...options
    });
    return response.data.task_id;
  }
  
  async getTaskStatus(taskId) {
    const response = await axios.get(`${this.baseUrl}/api/tasks/${taskId}`);
    return response.data;
  }
  
  async getTaskResult(taskId) {
    const response = await axios.get(`${this.baseUrl}/api/tasks/${taskId}/result`);
    return response.data;
  }
  
  watchTask(taskId, onUpdate) {
    const ws = new WebSocket(`ws://localhost:8000/ws/updates?task_id=${taskId}`);
    
    ws.on('message', (data) => {
      const message = JSON.parse(data);
      onUpdate(message);
    });
    
    return ws;
  }
}

// Usage
const client = new BrowserAutomationClient();

(async () => {
  const taskId = await client.executeTask('Search Amazon for gaming laptops under $1000');
  
  // Watch for real-time updates
  const ws = client.watchTask(taskId, (message) => {
    if (message.type === 'task_update') {
      console.log('Update:', message.data);
    }
  });
  
  // Poll for completion
  let status;
  do {
    await new Promise(resolve => setTimeout(resolve, 2000));
    status = await client.getTaskStatus(taskId);
    console.log('Status:', status.status);
  } while (status.status === 'pending' || status.status === 'running');
  
  if (status.status === 'completed') {
    const result = await client.getTaskResult(taskId);
    console.log('Result:', result.result);
  }
  
  ws.close();
})();
```

---

## 🚨 **Error Handling**

### **HTTP Error Codes**
- `400`: Bad Request - Invalid command or parameters
- `404`: Not Found - Task ID doesn't exist
- `429`: Too Many Requests - Rate limit exceeded
- `500`: Internal Server Error - Service error
- `503`: Service Unavailable - Browser or LLM not available

### **Error Response Format**
```json
{
  "detail": "Task not found",
  "status_code": 404,
  "timestamp": "2025-01-20T10:30:00.000Z"
}
```

### **Task Failure Response**
```json
{
  "task_id": "550e8400-e29b-41d4-a716-446655440000",
  "result": {
    "success": false,
    "error": "Browser automation failed: Connection timeout",
    "llm_provider": "mac_studio",
    "llm_model": "llama4:scout"
  }
}
```

---

## 📊 **Performance & Limits**

### **Rate Limits**
- **Max Concurrent Tasks**: 3 (configurable)
- **Queue Size**: Unlimited
- **WebSocket Connections**: Unlimited
- **Request Rate**: No global limit

### **Timeouts**
- **Task Execution**: 300 seconds (5 minutes)
- **LLM Response**: 30 seconds  
- **Browser Navigation**: 90 seconds per step
- **WebSocket Idle**: 3600 seconds (1 hour)

### **Performance Tips**
1. **Use Mac Studio models** for faster, unlimited responses
2. **Use specific commands** rather than vague instructions
3. **Monitor task queue** to avoid overwhelming the system
4. **Use WebSocket** for real-time progress instead of polling

---

## 🔧 **Development & Testing**

### **Interactive API Documentation**
Visit `http://localhost:8000/docs` for Swagger UI with interactive testing.

### **Health Check Monitoring**
```bash
# Basic health check
curl http://localhost:8000/api/health

# Detailed system status
curl http://localhost:8000/api/health | jq .
```

### **Development Mode**
```bash
# Start with auto-reload for development
docker compose up browser-automation-service
# OR
python main.py  # With RELOAD=true in environment
```

---

**🎯 The Browser Automation Service provides enterprise-grade AI-powered web automation through a simple REST API, enabling you to integrate human-like browser behavior into any application or workflow.**