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


def get_monday_of_current_week() -> str:
    """Return ISO date for the Monday of the current week.

    Uses Python's weekday convention: Monday=0 ... Sunday=6.
    """
    today = date.today()
    monday = today - timedelta(days=today.weekday())
    return monday.isoformat()


def get_monday_before_this_one() -> str:
    """Return ISO date for the Monday of the previous week."""
    this_monday = date.fromisoformat(get_monday_of_current_week())
    return (this_monday - timedelta(days=7)).isoformat()


def get_two_mondays_ago() -> str:
    """Return ISO date for the Monday two weeks before the current week."""
    this_monday = date.fromisoformat(get_monday_of_current_week())
    return (this_monday - timedelta(days=14)).isoformat()


def get_first_monday_of_current_month() -> str:
    """Return ISO date for the first Monday of the current month."""
    today = date.today()
    first = today.replace(day=1)
    # weekday(): Monday=0 ... Sunday=6
    offset = (0 - first.weekday()) % 7
    return (first + timedelta(days=offset)).isoformat()


def get_last_day_of_previous_month() -> str:
    """Return ISO date for the last calendar day of the previous month."""
    today = date.today()
    first_of_this_month = today.replace(day=1)
    last_of_prev_month = first_of_this_month - timedelta(days=1)
    return last_of_prev_month.isoformat()


def get_last_business_day_of_previous_month() -> str:
    """Return ISO date for the last weekday (Mon-Fri) of the previous month."""
    last = date.fromisoformat(get_last_day_of_previous_month())
    # weekday(): Monday=0 ... Sunday=6
    while last.weekday() >= 5:
        last -= timedelta(days=1)
    return last.isoformat()


def get_days_ago(days: int) -> str:
    """Return ISO date for N days ago."""
    return (date.today() - timedelta(days=days)).isoformat()


def get_day_after_tomorrow() -> str:
    """Return ISO date for the day after tomorrow."""
    return (date.today() + timedelta(days=2)).isoformat()


def get_last_weekday(target_weekday: int) -> str:
    """Return ISO date for the previous occurrence of a weekday.

    Args:
        target_weekday: Monday=0 ... Sunday=6

    Notes:
        Always returns a date strictly before today (i.e. "last Friday" on a Friday means 7 days ago).
    """
    today = date.today()
    delta = (today.weekday() - target_weekday) % 7
    if delta == 0:
        delta = 7
    return (today - timedelta(days=delta)).isoformat()


# =============================================================================
# Test Cases
# =============================================================================

EXPENSE_CASES: list[ExpenseCase] = [
    # --- Clear, unambiguous requests ---
    # These should be straightforward: explicit category and/or clear mapping, and an unambiguous date.
    ExpenseCase(
        name="clear_food_yesterday",
        prompt="Yesterday I bought a sandwich for $12.50.",
        expected_category="Food & drink",
        expected_date=get_yesterday(),
        expected_amount=12.50,
        difficulty="clear",
    ),

    # --- Hard-but-precise (relative-date) requests ---
    # These have a single correct date, but require calendar reasoning relative to "today".
    ExpenseCase(
        name="relative_date_monday_before_this_one",
        prompt="I bought a sandwich the Monday before this one for $12.50.",
        expected_category="Food & drink",
        expected_date=get_monday_before_this_one(),
        expected_amount=12.50,
        difficulty="edge_case",
    ),
    ExpenseCase(
        name="relative_date_two_mondays_ago",
        prompt="Two Mondays ago I spent $8.75 on coffee.",
        expected_category="Food & drink",
        expected_date=get_two_mondays_ago(),
        expected_amount=8.75,
        difficulty="edge_case",
    ),
    ExpenseCase(
        name="relative_date_first_monday_this_month",
        prompt="I bought a sandwich on the first Monday of this month for $12.50.",
        expected_category="Food & drink",
        expected_date=get_first_monday_of_current_month(),
        expected_amount=12.50,
        difficulty="edge_case",
    ),
    ExpenseCase(
        name="relative_date_last_day_last_month",
        prompt="On the last day of last month I spent $25.99 on a movie ticket.",
        expected_category="Media & streaming",
        expected_date=get_last_day_of_previous_month(),
        expected_amount=25.99,
        difficulty="edge_case",
    ),
    ExpenseCase(
        name="relative_date_last_business_day_last_month",
        prompt="I paid $60 for gas on the last business day of last month.",
        expected_category="Transit and Fuel",
        expected_date=get_last_business_day_of_previous_month(),
        expected_amount=60.0,
        difficulty="edge_case",
    ),
    ExpenseCase(
        name="relative_date_day_before_yesterday_coffee",
        prompt="The day before yesterday I spent $4.50 on coffee.",
        expected_category="Food & drink",
        expected_date=get_days_ago(2),
        expected_amount=4.50,
        difficulty="edge_case",
    ),
    ExpenseCase(
        name="relative_date_three_days_ago_rideshare",
        prompt="Three days ago I took an Uber to the airport for $38.",
        expected_category="Transit and Fuel",
        expected_date=get_days_ago(3),
        expected_amount=38.0,
        difficulty="edge_case",
    ),
    ExpenseCase(
        name="relative_date_last_friday_movie",
        prompt="Last Friday I spent $18 on a movie ticket.",
        expected_category="Media & streaming",
        expected_date=get_last_weekday(4),
        expected_amount=18.0,
        difficulty="edge_case",
    ),
    ExpenseCase(
        name="relative_date_day_after_tomorrow_bus_pass",
        prompt="The day after tomorrow I will buy a bus pass for $20.",
        expected_category="Transit and Fuel",
        expected_date=get_day_after_tomorrow(),
        expected_amount=20.0,
        difficulty="edge_case",
    ),
    # --- Hard-but-precise (category inference) requests ---
    # These have a single expected category/date, but require mapping from real-world phrasing.
    ExpenseCase(
        name="hard_category_grocery_delivery_yesterday",
        prompt="Yesterday I paid $65 for Instacart grocery delivery.",
        expected_category="Food & drink",
        expected_date=get_yesterday(),
        expected_amount=65.0,
        difficulty="edge_case",
    ),
    ExpenseCase(
        name="hard_category_headphones_last_day_last_month",
        prompt="On the last day of last month I bought headphones for $79.99.",
        # "Headphones" is intentionally hard-but-precise: it's not one of the category labels,
        # so the model must map it into our limited set. We treat it as an electronics purchase
        # and expect "electronics & tech" (vs plausible-but-wrong "apparel & beauty" / "arts & hobbies").
        expected_category="Electronics & tech",
        expected_date=get_last_day_of_previous_month(),
        expected_amount=79.99,
        difficulty="edge_case",
    ),
    # --- Edge cases ---
    # These are still precise, but stress the system with unusual inputs (currency, tiny/huge values, etc.).
    ExpenseCase(
        name="edge_large_amount",
        prompt="Yesterday I bought a car for 35000 USD.",
        expected_category="Misc",
        expected_date=get_yesterday(),
        expected_amount=35000.0,
        difficulty="edge_case",
    ),
    ExpenseCase(
        name="edge_small_amount",
        prompt="I paid $0.99 for an app yesterday.",
        expected_category="Electronics & tech",
        expected_date=get_yesterday(),
        expected_amount=0.99,
        difficulty="edge_case",
    ),
    ExpenseCase(
        name="edge_unknown_category",
        prompt="Yesterday I spent $200 on a spa treatment.",
        expected_category="Health & Fitness",
        expected_date=get_yesterday(),
        expected_amount=200.0,
        difficulty="edge_case",
    ),
    ExpenseCase(
        name="edge_currency_symbol",
        prompt="I spent €50 on dinner yesterday.",
        expected_category="Food & drink",
        expected_date=get_yesterday(),
        expected_amount=50.0,
        difficulty="edge_case",
        # Euro symbol instead of dollar
    ),
    # --- Spanish language cases ---
    # Keep a single Spanish case as a language-robustness check without adding
    # redundancy to the dataset.
    ExpenseCase(
        name="spanish_gadget",
        prompt="Ayer compré una laptop por 1200 dólares.",
        expected_category="Electronics & tech",
        expected_date=get_yesterday(),
        expected_amount=1200.0,
        difficulty="clear",
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


# =============================================================================
# Output Variant Test Cases
# =============================================================================


@dataclass
class OutputCase:
    """A test case for evaluating get_expenses output schema variants.

    Tests whether the agent can correctly interpret expense data returned
    by different output schema variants (str, list[dict], list[Expense])
    and answer questions about it.
    """

    name: str
    prompt: str
    # "count", "max_amount", "min_amount", "earliest_date",
    # "field_of_max", "top_n_table", "filter_table"
    check_type: str
    check_params: dict | None = None
    difficulty: str = "clear"


OUTPUT_CASES: list[OutputCase] = [
    OutputCase(
        name="count_all",
        prompt="How many expenses are recorded in total? Reply with just the number.",
        check_type="count",
    ),
    OutputCase(
        name="max_expense",
        prompt="What is the dollar amount of the single most expensive expense? Reply with just the number.",
        check_type="max_amount",
    ),
    OutputCase(
        name="min_expense",
        prompt="What is the dollar amount of the cheapest expense? Reply with just the number.",
        check_type="min_amount",
    ),
    OutputCase(
        name="earliest_date",
        prompt="What is the date of the earliest recorded expense? Reply in YYYY-MM-DD format.",
        check_type="earliest_date",
    ),
    OutputCase(
        name="category_of_max",
        prompt="What category does the most expensive expense belong to? Reply with just the category name.",
        check_type="field_of_max",
        check_params={"field": "category"},
    ),
    OutputCase(
        name="top3_table",
        prompt=(
            "Show the 3 most expensive expenses as a markdown table"
            " with columns: Description, Amount, Category, Date."
        ),
        check_type="top_n_table",
        check_params={"n": 3},
    ),
    OutputCase(
        name="electronics_table",
        prompt=(
            "Show all expenses in the 'Electronics & tech' category"
            " as a markdown table with columns: Description, Amount, Date."
        ),
        check_type="filter_table",
        check_params={"field": "category", "value": "Electronics & tech"},
    ),
]
