# tools.py
from crewai_tools import SerperDevTool
import os
from dotenv import load_dotenv

load_dotenv()

serper_tool = SerperDevTool(
    api_key=os.getenv("SERPER_API_KEY"),
   
)
