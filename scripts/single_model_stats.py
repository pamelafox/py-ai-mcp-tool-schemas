"""Get single-model eval numbers for slides from rerun2 (reasoning=medium)."""
import json

with open("evals/runs/gpt41mini_rerun/results.json") as f:
    data = json.load(f)

# Category table
print("=== Category (rerun2, reasoning=medium) ===")
for v in ["add_expense_cat_b", "add_expense_cat_c", "add_expense_cat_d", "add_expense_cat_e"]:
    results = [r for r in data["results"] if r.get("tool_variant") == v]
    total = len(results)
    match = sum(1 for r in results if r.get("eval_results", {}).get("category_match", {}).get("score", 0) == 1)
    valid = sum(1 for r in results if r.get("eval_results", {}).get("category_valid", {}).get("score", 0) == 1)
    called = sum(1 for r in results if r.get("eval_results", {}).get("tool_called", {}).get("score", 0) == 1)
    avg_input = sum(r.get("input_tokens", 0) or 0 for r in results) / total if total else 0
    short = v.replace("add_expense_", "")
    print(f"  {short}: match={match/total*100:.1f}% valid={valid/total*100:.1f}% called={called/total*100:.1f}% avg_input={avg_input:.0f}")

# Date table
print("\n=== Date (rerun2, reasoning=medium) ===")
for v in ["add_expense_date_a", "add_expense_date_b", "add_expense_date_c", "add_expense_date_d"]:
    results = [r for r in data["results"] if r.get("tool_variant") == v]
    total = len(results)
    match = sum(1 for r in results if r.get("eval_results", {}).get("date_match", {}).get("score", 0) == 1)
    fmt = sum(1 for r in results if r.get("eval_results", {}).get("date_format", {}).get("score", 0) == 1)
    called = sum(1 for r in results if r.get("eval_results", {}).get("tool_called", {}).get("score", 0) == 1)
    avg_input = sum(r.get("input_tokens", 0) or 0 for r in results) / total if total else 0
    short = v.replace("add_expense_", "")
    print(f"  {short}: match={match/total*100:.1f}% format={fmt/total*100:.1f}% called={called/total*100:.1f}% avg_input={avg_input:.0f}")
