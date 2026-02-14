"""Tests for skill_analysis tool."""
import pytest
from job_application_agent.tools.skill_analysis import analyze_skill_gap


class TestAnalyzeSkillGap:
    def test_basic_analysis(self):
        result = analyze_skill_gap("Python, SQL, Git", "backend developer")
        assert "Readiness Score" in result
        assert "[HAVE]" in result
        assert "[NEED]" in result

    def test_high_readiness(self):
        skills = "Python, SQL, REST APIs, Git, Database Design, Docker, AWS, Redis, Testing, Message Queues"
        result = analyze_skill_gap(skills, "backend developer")
        assert "Readiness Score" in result

    def test_low_readiness(self):
        result = analyze_skill_gap("HTML", "backend developer")
        assert "Readiness Score" in result
        assert "[NEED]" in result

    def test_frontend_role(self):
        result = analyze_skill_gap("HTML, CSS, JavaScript, React, Git", "frontend developer")
        assert "[HAVE]" in result

    def test_data_scientist_role(self):
        result = analyze_skill_gap("Python, SQL, Pandas", "data scientist")
        assert "Readiness Score" in result

    def test_unknown_role_uses_default(self):
        result = analyze_skill_gap("Python, Git", "blockchain developer")
        assert "Readiness Score" in result

    def test_empty_skills_returns_error(self):
        result = analyze_skill_gap("", "backend developer")
        assert "Error" in result

    def test_whitespace_skills_returns_error(self):
        result = analyze_skill_gap("   ", "backend developer")
        assert "Error" in result

    def test_includes_action_plan(self):
        result = analyze_skill_gap("Python", "backend developer")
        assert "Action Plan" in result

    def test_case_insensitive_skills(self):
        result = analyze_skill_gap("python, git, sql", "backend developer")
        assert "[HAVE]" in result

    def test_partial_skill_matching(self):
        # "docker" should match even if requirement says "Docker"
        result = analyze_skill_gap("docker, python", "backend developer")
        assert "[HAVE]" in result
