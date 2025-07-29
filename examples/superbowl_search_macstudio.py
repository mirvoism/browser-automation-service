from browser_use.llm.openai.chat import ChatOpenAI
from browser_use import Agent
import asyncio
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

async def main():
    print("\nSearching for SuperBowl 2025 information using Mac Studio LLM...")
    
    agent = Agent(
        task="Go to Google, search for 'SuperBowl 2025', find the first result that shows the teams and score, and extract: 1. The two teams that played, 2. The final score, 3. The date of the game",
        llm=ChatOpenAI(
            base_url="https://matiass-mac-studio.tail174e9b.ts.net/v1",
            api_key="ollama",  # placeholder - Ollama ignores this
            model="llama4:scout",  # Using Llama4:scout - best for browser automation
            temperature=0.7,
        ),
    )
    
    result = await agent.run()
    print("\nTask Result:", result)

if __name__ == "__main__":
    asyncio.run(main()) 