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


mcp = FastMCP("Expenses Tracker")


# =============================================================================
# Types
# =============================================================================


class Category(Enum):
    FOOD = "food"
    TRANSPORT = "transport"
    ENTERTAINMENT = "entertainment"
    SHOPPING = "shopping"
    GADGET = "gadget"
    OTHER = "other"


CATEGORY_LITERAL = Literal["food", "transport", "entertainment", "shopping", "gadget", "other"]


class Expense(BaseModel):
    """A single expense record."""

    expense_date: date = Field(alias="date", description="Date of the expense")
    amount: float = Field(description="Amount spent")
    category: str = Field(description="Category of expense")
    description: str = Field(description="Description of the expense")


# =============================================================================
# Shared Implementations
# =============================================================================


async def _add_expense_impl(
    expense_date: date,
    amount: float,
    category: str,
    description: str,
) -> str:
    """Shared implementation for all add_expense variants."""
    if amount <= 0:
        return "Error: Amount must be positive"

    date_iso = expense_date.isoformat()
    logger.info(f"Adding expense: ${amount} for {description} on {date_iso}")

    try:
        file_exists = EXPENSES_FILE.exists()

        with open(EXPENSES_FILE, "a", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)

            if not file_exists:
                writer.writerow(["date", "amount", "category", "description"])

            writer.writerow([date_iso, amount, category, description])

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
    """Add a new expense. Category: no constraints (plain str)."""
    return await _add_expense_impl(expense_date, amount, category, description)


@mcp.tool
async def add_expense_cat_b(
    expense_date: date,
    amount: float,
    category: Annotated[str, "Must be one of: food, transport, entertainment, shopping, gadget, other"],
    description: str,
) -> str:
    """Add a new expense. Category: description hints valid values."""
    return await _add_expense_impl(expense_date, amount, category, description)


@mcp.tool
async def add_expense_cat_c(
    expense_date: date,
    amount: float,
    category: Category,
    description: str,
) -> str:
    """Add a new expense. Category: Python Enum."""
    return await _add_expense_impl(expense_date, amount, category.value, description)


@mcp.tool
async def add_expense_cat_d(
    expense_date: date,
    amount: float,
    category: CATEGORY_LITERAL,
    description: str,
) -> str:
    """Add a new expense. Category: Literal with inline allowed values."""
    return await _add_expense_impl(expense_date, amount, category, description)


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
    """Add a new expense. Date: plain str, no format hint."""
    return await _add_expense_impl(_parse_date(expense_date), amount, category.value, description)


@mcp.tool
async def add_expense_date_b(
    expense_date: Annotated[str, "Date in YYYY-MM-DD format"],
    amount: float,
    category: Category,
    description: str,
) -> str:
    """Add a new expense. Date: str with description hint."""
    return await _add_expense_impl(_parse_date(expense_date), amount, category.value, description)


@mcp.tool
async def add_expense_date_c(
    expense_date: date,
    amount: float,
    category: Category,
    description: str,
) -> str:
    """Add a new expense. Date: Python date type."""
    return await _add_expense_impl(expense_date, amount, category.value, description)


@mcp.tool
async def add_expense_date_d(
    expense_date: Annotated[str, Field(pattern=r"^\d{4}-\d{2}-\d{2}$")],
    amount: float,
    category: Category,
    description: str,
) -> str:
    """Add a new expense. Date: str with regex pattern constraint."""
    return await _add_expense_impl(_parse_date(expense_date), amount, category.value, description)


# =============================================================================
# Output Variations (testing output schema handling)
# =============================================================================


@mcp.tool
def get_expenses_a() -> str:
    """Get all expenses. Returns: formatted text string."""
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
    """Get all expenses. Returns: untyped list of dicts."""
    return _get_expenses_impl()


@mcp.tool
def get_expenses_c() -> list[Expense]:
    """Get all expenses. Returns: typed list of Expense models."""
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
