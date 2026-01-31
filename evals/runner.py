"""Evaluation runner for MCP tool schema variant testing.

Runs test cases across different schema variants and models,
collecting metrics on tool-calling accuracy.

Usage:
    # Start the MCP server first:
    uv run python servers/expenses_mcp.py

    # Run evaluation:
    uv run python evals/runner.py

    # Run with specific tool variants:
    uv run python evals/runner.py --variants add_expense_cat_a,add_expense_cat_c

    # Run with specific test cases:
    uv run python evals/runner.py --cases clear_food_yesterday,clear_transport_today
"""

import argparse
import asyncio
import json
import logging
import os
import sys
from collections.abc import Callable
from dataclasses import dataclass, field
from datetime import datetime

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import logfire  # noqa: E402
from dotenv import load_dotenv  # noqa: E402

from agents.agentframework_agent import run_query as agentframework_run_query  # noqa: E402
from agents.copilotsdk_agent import run_query as copilot_run_query  # noqa: E402
from agents.langchain_agent import run_query as langchain_run_query  # noqa: E402
from agents.pydanticai_agent import ToolCallInfo  # noqa: E402
from agents.pydanticai_agent import run_query as pydanticai_run_query
from evals.dataset import EXPENSE_CASES, ExpenseCase  # noqa: E402

# Agent types
AGENT_PYDANTICAI = "pydanticai"
AGENT_COPILOT = "copilot"
AGENT_LANGCHAIN = "langchain"
AGENT_AGENTFRAMEWORK = "agentframework"
AVAILABLE_AGENTS = [AGENT_PYDANTICAI, AGENT_COPILOT, AGENT_LANGCHAIN, AGENT_AGENTFRAMEWORK]
from evals.evaluators import EvalResult, compute_score, run_all_evaluations  # noqa: E402
from evals.report import generate_markdown_report  # noqa: E402

load_dotenv(override=True)

# Configure Logfire tracing (console=False disables terminal output)
logfire.configure(console=False)
logfire.instrument_pydantic_ai()

logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger("eval_runner")
logger.setLevel(logging.INFO)

# =============================================================================
# Configuration
# =============================================================================

MCP_SERVER_URL = os.getenv("MCP_SERVER_URL", "http://localhost:8000/mcp")

# Tool variants to test
#
# NOTE: We intentionally exclude `add_expense_cat_a` (free-form `str`) from the
# default eval set because it is largely a "known-bad" baseline: models have no
# grounding for the allowed category set, so they often invent categories. It
# can still be included via `--include-cat-a` or by explicitly listing it in
# `--variants`.
CATEGORY_VARIANTS_DEFAULT = [
    "add_expense_cat_b",  # Annotated[str, Field(...)]
    "add_expense_cat_c",  # Literal[...]
    "add_expense_cat_d",  # Enum
    "add_expense_cat_e",  # Annotated[Enum, Field(description=...)]
]

CATEGORY_VARIANTS_ALL = [
    "add_expense_cat_a",  # str
    *CATEGORY_VARIANTS_DEFAULT,
]

DATE_VARIANTS = [
    "add_expense_date_a",  # str
    "add_expense_date_b",  # Annotated[str, Field(...)]
    "add_expense_date_c",  # date
    "add_expense_date_d",  # Annotated[date, Field(...)]
]

REIMBURSABLE_VARIANTS = [
    "add_expense_reimb_e",  # Annotated[bool | Literal["unknown"], Field(...)]
]

MODEL_INPUT_VARIANTS = [
    "add_expense_model_a",  # Pydantic model input (nested object)
]

# Default to all variants (category + date + reimbursable + nested model input)
ALL_VARIANTS = CATEGORY_VARIANTS_DEFAULT + DATE_VARIANTS + REIMBURSABLE_VARIANTS + MODEL_INPUT_VARIANTS


# =============================================================================
# Model Setup
# =============================================================================


REASONING_LEVELS = ["none", "minimal", "low", "medium", "high", "xhigh"]
DEFAULT_REASONING: str | None = None


DEFAULT_SEED = 42


def get_model_name(deployment: str | None = None) -> str:
    """Get the model name.
    
    Args:
        deployment: Optional deployment name override (defaults to AZURE_OPENAI_CHAT_DEPLOYMENT env var)
    """
    return deployment or os.environ.get("AZURE_OPENAI_CHAT_DEPLOYMENT", "unknown")


# =============================================================================
# Data Classes
# =============================================================================


@dataclass
class RunResult:
    """Result of a single test case run."""

    case_name: str
    user_query: str
    tool_variant: str
    tool_calls: list[ToolCallInfo]
    eval_results: dict[str, EvalResult]
    overall_score: float
    agent_output: str
    reasoning: str | None = None  # Model-provided reasoning summary text (if returned)
    error: str | None = None


@dataclass
class VariantSummary:
    """Summary metrics for a tool variant."""

    variant_name: str
    total_cases: int = 0
    passed_cases: int = 0
    total_score: float = 0.0
    eval_counts: dict[str, dict[str, int]] = field(default_factory=dict)

    @property
    def pass_rate(self) -> float:
        return self.passed_cases / self.total_cases if self.total_cases > 0 else 0.0

    @property
    def avg_score(self) -> float:
        return self.total_score / self.total_cases if self.total_cases > 0 else 0.0


# =============================================================================
# Runner
# =============================================================================


async def run_single_case(
    tool_variant: str,
    case: ExpenseCase,
    agent: str = AGENT_PYDANTICAI,
    deployment: str | None = None,
    seed: int | None = None,
    temperature: float | None = None,
    reasoning_effort: str | None = None,
) -> RunResult:
    """Run a single test case with a specific tool variant.
    
    Args:
        tool_variant: Name of the tool variant to test
        case: Test case to run
        agent: Agent framework to use (pydanticai, copilot, or langchain)
        deployment: Deployment/model name
        seed: Seed for determinism/reproducibility
        temperature: Sampling temperature
        reasoning_effort: Reasoning effort level (pydanticai only)
    """
    if agent == AGENT_COPILOT:
        query_result = await copilot_run_query(tool_variant, case.prompt, model=deployment)
    elif agent == AGENT_LANGCHAIN:
        # Note: langchain with Responses API doesn't support seed
        query_result = await langchain_run_query(
            tool_variant, case.prompt, model=deployment,
            temperature=temperature, reasoning_effort=reasoning_effort
        )
    elif agent == AGENT_AGENTFRAMEWORK:
        query_result = await agentframework_run_query(
            tool_variant, case.prompt, model=deployment, seed=seed,
            temperature=temperature, reasoning_effort=reasoning_effort
        )
    else:
        query_result = await pydanticai_run_query(
            tool_variant, case.prompt, model=deployment, seed=seed,
            temperature=temperature, reasoning_effort=reasoning_effort
        )

    # Convert agent-specific ToolCallInfo to pydanticai ToolCallInfo for compatibility
    tool_calls = [
        ToolCallInfo(tool_name=tc.tool_name, arguments=tc.arguments)
        for tc in query_result.tool_calls
    ]

    if query_result.error:
        logger.error(f"Error running case {case.name} with {tool_variant}: {query_result.error}")
        return RunResult(
            case_name=case.name,
            user_query=case.prompt,
            tool_variant=tool_variant,
            tool_calls=[],
            eval_results={},
            overall_score=0.0,
            agent_output="",
            error=query_result.error,
        )

    # Run evaluations
    eval_results = run_all_evaluations(tool_calls, case, tool_variant)
    overall_score = compute_score(eval_results)

    return RunResult(
        case_name=case.name,
        user_query=case.prompt,
        tool_variant=tool_variant,
        tool_calls=tool_calls,
        eval_results=eval_results,
        overall_score=overall_score,
        agent_output=query_result.output,
        reasoning=query_result.reasoning,
    )


async def run_evaluation(
    variants: list[str],
    cases: list[ExpenseCase],
    reasoning_effort: str = DEFAULT_REASONING,
    seed: int = DEFAULT_SEED,
    temperature: float | None = None,
    deployment: str | None = None,
    progress_callback: Callable[[str], None] | None = None,
    agent: str = AGENT_PYDANTICAI,
) -> tuple[list[RunResult], dict[str, VariantSummary], str, dict]:
    """Run full evaluation across variants and cases.

    Args:
        variants: List of tool variants to test
        cases: List of test cases to run
        reasoning_effort: Reasoning effort level (none, minimal, low, medium, high, xhigh)
        seed: Seed for determinism/reproducibility
        temperature: Optional sampling temperature
        deployment: Optional deployment/model name
        progress_callback: Optional callback for progress updates
        agent: Agent framework to use (pydanticai, copilot, or langchain)
    
    Returns:
        Tuple of (results, summaries, model_name, model_settings)
    """
    model_name = get_model_name(deployment)
    results: list[RunResult] = []
    summaries: dict[str, VariantSummary] = {v: VariantSummary(variant_name=v) for v in variants}

    # Build model_settings dict for metadata
    # Only include settings that are actually applied by the agent
    model_settings: dict = {"seed": seed}
    if temperature is not None:
        model_settings["temperature"] = temperature
    # reasoning_effort only applies to pydanticai agent (copilot uses VS Code settings)
    if reasoning_effort is not None and agent == AGENT_PYDANTICAI:
        model_settings["reasoning_effort"] = reasoning_effort

    total = len(variants) * len(cases)
    current = 0

    for variant in variants:
        for case in cases:
            current += 1
            if progress_callback:
                progress_callback(f"[{current}/{total}] {variant} / {case.name}")

            run_result = await run_single_case(
                tool_variant=variant,
                case=case,
                agent=agent,
                deployment=deployment,
                seed=seed,
                temperature=temperature,
                reasoning_effort=reasoning_effort,
            )
            results.append(run_result)

            # Add delay for copilot agent to avoid rate limiting
            if agent == AGENT_COPILOT:
                await asyncio.sleep(10)

            # Update summary
            summary = summaries[variant]
            summary.total_cases += 1
            summary.total_score += run_result.overall_score

            # Count as passed if tool was called and category is valid
            tool_called = run_result.eval_results.get("tool_called")
            category_valid = run_result.eval_results.get("category_valid")
            if tool_called and tool_called.passed and category_valid and category_valid.passed:
                summary.passed_cases += 1

            # Track individual eval results
            for eval_name, eval_result in run_result.eval_results.items():
                if eval_name not in summary.eval_counts:
                    summary.eval_counts[eval_name] = {"passed": 0, "failed": 0}
                if eval_result.passed:
                    summary.eval_counts[eval_name]["passed"] += 1
                else:
                    summary.eval_counts[eval_name]["failed"] += 1

    return results, summaries, model_name, model_settings


# =============================================================================
# Output
# =============================================================================


def print_results_table(results: list[RunResult]) -> None:
    """Print detailed results as a table."""
    print("\n" + "=" * 80)
    print("DETAILED RESULTS")
    print("=" * 80)

    for r in results:
        status = "PASS" if r.overall_score >= 0.8 else "FAIL"
        print(f"\n{r.tool_variant} / {r.case_name}: {status} (score: {r.overall_score:.2f})")

        if r.error:
            print(f"  Error: {r.error}")
            continue

        if r.tool_calls:
            for tc in r.tool_calls:
                print(f"  Tool: {tc.tool_name}")
                print(f"  Args: {json.dumps(tc.arguments, indent=4)}")
        else:
            print("  No tool calls made")

        for eval_name, eval_result in r.eval_results.items():
            status_symbol = "+" if eval_result.passed else "-"
            print(f"  [{status_symbol}] {eval_name}: {eval_result.message}")


def print_summary_table(summaries: dict[str, VariantSummary]) -> None:
    """Print summary comparison table."""
    print("\n" + "=" * 80)
    print("VARIANT COMPARISON SUMMARY")
    print("=" * 80)

    # Header
    print(f"\n{'Variant':<25} {'Pass Rate':>12} {'Avg Score':>12} {'Passed':>10} {'Total':>10}")
    print("-" * 70)

    # Rows sorted by avg score
    for summary in sorted(summaries.values(), key=lambda s: s.avg_score, reverse=True):
        print(
            f"{summary.variant_name:<25} "
            f"{summary.pass_rate:>11.1%} "
            f"{summary.avg_score:>12.2f} "
            f"{summary.passed_cases:>10} "
            f"{summary.total_cases:>10}"
        )

    # Detailed eval breakdown
    print("\n" + "-" * 70)
    print("EVALUATION BREAKDOWN")
    print("-" * 70)

    # Get all eval names
    all_evals = set()
    for summary in summaries.values():
        all_evals.update(summary.eval_counts.keys())

    for eval_name in sorted(all_evals):
        print(f"\n{eval_name}:")
        for summary in summaries.values():
            counts = summary.eval_counts.get(eval_name, {"passed": 0, "failed": 0})
            total = counts["passed"] + counts["failed"]
            rate = counts["passed"] / total if total > 0 else 0
            print(f"  {summary.variant_name:<23} {rate:>6.1%} ({counts['passed']}/{total})")


def export_results(
    results: list[RunResult],
    summaries: dict[str, VariantSummary],
    model_name: str,
    model_settings: dict,
    output_dir: str | None = None,
    agent: str = AGENT_PYDANTICAI,
) -> str:
    """Export results to a timestamped folder.
    
    Creates a folder with results.json and RESULTS.md.
    
    Returns:
        Path to the output folder.
    """
    # Create timestamped output folder
    if output_dir:
        folder = output_dir
    else:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        folder = os.path.join(os.path.dirname(__file__), "runs", timestamp)
    
    os.makedirs(folder, exist_ok=True)
    
    # Build data dict
    data = {
        "metadata": {
            "timestamp": datetime.now().isoformat(),
            "agent": agent,
            "model_name": model_name,
            "model_settings": model_settings,
            "mcp_server_url": MCP_SERVER_URL,
        },
        "summaries": {
            name: {
                "variant_name": s.variant_name,
                "total_cases": s.total_cases,
                "passed_cases": s.passed_cases,
                "pass_rate": s.pass_rate,
                "avg_score": s.avg_score,
                "eval_counts": s.eval_counts,
            }
            for name, s in summaries.items()
        },
        "results": [
            {
                "case_name": r.case_name,
                "user_query": r.user_query,
                "tool_variant": r.tool_variant,
                "tool_calls": [{"tool_name": tc.tool_name, "arguments": tc.arguments} for tc in r.tool_calls],
                "eval_results": {
                    name: {"passed": er.passed, "score": er.score, "message": er.message}
                    for name, er in r.eval_results.items()
                },
                "overall_score": r.overall_score,
                "agent_output": r.agent_output,
                "reasoning": r.reasoning,
                "error": r.error,
            }
            for r in results
        ],
    }
    
    # Write results.json
    json_path = os.path.join(folder, "results.json")
    with open(json_path, "w") as f:
        json.dump(data, f, indent=2)
    
    # Write RESULTS.md
    md_path = os.path.join(folder, "RESULTS.md")
    report = generate_markdown_report(data)
    with open(md_path, "w") as f:
        f.write(report)
    
    logger.info(f"Results exported to {folder}")
    return folder


# =============================================================================
# Main
# =============================================================================


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run MCP tool schema evaluation")
    parser.add_argument(
        "--variants",
        type=str,
        default="",
        help="Comma-separated list of tool variants (default: all variants)",
    )
    parser.add_argument(
        "--include-cat-a",
        action="store_true",
        help="Include add_expense_cat_a (free-form category: str) in the default variants",
    )
    parser.add_argument(
        "--cases",
        type=str,
        default="",
        help="Comma-separated list of case names (default: all cases)",
    )
    parser.add_argument(
        "--output",
        type=str,
        default="",
        help="Output folder path (default: evals/runs/<timestamp>)",
    )
    parser.add_argument(
        "--reasoning",
        type=str,
        default=DEFAULT_REASONING,
        choices=REASONING_LEVELS,
        help="Reasoning effort level (optional; if omitted, not sent)",
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=DEFAULT_SEED,
        help=f"Seed for reproducibility (default: {DEFAULT_SEED})",
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Print detailed results for each case",
    )
    parser.add_argument(
        "--temperature",
        type=float,
        default=None,
        help="Sampling temperature (e.g., 0-2). If omitted, provider default is used.",
    )
    parser.add_argument(
        "--deployment",
        type=str,
        default=None,
        help="Azure OpenAI deployment name (default: AZURE_OPENAI_CHAT_DEPLOYMENT env var)",
    )
    parser.add_argument(
        "--agent",
        type=str,
        default=AGENT_PYDANTICAI,
        choices=AVAILABLE_AGENTS,
        help=f"Agent framework to use (default: {AGENT_PYDANTICAI})",
    )
    return parser.parse_args()


async def main():
    args = parse_args()

    # Parse variants
    if not args.variants:
        variants = ALL_VARIANTS
        if args.include_cat_a:
            variants = CATEGORY_VARIANTS_ALL + DATE_VARIANTS
    else:
        variants = [v.strip() for v in args.variants.split(",") if v.strip()]

    # Parse cases
    if args.cases:
        case_names = {c.strip() for c in args.cases.split(",") if c.strip()}
        cases = [c for c in EXPENSE_CASES if c.name in case_names]
        if not cases:
            logger.error(f"No matching cases found for: {args.cases}")
            return
    else:
        cases = EXPENSE_CASES

    logger.info(
        "Running evaluation with %s variants, %s cases, agent=%s, reasoning=%s, seed=%s, deployment=%s",
        len(variants),
        len(cases),
        args.agent,
        args.reasoning,
        args.seed,
        args.deployment or "(env)",
    )

    def progress(msg: str) -> None:
        logger.info(msg)

    results, summaries, model_name, model_settings = await run_evaluation(
        variants,
        cases,
        reasoning_effort=args.reasoning,
        seed=args.seed,
        temperature=args.temperature,
        deployment=args.deployment,
        progress_callback=progress,
        agent=args.agent,
    )

    # Print summary
    print_summary_table(summaries)

    # Print detailed results if verbose
    if args.verbose:
        print_results_table(results)

    # Export results
    output_folder = export_results(
        results, summaries, model_name, model_settings, 
        args.output if args.output else None,
        agent=args.agent,
    )
    print(f"\nResults saved to: {output_folder}")


if __name__ == "__main__":
    asyncio.run(main())
