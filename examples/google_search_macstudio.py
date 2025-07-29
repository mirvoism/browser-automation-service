from browser_use.llm.openai.chat import ChatOpenAI
from browser_use import Agent
import asyncio
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

async def main():
    # Initialize the agent using Mac Studio LLM endpoint
    agent = Agent(
        task="Go to Google, search for 'browser-use github', and return the first result.",
        llm=ChatOpenAI(
            base_url="https://matiass-mac-studio.tail174e9b.ts.net/v1",
            api_key="ollama",  # placeholder - Ollama ignores this
            model="llama4:scout",  # Using Llama4:scout - best for browser automation
            temperature=0.7,
        ),
    )
    
    # Run the agent and get the result
    result = await agent.run()
    print("Task Result:", result)

if __name__ == "__main__":
    asyncio.run(main()) 