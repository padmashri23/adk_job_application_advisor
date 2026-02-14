"""Application Tracker Tool - Track job applications with persistent JSON storage."""
import json
import logging
import os
from datetime import datetime

logger = logging.getLogger(__name__)

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "data")
TRACKER_FILE = os.path.join(DATA_DIR, "applications.json")

VALID_STATUSES = [
    "applied", "screening", "interview", "technical", "offer", "rejected", "withdrawn"
]


def _ensure_data_dir() -> None:
    """Create data directory if it doesn't exist."""
    os.makedirs(DATA_DIR, exist_ok=True)


def _load_applications() -> list[dict]:
    """Load applications from the JSON file."""
    _ensure_data_dir()
    if not os.path.exists(TRACKER_FILE):
        return []
    try:
        with open(TRACKER_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        logger.warning("Could not read tracker file, starting fresh.")
        return []


def _save_applications(apps: list[dict]) -> None:
    """Save applications to the JSON file."""
    _ensure_data_dir()
    with open(TRACKER_FILE, "w", encoding="utf-8") as f:
        json.dump(apps, f, indent=2, ensure_ascii=False)


def add_application(company: str, role: str, status: str = "applied", notes: str = "") -> str:
    """Add a new job application to the tracker.

    Args:
        company: Company name (e.g., "Google").
        role: Job role applied for (e.g., "Software Engineer").
        status: Application status. One of: applied, screening, interview,
            technical, offer, rejected, withdrawn. Default: "applied".
        notes: Optional notes about the application.

    Returns:
        Confirmation message with application details.
    """
    if not company or not company.strip():
        return "Error: Company name is required."
    if not role or not role.strip():
        return "Error: Role/position is required."

    company = company.strip()
    role = role.strip()
    status = status.strip().lower() if status else "applied"
    notes = notes.strip() if notes else ""

    if status not in VALID_STATUSES:
        return f"Error: Invalid status '{status}'. Must be one of: {', '.join(VALID_STATUSES)}"

    apps = _load_applications()

    application = {
        "id": len(apps) + 1,
        "company": company,
        "role": role,
        "status": status,
        "notes": notes,
        "applied_date": datetime.now().strftime("%Y-%m-%d"),
        "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M"),
    }
    apps.append(application)
    _save_applications(apps)

    logger.info("Added application #%d: %s at %s", application["id"], role, company)
    return (
        f"Application #{application['id']} added!\n"
        f"  Company: {company}\n"
        f"  Role: {role}\n"
        f"  Status: {status}\n"
        f"  Date: {application['applied_date']}"
    )


def update_application(application_id: int, status: str, notes: str = "") -> str:
    """Update the status of an existing application.

    Args:
        application_id: The ID of the application to update.
        status: New status. One of: applied, screening, interview,
            technical, offer, rejected, withdrawn.
        notes: Optional updated notes.

    Returns:
        Confirmation message or error.
    """
    if not isinstance(application_id, (int, float)) or application_id < 1:
        return "Error: Please provide a valid application ID (positive number)."

    application_id = int(application_id)
    status = status.strip().lower() if status else ""

    if status not in VALID_STATUSES:
        return f"Error: Invalid status '{status}'. Must be one of: {', '.join(VALID_STATUSES)}"

    apps = _load_applications()
    for app in apps:
        if app["id"] == application_id:
            old_status = app["status"]
            app["status"] = status
            app["last_updated"] = datetime.now().strftime("%Y-%m-%d %H:%M")
            if notes:
                app["notes"] = notes.strip()
            _save_applications(apps)

            logger.info("Updated application #%d: %s -> %s", application_id, old_status, status)
            return (
                f"Application #{application_id} updated!\n"
                f"  {app['company']} - {app['role']}\n"
                f"  Status: {old_status} -> {status}"
            )

    return f"Error: Application #{application_id} not found."


def list_applications(status_filter: str = "") -> str:
    """List all tracked job applications, optionally filtered by status.

    Args:
        status_filter: Optional status to filter by (e.g., "interview").
            Leave empty to show all applications.

    Returns:
        Formatted list of applications with their details.
    """
    if status_filter and status_filter.strip():
        status_filter = status_filter.strip().lower()
        if status_filter not in VALID_STATUSES:
            return f"Error: Invalid filter '{status_filter}'. Must be one of: {', '.join(VALID_STATUSES)}"

    apps = _load_applications()

    if not apps:
        return "No applications tracked yet. Use add_application() to start tracking!"

    if status_filter:
        apps = [a for a in apps if a["status"] == status_filter]
        if not apps:
            return f"No applications with status '{status_filter}'."

    lines = [f"Job Applications ({len(apps)} total):\n"]

    # Group by status
    status_order = VALID_STATUSES
    for status in status_order:
        group = [a for a in apps if a["status"] == status]
        if not group:
            continue
        lines.append(f"**{status.upper()}** ({len(group)}):")
        for app in group:
            notes_str = f" | Notes: {app['notes']}" if app.get("notes") else ""
            lines.append(
                f"  #{app['id']} {app['company']} - {app['role']} "
                f"(applied: {app['applied_date']}){notes_str}"
            )
        lines.append("")

    # Summary stats
    total = len(apps)
    active = sum(1 for a in apps if a["status"] not in ("rejected", "withdrawn"))
    offers = sum(1 for a in apps if a["status"] == "offer")
    lines.append(f"Summary: {total} total | {active} active | {offers} offers")

    logger.info("Listed %d applications", total)
    return "\n".join(lines)
