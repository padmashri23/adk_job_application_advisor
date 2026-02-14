"""Job Search Tool - Generate search URLs across multiple job boards."""
import urllib.parse
import logging

logger = logging.getLogger(__name__)

SUPPORTED_PLATFORMS = [
    "LinkedIn", "Indeed", "Naukri", "Glassdoor", "Wellfound", "Internshala"
]


def search_jobs(job_title: str, location: str = "India") -> dict:
    """Search for jobs across multiple job boards and return direct search URLs.

    Args:
        job_title: The job title or role to search for (e.g., "Python Developer").
        location: The job location or region (default: "India").

    Returns:
        A dict with job board names as keys and search URLs as values.
    """
    if not job_title or not job_title.strip():
        return {"error": "job_title is required and cannot be empty."}

    job_title = job_title.strip()
    location = location.strip() if location else "India"

    encode = urllib.parse.quote
    slug = job_title.lower().replace(" ", "-")
    location_slug = location.lower().replace(" ", "-")

    urls = {
        "LinkedIn": (
            f"https://www.linkedin.com/jobs/search/"
            f"?keywords={encode(job_title)}&location={encode(location)}"
        ),
        "Indeed": (
            f"https://www.indeed.com/jobs"
            f"?q={encode(job_title)}&l={encode(location)}"
        ),
        "Naukri": (
            f"https://www.naukri.com/{slug}-jobs-in-{location_slug}"
        ),
        "Glassdoor": (
            f"https://www.glassdoor.co.in/Job/jobs.htm"
            f"?sc.keyword={encode(job_title)}&locT=C&locKeyword={encode(location)}"
        ),
        "Wellfound": (
            f"https://wellfound.com/role/r/{slug}"
        ),
        "Internshala": (
            f"https://internshala.com/jobs/{slug}-jobs-in-{location_slug}"
        ),
    }

    logger.info("Generated job search URLs for '%s' in '%s'", job_title, location)
    return urls
