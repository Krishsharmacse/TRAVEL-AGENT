# crew.py
from crewai import Crew, Process
from backend.agent import research_agent, planning_agent, budget_agent
from backend.task import create_itinerary


def run_travel_itinerary(destination: str, duration: int, budget: float, travelers: int, interests: list[str]):
    research_task, planning_task, budget_task = create_itinerary(
        destination, duration, budget, travelers, interests
    )

    travel_crew = Crew(
        agents=[research_agent, planning_agent, budget_agent],
        tasks=[research_task, planning_task, budget_task],
        process=Process.sequential,
        verbose=True
    )

    result = travel_crew.kickoff()
    return result
