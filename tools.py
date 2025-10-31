# tools.py
from crewai_tools import SerperDevTool
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize the Serper tool
serper_tool = SerperDevTool(
    api_key=os.getenv("SERPER_API_KEY"),
   
)
