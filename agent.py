
from datetime import datetime, timedelta
from typing import Dict, List
from langchain_openai import ChatOpenAI
from crewai import Agent, Task, Crew, Process, LLM
from dotenv import load_dotenv
import os
from tools import serper_tool

load_dotenv()

GEMINI_KEY = os.getenv("GEMINI_API_KEY")

llm = LLM(
    model="gemini/gemini-2.0-flash", 
    verbose=True,
    temperature=0.5,
    api_key=GEMINI_KEY 
)

    

research_agent = Agent(
            role="Travel Research Expert",
            goal="Gather detailed information about destinations, attractions, and local insights",
            backstory="You are a knowledgeable travel researcher with expertise in global destinations and local experiences.",
            llm=llm,
            verbose=True,
            memory=True,
            allow_delegation=True,
            tools=[serper_tool],
        )
        
        
planning_agent = Agent(
            role="Itinerary Planning Specialist", 
            goal="Create optimized, realistic travel itineraries that maximize enjoyment and efficiency",
            backstory="You are an experienced travel planner who creates perfect itineraries balancing activities, rest, and travel time.",
            llm=llm,
            verbose=True,
             tools=[serper_tool]
        )
        
        # Budget Agent
budget_agent = Agent(
            role="Budget Optimization Expert",
            goal="Ensure travel plans are financially feasible and provide best value",
            backstory="You specialize in travel budgeting and finding cost-effective solutions without compromising quality.",
            llm=llm,
            verbose=True,
             tools=[serper_tool]
        )