"""Analyze reasoning traces from codex failures."""
import json

with open("evals/runs/gpt53codex_rerun/results.json") as f:
    data = json.load(f)

# Find cases where tool wasn't called or category didn't match
for r in data["results"]:
    variant = r.get("tool_variant", "")
    case = r.get("case_name", "")
    ev = r.get("eval_results", {})
    tc = r.get("tool_calls", [])
    reasoning = r.get("reasoning", "")
    output = r.get("agent_output", "")

    tool_called = ev.get("tool_called", {}).get("score", 1)
    cat_match = ev.get("category_match", {}).get("score", 1)
    date_match = ev.get("date_match", {}).get("score", 1)

    failed = tool_called == 0 or cat_match == 0 or date_match == 0
    if not failed:
        continue

    # Only show cat and date variants
    if "cat_" not in variant and "date_" not in variant:
        continue

    print(f"=== {variant} / {case} ===")
    if tool_called == 0:
        print("  FAILURE: Tool not called")
    if cat_match == 0:
        cat_val = tc[0]["arguments"].get("category", "?") if tc else "N/A"
        print(f"  FAILURE: Category mismatch: got={cat_val}")
    if date_match == 0:
        date_val = tc[0]["arguments"].get("expense_date", "?") if tc else "N/A"
        print(f"  FAILURE: Date mismatch: got={date_val}")
    print(f"  Query: {r['user_query']}")
    if reasoning:
        # Show first 300 chars of reasoning
        print(f"  Reasoning: {reasoning[:400]}")
    else:
        print(f"  Reasoning: (none)")
    if not tc:
        print(f"  Output: {output[:300]}")
    print()
