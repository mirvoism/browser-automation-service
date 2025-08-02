#!/usr/bin/env python3
"""
Service Validation Script
Tests the complete browser automation service setup
"""

import asyncio
import requests
import json
import time
import sys
from pathlib import Path

class ServiceValidator:
    """Validates the browser automation service setup"""
    
    def __init__(self, base_url="http://localhost:8000"):
        self.base_url = base_url
        self.errors = []
        self.warnings = []
        
    def log_error(self, message):
        self.errors.append(message)
        print(f"❌ ERROR: {message}")
    
    def log_warning(self, message):
        self.warnings.append(message)
        print(f"⚠️  WARNING: {message}")
    
    def log_success(self, message):
        print(f"✅ {message}")
    
    def log_info(self, message):
        print(f"ℹ️  {message}")
    
    def test_file_structure(self):
        """Test that all required files exist"""
        print("\n🔍 Testing File Structure...")
        
        required_files = [
            "service/api_server.py",
            "service/browser_manager.py", 
            "service/browser_service.py",
            "service/llm_client.py",
            "service/prompt_manager.py",
            "service/task_queue.py",
            "service/websocket_manager.py",
            "main.py",
            "requirements-service.txt",
            "docker-compose.yml",
            "Dockerfile",
            "docs/API.md",
            "docs/DOCKER_GUIDE.md",
            "prompts/versions/v1.0.0/navigation.yaml",
            "prompts/versions/v1.0.0/ecommerce.yaml",
            "prompts/versions/v1.0.0/financial.yaml"
        ]
        
        for file_path in required_files:
            if Path(file_path).exists():
                self.log_success(f"Found {file_path}")
            else:
                self.log_error(f"Missing required file: {file_path}")
    
    def test_service_health(self):
        """Test service health endpoint"""
        print("\n🏥 Testing Service Health...")
        
        try:
            response = requests.get(f"{self.base_url}/api/health", timeout=10)
            if response.status_code == 200:
                health_data = response.json()
                self.log_success("Service health endpoint responding")
                
                # Check health data structure
                if health_data.get("status") == "healthy":
                    self.log_success("Service reports healthy status")
                else:
                    self.log_warning(f"Service status: {health_data.get('status')}")
                
                # Check browser status
                browser_status = health_data.get("browser_status", {})
                if browser_status.get("is_running"):
                    self.log_success("Browser manager is running")
                else:
                    self.log_warning("Browser manager not running")
                    
            else:
                self.log_error(f"Health endpoint returned {response.status_code}")
                
        except requests.exceptions.ConnectionError:
            self.log_error("Cannot connect to service - is it running?")
        except Exception as e:
            self.log_error(f"Health check failed: {e}")
    
    def test_api_endpoints(self):
        """Test all API endpoints"""
        print("\n🌐 Testing API Endpoints...")
        
        endpoints = [
            ("/api/health", "GET"),
            ("/api/models", "GET"),
            ("/api/prompts", "GET"),
            ("/api/prompts/versions", "GET"),
            ("/api/tasks", "GET"),
            ("/docs", "GET")
        ]
        
        for endpoint, method in endpoints:
            try:
                if method == "GET":
                    response = requests.get(f"{self.base_url}{endpoint}", timeout=10)
                    
                if response.status_code == 200:
                    self.log_success(f"{method} {endpoint} - OK")
                else:
                    self.log_warning(f"{method} {endpoint} - Status {response.status_code}")
                    
            except Exception as e:
                self.log_error(f"{method} {endpoint} - Failed: {e}")
    
    def test_prompt_system(self):
        """Test prompt management system"""
        print("\n🤖 Testing Prompt System...")
        
        try:
            response = requests.get(f"{self.base_url}/api/prompts", timeout=10)
            if response.status_code == 200:
                prompt_data = response.json()
                
                if prompt_data.get("prompts"):
                    self.log_success(f"Found {len(prompt_data['prompts'])} prompts")
                else:
                    self.log_warning("No prompts found")
                
                stats = prompt_data.get("stats", {})
                if stats.get("total_versions", 0) > 0:
                    self.log_success(f"Prompt versions available: {stats['total_versions']}")
                else:
                    self.log_warning("No prompt versions found")
                    
            else:
                self.log_error(f"Prompts endpoint returned {response.status_code}")
                
        except Exception as e:
            self.log_error(f"Prompt system test failed: {e}")
    
    def test_llm_models(self):
        """Test LLM model configuration"""
        print("\n🧠 Testing LLM Models...")
        
        try:
            response = requests.get(f"{self.base_url}/api/models", timeout=10)
            if response.status_code == 200:
                model_data = response.json()
                
                mac_studio_models = model_data.get("mac_studio_models", {})
                gemini_models = model_data.get("gemini_models", {})
                
                if mac_studio_models:
                    self.log_success(f"Mac Studio models: {len(mac_studio_models)}")
                    if "llama4:scout" in mac_studio_models:
                        self.log_success("llama4:scout model available")
                    else:
                        self.log_warning("llama4:scout model not found")
                else:
                    self.log_warning("No Mac Studio models found")
                
                if gemini_models:
                    self.log_success(f"Gemini models: {len(gemini_models)}")
                else:
                    self.log_info("Gemini models not configured (optional)")
                    
            else:
                self.log_error(f"Models endpoint returned {response.status_code}")
                
        except Exception as e:
            self.log_error(f"LLM models test failed: {e}")
    
    def test_task_execution(self):
        """Test task execution (if service is running)"""
        print("\n🚀 Testing Task Execution...")
        
        try:
            # Simple test task
            test_command = "Navigate to Google homepage and verify it loads"
            
            response = requests.post(
                f"{self.base_url}/api/execute",
                json={
                    "command": test_command,
                    "llm_provider": "mac_studio",
                    "llm_model": "llama4:scout"
                },
                timeout=10
            )
            
            if response.status_code == 200:
                task_data = response.json()
                task_id = task_data.get("task_id")
                
                if task_id:
                    self.log_success(f"Task created successfully: {task_id}")
                    
                    # Check task status
                    time.sleep(2)
                    status_response = requests.get(f"{self.base_url}/api/tasks/{task_id}")
                    if status_response.status_code == 200:
                        status_data = status_response.json()
                        self.log_success(f"Task status: {status_data.get('status')}")
                    else:
                        self.log_warning("Could not retrieve task status")
                else:
                    self.log_error("No task ID returned")
            else:
                self.log_error(f"Task execution failed: {response.status_code}")
                
        except Exception as e:
            self.log_warning(f"Task execution test failed: {e} (Service may not be fully started)")
    
    def test_docker_setup(self):
        """Test Docker configuration"""
        print("\n🐳 Testing Docker Setup...")
        
        # Check docker-compose.yml
        if Path("docker-compose.yml").exists():
            self.log_success("docker-compose.yml exists")
            
            try:
                with open("docker-compose.yml", 'r') as f:
                    content = f.read()
                    
                if "browser-automation-service:" in content:
                    self.log_success("browser-automation-service configured")
                else:
                    self.log_error("browser-automation-service not found in docker-compose.yml")
                    
                if "8000:8000" in content:
                    self.log_success("Port 8000 mapping configured")
                else:
                    self.log_warning("Port 8000 mapping not found")
                    
            except Exception as e:
                self.log_error(f"Could not read docker-compose.yml: {e}")
        else:
            self.log_error("docker-compose.yml not found")
        
        # Check Dockerfile
        if Path("Dockerfile").exists():
            self.log_success("Dockerfile exists")
        else:
            self.log_error("Dockerfile not found")
    
    def run_validation(self):
        """Run complete validation suite"""
        print("🔍 Browser Automation Service Validation")
        print("=" * 50)
        
        self.test_file_structure()
        self.test_docker_setup()
        self.test_service_health()
        self.test_api_endpoints()
        self.test_prompt_system()
        self.test_llm_models()
        self.test_task_execution()
        
        # Summary
        print("\n" + "=" * 50)
        print("📊 VALIDATION SUMMARY")
        print("=" * 50)
        
        if not self.errors and not self.warnings:
            print("🎉 ALL TESTS PASSED! Service is ready for use.")
            return True
        
        if self.warnings:
            print(f"⚠️  {len(self.warnings)} warnings:")
            for warning in self.warnings:
                print(f"   • {warning}")
        
        if self.errors:
            print(f"❌ {len(self.errors)} errors:")
            for error in self.errors:
                print(f"   • {error}")
            
            print("\n💡 To fix errors:")
            print("   1. Make sure all required files are present")
            print("   2. Start the service: docker compose up browser-automation-service")
            print("   3. Check logs: docker compose logs browser-automation-service")
            
            return False
        
        print("\n✅ Service validation completed with warnings only.")
        return True

def main():
    """Main validation function"""
    print("🚀 Browser Automation Service Validator")
    print("This script validates your service setup and configuration.\n")
    
    validator = ServiceValidator()
    success = validator.run_validation()
    
    if success:
        print("\n🎯 Next steps:")
        print("   • Start service: docker compose up browser-automation-service")
        print("   • API docs: http://localhost:8000/docs")
        print("   • Test API: curl http://localhost:8000/api/health")
        sys.exit(0)
    else:
        print("\n🔧 Fix the errors above and run validation again.")
        sys.exit(1)

if __name__ == "__main__":
    main()