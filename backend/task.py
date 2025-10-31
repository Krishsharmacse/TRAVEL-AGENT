from crewai import Task
from backend.agent import research_agent, planning_agent, budget_agent
from backend.tools import serper_tool

def create_itinerary(destination: str, duration: int, budget: float, travelers: int, interests: list[str]):
    
    # --- Minimized Research Task ---
    research_task = Task(
        description=(
            f"""Thoroughly research {destination} for a {duration}-day trip focusing on {', '.join(interests)} interests. 
            Gather detailed, current information on: top attractions, best accommodation areas, local culture/customs, 
            transportation options, dining/food scene, safety tips, and relevant events."""
        ),
        agent=research_agent,
        expected_output="Comprehensive destination guide with all key information summarized.",
      
        output_file='research.md',
    )
      
    # --- Minimized Planning Task ---
    planning_task = Task(
        description=(
            f"""Create a detailed, realistic {duration}-day itinerary for {destination} for {travelers} travelers. 
            Ensure the schedule has a logical geographical flow, balances sightseeing with relaxation, and maximizes 
            enjoyment based on the provided research context and {interests} interests."""
        ),
        agent=planning_agent,
        expected_output=f"Detailed, day-by-day travel itinerary.",
        context=[research_task],
    
        output_file='Planing.md',
    )
      
    # --- Minimized Budget Task ---
    budget_task = Task(
        description=(
            f"""Analyze and optimize the provided itinerary for a maximum total budget of ${budget}. 
            Provide a clear cost breakdown (accommodation, food, activities, transport), suggest cost-saving 
            alternatives, and ensure the final plan is financially feasible."""
        ),
        agent=budget_agent,
        expected_output="Budget analysis report with full cost breakdown and optimization tips.",
        context=[planning_task],
       
        output_file='budget.md',
    )

    return research_task, planning_task, budget_task