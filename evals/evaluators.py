"""Evaluators for MCP tool schema variant testing.

Evaluators check:
- Whether a tool was called
- Whether tool arguments are valid (correct types, valid enum values)
- Whether tool arguments match expected values
"""

import csv
import re
import sys
import os
from dataclasses import dataclass
from pathlib import Path
import json

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agents.pydanticai_agent import ToolCallInfo
from evals.dataset import ExpenseCase, OutputCase

# Valid category values (must match the Enum/Literal in expenses_mcp.py exactly)
# Exact string matching - no case normalization
# Note: Categories intentionally use inconsistent formatting (& vs "and", mixed casing)
VALID_CATEGORIES = {
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
}

# Date pattern for YYYY-MM-DD format
DATE_PATTERN = re.compile(r"^\d{4}-\d{2}-\d{2}$")

# Description patterns
DESCRIPTION_CAPITALIZED_PATTERN = re.compile(r"^[A-Z]")
DESCRIPTION_ENDS_PERIOD_PATTERN = re.compile(r"\.$")


def _extract_arg(arguments: dict, name: str):
    """Extract an argument value from either a flat or nested tool-call shape.

    Most variants call tools with flat args:
      {"expense_date": "...", "category": "...", ...}

    The Pydantic model input variant calls tools with a nested object:
      {"expense": {"expense_date": "...", "category": "...", ...}}
    """
    if not isinstance(arguments, dict):
        return None

    if name in arguments:
        return arguments.get(name)

    expense = arguments.get("expense")
    if isinstance(expense, str):
        try:
            expense = json.loads(expense)
        except json.JSONDecodeError:
            expense = None
    if isinstance(expense, dict):
        return expense.get(name)

    return None


@dataclass
class EvalResult:
    """Result of an evaluation."""

    passed: bool
    score: float  # 0.0 to 1.0
    message: str
    details: dict | None = None


def evaluate_tool_called(tool_calls: list[ToolCallInfo], expected_prefix: str = "add_expense") -> EvalResult:
    """Check if any tool with the expected prefix was called."""
    matching = [tc for tc in tool_calls if tc.tool_name.startswith(expected_prefix)]
    if matching:
        return EvalResult(
            passed=True,
            score=1.0,
            message=f"Tool '{matching[0].tool_name}' was called",
            details={"tool_name": matching[0].tool_name},
        )
    return EvalResult(
        passed=False,
        score=0.0,
        message=f"No tool starting with '{expected_prefix}' was called",
        details={"tool_calls": [tc.tool_name for tc in tool_calls]},
    )


def evaluate_category_valid(tool_calls: list[ToolCallInfo]) -> EvalResult:
    """Check if the category argument is a valid enum value."""
    for tc in tool_calls:
        if tc.tool_name.startswith("add_expense"):
            category = _extract_arg(tc.arguments, "category")
            if category is None:
                return EvalResult(
                    passed=False,
                    score=0.0,
                    message="Category argument missing",
                )
            # Exact string match - no normalization
            if category in VALID_CATEGORIES:
                return EvalResult(
                    passed=True,
                    score=1.0,
                    message=f"Category '{category}' is valid",
                    details={"category": category},
                )
            return EvalResult(
                passed=False,
                score=0.0,
                message=f"Category '{category}' is not a valid enum value",
                details={"category": category, "valid_categories": list(VALID_CATEGORIES)},
            )
    return EvalResult(
        passed=False,
        score=0.0,
        message="No add_expense tool call found",
    )


def evaluate_date_format(tool_calls: list[ToolCallInfo]) -> EvalResult:
    """Check if the date argument is in YYYY-MM-DD format."""
    for tc in tool_calls:
        if tc.tool_name.startswith("add_expense"):
            date_val = _extract_arg(tc.arguments, "expense_date")
            if date_val is None:
                return EvalResult(
                    passed=False,
                    score=0.0,
                    message="Date argument missing",
                )
            if DATE_PATTERN.match(str(date_val)):
                return EvalResult(
                    passed=True,
                    score=1.0,
                    message=f"Date '{date_val}' is in correct format",
                    details={"date": date_val},
                )
            return EvalResult(
                passed=False,
                score=0.0,
                message=f"Date '{date_val}' is not in YYYY-MM-DD format",
                details={"date": date_val},
            )
    return EvalResult(
        passed=False,
        score=0.0,
        message="No add_expense tool call found",
    )


def evaluate_category_match(tool_calls: list[ToolCallInfo], expected: str) -> EvalResult:
    """Check if the category matches the expected value."""
    for tc in tool_calls:
        if tc.tool_name.startswith("add_expense"):
            category = _extract_arg(tc.arguments, "category")
            if category is None:
                return EvalResult(
                    passed=False,
                    score=0.0,
                    message="Category argument missing",
                )
            # Exact string match - no normalization
            if category == expected:
                return EvalResult(
                    passed=True,
                    score=1.0,
                    message=f"Category '{category}' matches expected '{expected}'",
                )
            return EvalResult(
                passed=False,
                score=0.0,
                message=f"Category '{category}' does not match expected '{expected}'",
                details={"actual": category, "expected": expected},
            )
    return EvalResult(passed=False, score=0.0, message="No add_expense tool call found")


def evaluate_date_match(tool_calls: list[ToolCallInfo], expected: str) -> EvalResult:
    """Check if the date matches the expected value."""
    for tc in tool_calls:
        if tc.tool_name.startswith("add_expense"):
            date_val = _extract_arg(tc.arguments, "expense_date")
            if date_val is None:
                return EvalResult(
                    passed=False,
                    score=0.0,
                    message="Date argument missing",
                )
            if str(date_val) == expected:
                return EvalResult(
                    passed=True,
                    score=1.0,
                    message=f"Date '{date_val}' matches expected '{expected}'",
                )
            return EvalResult(
                passed=False,
                score=0.0,
                message=f"Date '{date_val}' does not match expected '{expected}'",
                details={"actual": date_val, "expected": expected},
            )
    return EvalResult(passed=False, score=0.0, message="No add_expense tool call found")


def evaluate_description_capitalized(tool_calls: list[ToolCallInfo]) -> EvalResult:
    """Check if the description starts with a capital letter."""
    for tc in tool_calls:
        if tc.tool_name.startswith("add_expense"):
            description = _extract_arg(tc.arguments, "description")
            if description is None:
                return EvalResult(
                    passed=False,
                    score=0.0,
                    message="Description argument missing",
                )
            if DESCRIPTION_CAPITALIZED_PATTERN.match(str(description)):
                return EvalResult(
                    passed=True,
                    score=1.0,
                    message=f"Description '{description}' starts with capital letter",
                    details={"description": description},
                )
            return EvalResult(
                passed=False,
                score=0.0,
                message=f"Description '{description}' does not start with capital letter",
                details={"description": description},
            )
    return EvalResult(passed=False, score=0.0, message="No add_expense tool call found")


def evaluate_description_ends_period(tool_calls: list[ToolCallInfo]) -> EvalResult:
    """Check if the description ends with a period."""
    for tc in tool_calls:
        if tc.tool_name.startswith("add_expense"):
            description = _extract_arg(tc.arguments, "description")
            if description is None:
                return EvalResult(
                    passed=False,
                    score=0.0,
                    message="Description argument missing",
                )
            if DESCRIPTION_ENDS_PERIOD_PATTERN.search(str(description)):
                return EvalResult(
                    passed=True,
                    score=1.0,
                    message=f"Description '{description}' ends with period",
                    details={"description": description},
                )
            return EvalResult(
                passed=False,
                score=0.0,
                message=f"Description '{description}' does not end with period",
                details={"description": description},
            )
    return EvalResult(passed=False, score=0.0, message="No add_expense tool call found")


def _variant_supports_eval(tool_variant: str, eval_name: str) -> bool:
    """Check if a tool variant should be evaluated by a given evaluator.

    Evaluators only apply to relevant variant families:
    - tool_called → all variants (universal)
    - category_valid, category_match → _cat_* or _model_* variants
    - date_format, date_match → _date_* or _model_* variants
    - description_capitalized, description_ends_period → _desc_* variants
    """
    # Universal evaluator
    if eval_name == "tool_called":
        return True

    # Model variants support all evaluators
    if "_model_" in tool_variant:
        return True

    # Category evaluators
    if eval_name in ("category_valid", "category_match"):
        return "_cat_" in tool_variant

    # Date evaluators
    if eval_name in ("date_format", "date_match"):
        return "_date_" in tool_variant

    # Description evaluators
    if eval_name in ("description_capitalized", "description_ends_period"):
        return "_desc_" in tool_variant

    # Unknown evaluator → default to True
    return True


def run_all_evaluations(
    tool_calls: list[ToolCallInfo], case: ExpenseCase, tool_variant: str = ""
) -> dict[str, EvalResult]:
    """Run all applicable evaluations for a test case.

    Args:
        tool_calls: List of tool calls made during the run.
        case: The expense case being evaluated.
        tool_variant: Name of the tool variant being tested (used to filter evaluators).
    """
    results: dict[str, EvalResult] = {}

    # Always check tool_called (universal)
    results["tool_called"] = evaluate_tool_called(tool_calls)

    # Category evaluators - only for category and model variants
    if _variant_supports_eval(tool_variant, "category_valid"):
        results["category_valid"] = evaluate_category_valid(tool_calls)
    if case.expected_category and _variant_supports_eval(tool_variant, "category_match"):
        results["category_match"] = evaluate_category_match(tool_calls, case.expected_category)

    # Date evaluators - only for date and model variants
    if _variant_supports_eval(tool_variant, "date_format"):
        results["date_format"] = evaluate_date_format(tool_calls)
    if case.expected_date and _variant_supports_eval(tool_variant, "date_match"):
        results["date_match"] = evaluate_date_match(tool_calls, case.expected_date)

    # Description evaluators - only for desc variants
    if _variant_supports_eval(tool_variant, "description_capitalized"):
        results["description_capitalized"] = evaluate_description_capitalized(tool_calls)
    if _variant_supports_eval(tool_variant, "description_ends_period"):
        results["description_ends_period"] = evaluate_description_ends_period(tool_calls)

    return results


def compute_score(results: dict[str, EvalResult]) -> float:
    """Compute overall score from evaluation results."""
    if not results:
        return 0.0
    return sum(r.score for r in results.values()) / len(results)


# =============================================================================
# Output Variant Evaluators
# =============================================================================

EXPENSES_FILE_DEFAULT = Path(__file__).parent.parent / "servers" / "expenses.csv"


def _get_expenses_file() -> Path:
    """Get the expenses file path, respecting the EXPENSES_FILE env var."""
    return Path(os.getenv("EXPENSES_FILE", EXPENSES_FILE_DEFAULT))


def _load_expenses_for_eval() -> list[dict]:
    """Load expenses from the CSV file for evaluation answer checking."""
    try:
        with open(_get_expenses_file(), newline="", encoding="utf-8") as f:
            return list(csv.DictReader(f))
    except FileNotFoundError:
        return []


def _extract_numbers(text: str) -> list[float]:
    """Extract numeric values from text, handling currency and comma formatting."""
    cleaned = re.sub(r"[$€£,]", "", text)
    matches = re.findall(r"\b\d+\.?\d*\b", cleaned)
    return [float(m) for m in matches]


def _number_close(expected: float, actual: float, tolerance: float = 0.015) -> bool:
    """Check if two numbers are close within relative tolerance."""
    if expected == 0:
        return abs(actual) < 0.01
    return abs(actual - expected) / abs(expected) < tolerance


def compute_expected_value(check_type: str, check_params: dict | None = None) -> str | float | int | list[dict]:
    """Compute the expected answer from the current expenses CSV data."""
    expenses = _load_expenses_for_eval()
    if not expenses:
        return 0

    amounts = [float(e["amount"]) for e in expenses]

    if check_type == "count":
        return len(expenses)
    elif check_type == "max_amount":
        return max(amounts)
    elif check_type == "min_amount":
        return min(amounts)
    elif check_type == "earliest_date":
        return min(e["date"] for e in expenses)
    elif check_type == "field_of_max":
        field = check_params["field"]
        max_row = max(expenses, key=lambda e: float(e["amount"]))
        return max_row[field]
    elif check_type == "top_n_table":
        n = check_params["n"]
        by_amount = sorted(expenses, key=lambda e: float(e["amount"]), reverse=True)[:n]
        return [{"description": e["description"], "amount": float(e["amount"]), "category": e["category"], "date": e["date"]} for e in by_amount]
    elif check_type == "filter_table":
        field = check_params["field"]
        value = check_params["value"]
        filtered = [e for e in expenses if e[field] == value]
        return [{"description": e["description"], "amount": float(e["amount"]), "date": e["date"]} for e in filtered]
    else:
        return ""


def _check_table_rows(agent_output: str, expected_rows: list[dict]) -> EvalResult:
    """Check that a markdown table in the agent output contains all expected rows."""
    output_lower = agent_output.lower()
    found = 0
    missing = []
    for row in expected_rows:
        # Check that the description appears in the output (case-insensitive)
        desc = row["description"].lower()
        if desc in output_lower:
            found += 1
        else:
            missing.append(row["description"])

    if found == len(expected_rows):
        # Also verify it looks like a markdown table (has | characters)
        has_pipe = "|" in agent_output
        if has_pipe:
            return EvalResult(
                passed=True,
                score=1.0,
                message=f"Markdown table contains all {len(expected_rows)} expected rows",
            )
        return EvalResult(
            passed=False,
            score=0.5,
            message=f"All {len(expected_rows)} rows found but output does not appear to be a markdown table",
            details={"output": agent_output[:500]},
        )

    score = found / len(expected_rows) if expected_rows else 0.0
    return EvalResult(
        passed=False,
        score=score,
        message=f"Table missing {len(missing)} of {len(expected_rows)} rows: {missing}",
        details={"found": found, "total": len(expected_rows), "missing": missing, "output": agent_output[:500]},
    )


def evaluate_output_answer(agent_output: str, case: OutputCase) -> EvalResult:
    """Evaluate whether the agent's text answer is correct for an output query."""
    expected = compute_expected_value(case.check_type, case.check_params)

    # Table checks
    if isinstance(expected, list):
        return _check_table_rows(agent_output, expected)

    if isinstance(expected, (int, float)):
        numbers = _extract_numbers(agent_output)
        expected_float = float(expected)
        if any(_number_close(expected_float, n) for n in numbers):
            return EvalResult(
                passed=True,
                score=1.0,
                message=f"Answer contains expected value {expected}",
                details={"expected": expected, "found_numbers": numbers},
            )
        return EvalResult(
            passed=False,
            score=0.0,
            message=f"Expected {expected}, found numbers: {numbers}",
            details={"expected": expected, "found_numbers": numbers, "output": agent_output[:200]},
        )

    # String match (e.g., date, category name)
    expected_str = str(expected)
    if expected_str.lower() in agent_output.lower():
        return EvalResult(
            passed=True,
            score=1.0,
            message=f"Answer contains expected value '{expected_str}'",
        )
    return EvalResult(
        passed=False,
        score=0.0,
        message=f"Expected '{expected_str}' not found in output",
        details={"expected": expected_str, "output": agent_output[:200]},
    )


def run_output_evaluations(
    tool_calls: list[ToolCallInfo], case: OutputCase, agent_output: str, tool_variant: str = ""
) -> dict[str, EvalResult]:
    """Run all evaluations for an output test case."""
    results: dict[str, EvalResult] = {}
    results["tool_called"] = evaluate_tool_called(tool_calls, expected_prefix="get_expenses")
    results["answer_correct"] = evaluate_output_answer(agent_output, case)
    return results
