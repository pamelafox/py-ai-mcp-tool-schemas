import csv
import logging
import os
from pathlib import Path

import logfire
from fastmcp import FastMCP

logging.basicConfig(level=logging.WARNING, format="%(asctime)s - %(message)s")
logger = logging.getLogger("ExpensesMCP")
logger.setLevel(logging.INFO)

SCRIPT_DIR = Path(__file__).parent
EXPENSES_FILE = Path(os.getenv("EXPENSES_FILE", SCRIPT_DIR / "expenses.csv"))
CSV_FIELDNAMES = ["date", "amount", "category", "description"]

mcp = FastMCP("Expenses Tracker")

# Configure Logfire tracing if LOGFIRE_TOKEN is set
# Reference: https://logfire.pydantic.dev/docs/integrations/llms/mcp/
if os.getenv("LOGFIRE_TOKEN"):
    logger.info("Setting up Logfire instrumentation")
    logfire.configure(service_name="basic-expenses-mcp")
    logfire.instrument_mcp()


@mcp.tool
async def add_expense(
    expense_date: str,
    amount: float,
    category: str,
    description: str,
) -> str:
    """Add a new expense."""
    if amount <= 0:
        return "Error: Amount must be positive"

    logger.info(f"Adding expense: ${amount} for {description} on {expense_date}")

    file_exists = EXPENSES_FILE.exists()
    with open(EXPENSES_FILE, "a", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=CSV_FIELDNAMES)
        if not file_exists:
            writer.writeheader()
        writer.writerow(
            {
                "date": expense_date,
                "amount": amount,
                "category": category,
                "description": description,
            }
        )

    return f"Successfully added expense: ${amount} for {description} on {expense_date}"


@mcp.tool
async def get_expenses() -> str:
    """Get all expenses."""
    logger.info("Expenses data accessed")

    try:
        with open(EXPENSES_FILE, newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            rows = list(reader)
    except FileNotFoundError:
        return "No expenses found."

    if not rows:
        return "No expenses found."

    lines = []
    for row in rows:
        lines.append(f"{row['date']}: ${row['amount']} - {row['category']} - {row['description']}")
    return "\n".join(lines)


if __name__ == "__main__":
    logger.info("MCP Expenses server starting (HTTP mode on port 8000)")
    mcp.run(transport="streamable-http", host="0.0.0.0", port=8000)
