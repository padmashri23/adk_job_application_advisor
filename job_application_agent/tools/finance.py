"""Finance Tool - Expense tracking, budgets, savings goals, income, and financial advice."""
import json
import logging
import os
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "data")
EXPENSES_FILE = os.path.join(DATA_DIR, "expenses.json")
INCOME_FILE = os.path.join(DATA_DIR, "income.json")
BUDGET_FILE = os.path.join(DATA_DIR, "budget.json")
SAVINGS_FILE = os.path.join(DATA_DIR, "savings.json")

EXPENSE_CATEGORIES = [
    "food", "transport", "rent", "utilities", "entertainment",
    "shopping", "health", "education", "subscriptions", "other"
]

INCOME_TYPES = ["salary", "freelance", "investment", "gift", "refund", "other"]


def _ensure_data_dir() -> None:
    os.makedirs(DATA_DIR, exist_ok=True)


def _load_json(filepath: str) -> list:
    _ensure_data_dir()
    if not os.path.exists(filepath):
        return []
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data if isinstance(data, list) else [data] if isinstance(data, dict) else []
    except (json.JSONDecodeError, IOError):
        return []


def _load_json_dict(filepath: str) -> dict:
    _ensure_data_dir()
    if not os.path.exists(filepath):
        return {}
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data if isinstance(data, dict) else {}
    except (json.JSONDecodeError, IOError):
        return {}


def _save_json(filepath: str, data) -> None:
    _ensure_data_dir()
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


# ── Expense Tracking ─────────────────────────────────────────


def add_expense(amount: float, category: str, description: str = "") -> str:
    """Log an expense.

    Args:
        amount: The amount spent (in your local currency).
        category: Category of expense. One of: food, transport, rent, utilities,
            entertainment, shopping, health, education, subscriptions, other.
        description: Optional description of the expense.

    Returns:
        Confirmation with expense details and daily total.
    """
    if not isinstance(amount, (int, float)) or amount <= 0:
        return "Error: Amount must be a positive number."

    category = category.strip().lower() if category else "other"
    if category not in EXPENSE_CATEGORIES:
        return f"Error: Invalid category. Choose from: {', '.join(EXPENSE_CATEGORIES)}"

    amount = round(float(amount), 2)
    today = datetime.now().strftime("%Y-%m-%d")

    expenses = _load_json(EXPENSES_FILE)
    expense = {
        "id": len(expenses) + 1,
        "amount": amount,
        "category": category,
        "description": description.strip() if description else "",
        "date": today,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M"),
    }
    expenses.append(expense)
    _save_json(EXPENSES_FILE, expenses)

    # Today's total
    today_total = sum(e["amount"] for e in expenses if e["date"] == today)

    # Check budget
    budget = _load_json_dict(BUDGET_FILE)
    budget_warn = ""
    if budget:
        monthly_budget = budget.get("monthly_total", 0)
        month = datetime.now().strftime("%Y-%m")
        month_total = sum(e["amount"] for e in expenses if e["date"].startswith(month))
        if monthly_budget > 0 and month_total > monthly_budget * 0.8:
            pct = round((month_total / monthly_budget) * 100)
            budget_warn = f"\n  WARNING: You've used {pct}% of your monthly budget!"

    desc_str = f" - {expense['description']}" if expense["description"] else ""
    return (
        f"Expense #{expense['id']} logged!\n"
        f"  {category.title()}: Rs.{amount}{desc_str}\n"
        f"  Today's total: Rs.{today_total}{budget_warn}"
    )


def view_expenses(period: str = "month") -> str:
    """View expense summary for a given period.

    Args:
        period: Time period - "today", "week", "month", or "all". Default: "month".

    Returns:
        Expense breakdown by category with totals.
    """
    expenses = _load_json(EXPENSES_FILE)
    if not expenses:
        return "No expenses logged yet! Use add_expense() to start tracking."

    period = period.strip().lower() if period else "month"
    now = datetime.now()

    if period == "today":
        cutoff = now.strftime("%Y-%m-%d")
        filtered = [e for e in expenses if e["date"] == cutoff]
        period_label = "Today"
    elif period == "week":
        cutoff = (now - timedelta(days=now.weekday())).strftime("%Y-%m-%d")
        filtered = [e for e in expenses if e["date"] >= cutoff]
        period_label = "This Week"
    elif period == "month":
        cutoff = now.strftime("%Y-%m")
        filtered = [e for e in expenses if e["date"].startswith(cutoff)]
        period_label = now.strftime("%B %Y")
    else:
        filtered = expenses
        period_label = "All Time"

    if not filtered:
        return f"No expenses found for {period_label}."

    total = sum(e["amount"] for e in filtered)

    # By category
    by_cat = {}
    for e in filtered:
        by_cat[e["category"]] = by_cat.get(e["category"], 0) + e["amount"]

    lines = [f"**Expenses - {period_label}**\n"]
    lines.append(f"Total: Rs.{total:,.2f} ({len(filtered)} transactions)\n")

    lines.append("**By Category:**")
    for cat, amt in sorted(by_cat.items(), key=lambda x: -x[1]):
        pct = round((amt / total) * 100)
        bar = "#" * (pct // 5)
        lines.append(f"  {cat:15s} Rs.{amt:>10,.2f}  {bar} {pct}%")

    # Budget comparison
    budget = _load_json_dict(BUDGET_FILE)
    if budget and period == "month":
        monthly_budget = budget.get("monthly_total", 0)
        if monthly_budget > 0:
            remaining = monthly_budget - total
            lines.append(f"\n**Budget:** Rs.{monthly_budget:,.2f}")
            lines.append(f"  Spent: Rs.{total:,.2f} | Remaining: Rs.{remaining:,.2f}")
            if remaining < 0:
                lines.append(f"  You're Rs.{abs(remaining):,.2f} OVER budget!")

    return "\n".join(lines)


# ── Income Tracking ──────────────────────────────────────────


def add_income(amount: float, source: str = "salary", description: str = "") -> str:
    """Log an income entry.

    Args:
        amount: The income amount.
        source: Income source - salary, freelance, investment, gift, refund, other.
        description: Optional description.

    Returns:
        Confirmation with income details.
    """
    if not isinstance(amount, (int, float)) or amount <= 0:
        return "Error: Amount must be a positive number."

    source = source.strip().lower() if source else "salary"
    if source not in INCOME_TYPES:
        source = "other"

    amount = round(float(amount), 2)

    income = _load_json(INCOME_FILE)
    entry = {
        "id": len(income) + 1,
        "amount": amount,
        "source": source,
        "description": description.strip() if description else "",
        "date": datetime.now().strftime("%Y-%m-%d"),
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M"),
    }
    income.append(entry)
    _save_json(INCOME_FILE, income)

    month = datetime.now().strftime("%Y-%m")
    month_income = sum(i["amount"] for i in income if i["date"].startswith(month))

    return (
        f"Income logged!\n"
        f"  Source: {source.title()} | Amount: Rs.{amount:,.2f}\n"
        f"  This month's total income: Rs.{month_income:,.2f}"
    )


# ── Budget Management ────────────────────────────────────────


def set_budget(monthly_total: float, category_budgets: str = "") -> str:
    """Set your monthly budget.

    Args:
        monthly_total: Total monthly budget amount.
        category_budgets: Optional comma-separated category budgets
            like "food:5000,transport:2000,entertainment:1500".

    Returns:
        Confirmation with budget details.
    """
    if not isinstance(monthly_total, (int, float)) or monthly_total <= 0:
        return "Error: Monthly budget must be a positive number."

    budget = {
        "monthly_total": round(float(monthly_total), 2),
        "categories": {},
        "set_date": datetime.now().strftime("%Y-%m-%d"),
    }

    if category_budgets and category_budgets.strip():
        for item in category_budgets.split(","):
            item = item.strip()
            if ":" in item:
                cat, amt = item.split(":", 1)
                cat = cat.strip().lower()
                try:
                    budget["categories"][cat] = round(float(amt.strip()), 2)
                except ValueError:
                    pass

    _save_json(BUDGET_FILE, budget)

    lines = [f"Monthly budget set: Rs.{budget['monthly_total']:,.2f}\n"]
    if budget["categories"]:
        lines.append("Category limits:")
        for cat, amt in budget["categories"].items():
            lines.append(f"  {cat.title()}: Rs.{amt:,.2f}")

    lines.append(
        "\nTip: The 50/30/20 rule - 50% needs, 30% wants, 20% savings."
    )
    return "\n".join(lines)


# ── Savings Goals ────────────────────────────────────────────


def set_savings_goal(name: str, target_amount: float, deadline: str = "") -> str:
    """Create a savings goal to work towards.

    Args:
        name: Name of the savings goal (e.g., "Emergency Fund", "New Laptop").
        target_amount: Target amount to save.
        deadline: Optional deadline in YYYY-MM-DD format.

    Returns:
        Confirmation with goal details.
    """
    if not name or not name.strip():
        return "Error: Goal name is required."
    if not isinstance(target_amount, (int, float)) or target_amount <= 0:
        return "Error: Target amount must be a positive number."

    name = name.strip()
    savings = _load_json(SAVINGS_FILE)

    goal = {
        "id": len(savings) + 1,
        "name": name,
        "target": round(float(target_amount), 2),
        "saved": 0,
        "deadline": deadline.strip() if deadline else "",
        "deposits": [],
        "created": datetime.now().strftime("%Y-%m-%d"),
    }
    savings.append(goal)
    _save_json(SAVINGS_FILE, savings)

    deadline_str = f"\n  Deadline: {goal['deadline']}" if goal["deadline"] else ""
    return (
        f"Savings goal created!\n"
        f"  Goal #{goal['id']}: {name}\n"
        f"  Target: Rs.{goal['target']:,.2f}{deadline_str}\n"
        f"  Start saving with add_to_savings()!"
    )


def add_to_savings(goal_id: int, amount: float) -> str:
    """Add money to a savings goal.

    Args:
        goal_id: The ID of the savings goal.
        amount: Amount to add to savings.

    Returns:
        Updated progress towards the goal.
    """
    if not isinstance(goal_id, (int, float)) or goal_id < 1:
        return "Error: Please provide a valid goal ID."
    if not isinstance(amount, (int, float)) or amount <= 0:
        return "Error: Amount must be a positive number."

    goal_id = int(goal_id)
    amount = round(float(amount), 2)

    savings = _load_json(SAVINGS_FILE)
    for goal in savings:
        if goal["id"] == goal_id:
            goal["saved"] = round(goal["saved"] + amount, 2)
            goal["deposits"].append({
                "amount": amount,
                "date": datetime.now().strftime("%Y-%m-%d"),
            })
            _save_json(SAVINGS_FILE, savings)

            remaining = max(0, goal["target"] - goal["saved"])
            pct = min(100, round((goal["saved"] / goal["target"]) * 100))
            bar = "#" * (pct // 5) + "-" * ((100 - pct) // 5)

            result = (
                f"Added Rs.{amount:,.2f} to '{goal['name']}'!\n"
                f"  Progress: Rs.{goal['saved']:,.2f} / Rs.{goal['target']:,.2f} ({pct}%)\n"
                f"  [{bar}]\n"
                f"  Remaining: Rs.{remaining:,.2f}"
            )

            if pct >= 100:
                result += "\n\n  GOAL REACHED! Congratulations!"
            return result

    return f"Error: Savings goal #{goal_id} not found."


def view_savings() -> str:
    """View all savings goals and their progress.

    Returns:
        Summary of all savings goals.
    """
    savings = _load_json(SAVINGS_FILE)
    if not savings:
        return "No savings goals yet! Use set_savings_goal() to create one."

    lines = [f"**Your Savings Goals ({len(savings)}):**\n"]

    total_saved = 0
    total_target = 0

    for goal in savings:
        pct = min(100, round((goal["saved"] / goal["target"]) * 100)) if goal["target"] > 0 else 0
        bar = "#" * (pct // 5) + "-" * ((100 - pct) // 5)
        deadline = f" | Deadline: {goal['deadline']}" if goal.get("deadline") else ""
        status = " (REACHED!)" if pct >= 100 else ""

        lines.append(f"  #{goal['id']} {goal['name']}{status}")
        lines.append(f"    Rs.{goal['saved']:,.2f} / Rs.{goal['target']:,.2f} ({pct}%){deadline}")
        lines.append(f"    [{bar}]")
        lines.append("")

        total_saved += goal["saved"]
        total_target += goal["target"]

    lines.append(f"**Total Saved: Rs.{total_saved:,.2f} / Rs.{total_target:,.2f}**")
    return "\n".join(lines)


# ── Financial Summary ────────────────────────────────────────


def financial_summary(period: str = "month") -> str:
    """Get a comprehensive financial summary.

    Args:
        period: Time period - "month" or "all". Default: "month".

    Returns:
        Complete financial overview with income, expenses, savings, and advice.
    """
    now = datetime.now()

    if period == "month":
        month = now.strftime("%Y-%m")
        period_label = now.strftime("%B %Y")
        date_filter = lambda d: d.startswith(month)
    else:
        period_label = "All Time"
        date_filter = lambda d: True

    expenses = _load_json(EXPENSES_FILE)
    income = _load_json(INCOME_FILE)
    savings = _load_json(SAVINGS_FILE)
    budget = _load_json_dict(BUDGET_FILE)

    filtered_exp = [e for e in expenses if date_filter(e["date"])]
    filtered_inc = [i for i in income if date_filter(i["date"])]

    total_expense = sum(e["amount"] for e in filtered_exp)
    total_income = sum(i["amount"] for i in filtered_inc)
    net = total_income - total_expense

    lines = [f"**Financial Summary - {period_label}**\n"]

    # Income
    lines.append(f"**Income:** Rs.{total_income:,.2f}")
    if filtered_inc:
        by_source = {}
        for i in filtered_inc:
            by_source[i["source"]] = by_source.get(i["source"], 0) + i["amount"]
        for src, amt in sorted(by_source.items(), key=lambda x: -x[1]):
            lines.append(f"  {src.title()}: Rs.{amt:,.2f}")
    lines.append("")

    # Expenses
    lines.append(f"**Expenses:** Rs.{total_expense:,.2f}")
    if filtered_exp:
        by_cat = {}
        for e in filtered_exp:
            by_cat[e["category"]] = by_cat.get(e["category"], 0) + e["amount"]
        for cat, amt in sorted(by_cat.items(), key=lambda x: -x[1])[:5]:
            lines.append(f"  {cat.title()}: Rs.{amt:,.2f}")
    lines.append("")

    # Net
    net_label = "Surplus" if net >= 0 else "Deficit"
    lines.append(f"**Net {net_label}:** Rs.{abs(net):,.2f}")

    # Budget status
    if budget and period == "month":
        monthly_budget = budget.get("monthly_total", 0)
        if monthly_budget > 0:
            pct_used = round((total_expense / monthly_budget) * 100)
            lines.append(f"\n**Budget:** Rs.{total_expense:,.2f} / Rs.{monthly_budget:,.2f} ({pct_used}% used)")

    # Savings
    total_saved = sum(g["saved"] for g in savings)
    total_target = sum(g["target"] for g in savings)
    if savings:
        lines.append(f"\n**Savings Progress:** Rs.{total_saved:,.2f} / Rs.{total_target:,.2f}")

    # Advice
    lines.append("\n**Quick Advice:**")
    if total_income > 0:
        savings_rate = round(((total_income - total_expense) / total_income) * 100)
        lines.append(f"  Savings rate: {savings_rate}%")
        if savings_rate >= 20:
            lines.append(f"  Excellent! You're saving more than the recommended 20%.")
        elif savings_rate >= 10:
            lines.append(f"  Good progress! Aim for 20% savings rate.")
        elif savings_rate > 0:
            lines.append(f"  Try to increase savings. Cut the highest expense category first.")
        else:
            lines.append(f"  You're spending more than you earn. Review your top expenses.")
    else:
        lines.append(f"  Log your income with add_income() for better insights.")

    return "\n".join(lines)
