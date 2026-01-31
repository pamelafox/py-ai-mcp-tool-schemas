"""Generate markdown report from evaluation results.

Usage:
    uv run python evals/report.py results.json
"""

import argparse
import json

from evals.dataset import EXPENSE_CASES

# Descriptions for each variant type
VARIANT_DESCRIPTIONS = {
    "add_expense_cat_a": "category: str",
    "add_expense_cat_b": "category: Annotated[str, ...]",
    "add_expense_cat_c": "category: Literal[...]",
    "add_expense_cat_d": "category: ExpenseCategory (Enum)",
    "add_expense_cat_e": "category: Annotated[ExpenseCategory, Field(description=...)]",
    "add_expense_date_a": "expense_date: str",
    "add_expense_date_b": "expense_date: Annotated[str, ...]",
    "add_expense_date_c": "expense_date: date",
    "add_expense_date_d": "expense_date: Annotated[str, Field(pattern=...)]",
    "add_expense_model_a": "expense: ExpenseInput (Pydantic model)",
    "add_expense_reimb_e": 'reimbursable: bool | Literal["unknown"]',
}


def get_variant_description(name: str) -> str:
    """Get description for a variant, or empty string if unknown."""
    return VARIANT_DESCRIPTIONS.get(name, "")


def generate_markdown_report(data: dict) -> str:
    """Generate a markdown report from evaluation JSON data."""
    lines = []

    case_prompts = {c.name: c.prompt for c in EXPENSE_CASES}

    def _md_escape_cell(value: object) -> str:
        # Keep tables well-formed even if messages contain pipes/newlines.
        return str(value).replace("|", "\\|").replace("\n", " ").strip()

    def _append_blockquote(text: str) -> None:
        for line in text.splitlines() or [""]:
            lines.append(f"> {line}".rstrip())

    # Header
    lines.append("# MCP Tool Schema Evaluation Report")
    lines.append("")

    # Metadata
    meta = data.get("metadata", {})
    lines.append("## Metadata")
    lines.append("")
    lines.append(f"- **Timestamp**: {meta.get('timestamp', 'N/A')}")
    lines.append(f"- **Agent**: {meta.get('agent', 'N/A')}")
    lines.append(f"- **API Host**: {meta.get('api_host', 'N/A')}")
    lines.append(f"- **Model**: {meta.get('model_name', 'N/A')}")
    model_settings = meta.get("model_settings", {})
    if model_settings:
        # Support both old (openai_reasoning_effort) and new (reasoning_effort) key names
        reasoning_effort = model_settings.get('reasoning_effort') or model_settings.get('openai_reasoning_effort', 'N/A')
        reasoning_summary = model_settings.get('reasoning_summary') or model_settings.get('openai_reasoning_summary', 'N/A')
        lines.append(f"- **Reasoning Effort**: {reasoning_effort}")
        lines.append(f"- **Reasoning Summary**: {reasoning_summary}")
        lines.append(f"- **Seed**: {model_settings.get('seed', 'N/A')}")
        # Keep temperature for older runs that may have it.
        lines.append(f"- **Temperature**: {model_settings.get('temperature', 'N/A')}")
    lines.append(f"- **MCP Server URL**: {meta.get('mcp_server_url', 'N/A')}")
    lines.append("")

    # Summary table
    summaries = data.get("summaries", {})
    if summaries:
        lines.append("## Variant Comparison")
        lines.append("")
        lines.append("| Variant | Description | Avg Score | Total |")
        lines.append("|---------|-------------|-----------|-------|")

        # Sort alphabetically by variant name (a -> d)
        sorted_summaries = sorted(summaries.items(), key=lambda x: x[0])

        for name, s in sorted_summaries:
            desc = get_variant_description(name)
            avg_score = s.get("avg_score", 0)
            total = s.get("total_cases", 0)
            lines.append(
                f"| {_md_escape_cell(name)} | {_md_escape_cell(desc)} | {avg_score:.2f} | {_md_escape_cell(total)} |"
            )

        lines.append("")

    # Evaluation breakdown
    if summaries:
        lines.append("## Evaluation Breakdown")
        lines.append("")

        # Collect all eval names
        all_evals = set()
        for s in summaries.values():
            all_evals.update(s.get("eval_counts", {}).keys())

        has_cat_variants = any("_cat_" in n for n, _ in sorted_summaries)
        has_date_variants = any("_date_" in n for n, _ in sorted_summaries)
        has_model_variants = any("_model_" in n for n, _ in sorted_summaries)
        has_reimb_variants = any("_reimb_" in n for n, _ in sorted_summaries)

        for eval_name in sorted(all_evals):
            # Prefer: show the variants that actually have counts for this evaluator.
            # This matters for post-processed runs where an evaluator was added later.
            relevant_summaries = [(n, s) for n, s in sorted_summaries if eval_name in s.get("eval_counts", {})]

            # Fallback: keep older heuristic filters if somehow none have counts.
            if not relevant_summaries:
                if eval_name in ("category_match", "category_valid") and (has_cat_variants or has_model_variants):
                    relevant_summaries = [(n, s) for n, s in sorted_summaries if ("_cat_" in n or "_model_" in n)]
                elif eval_name in ("date_match", "date_format") and (has_date_variants or has_model_variants):
                    relevant_summaries = [(n, s) for n, s in sorted_summaries if ("_date_" in n or "_model_" in n)]
                elif eval_name in ("reimbursable_match",) and (has_reimb_variants or has_model_variants):
                    relevant_summaries = [(n, s) for n, s in sorted_summaries if ("_reimb_" in n or "_model_" in n)]
                else:
                    relevant_summaries = sorted_summaries

            lines.append(f"### {eval_name}")
            lines.append("")
            lines.append("| Variant | Description | Pass Rate | Passed | Total |")
            lines.append("|---------|-------------|-----------|--------|-------|")

            for name, s in relevant_summaries:
                desc = get_variant_description(name)
                counts = s.get("eval_counts", {}).get(eval_name, {"passed": 0, "failed": 0})
                total = counts["passed"] + counts["failed"]
                rate = (counts["passed"] / total * 100) if total > 0 else 0
                passed = _md_escape_cell(counts["passed"])
                total_ = _md_escape_cell(total)
                lines.append(
                    f"| {_md_escape_cell(name)} | {_md_escape_cell(desc)} | {rate:.1f}% |"
                    f" {passed} | {total_} |"
                )

            lines.append("")

    # Individual results (collapsed)
    results = data.get("results", [])
    if results:
        lines.append("## Detailed Results")
        lines.append("")
        lines.append("<details>")
        lines.append("<summary>Click to expand</summary>")
        lines.append("")

        for r in results:
            case = r.get("case_name", "N/A")
            variant = r.get("tool_variant", "N/A")
            score = r.get("overall_score", 0)

            lines.append(f"### {variant} / {case}: {score:.2f}")
            lines.append("")

            user_query = r.get("user_query") or r.get("prompt") or case_prompts.get(case)
            if user_query:
                lines.append("**User Query**:")
                lines.append("")
                _append_blockquote(str(user_query))
                lines.append("")

            if r.get("error"):
                lines.append(f"**Error**: {r['error']}")
                lines.append("")
                continue

            tool_calls = r.get("tool_calls", [])
            if tool_calls:
                lines.append("**Tool Calls**:")
                lines.append("")
                for tc in tool_calls:
                    lines.append(f"- Tool: `{tc['tool_name']}`")
                    lines.append("")
                    lines.append("```json")
                    lines.append(json.dumps(tc["arguments"], indent=2))
                    lines.append("```")
                    lines.append("")
            else:
                lines.append("**No tool calls made**")

            lines.append("")

            agent_output = r.get("agent_output")
            if agent_output:
                lines.append("**Assistant Output**:")
                lines.append("")
                _append_blockquote(agent_output)
                lines.append("")

            # Show model-provided reasoning summary text (not chain-of-thought)
            reasoning = r.get("reasoning")
            lines.append("**Reasoning Summary**:")
            lines.append("")
            lines.append("```")
            lines.append(reasoning if reasoning else "(none returned)")
            lines.append("```")
            lines.append("")

            eval_results = r.get("eval_results", {})
            if eval_results:
                lines.append("**Evaluations**:")
                lines.append("")
                lines.append("| Result | Evaluator | Message |")
                lines.append("|---|---|---|")
                for eval_name, er in eval_results.items():
                    symbol = "✅ Pass" if er.get("passed") else "❌ Fail"
                    message = _md_escape_cell(er.get("message", ""))
                    lines.append(f"| {symbol} | {_md_escape_cell(eval_name)} | {message} |")
                lines.append("")

        lines.append("</details>")
        lines.append("")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Generate markdown report from evaluation results")
    parser.add_argument("input", help="Input JSON file from evaluation runner")
    parser.add_argument("-o", "--output", help="Output markdown file (default: stdout)")
    args = parser.parse_args()

    with open(args.input) as f:
        data = json.load(f)

    report = generate_markdown_report(data)

    if args.output:
        with open(args.output, "w") as f:
            f.write(report)
        print(f"Report written to {args.output}")
    else:
        print(report)


if __name__ == "__main__":
    main()
