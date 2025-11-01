from crewai import Task

def create_research_task(destination_info, destination, duration, travelers, interests, budget, research_agent):
    return Task(
        description=f"""Research {destination} using this search information:
        
        {destination_info}
        
        Duration: {duration} days
        Travelers: {travelers} people
        Interests: {', '.join(interests)}
        Budget: ${budget}
        
        Analyze and extract key insights about attractions, culture, transportation, food, and safety.""",
        agent=research_agent,
        expected_output="Destination analysis with key insights"
    )

def create_planning_task(duration, destination, budget, travelers, interests, planning_agent, research_task):
    return Task(
        description=f"""Create a detailed {duration}-day itinerary for {destination}:
        
        Requirements:
        - Duration: {duration} days
        - Budget: ${budget} total
        - Travelers: {travelers} people
        - Interests: {', '.join(interests)}
        
        Include day-by-day schedule, logical flow, activity mix, and practical tips.""",
        agent=planning_agent,
        expected_output=f"Detailed {duration}-day itinerary with daily schedule",
        context=[research_task]
    )