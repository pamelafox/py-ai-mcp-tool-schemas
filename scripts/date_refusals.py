"""Find tool_called failures for date variants in gpt-4.1-mini."""
import json

with open("evals/runs/gpt41mini_rerun/results.json") as f:
    data = json.load(f)

for variant in ["add_expense_date_a", "add_expense_date_b", "add_expense_date_c", "add_expense_date_d"]:
    short = variant.replace("add_expense_", "")
    for r in data["results"]:
        if r.get("tool_variant") != variant:
            continue
        ev = r.get("eval_results", {})
        if ev.get("tool_called", {}).get("score", 1) == 0:
            print(f"{short} / {r['case_name']}")
            print(f"  Query: {r['user_query']}")
            print(f"  Output: {r['agent_output'][:250]}")
            print()
