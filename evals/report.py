"""Generate markdown report from evaluation results.

Usage:
    uv run python evals/report.py results.json
"""

import argparse
import json

# Descriptions for each variant type
VARIANT_DESCRIPTIONS = {
    "add_expense_cat_a": "category: str",
    "add_expense_cat_b": "category: Annotated[str, ...]",
    "add_expense_cat_c": "category: Literal[...]",
    "add_expense_cat_d": "category: ExpenseCategory (Enum)",
    "add_expense_date_a": "expense_date: str",
    "add_expense_date_b": "expense_date: Annotated[str, ...]",
    "add_expense_date_c": "expense_date: date",
    "add_expense_date_d": "expense_date: datetime",
}


def get_variant_description(name: str) -> str:
    """Get description for a variant, or empty string if unknown."""
    return VARIANT_DESCRIPTIONS.get(name, "")


def generate_markdown_report(data: dict) -> str:
    """Generate a markdown report from evaluation JSON data."""
    lines = []

    # Header
    lines.append("# MCP Tool Schema Evaluation Report")
    lines.append("")

    # Metadata
    meta = data.get("metadata", {})
    lines.append("## Metadata")
    lines.append("")
    lines.append(f"- **Timestamp**: {meta.get('timestamp', 'N/A')}")
    lines.append(f"- **API Host**: {meta.get('api_host', 'N/A')}")
    lines.append(f"- **Model**: {meta.get('model_name', 'N/A')}")
    model_settings = meta.get("model_settings", {})
    if model_settings:
        lines.append(f"- **Temperature**: {model_settings.get('temperature', 'N/A')}")
        lines.append(f"- **Seed**: {model_settings.get('seed', 'N/A')}")
    lines.append(f"- **MCP Server URL**: {meta.get('mcp_server_url', 'N/A')}")
    lines.append("")

    # Summary table
    summaries = data.get("summaries", {})
    if summaries:
        lines.append("## Variant Comparison")
        lines.append("")
        lines.append("| Variant | Description | Pass Rate | Avg Score | Passed | Total |")
        lines.append("|---------|-------------|-----------|-----------|--------|-------|")

        # Sort alphabetically by variant name (a -> d)
        sorted_summaries = sorted(summaries.items(), key=lambda x: x[0])

        for name, s in sorted_summaries:
            desc = get_variant_description(name)
            pass_rate = s.get("pass_rate", 0) * 100
            avg_score = s.get("avg_score", 0)
            passed = s.get("passed_cases", 0)
            total = s.get("total_cases", 0)
            lines.append(f"| {name} | {desc} | {pass_rate:.1f}% | {avg_score:.2f} | {passed} | {total} |")

        lines.append("")

    # Evaluation breakdown
    if summaries:
        lines.append("## Evaluation Breakdown")
        lines.append("")

        # Collect all eval names
        all_evals = set()
        for s in summaries.values():
            all_evals.update(s.get("eval_counts", {}).keys())

        for eval_name in sorted(all_evals):
            # Filter variants based on eval type
            if eval_name in ("category_match", "category_valid"):
                relevant_summaries = [(n, s) for n, s in sorted_summaries if "_cat_" in n]
            elif eval_name in ("date_match", "date_format"):
                relevant_summaries = [(n, s) for n, s in sorted_summaries if "_date_" in n]
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
                lines.append(f"| {name} | {desc} | {rate:.1f}% | {counts['passed']} | {total} |")

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
            status = "PASS" if score >= 0.8 else "FAIL"

            lines.append(f"### {variant} / {case}: {status} ({score:.2f})")
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
                    lines.append(f"- `{tc['tool_name']}`")
                    lines.append("  ```json")
                    lines.append(f"  {json.dumps(tc['arguments'], indent=2)}")
                    lines.append("  ```")
            else:
                lines.append("**No tool calls made**")

            lines.append("")

            eval_results = r.get("eval_results", {})
            if eval_results:
                lines.append("**Evaluations**:")
                lines.append("")
                for eval_name, er in eval_results.items():
                    status_symbol = "+" if er.get("passed") else "-"
                    lines.append(f"- [{status_symbol}] {eval_name}: {er.get('message', '')}")
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
