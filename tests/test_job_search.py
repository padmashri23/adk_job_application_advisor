"""Tests for job_search tool."""
import pytest
from job_application_agent.tools.job_search import search_jobs


class TestSearchJobs:
    def test_returns_all_platforms(self):
        result = search_jobs("Python Developer")
        assert "LinkedIn" in result
        assert "Indeed" in result
        assert "Naukri" in result
        assert "Glassdoor" in result
        assert "Wellfound" in result
        assert "Internshala" in result

    def test_urls_contain_job_title(self):
        result = search_jobs("Data Scientist", "Bangalore")
        assert "Data+Scientist" in result["LinkedIn"] or "Data%20Scientist" in result["LinkedIn"]
        assert "Data" in result["Indeed"]

    def test_default_location_india(self):
        result = search_jobs("Developer")
        assert "India" in result["LinkedIn"]

    def test_custom_location(self):
        result = search_jobs("Developer", "New York")
        assert "New" in result["LinkedIn"]

    def test_naukri_includes_location(self):
        result = search_jobs("Python Developer", "Mumbai")
        assert "mumbai" in result["Naukri"].lower()

    def test_empty_job_title_returns_error(self):
        result = search_jobs("")
        assert "error" in result

    def test_whitespace_job_title_returns_error(self):
        result = search_jobs("   ")
        assert "error" in result

    def test_strips_whitespace(self):
        result = search_jobs("  Python Developer  ", "  India  ")
        assert "Python" in result["LinkedIn"]
        assert "error" not in result

    def test_urls_are_valid_https(self):
        result = search_jobs("Engineer")
        for platform, url in result.items():
            assert url.startswith("https://"), f"{platform} URL is not HTTPS"

    def test_special_characters_encoded(self):
        result = search_jobs("C++ Developer")
        # URL encoding should handle the + signs
        assert "error" not in result
        assert "LinkedIn" in result
