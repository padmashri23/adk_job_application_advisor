"""Tests for daily planner tool."""
import os
import pytest
from job_application_agent.tools.daily_planner import (
    add_task, complete_task, list_tasks,
    track_habit, view_habits,
    set_weekly_goal, complete_goal, weekly_progress_report,
    TODOS_FILE, HABITS_FILE, GOALS_FILE,
)


@pytest.fixture(autouse=True)
def clean_files():
    for f in [TODOS_FILE, HABITS_FILE, GOALS_FILE]:
        if os.path.exists(f):
            os.remove(f)
    yield
    for f in [TODOS_FILE, HABITS_FILE, GOALS_FILE]:
        if os.path.exists(f):
            os.remove(f)


class TestAddTask:
    def test_add_basic(self):
        result = add_task("Buy groceries")
        assert "#1" in result
        assert "Buy groceries" in result

    def test_add_with_priority(self):
        result = add_task("Study DSA", priority="high")
        assert "HIGH" in result

    def test_add_with_due_date(self):
        result = add_task("Submit report", due_date="2026-03-01")
        assert "2026-03-01" in result

    def test_empty_task(self):
        result = add_task("")
        assert "Error" in result

    def test_invalid_priority(self):
        result = add_task("Test", priority="urgent")
        assert "Error" in result


class TestCompleteTask:
    def test_complete(self):
        add_task("Test task")
        result = complete_task(1)
        assert "completed" in result.lower()

    def test_complete_nonexistent(self):
        result = complete_task(999)
        assert "not found" in result.lower()

    def test_complete_already_done(self):
        add_task("Test task")
        complete_task(1)
        result = complete_task(1)
        assert "already" in result.lower()


class TestListTasks:
    def test_empty(self):
        result = list_tasks()
        assert "No tasks" in result

    def test_with_tasks(self):
        add_task("Task A", priority="high")
        add_task("Task B", priority="low")
        result = list_tasks()
        assert "Task A" in result
        assert "Task B" in result

    def test_all_completed(self):
        add_task("Task A")
        complete_task(1)
        result = list_tasks()
        assert "crushing it" in result.lower() or "completed" in result.lower()


class TestTrackHabit:
    def test_track_new_habit(self):
        result = track_habit("exercise")
        assert "exercise" in result
        assert "streak" in result.lower()

    def test_streak_builds(self):
        result = track_habit("reading")
        assert "1 day" in result

    def test_empty_habit(self):
        result = track_habit("")
        assert "Error" in result


class TestViewHabits:
    def test_empty(self):
        result = view_habits()
        assert "No habits" in result

    def test_with_habits(self):
        track_habit("exercise")
        track_habit("meditation")
        result = view_habits()
        assert "exercise" in result
        assert "meditation" in result


class TestWeeklyGoals:
    def test_set_goal(self):
        result = set_weekly_goal("Complete 10 LeetCode problems", "career")
        assert "#1" in result
        assert "CAREER" in result

    def test_empty_goal(self):
        result = set_weekly_goal("")
        assert "Error" in result

    def test_complete_goal(self):
        set_weekly_goal("Test goal")
        result = complete_goal(1)
        assert "completed" in result.lower()

    def test_complete_nonexistent(self):
        result = complete_goal(999)
        assert "not found" in result.lower()


class TestWeeklyProgressReport:
    def test_empty_report(self):
        result = weekly_progress_report()
        assert "Progress Report" in result

    def test_with_data(self):
        add_task("Test task")
        complete_task(1)
        set_weekly_goal("Test goal")
        result = weekly_progress_report()
        assert "Tasks" in result
        assert "Goals" in result
