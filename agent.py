from langchain_openai import ChatOpenAI
from crewai import Agent,LLM
import os
from dotenv import load_dotenv

load_dotenv()

GEMINI_KEY = os.getenv("GEMINI_API_KEY")

llm = LLM(
    model="gemini/gemini-2.0-flash",
    verbose=True,
    temperature=0.5,
    api_key=GEMINI_KEY
)

def create_research_agent():
    return Agent(
        role="Travel Research Expert",
        goal="Gather detailed information about destinations using web search",
        backstory="You are a travel researcher who finds current destination information.",
        llm=llm,
        verbose=True
    )

def create_planning_agent():
    return Agent(
        role="Itinerary Planning Specialist",
        goal="Create optimized travel itineraries",
        backstory="You create practical travel itineraries balancing activities and rest.",
        llm=llm,
        verbose=True
    )