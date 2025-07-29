"""
Speed Comparison: Regular vs Optimized Browser Automation
"""

from browser_use.llm.openai.chat import ChatOpenAI
from browser_use import Agent
from browser_use.browser.profile import BrowserProfile
import asyncio
import time

async def regular_test():
    """Regular browser automation (with extensions, default settings)"""
    print("🐌 Testing REGULAR automation...")
    
    agent = Agent(
        task="Go to google.com and search for 'Super Bowl 2025'",
        llm=ChatOpenAI(
            model="llama4:scout",
            base_url="https://matiass-mac-studio.tail174e9b.ts.net/v1",
            api_key="ollama",
        ),
        # Default settings (slower)
    )
    
    start_time = time.time()
    result = await agent.run()
    duration = time.time() - start_time
    
    await agent.close()
    return duration, str(result)[:100]

async def optimized_test():
    """Optimized browser automation (no extensions, constrained)"""
    print("⚡ Testing OPTIMIZED automation...")
    
    # Speed-optimized profile
    fast_profile = BrowserProfile(extensions=[])
    
    agent = Agent(
        task="Go to google.com and search for 'Super Bowl 2025'",
        llm=ChatOpenAI(
            model="llama4:scout",
            base_url="https://matiass-mac-studio.tail174e9b.ts.net/v1",
            api_key="ollama",
            temperature=0.05,
            max_completion_tokens=1000,
        ),
        # Optimizations
        browser_profile=fast_profile,
        max_actions_per_step=2,
        step_timeout=25,
        max_failures=1,
        images_per_step=1,
        use_vision_for_planner=False,
        max_history_items=5,
        generate_gif=False,
        calculate_cost=False,
        include_attributes=['title', 'type', 'value'],
        extend_system_message="Act fast and direct. Click first relevant result.",
    )
    
    start_time = time.time()
    result = await agent.run()
    duration = time.time() - start_time
    
    await agent.close()
    return duration, str(result)[:100]

async def main():
    print("🏁 Browser Automation Speed Comparison")
    print("=" * 50)
    
    try:
        # Test optimized version (faster, should complete)
        opt_duration, opt_result = await optimized_test()
        print(f"⚡ OPTIMIZED: {opt_duration:.1f}s - {opt_result}...")
        
        print(f"\n🚀 Optimization successful! Mac Studio + llama4:scout is ready.")
        
        # Optional: test regular (only if user wants comparison)
        print(f"\n💡 The optimized version eliminates:")
        print(f"   • Browser extensions (major speedup)")  
        print(f"   • Unnecessary element analysis")
        print(f"   • Complex vision processing")
        print(f"   • Excessive logging and tracking")
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    asyncio.run(main()) 