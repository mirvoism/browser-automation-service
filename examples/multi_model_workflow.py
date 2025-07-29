"""
Multi-Model Workflow Example
Demonstrates using different Mac Studio models for different parts of a complex task
"""

from browser_use.llm.openai.chat import ChatOpenAI
from browser_use import Agent
import asyncio
import time

async def search_with_scout(search_query):
    """Use llama4:scout for initial search and navigation"""
    print(f"🔍 Step 1: Using llama4:scout for search...")
    
    agent = Agent(
        task=f"Go to Google, search for '{search_query}', and find the most relevant result. Click on it and summarize what you find on the first page.",
        llm=ChatOpenAI(
            base_url="https://matiass-mac-studio.tail174e9b.ts.net/v1",
            api_key="ollama",
            model="llama4:scout",  # Best for navigation and search
            temperature=0.3,
        ),
    )
    
    result = await agent.run()
    print(f"✅ Scout found: {str(result)[:200]}...")
    return result

async def analyze_with_maverick(initial_findings):
    """Use maverick for complex analysis and decision-making"""
    print(f"\n🧠 Step 2: Using maverick for detailed analysis...")
    
    agent = Agent(
        task=f"Based on the previous findings, navigate to find more detailed information. Look for specific data points, numbers, or technical details. Extract and organize the key information systematically.",
        llm=ChatOpenAI(
            base_url="https://matiass-mac-studio.tail174e9b.ts.net/v1",
            api_key="ollama",
            model="maverick",  # Best for complex reasoning and extraction
            temperature=0.2,  # Lower temperature for more precise analysis
        ),
    )
    
    result = await agent.run()
    print(f"✅ Maverick analyzed: {str(result)[:200]}...")
    return result

async def comprehensive_research_workflow():
    """Demonstrate a multi-model workflow for comprehensive research"""
    print("🚀 Multi-Model Research Workflow")
    print("=" * 50)
    
    search_topic = "renewable energy storage solutions 2024"
    
    start_time = time.time()
    
    # Step 1: Use scout for initial search and navigation
    initial_findings = await search_with_scout(search_topic)
    
    # Step 2: Use maverick for detailed analysis  
    detailed_analysis = await analyze_with_maverick(initial_findings)
    
    end_time = time.time()
    total_duration = end_time - start_time
    
    print(f"\n📊 Workflow Complete!")
    print(f"⏱️  Total time: {total_duration:.1f} seconds")
    print(f"🎯 Strategy: Scout for navigation, Maverick for analysis")
    
    return {
        "search_results": initial_findings,
        "detailed_analysis": detailed_analysis,
        "total_time": total_duration
    }

async def compare_single_vs_multi_model():
    """Compare using one model vs strategic multi-model approach"""
    print("\n⚔️  Single Model vs Multi-Model Comparison")
    print("=" * 50)
    
    task = "Research electric vehicle charging infrastructure and extract key statistics"
    
    # Single model approach (maverick for everything)
    print("🔄 Testing single model approach (maverick only)...")
    start_time = time.time()
    
    single_agent = Agent(
        task=f"{task}. Start by searching Google, then navigate and extract detailed information.",
        llm=ChatOpenAI(
            base_url="https://matiass-mac-studio.tail174e9b.ts.net/v1",
            api_key="ollama",
            model="maverick",
            temperature=0.3,
        ),
    )
    
    single_result = await single_agent.run()
    single_time = time.time() - start_time
    
    print(f"✅ Single model completed in {single_time:.1f}s")
    
    # Multi-model approach would go here if we wanted to run both
    # (Commented out to avoid long execution)
    """
    print("🔄 Testing multi-model approach...")
    multi_start = time.time()
    multi_result = await comprehensive_research_workflow()
    multi_time = time.time() - multi_start
    
    print(f"✅ Multi-model completed in {multi_time:.1f}s")
    """
    
    print(f"\n💡 Strategy Insights:")
    print(f"   • Single model: Simple setup, may be slower for complex tasks")
    print(f"   • Multi-model: Optimized performance, each model for its strength")
    print(f"   • Use scout for navigation, maverick for analysis")

async def main():
    """Main function to run the examples"""
    choice = input("\nChoose example:\n1. Multi-model workflow\n2. Single vs Multi comparison\nEnter (1 or 2): ").strip()
    
    if choice == "1":
        await comprehensive_research_workflow()
    elif choice == "2":
        await compare_single_vs_multi_model()
    else:
        print("Running comprehensive research workflow by default...")
        await comprehensive_research_workflow()

if __name__ == "__main__":
    asyncio.run(main()) 