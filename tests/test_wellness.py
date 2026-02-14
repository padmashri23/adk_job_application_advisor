"""Tests for wellness tool."""
import os
import pytest
from job_application_agent.tools.wellness import (
    log_mood, get_mood_history, get_motivation,
    get_breathing_exercise, journal_entry, weekly_checkin,
    MOOD_FILE, JOURNAL_FILE,
)


@pytest.fixture(autouse=True)
def clean_files():
    for f in [MOOD_FILE, JOURNAL_FILE]:
        if os.path.exists(f):
            os.remove(f)
    yield
    for f in [MOOD_FILE, JOURNAL_FILE]:
        if os.path.exists(f):
            os.remove(f)


class TestLogMood:
    def test_log_valid_mood(self):
        result = log_mood("good")
        assert "good" in result.lower()
        assert "logged" in result.lower()

    def test_log_stressed_gives_tips(self):
        result = log_mood("stressed")
        assert "help" in result.lower() or "tip" in result.lower() or "walk" in result.lower()

    def test_log_great_gives_affirmation(self):
        result = log_mood("great")
        assert "wonderful" in result.lower() or "affirmation" in result.lower() or "energy" in result.lower()

    def test_invalid_mood(self):
        result = log_mood("ecstatic")
        assert "don't recognize" in result.lower() or "try one of" in result.lower()

    def test_empty_mood(self):
        result = log_mood("")
        assert "please" in result.lower() or "options" in result.lower()

    def test_mood_with_notes(self):
        result = log_mood("sad", "bad day at work")
        assert "logged" in result.lower()


class TestGetMoodHistory:
    def test_empty_history(self):
        result = get_mood_history()
        assert "No mood entries" in result

    def test_with_entries(self):
        log_mood("good")
        log_mood("stressed")
        result = get_mood_history()
        assert "good" in result
        assert "stressed" in result

    def test_mood_breakdown(self):
        log_mood("good")
        log_mood("good")
        log_mood("stressed")
        result = get_mood_history()
        assert "breakdown" in result.lower() or "good" in result


class TestGetMotivation:
    def test_returns_quote(self):
        result = get_motivation()
        assert "Motivation" in result
        assert "Affirmation" in result

    def test_not_empty(self):
        result = get_motivation()
        assert len(result) > 50


class TestGetBreathingExercise:
    def test_calm(self):
        result = get_breathing_exercise("calm")
        assert "4-7-8" in result or "Breathe" in result

    def test_focus(self):
        result = get_breathing_exercise("focus")
        assert "Box" in result or "Breathe" in result

    def test_ground(self):
        result = get_breathing_exercise("ground")
        assert "5-5-5" in result or "Grounding" in result

    def test_default(self):
        result = get_breathing_exercise("unknown")
        assert "Breathe" in result or "seconds" in result


class TestJournalEntry:
    def test_get_prompt(self):
        result = journal_entry(get_prompt=True)
        assert "Prompt" in result

    def test_empty_gets_prompt(self):
        result = journal_entry("")
        assert "Prompt" in result

    def test_save_entry(self):
        result = journal_entry("Today was a productive day. I learned a lot.")
        assert "saved" in result.lower()
        assert "Words" in result


class TestWeeklyCheckin:
    def test_empty_checkin(self):
        result = weekly_checkin()
        assert "Weekly" in result

    def test_with_data(self):
        log_mood("good")
        journal_entry("Feeling great today")
        result = weekly_checkin()
        assert "Mood" in result
        assert "Journal" in result
