from crewai import Crew, Process
from agent import create_research_agent, create_planning_agent
from task import create_research_task, create_planning_task
from tools import search_destination

def create_travel_itinerary(destination, duration, budget, travelers, interests):
    research_agent = create_research_agent()
    planning_agent = create_planning_agent()
    
    destination_info = search_destination(destination, duration, interests)
    
    research_task = create_research_task(
        destination_info, destination, duration, travelers, interests, budget, research_agent
    )
    
    planning_task = create_planning_task(
        duration, destination, budget, travelers, interests, planning_agent, research_task
    )
    
    travel_crew = Crew(
        agents=[research_agent, planning_agent],
        tasks=[research_task, planning_task],
        process=Process.sequential,
        verbose=True
    )
    
    return travel_crew.kickoff()