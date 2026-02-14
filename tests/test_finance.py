"""Tests for finance tool."""
import os
import pytest
from job_application_agent.tools.finance import (
    add_expense, view_expenses, add_income,
    set_budget, set_savings_goal, add_to_savings, view_savings,
    financial_summary,
    EXPENSES_FILE, INCOME_FILE, BUDGET_FILE, SAVINGS_FILE,
)


@pytest.fixture(autouse=True)
def clean_files():
    for f in [EXPENSES_FILE, INCOME_FILE, BUDGET_FILE, SAVINGS_FILE]:
        if os.path.exists(f):
            os.remove(f)
    yield
    for f in [EXPENSES_FILE, INCOME_FILE, BUDGET_FILE, SAVINGS_FILE]:
        if os.path.exists(f):
            os.remove(f)


class TestAddExpense:
    def test_add_basic(self):
        result = add_expense(500, "food", "lunch")
        assert "500" in result
        assert "food" in result.lower()

    def test_invalid_amount(self):
        result = add_expense(-100, "food")
        assert "Error" in result

    def test_zero_amount(self):
        result = add_expense(0, "food")
        assert "Error" in result

    def test_invalid_category(self):
        result = add_expense(100, "gambling")
        assert "Error" in result

    def test_daily_total(self):
        add_expense(200, "food")
        result = add_expense(300, "transport")
        assert "500" in result  # today's total


class TestViewExpenses:
    def test_empty(self):
        result = view_expenses()
        assert "No expenses" in result

    def test_with_expenses(self):
        add_expense(500, "food")
        add_expense(200, "transport")
        result = view_expenses("month")
        assert "700" in result
        assert "food" in result.lower()

    def test_today(self):
        add_expense(100, "food")
        result = view_expenses("today")
        assert "100" in result


class TestAddIncome:
    def test_add_salary(self):
        result = add_income(50000, "salary")
        assert "50,000" in result or "50000" in result
        assert "Salary" in result

    def test_invalid_amount(self):
        result = add_income(-1000, "salary")
        assert "Error" in result

    def test_freelance(self):
        result = add_income(5000, "freelance", "Web project")
        assert "Freelance" in result


class TestSetBudget:
    def test_set_basic(self):
        result = set_budget(30000)
        assert "30,000" in result or "30000" in result

    def test_with_categories(self):
        result = set_budget(30000, "food:8000,transport:3000")
        assert "Food" in result
        assert "Transport" in result

    def test_invalid_amount(self):
        result = set_budget(-100)
        assert "Error" in result

    def test_budget_warning(self):
        set_budget(1000)
        add_expense(900, "food")
        result = add_expense(50, "food")
        assert "WARNING" in result or "budget" in result.lower()


class TestSavingsGoal:
    def test_create_goal(self):
        result = set_savings_goal("Emergency Fund", 100000)
        assert "Emergency Fund" in result
        assert "100,000" in result or "100000" in result

    def test_empty_name(self):
        result = set_savings_goal("", 100000)
        assert "Error" in result

    def test_invalid_amount(self):
        result = set_savings_goal("Test", -5000)
        assert "Error" in result

    def test_add_to_savings(self):
        set_savings_goal("Laptop", 50000)
        result = add_to_savings(1, 10000)
        assert "10,000" in result or "10000" in result
        assert "20%" in result

    def test_goal_reached(self):
        set_savings_goal("Small goal", 1000)
        result = add_to_savings(1, 1000)
        assert "REACHED" in result or "100%" in result

    def test_add_to_nonexistent(self):
        result = add_to_savings(999, 1000)
        assert "not found" in result.lower()


class TestViewSavings:
    def test_empty(self):
        result = view_savings()
        assert "No savings" in result

    def test_with_goals(self):
        set_savings_goal("Fund A", 50000)
        set_savings_goal("Fund B", 100000)
        add_to_savings(1, 25000)
        result = view_savings()
        assert "Fund A" in result
        assert "Fund B" in result
        assert "50%" in result


class TestFinancialSummary:
    def test_empty(self):
        result = financial_summary()
        assert "Financial Summary" in result

    def test_with_data(self):
        add_income(50000, "salary")
        add_expense(5000, "food")
        add_expense(2000, "transport")
        result = financial_summary()
        assert "Income" in result
        assert "Expense" in result
        assert "50,000" in result or "50000" in result
