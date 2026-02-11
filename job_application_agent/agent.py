from google.adk.agents import LlmAgent
from datetime import datetime
from .tools import search_jobs, get_dsa_roadmap, get_resume_tips, get_portfolio_ideas

current_date = datetime.now().strftime("%B %d, %Y")

root_agent = LlmAgent(
    name="career_catalyst",
    model="groq/llama-3.1-8b-instant",
    description="AI career assistant.",
    instruction=f"""You are Career Catalyst - a helpful job search assistant.

IMPORTANT: Today's date is {current_date}. Use this for any date/age calculations.

Use tools when needed:
- search_jobs(job_title, location): Get job URLs from LinkedIn, Indeed, Naukri, Glassdoor
- get_dsa_roadmap(weeks): Get DSA study plan
- get_resume_tips(): Get resume advice  
- get_portfolio_ideas(tech): Get project ideas

Be concise and helpful.""",
    tools=[search_jobs, get_dsa_roadmap, get_resume_tips, get_portfolio_ideas],
)

