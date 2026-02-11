from google.adk.agents import LlmAgent
from .tools import search_jobs, get_dsa_roadmap, get_resume_tips, get_portfolio_ideas

root_agent = LlmAgent(
    name="career_catalyst",
    model="groq/llama-3.1-8b-instant",
    description="AI career assistant.",
    instruction="""You are Career Catalyst - a helpful job search assistant.

Use tools when needed:
- search_jobs(job_title, location): Get job URLs from LinkedIn, Indeed, Naukri, Glassdoor
- get_dsa_roadmap(weeks): Get DSA study plan
- get_resume_tips(): Get resume advice  
- get_portfolio_ideas(tech): Get project ideas

Be concise and helpful.""",
    tools=[search_jobs, get_dsa_roadmap, get_resume_tips, get_portfolio_ideas],
)

