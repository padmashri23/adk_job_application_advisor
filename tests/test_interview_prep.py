"""Tests for interview_prep tool."""
import pytest
from job_application_agent.tools.interview_prep import get_interview_questions
class TestGetInterviewQuestions:
    def test_default_params(self):
        result = get_interview_questions()
        assert "Technical Questions" in result
        assert "Behavioral Questions" in result
    def test_python_questions(self):
        result = get_interview_questions(tech="python")
        assert "decorator" in result.lower() or "GIL" in result
    def test_javascript_questions(self):
        result = get_interview_questions(tech="javascript")
        assert "closure" in result.lower() or "event loop" in result.lower()
    def test_java_questions(self):
        result = get_interview_questions(tech="java")
        assert "abstract" in result.lower() or "interface" in result.lower()
    def test_unknown_tech_uses_default(self):
        result = get_interview_questions(tech="rust")
        assert "Technical Questions" in result
        assert "RESTful" in result or "SQL" in result
    def test_senior_role_includes_system_design(self):
        result = get_interview_questions(role="senior software engineer")
        assert "System Design" in result
    def test_lead_role_includes_system_design(self):
        result = get_interview_questions(role="tech lead")
        assert "System Design" in result
    def test_junior_role_no_system_design(self):
        result = get_interview_questions(role="junior developer")
        assert "System Design" not in result
    def test_includes_star_method(self):
        result = get_interview_questions()
        assert "STAR" in result
    def test_includes_tips(self):
        result = get_interview_questions()
        assert "Tips" in result
    def test_empty_role_uses_default(self):
        result = get_interview_questions(role="", tech="python")
        assert "Technical Questions" in result
    def test_empty_tech_uses_default(self):
        result = get_interview_questions(role="developer", tech="")
        assert "Technical Questions" in result
