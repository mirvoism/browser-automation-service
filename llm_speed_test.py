"""
Direct Mac Studio LLM Speed Test
Tests the raw speed of llama4:scout without browser automation
"""

from browser_use.llm.openai.chat import ChatOpenAI
import asyncio
import time

async def test_llm_speed():
    print("🧪 Testing Mac Studio llama4:scout speed directly...")
    
    llm = ChatOpenAI(
        model="llama4:scout",
        base_url="https://matiass-mac-studio.tail174e9b.ts.net/v1", 
        api_key="ollama",
        temperature=0.3,
    )
    
    # Test different prompt sizes
    tests = [
        ("Short", "Say hello briefly"),
        ("Medium", "Explain what Super Bowl 2025 is in 2-3 sentences"),
        ("Long", "Describe the history of the Super Bowl, who typically plays, and what makes it culturally significant in America. Include details about the halftime show.")
    ]
    
    print("\n⚡ Speed Test Results:")
    print("-" * 50)
    
    for test_name, prompt in tests:
        print(f"🧠 Testing {test_name} prompt...")
        
        start_time = time.time()
        
        try:
            # Direct LLM call
            from browser_use.llm.messages import UserMessage
            messages = [UserMessage(content=prompt)]
            
            response = await llm.ainvoke(messages)
            
            end_time = time.time()
            duration = end_time - start_time
            
            response_text = response.content if hasattr(response, 'content') else str(response)
            
            print(f"✅ {test_name}: {duration:.2f}s - {response_text[:100]}...")
            
        except Exception as e:
            end_time = time.time()
            duration = end_time - start_time
            print(f"❌ {test_name}: {duration:.2f}s - Error: {e}")
    
    print(f"\n🎯 Mac Studio LLM Performance Summary:")
    print(f"   • If times are <2s: Mac Studio is VERY fast ⚡")
    print(f"   • If times are 2-5s: Normal speed 👍") 
    print(f"   • If times are >5s: Check Mac Studio load 🔍")
    print(f"\n💡 Browser automation delays are from visual processing, not LLM speed!")

if __name__ == "__main__":
    asyncio.run(test_llm_speed()) 