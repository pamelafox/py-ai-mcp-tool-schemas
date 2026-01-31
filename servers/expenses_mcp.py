import csv
import logging
import os
from datetime import date
from enum import Enum
from pathlib import Path
from typing import Annotated, Literal

import logfire
from dotenv import load_dotenv
from fastmcp import FastMCP
from pydantic import BaseModel, Field

load_dotenv(override=True)

logging.basicConfig(level=logging.WARNING, format="%(asctime)s - %(message)s")
logger = logging.getLogger("ExpensesMCP")
logger.setLevel(logging.INFO)

# Configure Logfire tracing if LOGFIRE_TOKEN is set
# Reference: https://logfire.pydantic.dev/docs/integrations/llms/mcp/
if os.getenv("LOGFIRE_TOKEN"):
    logger.info("Setting up Logfire instrumentation")
    logfire.configure(service_name="expenses-mcp")
    logfire.instrument_mcp()


SCRIPT_DIR = Path(__file__).parent
EXPENSES_FILE = SCRIPT_DIR / "expenses.csv"

CSV_FIELDNAMES = ["date", "amount", "category", "description", "payment_method", "reimbursable"]


mcp = FastMCP("Expenses Tracker")


# =============================================================================
# Types
# =============================================================================


class Category(Enum):
    FOOD_AND_DRINK = "Food & drink"
    TRANSIT_AND_FUEL = "Transit and Fuel"
    MEDIA_AND_STREAMING = "Media & streaming"
    APPAREL_AND_BEAUTY = "Apparel and Beauty"
    ELECTRONICS_AND_TECH = "Electronics & tech"
    HOME_AND_OFFICE = "Home and office"
    HEALTH_AND_FITNESS = "Health & Fitness"
    ARTS_AND_HOBBIES = "Arts and hobbies"
    FEES_AND_SERVICES = "Fees & services"
    MISC = "Misc"


CATEGORY_LITERAL = Literal[
    "Food & drink",
    "Transit and Fuel",
    "Media & streaming",
    "Apparel and Beauty",
    "Electronics & tech",
    "Home and office",
    "Health & Fitness",
    "Arts and hobbies",
    "Fees & services",
    "Misc",
]


class Expense(BaseModel):
    """A single expense record."""

    expense_date: date = Field(alias="date", description="Date of the expense")
    amount: float = Field(description="Amount spent")
    category: str = Field(description="Category of expense")
    description: str = Field(description="Description of the expense")


class ExpenseInput(BaseModel):
    """Input model for adding a single expense.

    This is used to test how models handle a single nested JSON object argument.
    """

    expense_date: date = Field(description="Date of the expense")
    amount: float = Field(description="Amount spent")
    category: Category = Field(description="Category of expense")
    description: str = Field(description="Description of the expense")


# =============================================================================
# Shared Implementations
# =============================================================================


async def _add_expense_impl(
    expense_date: date | str,
    amount: float,
    category: str,
    description: str,
    reimbursable: str | None = None,
) -> str:
    """Shared implementation for all add_expense variants."""
    if amount <= 0:
        return "Error: Amount must be positive"

    date_iso = expense_date.isoformat() if isinstance(expense_date, date) else str(expense_date)
    logger.info(f"Adding expense: ${amount} for {description} on {date_iso}")

    try:
        file_exists = EXPENSES_FILE.exists()
        with open(EXPENSES_FILE, "a", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=CSV_FIELDNAMES)
            if not file_exists:
                writer.writeheader()

            writer.writerow(
                {
                    "date": date_iso,
                    "amount": amount,
                    "category": category,
                    "description": description,
                    # The tools currently do not capture payment method.
                    "payment_method": "",
                    "reimbursable": reimbursable or "",
                }
            )

        return f"Successfully added expense: ${amount} for {description} on {date_iso}"

    except Exception as e:
        logger.error(f"Error adding expense: {str(e)}")
        return "Error: Unable to add expense"


def _get_expenses_impl() -> list[dict]:
    """Shared implementation for all get_expenses variants."""
    logger.info("Expenses data accessed")

    try:
        with open(EXPENSES_FILE, newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            return list(reader)
    except FileNotFoundError:
        logger.error("Expenses file not found")
        return []
    except Exception as e:
        logger.error(f"Error reading expenses: {str(e)}")
        return []


def _parse_date(date_str: str) -> date:
    """Parse a date string in YYYY-MM-DD format."""
    return date.fromisoformat(date_str)


# =============================================================================
# Category Field Variants (testing constrained values)
# =============================================================================


@mcp.tool
async def add_expense_cat_a(
    expense_date: date,
    amount: float,
    category: str,
    description: str,
) -> str:
    """Add a new expense."""
    return await _add_expense_impl(expense_date, amount, category, description)


@mcp.tool
async def add_expense_cat_b(
    expense_date: date,
    amount: float,
    category: Annotated[
        str,
        "Must be one of: Food & drink, Transit and Fuel, Media & streaming, Apparel and Beauty, "
        "Electronics & tech, Home and office, Health & Fitness, Arts and hobbies, Fees & services, Misc",
    ],
    description: str,
) -> str:
    """Add a new expense."""
    return await _add_expense_impl(expense_date, amount, category, description)


@mcp.tool
async def add_expense_cat_c(
    expense_date: date,
    amount: float,
    category: CATEGORY_LITERAL,
    description: str,
) -> str:
    """Add a new expense."""
    return await _add_expense_impl(expense_date, amount, category, description)


@mcp.tool
async def add_expense_cat_d(
    expense_date: date,
    amount: float,
    category: Category,
    description: str,
) -> str:
    """Add a new expense."""
    return await _add_expense_impl(expense_date, amount, category.value, description)


@mcp.tool
async def add_expense_cat_e(
    expense_date: date,
    amount: float,
    category: Annotated[
        Category,
        Field(
            description=(
                "Choose the closest category for the expense. Do not ask follow-up questions just to "
                "disambiguate the category; pick the best fit using the description and common sense. "
                "If truly unclear, use Misc.\n\n"
                "Heuristics: "
                "Food & drink=meals, groceries, coffee, restaurants, snacks; "
                "Transit and Fuel=rideshare, taxi, gas, parking, public transit, tolls; "
                "Media & streaming=movies, concerts, subscriptions, streaming, games, tickets; "
                "Apparel and Beauty=clothing, shoes, cosmetics, haircuts, personal care; "
                "Electronics & tech=devices, gadgets, accessories, apps, software; "
                "Home and office=furniture, supplies, housewares, decor, cleaning; "
                "Health & Fitness=gym, medical, wellness, supplements, pharmacy; "
                "Arts and hobbies=crafts, sports equipment, creative supplies, lessons; "
                "Fees & services=banking, professional services, insurance, subscriptions; "
                "Misc=anything that does not fit well into other categories."
            )
        ),
    ],
    description: str,
) -> str:
    """Add a new expense."""
    return await _add_expense_impl(expense_date, amount, category.value, description)


# =============================================================================
# Date Field Variants (testing date format handling)
# =============================================================================


@mcp.tool
async def add_expense_date_a(
    expense_date: str,
    amount: float,
    category: Category,
    description: str,
) -> str:
    """Add a new expense."""
    return await _add_expense_impl(_parse_date(expense_date), amount, category.value, description)


@mcp.tool
async def add_expense_date_b(
    expense_date: Annotated[str, "Date in YYYY-MM-DD format"],
    amount: float,
    category: Category,
    description: str,
) -> str:
    """Add a new expense."""
    return await _add_expense_impl(_parse_date(expense_date), amount, category.value, description)


@mcp.tool
async def add_expense_date_c(
    expense_date: date,
    amount: float,
    category: Category,
    description: str,
) -> str:
    """Add a new expense."""
    return await _add_expense_impl(expense_date, amount, category.value, description)


@mcp.tool
async def add_expense_date_d(
    expense_date: Annotated[str, Field(pattern=r"^\d{4}-\d{2}-\d{2}$")],
    amount: float,
    category: Category,
    description: str,
) -> str:
    """Add a new expense."""
    return await _add_expense_impl(_parse_date(expense_date), amount, category.value, description)


# =============================================================================
# Pydantic Model Input Variants (testing nested object arguments)
# =============================================================================


@mcp.tool
async def add_expense_model_a(expense: ExpenseInput) -> str:
    """Add a new expense."""
    return await _add_expense_impl(
        expense.expense_date,
        expense.amount,
        expense.category.value,
        expense.description,
    )


# =============================================================================
# Reimbursable Field Variants (testing union/sentinel handling)
# =============================================================================


@mcp.tool
async def add_expense_reimb_e(
    expense_date: date,
    amount: float,
    category: Category,
    description: str,
    reimbursable: Annotated[
        bool | Literal["unknown"],
        Field(
            description=(
                "Whether this expense is reimbursable.\n\n"
                "Infer reimbursable status from context; the user does not need to literally say \"reimbursable\". "
                "Use true when the expense is clearly for work/business (e.g., work trip, client meeting, business lunch). "
                "Use false when the expense is clearly personal (e.g., lunch with friends, personal expense). "
                "If it's ambiguous or mixed, use the literal string \"unknown\".\n\n"
                "Examples: \n"
                "- true: 'Work trip hotel' / 'Taxi to client meeting' / 'Business lunch'\n"
                "- false: 'Lunch with friends' / 'Personal expense' / 'Not work-related'\n"
                "- unknown: no work/personal signal, or user is unsure"
            )
        ),
    ],
) -> str:
    """Add a new expense."""
    reimbursable_str = (
        reimbursable
        if isinstance(reimbursable, str) and reimbursable == "unknown"
        else ("true" if reimbursable else "false")
    )
    return await _add_expense_impl(expense_date, amount, category.value, description, reimbursable=reimbursable_str)


# =============================================================================
# Output Variations (testing output schema handling)
# =============================================================================


@mcp.tool
def get_expenses_a() -> str:
    """Get all expenses."""
    expenses = _get_expenses_impl()
    if not expenses:
        return "No expenses found."

    lines = [f"Expense data ({len(expenses)} entries):\n"]
    for exp in expenses:
        lines.append(
            f"Date: {exp['date']}, Amount: ${exp['amount']}, "
            f"Category: {exp['category']}, Description: {exp['description']}"
        )
    return "\n".join(lines)


@mcp.tool
def get_expenses_b() -> list[dict]:
    """Get all expenses."""
    return _get_expenses_impl()


@mcp.tool
def get_expenses_c() -> list[Expense]:
    """Get all expenses."""
    expenses = _get_expenses_impl()
    return [
        Expense(
            date=date.fromisoformat(exp["date"]),
            amount=float(exp["amount"]),
            category=exp["category"],
            description=exp["description"],
        )
        for exp in expenses
    ]


# =============================================================================
# Main
# =============================================================================


if __name__ == "__main__":
    logger.info("MCP Expenses server starting (HTTP mode on port 8000)")
    mcp.run(transport="streamable-http", host="0.0.0.0", port=8000)
