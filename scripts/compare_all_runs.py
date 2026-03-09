"""Compare all codex reasoning levels for the single-model eval slide."""
import json

runs = {
    "low": "evals/runs/gpt53codex_low/results.json",
    "medium": "evals/runs/gpt53codex_medium/results.json",
    "high": "evals/runs/gpt53codex_high/results.json",
}

for label, path in runs.items():
    with open(path) as f:
        data = json.load(f)
    print(f"\n=== reasoning={label} ===")
    for v in ["add_expense_cat_b", "add_expense_cat_c", "add_expense_cat_d", "add_expense_cat_e"]:
        results = [r for r in data["results"] if r.get("tool_variant") == v]
        total = len(results)
        match = sum(1 for r in results if r.get("eval_results", {}).get("category_match", {}).get("score", 0) == 1)
        valid = sum(1 for r in results if r.get("eval_results", {}).get("category_valid", {}).get("score", 0) == 1)
        called = sum(1 for r in results if r.get("eval_results", {}).get("tool_called", {}).get("score", 0) == 1)
        short = v.replace("add_expense_", "")
        print(f"  {short}: match={match/total*100:.1f}% valid={valid/total*100:.1f}% called={called/total*100:.1f}%")

# Also check gpt-4o and gpt-4.1-mini for comparison
other_runs = {
    "gpt-4o": "evals/runs/gpt4o_rerun/results.json",
    "gpt-4.1-mini": "evals/runs/gpt41mini_rerun/results.json",
}
for label, path in other_runs.items():
    with open(path) as f:
        data = json.load(f)
    print(f"\n=== {label} ===")
    for v in ["add_expense_cat_b", "add_expense_cat_c", "add_expense_cat_d", "add_expense_cat_e"]:
        results = [r for r in data["results"] if r.get("tool_variant") == v]
        total = len(results)
        match = sum(1 for r in results if r.get("eval_results", {}).get("category_match", {}).get("score", 0) == 1)
        valid = sum(1 for r in results if r.get("eval_results", {}).get("category_valid", {}).get("score", 0) == 1)
        called = sum(1 for r in results if r.get("eval_results", {}).get("tool_called", {}).get("score", 0) == 1)
        short = v.replace("add_expense_", "")
        print(f"  {short}: match={match/total*100:.1f}% valid={valid/total*100:.1f}% called={called/total*100:.1f}%")
