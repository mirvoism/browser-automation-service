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
    # Initialize the agent with a simple task
    agent = Agent(
        task="look up the website for AGG fund, select the official asset manager page for the fund, search for Duration and yield, and return the value of both.",
        llm=ChatGoogleGenerativeAI(
            model="gemini-1.5-flash",
            temperature=0.7,
        ),
    )
    
    # Run the agent and get the result
    result = await agent.run()
    print("Task Result:", result)

if __name__ == "__main__":
    asyncio.run(main()) 