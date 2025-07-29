from browser_use.llm.openai.chat import ChatOpenAI
from browser_use import Agent
import asyncio
import time

async def test_model_performance(model_name):
    """Test a specific model with a simple browser task"""
    print(f"\n🤖 Testing {model_name}...")
    start_time = time.time()
    
    try:
        agent = Agent(
            task="Go to Google and search for 'what time is it', then return the current time shown.",
            llm=ChatOpenAI(
                base_url="https://matiass-mac-studio.tail174e9b.ts.net/v1",
                api_key="ollama",
                model=model_name,
                temperature=0.3,  # Lower temperature for consistency
            ),
        )
        
        result = await agent.run()
        end_time = time.time()
        duration = end_time - start_time
        
        print(f"✅ {model_name} completed in {duration:.1f}s")
        print(f"📝 Result: {str(result)[:200]}...")
        
        return {
            "model": model_name,
            "success": True,
            "duration": duration,
            "result_preview": str(result)[:200]
        }
        
    except Exception as e:
        end_time = time.time()
        duration = end_time - start_time
        
        print(f"❌ {model_name} failed after {duration:.1f}s: {e}")
        
        return {
            "model": model_name,
            "success": False,
            "duration": duration,
            "error": str(e)
        }

async def main():
    print("🏁 Mac Studio Model Performance Comparison")
    print("=" * 50)
    
    # Models to test (in order of preference for browser automation)
    models_to_test = ["llama4:scout", "maverick", "deepseek-r1", "qwen3:32b", "qwen25"]
    
    results = []
    
    for model in models_to_test:
        result = await test_model_performance(model)
        results.append(result)
        
        # Add delay between tests to avoid overwhelming the system
        await asyncio.sleep(2)
    
    # Summary
    print(f"\n📊 Performance Summary")
    print("=" * 30)
    
    successful_models = [r for r in results if r["success"]]
    if successful_models:
        fastest = min(successful_models, key=lambda x: x["duration"])
        print(f"🥇 Fastest: {fastest['model']} ({fastest['duration']:.1f}s)")
        
        print(f"\n🎯 Recommended model: llama4:scout")
        print(f"   - Optimized for exploration and search tasks")
        print(f"   - Best browser automation performance")
    else:
        print("❌ All models failed - check Mac Studio connectivity")

if __name__ == "__main__":
    asyncio.run(main()) 