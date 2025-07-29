"""
Production Visual Browser Agent - Anti-Bot Ready
Optimized for websites with heavy anti-bot protection
Accepts slower speed as trade-off for human-like behavior
"""

from browser_use.llm.openai.chat import ChatOpenAI
from browser_use import Agent
from browser_use.browser.profile import BrowserProfile
import asyncio
import time
import random

async def create_production_agent(task: str, model: str = "llama4:scout") -> Agent:
    """Create a production-ready visual agent for anti-bot scenarios"""
    
    # Anti-bot optimized browser profile
    anti_bot_profile = BrowserProfile(
        viewport_size=(1920, 1080),  # Common desktop resolution
        user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        # Keep some extensions to look more human-like
        extensions=[],  # Can be enabled if needed
    )
    
    agent = Agent(
        task=task,
        
        # Mac Studio LLM Configuration
        llm=ChatOpenAI(
            model=model,
            base_url="https://matiass-mac-studio.tail174e9b.ts.net/v1",
            api_key="ollama",
            temperature=0.2,  # Balanced for consistency
            max_completion_tokens=3000,
        ),
        
        # Anti-Bot Optimized Settings
        browser_profile=anti_bot_profile,
        
        # Timing - Accept slower speed for reliability
        step_timeout=90,              # Longer timeout for visual processing
        max_failures=3,               # More retries for robust operation
        retry_delay=5,                # Human-like delays
        
        # Visual Processing
        use_vision=True,              # Essential for anti-bot
        images_per_step=1,            # Efficient but thorough
        use_vision_for_planner=True,  # Better decision making
        
        # Memory and History
        max_history_items=20,         # Better context retention
        max_actions_per_step=3,       # Balanced efficiency
        
        # Human-like Behavior Instructions
        extend_system_message="""
        ANTI-BOT OPERATION MODE:
        1. Act like a real human - take time to "read" pages
        2. Use natural mouse movements and reasonable delays
        3. If you encounter CAPTCHAs or bot detection, pause and report
        4. Focus on completing the task thoroughly, not quickly
        5. Look for multiple ways to complete actions if blocked
        6. Pay attention to page loading and dynamic content
        7. Extract all requested information before concluding
        """,
        
        # Performance monitoring
        generate_gif=False,           # Disable for performance
        save_conversation_path=None,  # Optional: enable for debugging
        calculate_cost=True,          # Monitor token usage
    )
    
    return agent

async def visual_search_task(search_query: str, extract_info: str):
    """
    Production visual search task
    Designed to work with anti-bot protection
    """
    
    task = f"""
    Go to Google and search for '{search_query}'. 
    Navigate through the results to find {extract_info}.
    Take your time to analyze pages thoroughly.
    If you encounter any anti-bot measures, report them.
    Return the specific information requested.
    """
    
    print(f"🤖 Starting VISUAL search for: {search_query}")
    print(f"🎯 Goal: Extract {extract_info}")
    print(f"⏱️ Expected time: 3-5 minutes (visual processing)")
    print("=" * 60)
    
    agent = await create_production_agent(task)
    
    start_time = time.time()
    
    try:
        # Add random delay to appear more human
        await asyncio.sleep(random.uniform(1, 3))
        
        result = await agent.run()
        
        end_time = time.time()
        duration = end_time - start_time
        
        print(f"\n✅ VISUAL TASK COMPLETED!")
        print(f"⏱️ Total time: {duration/60:.1f} minutes")
        print(f"🎯 Result: {result}")
        
        return result
        
    except Exception as e:
        end_time = time.time()
        duration = end_time - start_time
        
        print(f"\n⚠️ Task encountered issues after {duration/60:.1f} minutes")
        print(f"❌ Error: {e}")
        print(f"💡 This may be due to anti-bot measures or complex page structure")
        
        return None
        
    finally:
        await agent.close()

async def test_super_bowl_search():
    """Test case: Super Bowl 2025 search with anti-bot handling"""
    
    result = await visual_search_task(
        search_query="Super Bowl 2025 results score teams",
        extract_info="the two teams that played and the final score"
    )
    
    return result

async def test_financial_data():
    """Test case: Financial data extraction (less anti-bot protection)"""
    
    result = await visual_search_task(
        search_query="AGG ETF fund yield duration",
        extract_info="current yield percentage and duration"
    )
    
    return result

async def main():
    """Main function with test options"""
    
    print("🚀 Mac Studio Visual Browser Agent - Anti-Bot Ready")
    print("=" * 60)
    print("This version prioritizes reliability over speed")
    print("Perfect for bypassing anti-bot protection")
    print("")
    
    # Choose test
    choice = input("Choose test:\n1. Super Bowl 2025 search\n2. Financial data (AGG ETF)\n3. Custom search\nEnter (1/2/3): ").strip()
    
    if choice == "1":
        await test_super_bowl_search()
    elif choice == "2":
        await test_financial_data()
    elif choice == "3":
        query = input("Enter search query: ")
        info = input("What info to extract: ")
        await visual_search_task(query, info)
    else:
        print("Running Super Bowl search by default...")
        await test_super_bowl_search()

if __name__ == "__main__":
    asyncio.run(main()) 