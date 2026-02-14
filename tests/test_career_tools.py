"""Tests for career_tools."""
import pytest
from job_application_agent.tools.career_tools import (
    get_dsa_roadmap,
    get_resume_tips,
    get_portfolio_ideas,
)


class TestGetDsaRoadmap:
    def test_default_4_weeks(self):
        result = get_dsa_roadmap()
        assert "Week 1" in result
        assert "Week 4" in result

    def test_custom_weeks(self):
        result = get_dsa_roadmap(8)
        assert "Week 1" in result
        assert "Week 8" in result

    def test_1_week_plan(self):
        result = get_dsa_roadmap(1)
        assert "Week 1" in result

    def test_16_week_plan(self):
        result = get_dsa_roadmap(16)
        assert "Week 1" in result

    def test_clamps_to_max_16(self):
        result = get_dsa_roadmap(100)
        # 15 topics available, so max 15 weeks even if more requested
        assert "Week 15" in result
        assert "Week 17" not in result

    def test_clamps_to_min_1(self):
        result = get_dsa_roadmap(0)
        assert "Week 1" in result

    def test_negative_weeks_clamps_to_1(self):
        result = get_dsa_roadmap(-5)
        assert "Week 1" in result

    def test_includes_practice_tip(self):
        result = get_dsa_roadmap()
        assert "Tip:" in result

    def test_includes_problem_counts(self):
        result = get_dsa_roadmap()
        assert "problems" in result

    def test_different_weeks_give_different_plans(self):
        plan_2 = get_dsa_roadmap(2)
        plan_8 = get_dsa_roadmap(8)
        assert plan_2 != plan_8


class TestGetResumeTips:
    def test_returns_string(self):
        result = get_resume_tips()
        assert isinstance(result, str)

    def test_has_categories(self):
        result = get_resume_tips()
        assert "Format" in result
        assert "Content" in result
        assert "Mistakes To Avoid" in result

    def test_has_actionable_tips(self):
        result = get_resume_tips()
        assert "Quantify" in result
        assert "action verbs" in result

    def test_not_empty(self):
        result = get_resume_tips()
        assert len(result) > 100


class TestGetPortfolioIdeas:
    def test_default_python(self):
        result = get_portfolio_ideas()
        assert "Python" in result

    def test_javascript_ideas(self):
        result = get_portfolio_ideas("JavaScript")
        assert "JavaScript" in result
        assert "React" in result or "Next.js" in result

    def test_java_ideas(self):
        result = get_portfolio_ideas("Java")
        assert "Java" in result
        assert "Spring" in result

    def test_unknown_tech_uses_default(self):
        result = get_portfolio_ideas("Haskell")
        assert "Haskell" in result
        assert "REST API" in result

    def test_empty_tech_defaults_to_python(self):
        result = get_portfolio_ideas("")
        assert "Python" in result

    def test_includes_tip(self):
        result = get_portfolio_ideas()
        assert "Tip:" in result

    def test_case_insensitive(self):
        result1 = get_portfolio_ideas("python")
        result2 = get_portfolio_ideas("PYTHON")
        # Both should get Python-specific ideas
        assert "FastAPI" in result1
        assert "FastAPI" in result2
