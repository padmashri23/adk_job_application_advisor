"""Tests for application_tracker tool."""
import json
import os
import pytest
from job_application_agent.tools.application_tracker import (
    add_application,
    update_application,
    list_applications,
    TRACKER_FILE,
    DATA_DIR,
)
@pytest.fixture(autouse=True)
def clean_tracker():
    """Remove tracker file before and after each test."""
    if os.path.exists(TRACKER_FILE):
        os.remove(TRACKER_FILE)
    yield
    if os.path.exists(TRACKER_FILE):
        os.remove(TRACKER_FILE)
class TestAddApplication:
    def test_add_basic(self):
        result = add_application("Google", "Software Engineer")
        assert "Google" in result
        assert "Software Engineer" in result
        assert "#1" in result
    def test_add_with_status(self):
        result = add_application("Meta", "Frontend Dev", status="screening")
        assert "screening" in result
    def test_add_with_notes(self):
        result = add_application("Amazon", "SDE", notes="Referred by friend")
        assert "Amazon" in result
    def test_add_multiple(self):
        add_application("Google", "SWE")
        result = add_application("Meta", "SWE")
        assert "#2" in result

    def test_invalid_status(self):
        result = add_application("Google", "SWE", status="invalid")
        assert "Error" in result

    def test_empty_company(self):
        result = add_application("", "SWE")
        assert "Error" in result

    def test_empty_role(self):
        result = add_application("Google", "")
        assert "Error" in result

    def test_persists_to_file(self):
        add_application("Google", "SWE")
        assert os.path.exists(TRACKER_FILE)
        with open(TRACKER_FILE, "r") as f:
            data = json.load(f)
        assert len(data) == 1
        assert data[0]["company"] == "Google"


class TestUpdateApplication:
    def test_update_status(self):
        add_application("Google", "SWE")
        result = update_application(1, "interview")
        assert "interview" in result
        assert "applied" in result  # old status shown

    def test_update_nonexistent(self):
        result = update_application(999, "interview")
        assert "Error" in result
        assert "not found" in result

    def test_update_invalid_status(self):
        add_application("Google", "SWE")
        result = update_application(1, "invalid_status")
        assert "Error" in result

    def test_update_with_notes(self):
        add_application("Google", "SWE")
        update_application(1, "interview", notes="Phone screen scheduled")
        with open(TRACKER_FILE, "r") as f:
            data = json.load(f)
        assert data[0]["notes"] == "Phone screen scheduled"


class TestListApplications:
    def test_empty_list(self):
        result = list_applications()
        assert "No applications" in result

    def test_list_all(self):
        add_application("Google", "SWE")
        add_application("Meta", "Frontend Dev")
        result = list_applications()
        assert "Google" in result
        assert "Meta" in result
        assert "2 total" in result

    def test_filter_by_status(self):
        add_application("Google", "SWE", status="applied")
        add_application("Meta", "Frontend Dev", status="interview")
        result = list_applications("interview")
        assert "Meta" in result
        assert "Google" not in result

    def test_filter_invalid_status(self):
        result = list_applications("invalid")
        assert "Error" in result

    def test_filter_no_matches(self):
        add_application("Google", "SWE", status="applied")
        result = list_applications("offer")
        assert "No applications" in result
