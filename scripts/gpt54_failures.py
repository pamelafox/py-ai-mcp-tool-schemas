"""Analyze gpt-5.4 failures with reasoning traces."""
import json

with open("evals/runs/gpt54_medium/results.json") as f:
    data = json.load(f)

for variant_label, variant, evals_to_check in [
    ("cat_e", "add_expense_cat_e", ["tool_called", "category_valid", "category_match"]),
    ("date_b", "add_expense_date_b", ["tool_called", "date_match"]),
    ("date_d", "add_expense_date_d", ["tool_called", "date_match"]),
]:
    print(f"\n{'='*60}")
    print(f"  {variant_label} failures")
    print(f"{'='*60}")
    for r in data["results"]:
        if r.get("tool_variant") != variant:
            continue
        ev = r.get("eval_results", {})
        failed = [e for e in evals_to_check if ev.get(e, {}).get("score", 1) == 0]
        if not failed:
            continue
        print(f"\n  Case: {r['case_name']}  (failed: {', '.join(failed)})")
        print(f"  Query: {r['user_query']}")
        calls = r.get("tool_calls", [])
        if calls:
            args = calls[0].get("arguments", {})
            print(f"  Args: category={args.get('category','?')} date={args.get('expense_date','?')}")
        else:
            print(f"  No tool call!")
            print(f"  Output: {r['agent_output'][:300]}")
        reasoning = r.get("reasoning", "") or ""
        if reasoning:
            print(f"  Reasoning: {reasoning[:500]}")

# Also compare same cases against 5.3-codex
print(f"\n\n{'='*60}")
print("  Same cases in gpt-5.3-codex (medium)")
print(f"{'='*60}")

with open("evals/runs/gpt53codex_medium/results.json") as f:
    codex = json.load(f)

# Get failing case names from 5.4
failing_cases = {}
for r in data["results"]:
    ev = r.get("eval_results", {})
    v = r.get("tool_variant", "")
    for e in ["tool_called", "category_valid", "category_match", "date_match"]:
        if ev.get(e, {}).get("score", 1) == 0:
            failing_cases[(v, r["case_name"])] = True

for r in codex["results"]:
    key = (r.get("tool_variant", ""), r.get("case_name", ""))
    if key not in failing_cases:
        continue
    ev = r.get("eval_results", {})
    print(f"\n  {key[0]} / {key[1]}")
    calls = r.get("tool_calls", [])
    if calls:
        args = calls[0].get("arguments", {})
        print(f"  Args: category={args.get('category','?')} date={args.get('expense_date','?')}")
    tc = ev.get("tool_called", {}).get("score", "?")
    cm = ev.get("category_match", {}).get("score", "?")
    dm = ev.get("date_match", {}).get("score", "?")
    print(f"  tool_called={tc} category_match={cm} date_match={dm}")
    reasoning = r.get("reasoning", "") or ""
    if reasoning:
        print(f"  Reasoning: {reasoning[:400]}")
