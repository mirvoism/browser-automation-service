# 🐳 Docker Setup & Port Management Guide

**Browser Automation Service** - Complete Docker deployment guide with port conflict prevention.

---

## 🚀 **Quick Start**

### **1. One-Command Setup**
```bash
# Clone and start service  
git clone <repository-url>
cd browser-automation-service
docker compose up browser-automation-service
```

### **2. Service Endpoints**
Once running, access these endpoints:
- **🌐 API**: http://localhost:8000
- **📡 WebSocket**: ws://localhost:8000/ws/updates  
- **📚 API Docs**: http://localhost:8000/docs
- **❤️ Health Check**: http://localhost:8000/api/health

---

## 📋 **Port Assignments & Conflict Prevention**

### **🎯 This Project's Ports**
| Port | Service | Purpose | Configurable |
|------|---------|---------|--------------|
| **8000** | API Service | REST API + WebSocket | ✅ |
| 5900 | VNC Server | Browser debugging (optional) | ✅ |
| 6901 | noVNC Web | Browser GUI access (optional) | ✅ |

### **🚨 Common Port Conflicts**
Make sure these ports are NOT in use by other projects:

**Development Servers:**
- 3000 (React/Next.js)
- 8080 (Local dev servers)
- 5173 (Vite)
- 4200 (Angular)

**Databases:**
- 5432 (PostgreSQL)
- 3306 (MySQL)
- 6379 (Redis)
- 27017 (MongoDB)

**Other Services:**
- 9000 (Various dashboards)
- 8888 (Jupyter)
- 7000-7999 (Common service range)

### **🔧 Changing the Service Port**
If port 8000 conflicts with your setup:

**Method 1: Environment Variable**
```bash
export PORT=8001
docker compose up browser-automation-service
```

**Method 2: Docker Compose Override**
```yaml
# docker-compose.override.yml
version: '3.8'
services:
  browser-automation-service:
    ports:
      - "8001:8001"  # Change host port
    environment:
      - PORT=8001     # Change container port
```

**Method 3: Custom .env**
```bash
# .env.local
PORT=8001
HOST=0.0.0.0
```

Then:
```bash
docker compose --env-file .env.local up browser-automation-service
```

---

## 🏗️ **Service Architecture**

### **🎯 Main Service: browser-automation-service**
```yaml
browser-automation-service:
  build: .
  container_name: browser-automation-api
  ports:
    - "8000:8000"
  environment:
    - HOST=0.0.0.0
    - PORT=8000
    - DEFAULT_LLM_PROVIDER=mac_studio
    - DEFAULT_LLM_MODEL=llama4:scout
    - MAC_STUDIO_URL=https://matiass-mac-studio.tail174e9b.ts.net/v1
    - DEFAULT_BROWSER_PROFILE=anti_bot
    - MAX_CONCURRENT_TASKS=3
  volumes:
    - ./results:/app/results
    - ./screenshots:/app/screenshots
    - ./logs:/app/logs
  restart: unless-stopped
```

### **📦 Legacy Services (Optional)**
The docker-compose.yml also includes legacy example services:
- `browser-automation-gemini`: Google Gemini examples
- `browser-automation-macstudio`: Mac Studio examples  
- `production-agent`: Production visual agent
- `dev-environment`: Development container

**⚠️ These use different ports and are separate from the main API service.**

---

## 🔧 **Configuration Options**

### **Environment Variables**
```bash
# Server Configuration
HOST=0.0.0.0              # Bind address
PORT=8000                 # Service port
LOG_LEVEL=info            # Logging level
WORKERS=1                 # Uvicorn workers

# LLM Configuration  
DEFAULT_LLM_PROVIDER=mac_studio     # mac_studio or gemini
DEFAULT_LLM_MODEL=llama4:scout      # Model to use
MAC_STUDIO_URL=https://...          # Mac Studio endpoint
GOOGLE_API_KEY=your_key             # For Gemini (optional)

# Browser Configuration
DEFAULT_BROWSER_PROFILE=anti_bot    # Browser profile
MAX_CONCURRENT_TASKS=3              # Task concurrency

# CORS Configuration
ENABLE_CORS=true                    # Enable CORS
CORS_ORIGINS=*                      # Allowed origins
```

### **Volume Mounts**
```yaml
volumes:
  - ./results:/app/results         # Automation results
  - ./screenshots:/app/screenshots # Browser screenshots  
  - ./logs:/app/logs              # Service logs
  - /tmp/.X11-unix:/tmp/.X11-unix:rw  # X11 for GUI (Linux)
```

---

## 📊 **Multiple Environments**

### **Development Setup**
```bash
# docker-compose.dev.yml
version: '3.8'
services:
  browser-automation-service:
    extends:
      file: docker-compose.yml
      service: browser-automation-service
    environment:
      - RELOAD=true           # Auto-reload on changes
      - LOG_LEVEL=debug       # Verbose logging
    volumes:
      - .:/app               # Mount source code
    ports:
      - "8000:8000"
```

```bash
docker compose -f docker-compose.yml -f docker-compose.dev.yml up
```

### **Production Setup**
```bash
# docker-compose.prod.yml
version: '3.8'
services:
  browser-automation-service:
    extends:
      file: docker-compose.yml  
      service: browser-automation-service
    environment:
      - WORKERS=4             # Multiple workers
      - LOG_LEVEL=warning     # Less verbose
      - MAX_CONCURRENT_TASKS=10  # Higher concurrency
    deploy:
      resources:
        limits:
          memory: 2G
          cpus: '1.5'
    restart: always
```

### **Testing Setup**
```bash
# docker-compose.test.yml
version: '3.8'
services:
  browser-automation-service:
    extends:
      file: docker-compose.yml
      service: browser-automation-service
    ports:
      - "8001:8000"          # Different port for testing
    environment:
      - MAX_CONCURRENT_TASKS=1  # Limited for testing
```

---

## 🔍 **Health Checks & Monitoring**

### **Built-in Health Check**
The service includes automatic health monitoring:
```yaml
healthcheck:
  test: ["CMD", "curl", "-f", "http://localhost:8000/api/health"]
  interval: 30s
  timeout: 10s
  retries: 3
  start_period: 40s
```

### **Manual Health Check**
```bash
# Check if service is healthy
docker compose ps browser-automation-service

# View health check logs
docker compose logs browser-automation-service

# Manual health test
curl http://localhost:8000/api/health
```

### **Service Logs**
```bash
# View real-time logs
docker compose logs -f browser-automation-service

# View specific number of lines
docker compose logs --tail=100 browser-automation-service

# Search logs
docker compose logs browser-automation-service | grep ERROR
```

---

## 🛠️ **Troubleshooting**

### **❌ Port Already in Use**
```bash
# Find what's using port 8000
lsof -i :8000
# or
netstat -tulpn | grep 8000

# Kill the process
kill -9 <PID>

# Or change the port
export PORT=8001
docker compose up browser-automation-service
```

### **❌ Browser Won't Start**
```bash
# Check if X11 is available (Linux)
echo $DISPLAY

# For macOS, install XQuartz
brew install --cask xquartz

# Allow X11 connections (Linux)
xhost +local:docker
```

### **❌ Mac Studio Connection Failed**
```bash
# Test Mac Studio connectivity
curl https://matiass-mac-studio.tail174e9b.ts.net/v1/models

# Check Tailscale status
tailscale status

# Verify environment variable
docker compose exec browser-automation-service env | grep MAC_STUDIO
```

### **❌ Memory/Performance Issues**
```bash
# Check resource usage
docker stats browser-automation-api

# Limit memory usage
docker compose up browser-automation-service --memory=1g

# Reduce concurrent tasks
export MAX_CONCURRENT_TASKS=1
```

---

## 🏃‍♂️ **Performance Optimization**

### **Production Optimization**
```yaml
# docker-compose.prod.yml
services:
  browser-automation-service:
    deploy:
      resources:
        limits:
          memory: 4G        # Adequate memory for browser
          cpus: '2.0'       # Multiple CPU cores
        reservations:
          memory: 2G
          cpus: '1.0'
    environment:
      - WORKERS=4           # Multiple workers
      - MAX_CONCURRENT_TASKS=8  # Higher concurrency
    restart: always
```

### **Development Optimization**
```yaml
# docker-compose.dev.yml  
services:
  browser-automation-service:
    environment:
      - RELOAD=true         # Auto-reload
      - MAX_CONCURRENT_TASKS=1  # Single task for debugging
      - LOG_LEVEL=debug     # Verbose logging
    volumes:
      - .:/app             # Live code mounting
```

---

## 🌐 **Network Configuration**

### **Custom Network**
```yaml
networks:
  automation-network:
    driver: bridge
    ipam:
      config:
        - subnet: 172.20.0.0/16
```

### **External Network Integration**
```yaml
# Connect to existing network
services:
  browser-automation-service:
    networks:
      - default
      - external-network
      
networks:
  external-network:
    external: true
```

---

## 📝 **Quick Commands Reference**

```bash
# Start service
docker compose up browser-automation-service

# Start in background
docker compose up -d browser-automation-service

# View logs
docker compose logs -f browser-automation-service

# Stop service
docker compose down

# Rebuild and start
docker compose up --build browser-automation-service

# Execute commands in container
docker compose exec browser-automation-service bash

# Check service status
docker compose ps

# View resource usage
docker stats browser-automation-api

# Clean up
docker compose down -v
docker system prune -f
```

---

**🎯 This Docker setup provides a production-ready, isolated browser automation service that avoids port conflicts and integrates seamlessly with your existing development workflow.**