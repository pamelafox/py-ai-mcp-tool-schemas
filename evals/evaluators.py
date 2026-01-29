"""Evaluators for MCP tool schema variant testing.

Evaluators check:
- Whether a tool was called
- Whether tool arguments are valid (correct types, valid enum values)
- Whether tool arguments match expected values
"""

import re
from dataclasses import dataclass

from evals.dataset import ExpenseCase

# Valid category values (must match the Enum/Literal in expenses_mcp.py)
VALID_CATEGORIES = {"food", "transport", "entertainment", "shopping", "gadget", "other"}

# Date pattern for YYYY-MM-DD format
DATE_PATTERN = re.compile(r"^\d{4}-\d{2}-\d{2}$")


@dataclass
class ToolCallInfo:
    """Information extracted from a tool call."""

    tool_name: str
    arguments: dict
    result: str | None = None


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
            category = tc.arguments.get("category")
            if category is None:
                return EvalResult(
                    passed=False,
                    score=0.0,
                    message="Category argument missing",
                )
            # Normalize to lowercase for comparison
            category_lower = category.lower() if isinstance(category, str) else str(category).lower()
            if category_lower in VALID_CATEGORIES:
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
            date_val = tc.arguments.get("expense_date")
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
            category = tc.arguments.get("category")
            if category is None:
                return EvalResult(
                    passed=False,
                    score=0.0,
                    message="Category argument missing",
                )
            category_lower = category.lower() if isinstance(category, str) else str(category).lower()
            if category_lower == expected.lower():
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
            date_val = tc.arguments.get("expense_date")
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


def run_all_evaluations(
    tool_calls: list[ToolCallInfo], case: ExpenseCase
) -> dict[str, EvalResult]:
    """Run all applicable evaluations for a test case."""
    results: dict[str, EvalResult] = {}

    # Always check these
    results["tool_called"] = evaluate_tool_called(tool_calls)
    results["category_valid"] = evaluate_category_valid(tool_calls)
    results["date_format"] = evaluate_date_format(tool_calls)

    # Check expected values if specified
    if case.expected_category:
        results["category_match"] = evaluate_category_match(tool_calls, case.expected_category)
    if case.expected_date:
        results["date_match"] = evaluate_date_match(tool_calls, case.expected_date)

    return results


def compute_score(results: dict[str, EvalResult]) -> float:
    """Compute overall score from evaluation results."""
    if not results:
        return 0.0
    return sum(r.score for r in results.values()) / len(results)
