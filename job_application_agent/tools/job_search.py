"""Job Search Tool"""
import urllib.parse

def search_jobs(job_title: str, location: str = "India") -> dict:
    """Get job URLs from LinkedIn, Indeed, Naukri, Glassdoor."""
    e = urllib.parse.quote
    slug = job_title.lower().replace(" ", "-")
    return {
        "LinkedIn": f"https://www.linkedin.com/jobs/search/?keywords={e(job_title)}&location={e(location)}",
        "Indeed": f"https://in.indeed.com/jobs?q={e(job_title)}&l={e(location)}",
        "Naukri": f"https://www.naukri.com/{slug}-jobs",
        "Glassdoor": f"https://www.glassdoor.co.in/Job/jobs.htm?sc.keyword={e(job_title)}",
    }
