"""
Anti-Bot Scenario Examples
Different use cases where visual AI navigation is essential
"""

from production_visual_agent import create_production_agent
import asyncio

# Scenario 1: E-commerce with heavy protection
async def protected_ecommerce_search():
    """Search for products on heavily protected e-commerce sites"""
    
    task = """
    Go to Amazon and search for 'gaming laptop under $1000'.
    Navigate through the results and find the top 3 laptops with:
    - Price
    - Rating 
    - Key specifications
    Handle any CAPTCHAs or bot detection gracefully.
    """
    
    agent = await create_production_agent(task, model="llama4:scout")
    
    print("🛡️ Testing anti-bot navigation on e-commerce...")
    result = await agent.run()
    await agent.close()
    
    return result

# Scenario 2: Financial data with authentication
async def financial_data_extraction():
    """Extract financial data from protected financial sites"""
    
    task = """
    Search for 'Tesla stock price today earnings' on a financial website.
    Extract current stock price, market cap, and recent news.
    Be patient with loading times and dynamic content.
    """
    
    agent = await create_production_agent(task, model="maverick")  # Use maverick for complex reasoning
    
    print("💰 Testing financial data extraction...")
    result = await agent.run()
    await agent.close()
    
    return result

# Scenario 3: Social media monitoring
async def social_media_research():
    """Research topics on social media platforms with bot protection"""
    
    task = """
    Search for discussions about 'AI browser automation' on recent social media.
    Find 3-5 recent posts or discussions about this topic.
    Note any trends or common opinions.
    """
    
    agent = await create_production_agent(task, model="llama4:scout")
    
    print("📱 Testing social media research...")
    result = await agent.run()
    await agent.close()
    
    return result

# Scenario 4: Real estate with CAPTCHA protection
async def real_estate_search():
    """Search real estate listings on protected sites"""
    
    task = """
    Search for 'homes for sale San Francisco under 2 million' on a real estate website.
    Find 3 listings with:
    - Address
    - Price
    - Bedrooms/bathrooms
    - Square footage
    Handle any verification steps.
    """
    
    agent = await create_production_agent(task, model="maverick")
    
    print("🏠 Testing real estate search with anti-bot...")
    result = await agent.run()
    await agent.close()
    
    return result

async def main():
    """Demo different anti-bot scenarios"""
    
    print("🤖 Mac Studio Anti-Bot Visual Navigation Demos")
    print("=" * 50)
    
    scenarios = {
        "1": ("E-commerce Search", protected_ecommerce_search),
        "2": ("Financial Data", financial_data_extraction), 
        "3": ("Social Media Research", social_media_research),
        "4": ("Real Estate Search", real_estate_search),
    }
    
    print("Available scenarios:")
    for key, (name, _) in scenarios.items():
        print(f"{key}. {name}")
    
    choice = input("\nChoose scenario (1-4): ").strip()
    
    if choice in scenarios:
        name, func = scenarios[choice]
        print(f"\n🚀 Starting: {name}")
        print("⏱️ This will take several minutes due to visual processing...")
        
        result = await func()
        print(f"\n✅ {name} completed!")
        print("📝 Result:", result)
    else:
        print("Invalid choice. Running financial data demo...")
        await financial_data_extraction()

if __name__ == "__main__":
    asyncio.run(main()) 