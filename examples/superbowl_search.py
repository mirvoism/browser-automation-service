from langchain_google_genai import ChatGoogleGenerativeAI
from browser_use import Agent
import asyncio
from dotenv import load_dotenv
import google.generativeai as genai
import os

# Load environment variables
load_dotenv()

# Configure Gemini
genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))

async def main():
    print("\nSearching for SuperBowl 2025 information...")
    
    agent = Agent(
        task="Go to Google, search for 'SuperBowl 2025', find the first result that shows the teams and score, and extract: 1. The two teams that played, 2. The final score, 3. The date of the game",
        llm=ChatGoogleGenerativeAI(
            model="gemini-1.5-flash",
            temperature=0.7,
        ),
    )
    
    result = await agent.run()
    print("\nTask Result:", result)

if __name__ == "__main__":
    asyncio.run(main()) 