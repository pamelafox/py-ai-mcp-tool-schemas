import argparse
import asyncio
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

from pydantic_ai.mcp import MCPServerStreamableHTTP

# Ensure imports work when this file is executed as a script.
REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))


def _load_agent_functions():
    # Import after we ensure REPO_ROOT is on sys.path.
    from agents.pydanticai_agent import get_model, run_query

    return get_model, run_query


DEFAULT_QUERY = "Yesterday I bought a sandwich for $12.50."
DEFAULT_TOOL = "add_expense_cat_c"
DEFAULT_LEVELS = ["none", "low", "medium", "high", "xhigh"]
DEFAULT_SEED = 42
MCP_SERVER_URL = os.getenv("MCP_SERVER_URL", "http://localhost:8000/mcp")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate a reasoning diff markdown file")
    parser.add_argument("--query", type=str, default=DEFAULT_QUERY)
    parser.add_argument("--tool", type=str, default=DEFAULT_TOOL)
    parser.add_argument("--levels", type=str, default=",".join(DEFAULT_LEVELS))
    parser.add_argument("--seed", type=int, default=DEFAULT_SEED)
    parser.add_argument("--output", type=str, default="reasoning_diff.md")
    return parser.parse_args()


def _anchor(s: str) -> str:
    return s.lower().replace(" ", "-")


def _summarize(text: str | None) -> str:
    if not text:
        return "<none>"
    one = " ".join(text.split())
    return (one[:140] + "…") if len(one) > 140 else one


def _summarize_error(text: str | None) -> str:
    if not text:
        return "<none>"
    one = " ".join(text.split())
    return (one[:140] + "…") if len(one) > 140 else one


def _escape_md_cell(s: str) -> str:
    return s.replace("|", "\\|").replace("\n", "<br>")


async def main() -> None:
    args = parse_args()

    get_model, run_query = _load_agent_functions()

    query = args.query
    tool = args.tool
    levels = [s.strip() for s in args.levels.split(",") if s.strip()]
    seed = args.seed
    # NOTE: For GPT-5 models, OpenAI docs indicate `summary="auto"` is equivalent
    # to the most detailed summarizer available. We keep this fixed to `auto`.
    reasoning_summary = "auto"
    output_path = Path(args.output)

    rows: list[dict] = []

    async with MCPServerStreamableHTTP(url=MCP_SERVER_URL) as server:
        for level in levels:
            model = None
            model_settings = None
            cred = None
            try:
                model, model_settings, cred = get_model(level, seed=seed)
                result = await run_query(server, model, tool, query, model_settings)
                rows.append(
                    {
                        "reasoning_effort": level,
                        "reasoning_summary": reasoning_summary,
                        "seed": seed,
                        "tool": tool,
                        "query": query,
                        "reasoning": result.reasoning,
                        "output": result.output,
                        "tool_calls": [
                            {"tool_name": tc.tool_name, "arguments": tc.arguments}
                            for tc in result.tool_calls
                        ],
                        "error": result.error,
                    }
                )
            finally:
                if cred is not None:
                    await cred.close()

    now = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")

    md: list[str] = []
    md.append("# Reasoning diff\n")
    md.append(f"Generated: {now}  ")
    md.append(f"Query: `{query}`  ")
    md.append(f"Tool: `{tool}`  ")
    md.append(f"Reasoning summary: `{reasoning_summary}`  ")
    md.append(f"Seed: `{seed}`\n")

    md.append("## Table\n")
    md.append("| Reasoning effort | Reasoning (verbatim excerpt) | Full text |")
    md.append("|---|---|---|")
    for r in rows:
        effort = r["reasoning_effort"]
        if r.get("error"):
            excerpt = _escape_md_cell("ERROR: " + _summarize_error(r["error"]))
        else:
            excerpt = _escape_md_cell(_summarize(r["reasoning"]))
        link = f"[full](#{_anchor('reasoning-' + effort)})"
        md.append(f"| `{effort}` | {excerpt} | {link} |")

    md.append("\n## Noted differences\n")
    errors = [r for r in rows if r.get("error")]
    if errors:
        efforts = ", ".join(f"`{r['reasoning_effort']}`" for r in errors)
        md.append(f"- Errors occurred for: {efforts}.")

    tool_called = [r for r in rows if (r.get("tool_calls") or [])]
    no_tool_called = [r for r in rows if not (r.get("tool_calls") or []) and not r.get("error")]

    if tool_called:
        efforts = ", ".join(f"`{r['reasoning_effort']}`" for r in tool_called)
        md.append(f"- Tool was called for: {efforts}.")
    if no_tool_called:
        efforts = ", ".join(f"`{r['reasoning_effort']}`" for r in no_tool_called)
        md.append(f"- No tool call was made for: {efforts}.")

    md.append(
        "- Reasoning text is a model-provided summary (not full chain-of-thought).\n"
    )

    md.append("## Full reasoning text\n")
    for r in rows:
        effort = r["reasoning_effort"]
        md.append(f"### reasoning-{effort}\n")
        if r.get("error"):
            md.append(f"Error: `{r['error']}`\n")

        md.append("Reasoning (verbatim):")
        md.append("```")
        md.append(r["reasoning"] if r["reasoning"] else "<no reasoning returned>")
        md.append("```")

        md.append("\nOutput (verbatim):")
        md.append("```")
        md.append(r["output"] if r["output"] else "<no output>")
        md.append("```")
        md.append("")

    output_path.write_text("\n".join(md), encoding="utf-8")
    print(f"Wrote {output_path}")


if __name__ == "__main__":
    asyncio.run(main())
