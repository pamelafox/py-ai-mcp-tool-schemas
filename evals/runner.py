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

import logfire
from azure.identity.aio import DefaultAzureCredential, get_bearer_token_provider
from dotenv import load_dotenv
from openai import AsyncOpenAI
from pydantic_ai import Agent
from pydantic_ai.mcp import MCPServerStreamableHTTP
from pydantic_ai.models.openai import OpenAIResponsesModel
from pydantic_ai.providers.openai import OpenAIProvider

from evals.dataset import EXPENSE_CASES, ExpenseCase
from evals.evaluators import EvalResult, ToolCallInfo, compute_score, run_all_evaluations
from evals.report import generate_markdown_report

load_dotenv(override=True)

# Configure Logfire tracing
logfire.configure()
logfire.instrument_pydantic_ai()

logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger("eval_runner")
logger.setLevel(logging.INFO)

# =============================================================================
# Configuration
# =============================================================================

API_HOST = os.getenv("API_HOST", "github")
MCP_SERVER_URL = os.getenv("MCP_SERVER_URL", "http://localhost:8000/mcp")

# Model settings for reproducibility
MODEL_SETTINGS = {
    "temperature": 0,
    "seed": 42,
}

# Tool variants to test
CATEGORY_VARIANTS = [
    "add_expense_cat_a",  # str
    "add_expense_cat_b",  # Annotated[str, Field(...)]
    "add_expense_cat_c",  # Literal[...]
    "add_expense_cat_d",  # Enum
]

DATE_VARIANTS = [
    "add_expense_date_a",  # str
    "add_expense_date_b",  # Annotated[str, Field(...)]
    "add_expense_date_c",  # date
    "add_expense_date_d",  # Annotated[date, Field(...)]
]

# Default to category variants
DEFAULT_VARIANTS = CATEGORY_VARIANTS


@dataclass
class RunResult:
    """Result of a single test case run."""

    case_name: str
    tool_variant: str
    tool_calls: list[ToolCallInfo]
    eval_results: dict[str, EvalResult]
    overall_score: float
    agent_output: str
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
# Model Setup
# =============================================================================


def get_model() -> tuple[OpenAIResponsesModel, DefaultAzureCredential | None, str]:
    """Configure the model based on API_HOST environment variable.
    
    Returns:
        Tuple of (model, async_credential, model_name)
    """
    async_credential = None

    if API_HOST == "azure":
        async_credential = DefaultAzureCredential()
        token_provider = get_bearer_token_provider(async_credential, "https://cognitiveservices.azure.com/.default")
        client = AsyncOpenAI(
            base_url=os.environ["AZURE_OPENAI_ENDPOINT"],
            api_key=token_provider,
        )
        model_name = os.environ["AZURE_OPENAI_CHAT_DEPLOYMENT"]
        model = OpenAIResponsesModel(model_name, provider=OpenAIProvider(openai_client=client))
    elif API_HOST == "github":
        client = AsyncOpenAI(api_key=os.environ["GITHUB_TOKEN"], base_url="https://models.inference.ai.azure.com")
        model_name = os.getenv("GITHUB_MODEL", "gpt-4o")
        model = OpenAIResponsesModel(model_name, provider=OpenAIProvider(openai_client=client))
    elif API_HOST == "ollama":
        client = AsyncOpenAI(base_url=os.environ.get("OLLAMA_ENDPOINT", "http://localhost:11434/v1"), api_key="none")
        model_name = os.environ["OLLAMA_MODEL"]
        model = OpenAIResponsesModel(model_name, provider=OpenAIProvider(openai_client=client))
    else:
        client = AsyncOpenAI(api_key=os.environ["OPENAI_API_KEY"])
        model_name = os.environ.get("OPENAI_MODEL", "gpt-4o")
        model = OpenAIResponsesModel(model_name, provider=OpenAIProvider(openai_client=client))

    return model, async_credential, model_name


# =============================================================================
# Tool Call Extraction
# =============================================================================


def extract_tool_calls(result) -> list[ToolCallInfo]:
    """Extract tool call information from agent result.

    Pydantic AI agent results contain message history with tool calls.
    """
    tool_calls = []

    # Access all messages from the result
    for message in result.all_messages():
        # Look for model responses with tool calls
        if hasattr(message, "parts"):
            for part in message.parts:
                if hasattr(part, "tool_name") and hasattr(part, "args"):
                    # This is a ToolCallPart
                    # args can be a JSON string or dict depending on model
                    args = part.args
                    if isinstance(args, str):
                        try:
                            args = json.loads(args)
                        except json.JSONDecodeError:
                            args = {}
                    elif not isinstance(args, dict):
                        args = {}
                    tool_calls.append(
                        ToolCallInfo(
                            tool_name=part.tool_name,
                            arguments=args,
                        )
                    )

    return tool_calls


# =============================================================================
# Runner
# =============================================================================


async def run_single_case(
    server,
    model: OpenAIResponsesModel,
    tool_variant: str,
    case: ExpenseCase,
) -> RunResult:
    """Run a single test case with a specific tool variant."""
    try:
        # Filter to only the specified tool variant
        toolset = server.filtered(lambda ctx, tool, tv=tool_variant: tool.name == tv)

        agent = Agent(
            model,
            system_prompt=f"You help users log expenses. Today's date is {datetime.now().strftime('%Y-%m-%d')}.",
            output_type=str,
            toolsets=[toolset],
        )

        result = await agent.run(case.prompt, model_settings=MODEL_SETTINGS)

        # Extract tool calls from result
        tool_calls = extract_tool_calls(result)

        # Run evaluations
        eval_results = run_all_evaluations(tool_calls, case)
        overall_score = compute_score(eval_results)

        return RunResult(
            case_name=case.name,
            tool_variant=tool_variant,
            tool_calls=tool_calls,
            eval_results=eval_results,
            overall_score=overall_score,
            agent_output=result.output,
        )

    except Exception as e:
        logger.exception(f"Error running case {case.name} with {tool_variant}")
        return RunResult(
            case_name=case.name,
            tool_variant=tool_variant,
            tool_calls=[],
            eval_results={},
            overall_score=0.0,
            agent_output="",
            error=str(e),
        )


async def run_evaluation(
    variants: list[str],
    cases: list[ExpenseCase],
    progress_callback: Callable[[str], None] | None = None,
) -> tuple[list[RunResult], dict[str, VariantSummary], str]:
    """Run full evaluation across variants and cases.
    
    Returns:
        Tuple of (results, summaries, model_name)
    """
    model, async_credential, model_name = get_model()
    results: list[RunResult] = []
    summaries: dict[str, VariantSummary] = {v: VariantSummary(variant_name=v) for v in variants}

    try:
        async with MCPServerStreamableHTTP(url=MCP_SERVER_URL) as server:
            total = len(variants) * len(cases)
            current = 0

            for variant in variants:
                for case in cases:
                    current += 1
                    if progress_callback:
                        progress_callback(f"[{current}/{total}] {variant} / {case.name}")

                    run_result = await run_single_case(server, model, variant, case)
                    results.append(run_result)

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

    finally:
        if async_credential:
            await async_credential.close()

    return results, summaries, model_name


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
    output_dir: str | None = None,
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
            "api_host": API_HOST,
            "model_name": model_name,
            "model_settings": MODEL_SETTINGS,
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
                "tool_variant": r.tool_variant,
                "tool_calls": [{"tool_name": tc.tool_name, "arguments": tc.arguments} for tc in r.tool_calls],
                "eval_results": {
                    name: {"passed": er.passed, "score": er.score, "message": er.message}
                    for name, er in r.eval_results.items()
                },
                "overall_score": r.overall_score,
                "agent_output": r.agent_output,
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
        default=",".join(DEFAULT_VARIANTS),
        help=f"Comma-separated list of tool variants (default: {','.join(DEFAULT_VARIANTS)})",
    )
    parser.add_argument(
        "--all",
        action="store_true",
        dest="all_variants",
        help="Run all variants (category + date)",
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
        "--verbose",
        action="store_true",
        help="Print detailed results for each case",
    )
    return parser.parse_args()


async def main():
    args = parse_args()

    # Parse variants
    if args.all_variants:
        variants = CATEGORY_VARIANTS + DATE_VARIANTS
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

    logger.info(f"Running evaluation with {len(variants)} variants and {len(cases)} cases")

    def progress(msg: str) -> None:
        logger.info(msg)

    results, summaries, model_name = await run_evaluation(variants, cases, progress_callback=progress)

    # Print summary
    print_summary_table(summaries)

    # Print detailed results if verbose
    if args.verbose:
        print_results_table(results)

    # Export results
    output_folder = export_results(results, summaries, model_name, args.output if args.output else None)
    print(f"\nResults saved to: {output_folder}")


if __name__ == "__main__":
    asyncio.run(main())
