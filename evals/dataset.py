"""Test dataset for evaluating MCP tool schema variants.

Contains test cases with expense-logging prompts categorized by difficulty:
- Clear: Unambiguous requests with all required info
- Ambiguous: Missing date, vague categories, etc.
- Edge cases: Negative amounts, future dates, unknown categories
"""

from dataclasses import dataclass
from datetime import date, timedelta


@dataclass
class ExpenseCase:
    """A single test case for expense logging."""

    name: str
    prompt: str
    expected_category: str | None = None  # Expected category value (if applicable)
    expected_date: str | None = None  # Expected date in YYYY-MM-DD format
    expected_amount: float | None = None
    difficulty: str = "clear"  # clear, ambiguous, edge_case


def get_today() -> str:
    return date.today().isoformat()


def get_yesterday() -> str:
    return (date.today() - timedelta(days=1)).isoformat()


def get_tomorrow() -> str:
    return (date.today() + timedelta(days=1)).isoformat()


# =============================================================================
# Test Cases
# =============================================================================

EXPENSE_CASES: list[ExpenseCase] = [
    # --- Clear, unambiguous requests ---
    ExpenseCase(
        name="clear_food_yesterday",
        prompt="Yesterday I bought a sandwich for $12.50.",
        expected_category="food",
        expected_date=get_yesterday(),
        expected_amount=12.50,
        difficulty="clear",
    ),
    ExpenseCase(
        name="clear_transport_today",
        prompt=f"I paid $45 for gas today ({get_today()}).",
        expected_category="transport",
        expected_date=get_today(),
        expected_amount=45.0,
        difficulty="clear",
    ),
    ExpenseCase(
        name="clear_entertainment",
        prompt="On 2026-01-15 I spent $25.99 on a movie ticket.",
        expected_category="entertainment",
        expected_date="2026-01-15",
        expected_amount=25.99,
        difficulty="clear",
    ),
    ExpenseCase(
        name="clear_shopping",
        prompt="I bought new shoes for $125 on January 20, 2026.",
        expected_category="shopping",
        expected_date="2026-01-20",
        expected_amount=125.0,
        difficulty="clear",
    ),
    ExpenseCase(
        name="clear_gadget",
        prompt="Yesterday I purchased a laptop for $1200.",
        expected_category="gadget",
        expected_date=get_yesterday(),
        expected_amount=1200.0,
        difficulty="clear",
    ),
    # --- Ambiguous requests ---
    ExpenseCase(
        name="ambiguous_no_date",
        prompt="I spent $50 on groceries.",
        expected_category="food",
        expected_amount=50.0,
        difficulty="ambiguous",
        # Date not specified - model should use today or ask
    ),
    ExpenseCase(
        name="ambiguous_vague_category",
        prompt="Yesterday I paid $30 for stuff at the store.",
        expected_date=get_yesterday(),
        expected_amount=30.0,
        difficulty="ambiguous",
        # Category unclear - could be shopping or other
    ),
    ExpenseCase(
        name="ambiguous_relative_date",
        prompt="Last week I spent $89 on concert tickets.",
        expected_category="entertainment",
        expected_amount=89.0,
        difficulty="ambiguous",
        # "Last week" is vague - which day?
    ),
    ExpenseCase(
        name="ambiguous_mixed_items",
        prompt="I bought coffee and a phone case for $55 yesterday.",
        expected_date=get_yesterday(),
        expected_amount=55.0,
        difficulty="ambiguous",
        # Multiple categories in one purchase
    ),
    # --- Edge cases ---
    ExpenseCase(
        name="edge_future_date",
        prompt=f"I will spend $100 on a hotel tomorrow ({get_tomorrow()}).",
        expected_date=get_tomorrow(),
        expected_amount=100.0,
        difficulty="edge_case",
        # Future date - should this be allowed?
    ),
    ExpenseCase(
        name="edge_large_amount",
        prompt="Yesterday I bought a car for $35000.",
        expected_category="other",
        expected_date=get_yesterday(),
        expected_amount=35000.0,
        difficulty="edge_case",
    ),
    ExpenseCase(
        name="edge_small_amount",
        prompt="I paid $0.99 for an app yesterday.",
        expected_category="gadget",
        expected_date=get_yesterday(),
        expected_amount=0.99,
        difficulty="edge_case",
    ),
    ExpenseCase(
        name="edge_unknown_category",
        prompt="Yesterday I spent $200 on a spa treatment.",
        expected_date=get_yesterday(),
        expected_amount=200.0,
        difficulty="edge_case",
        # "spa treatment" doesn't fit standard categories
    ),
    ExpenseCase(
        name="edge_currency_symbol",
        prompt="I spent €50 on dinner yesterday.",
        expected_category="food",
        expected_date=get_yesterday(),
        expected_amount=50.0,
        difficulty="edge_case",
        # Euro symbol instead of dollar
    ),
]


def get_cases_by_difficulty(difficulty: str) -> list[ExpenseCase]:
    """Get test cases filtered by difficulty level."""
    return [c for c in EXPENSE_CASES if c.difficulty == difficulty]


def get_clear_cases() -> list[ExpenseCase]:
    return get_cases_by_difficulty("clear")


def get_ambiguous_cases() -> list[ExpenseCase]:
    return get_cases_by_difficulty("ambiguous")


def get_edge_cases() -> list[ExpenseCase]:
    return get_cases_by_difficulty("edge_case")
