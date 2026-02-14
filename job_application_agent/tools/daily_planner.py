"""Daily Planner Tool - Todos, habits, schedule, weekly goals, progress reports."""
import json
import logging
import os
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "data")
TODOS_FILE = os.path.join(DATA_DIR, "todos.json")
HABITS_FILE = os.path.join(DATA_DIR, "habits.json")
GOALS_FILE = os.path.join(DATA_DIR, "goals.json")

TODO_PRIORITIES = ["high", "medium", "low"]


def _ensure_data_dir() -> None:
    os.makedirs(DATA_DIR, exist_ok=True)


def _load_json(filepath: str) -> list:
    _ensure_data_dir()
    if not os.path.exists(filepath):
        return []
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return []


def _save_json(filepath: str, data: list) -> None:
    _ensure_data_dir()
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


# ── Todo Management ──────────────────────────────────────────


def add_task(task: str, priority: str = "medium", due_date: str = "") -> str:
    """Add a new task to your daily todo list.

    Args:
        task: Description of the task to add.
        priority: Priority level - high, medium, or low. Default: medium.
        due_date: Optional due date in YYYY-MM-DD format.

    Returns:
        Confirmation with task details.
    """
    if not task or not task.strip():
        return "Error: Task description is required."

    task = task.strip()
    priority = priority.strip().lower() if priority else "medium"
    if priority not in TODO_PRIORITIES:
        return f"Error: Priority must be one of: {', '.join(TODO_PRIORITIES)}"

    todos = _load_json(TODOS_FILE)
    todo = {
        "id": len(todos) + 1,
        "task": task,
        "priority": priority,
        "status": "pending",
        "due_date": due_date.strip() if due_date else "",
        "created": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "completed_at": "",
    }
    todos.append(todo)
    _save_json(TODOS_FILE, todos)

    due_str = f" | Due: {todo['due_date']}" if todo["due_date"] else ""
    return (
        f"Task #{todo['id']} added!\n"
        f"  [{priority.upper()}] {task}{due_str}"
    )


def complete_task(task_id: int) -> str:
    """Mark a task as completed.

    Args:
        task_id: The ID of the task to complete.

    Returns:
        Confirmation message.
    """
    if not isinstance(task_id, (int, float)) or task_id < 1:
        return "Error: Please provide a valid task ID."

    task_id = int(task_id)
    todos = _load_json(TODOS_FILE)

    for todo in todos:
        if todo["id"] == task_id:
            if todo["status"] == "completed":
                return f"Task #{task_id} is already completed!"
            todo["status"] = "completed"
            todo["completed_at"] = datetime.now().strftime("%Y-%m-%d %H:%M")
            _save_json(TODOS_FILE, todos)

            pending = sum(1 for t in todos if t["status"] == "pending")
            completed = sum(1 for t in todos if t["status"] == "completed")
            return (
                f"Task #{task_id} completed: {todo['task']}\n"
                f"Progress: {completed} done, {pending} remaining. Keep going!"
            )

    return f"Error: Task #{task_id} not found."


def list_tasks(show_completed: bool = False) -> str:
    """View your current tasks organized by priority.

    Args:
        show_completed: Set to True to include completed tasks. Default: False.

    Returns:
        Formatted task list grouped by priority.
    """
    todos = _load_json(TODOS_FILE)
    if not todos:
        return "No tasks yet! Use add_task() to get started."

    if not show_completed:
        todos = [t for t in todos if t["status"] == "pending"]
        if not todos:
            return "All tasks completed! You're crushing it! Add more with add_task()."

    lines = [f"Your Tasks ({len(todos)}):\n"]

    for priority in TODO_PRIORITIES:
        group = [t for t in todos if t["priority"] == priority]
        if not group:
            continue

        icon = {"high": "!!!", "medium": " ! ", "low": "   "}[priority]
        lines.append(f"**{priority.upper()} PRIORITY:**")
        for t in group:
            status = "[x]" if t["status"] == "completed" else "[ ]"
            due = f" (due: {t['due_date']})" if t.get("due_date") else ""
            lines.append(f"  {status} #{t['id']} {t['task']}{due}")
        lines.append("")

    pending = sum(1 for t in todos if t["status"] == "pending")
    completed = sum(1 for t in todos if t["status"] == "completed")
    if completed > 0:
        lines.append(f"Progress: {completed}/{completed + pending} tasks done")

    return "\n".join(lines)


# ── Habit Tracking ───────────────────────────────────────────


def track_habit(habit_name: str, completed: bool = True) -> str:
    """Track a daily habit completion.

    Args:
        habit_name: Name of the habit (e.g., "exercise", "reading", "meditation").
        completed: Whether the habit was completed today. Default: True.

    Returns:
        Confirmation with streak information.
    """
    if not habit_name or not habit_name.strip():
        return "Error: Habit name is required."

    habit_name = habit_name.strip().lower()
    today = datetime.now().strftime("%Y-%m-%d")

    habits = _load_json(HABITS_FILE)

    # Find or create habit
    habit = None
    for h in habits:
        if h["name"] == habit_name:
            habit = h
            break

    if habit is None:
        habit = {"name": habit_name, "entries": [], "created": today}
        habits.append(habit)

    # Check if already logged today
    today_entry = next((e for e in habit["entries"] if e["date"] == today), None)
    if today_entry:
        today_entry["completed"] = completed
    else:
        habit["entries"].append({"date": today, "completed": completed})

    _save_json(HABITS_FILE, habits)

    # Calculate streak
    streak = 0
    entries_by_date = {e["date"]: e["completed"] for e in habit["entries"]}
    check_date = datetime.now()
    while True:
        date_str = check_date.strftime("%Y-%m-%d")
        if entries_by_date.get(date_str):
            streak += 1
            check_date -= timedelta(days=1)
        else:
            break

    total_done = sum(1 for e in habit["entries"] if e["completed"])
    total_days = len(habit["entries"])
    rate = round((total_done / total_days) * 100) if total_days > 0 else 0

    status = "Done" if completed else "Skipped"
    return (
        f"Habit: {habit_name} - {status} for today!\n"
        f"  Current streak: {streak} days\n"
        f"  Completion rate: {rate}% ({total_done}/{total_days} days)\n"
        f"  {'Keep the streak alive!' if streak > 1 else 'Start building that streak!'}"
    )


def view_habits() -> str:
    """View all tracked habits with streaks and completion rates.

    Returns:
        Summary of all habits with statistics.
    """
    habits = _load_json(HABITS_FILE)
    if not habits:
        return "No habits tracked yet! Use track_habit('exercise') to start."

    today = datetime.now().strftime("%Y-%m-%d")
    lines = [f"Your Habits ({len(habits)} tracked):\n"]

    for habit in habits:
        name = habit["name"]
        entries = habit["entries"]
        total_done = sum(1 for e in entries if e["completed"])
        total = len(entries)
        rate = round((total_done / total) * 100) if total > 0 else 0

        # Streak
        streak = 0
        entries_by_date = {e["date"]: e["completed"] for e in entries}
        check_date = datetime.now()
        while True:
            date_str = check_date.strftime("%Y-%m-%d")
            if entries_by_date.get(date_str):
                streak += 1
                check_date -= timedelta(days=1)
            else:
                break

        done_today = entries_by_date.get(today, False)
        today_icon = "[x]" if done_today else "[ ]"

        lines.append(
            f"  {today_icon} {name}: {streak} day streak | "
            f"{rate}% rate ({total_done}/{total})"
        )

    lines.append(f"\nTip: Consistency > perfection. Even 1% daily improvement compounds.")
    return "\n".join(lines)


# ── Weekly Goals & Progress ──────────────────────────────────


def set_weekly_goal(goal: str, category: str = "general") -> str:
    """Set a goal for this week.

    Args:
        goal: Description of the goal.
        category: Category - career, health, learning, personal, or general.

    Returns:
        Confirmation with goal details.
    """
    if not goal or not goal.strip():
        return "Error: Goal description is required."

    goal = goal.strip()
    category = category.strip().lower() if category else "general"
    valid_categories = ["career", "health", "learning", "personal", "general"]
    if category not in valid_categories:
        category = "general"

    goals = _load_json(GOALS_FILE)

    # Get current week
    now = datetime.now()
    week_start = (now - timedelta(days=now.weekday())).strftime("%Y-%m-%d")

    goal_entry = {
        "id": len(goals) + 1,
        "goal": goal,
        "category": category,
        "status": "in_progress",
        "week_start": week_start,
        "created": now.strftime("%Y-%m-%d %H:%M"),
        "completed_at": "",
    }
    goals.append(goal_entry)
    _save_json(GOALS_FILE, goals)

    return (
        f"Weekly goal #{goal_entry['id']} set!\n"
        f"  [{category.upper()}] {goal}\n"
        f"  Week of: {week_start}\n"
        f"  Break this into daily tasks with add_task() for best results!"
    )


def complete_goal(goal_id: int) -> str:
    """Mark a weekly goal as completed.

    Args:
        goal_id: The ID of the goal to complete.

    Returns:
        Confirmation message.
    """
    if not isinstance(goal_id, (int, float)) or goal_id < 1:
        return "Error: Please provide a valid goal ID."

    goal_id = int(goal_id)
    goals = _load_json(GOALS_FILE)

    for g in goals:
        if g["id"] == goal_id:
            g["status"] = "completed"
            g["completed_at"] = datetime.now().strftime("%Y-%m-%d %H:%M")
            _save_json(GOALS_FILE, goals)
            return f"Goal #{goal_id} completed: {g['goal']}\nAmazing work! Celebrate this win!"

    return f"Error: Goal #{goal_id} not found."


def weekly_progress_report() -> str:
    """Get a comprehensive weekly progress report covering tasks, habits, and goals.

    Returns:
        Detailed progress report with stats and recommendations.
    """
    now = datetime.now()
    week_start = (now - timedelta(days=now.weekday())).strftime("%Y-%m-%d")

    # Tasks
    todos = _load_json(TODOS_FILE)
    week_todos = [t for t in todos if t["created"][:10] >= week_start]
    completed_todos = [t for t in week_todos if t["status"] == "completed"]

    # Habits
    habits = _load_json(HABITS_FILE)

    # Goals
    goals = _load_json(GOALS_FILE)
    week_goals = [g for g in goals if g["week_start"] == week_start]
    completed_goals = [g for g in week_goals if g["status"] == "completed"]

    lines = ["**Weekly Progress Report**\n"]
    lines.append(f"Week of {week_start} | Generated: {now.strftime('%Y-%m-%d %H:%M')}\n")

    # Tasks section
    lines.append(f"**Tasks:**")
    if week_todos:
        lines.append(f"  Total: {len(week_todos)} | Completed: {len(completed_todos)} | "
                     f"Pending: {len(week_todos) - len(completed_todos)}")
        rate = round((len(completed_todos) / len(week_todos)) * 100)
        lines.append(f"  Completion rate: {rate}%")
    else:
        lines.append(f"  No tasks created this week")
    lines.append("")

    # Habits section
    lines.append(f"**Habits:**")
    if habits:
        for h in habits:
            week_entries = [e for e in h["entries"] if e["date"] >= week_start]
            done = sum(1 for e in week_entries if e["completed"])
            total = len(week_entries)
            lines.append(f"  {h['name']}: {done}/{total} days this week")
    else:
        lines.append(f"  No habits tracked yet")
    lines.append("")

    # Goals section
    lines.append(f"**Weekly Goals:**")
    if week_goals:
        for g in week_goals:
            status = "DONE" if g["status"] == "completed" else "IN PROGRESS"
            lines.append(f"  [{status}] {g['goal']} ({g['category']})")
        lines.append(f"  Completed: {len(completed_goals)}/{len(week_goals)}")
    else:
        lines.append(f"  No goals set this week. Use set_weekly_goal() to set some!")
    lines.append("")

    # Overall score
    scores = []
    if week_todos:
        scores.append(len(completed_todos) / len(week_todos))
    if week_goals:
        scores.append(len(completed_goals) / len(week_goals))

    if scores:
        overall = round((sum(scores) / len(scores)) * 100)
        lines.append(f"**Overall Score: {overall}%**")
        if overall >= 80:
            lines.append("Incredible week! You're on fire!")
        elif overall >= 60:
            lines.append("Solid progress! Keep pushing forward.")
        elif overall >= 40:
            lines.append("Good start. Focus on fewer goals next week for better completion.")
        else:
            lines.append("Tough week. Reset and come back stronger. Progress is not linear.")
    else:
        lines.append("Start tracking tasks and goals to see your weekly score!")

    return "\n".join(lines)
