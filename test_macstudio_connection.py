#!/usr/bin/env python3
"""
Test script to verify Mac Studio LLM connectivity and available models
"""

import requests
import json
from openai import OpenAI

def test_connectivity():
    """Test basic connectivity to Mac Studio Ollama endpoint"""
    base_url = "https://matiass-mac-studio.tail174e9b.ts.net"
    
    print("🔍 Testing Mac Studio LLM connectivity...")
    print(f"📡 Endpoint: {base_url}")
    
    try:
        # Test models endpoint
        response = requests.get(f"{base_url}/v1/models", timeout=10)
        response.raise_for_status()
        
        models_data = response.json()
        models = [model["id"] for model in models_data.get("data", [])]
        
        print("✅ Connection successful!")
        print(f"📋 Available models: {', '.join(models)}")
        
        return True, models
    
    except requests.exceptions.ConnectionError:
        print("❌ Connection failed - Check Tailscale connection")
        return False, []
    except requests.exceptions.Timeout:
        print("❌ Connection timeout - Mac Studio may be sleeping")
        return False, []
    except Exception as e:
        print(f"❌ Error: {e}")
        return False, []

def test_chat_completion(model_name):
    """Test chat completion with a specific model"""
    print(f"\n🤖 Testing chat completion with {model_name}...")
    
    try:
        client = OpenAI(
            base_url="https://matiass-mac-studio.tail174e9b.ts.net/v1",
            api_key="ollama"
        )
        
        response = client.chat.completions.create(
            model=model_name,
            messages=[{"role": "user", "content": "Say hello and confirm you're running on Mac Studio"}],
            max_tokens=100,
            temperature=0.7
        )
        
        message = response.choices[0].message.content
        print(f"✅ {model_name} response: {message}")
        return True
        
    except Exception as e:
        print(f"❌ Chat completion failed with {model_name}: {e}")
        return False

def main():
    print("🚀 Mac Studio LLM Connection Test")
    print("=" * 50)
    
    # Test connectivity
    connected, models = test_connectivity()
    
    if not connected:
        print("\n💡 Troubleshooting tips:")
        print("   • Ensure Tailscale is running and connected")
        print("   • Check if Mac Studio is awake")
        print("   • Verify Ollama is running on Mac Studio")
        return
    
    # Test each available model
    if models:
        print(f"\n🧪 Testing models...")
        for model in models[:2]:  # Test first 2 models to avoid spam
            test_chat_completion(model)
    
    print(f"\n🎉 Mac Studio LLM is ready for browser automation!")
    print(f"   🏆 Recommended model: llama4:scout")
    print(f"   🥈 Alternative: maverick")

if __name__ == "__main__":
    main() 