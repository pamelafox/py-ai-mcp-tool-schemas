"""Get rerun2 (reasoning=medium) numbers for cross-model table update."""
import json

with open("evals/runs/gpt53codex_rerun2/results.json") as f:
    data = json.load(f)

for metric, variants in [
    ("category_valid", ["add_expense_cat_b", "add_expense_cat_c", "add_expense_cat_d", "add_expense_cat_e"]),
    ("category_match", ["add_expense_cat_b", "add_expense_cat_c", "add_expense_cat_d", "add_expense_cat_e"]),
    ("date_format", ["add_expense_date_a", "add_expense_date_b", "add_expense_date_c", "add_expense_date_d"]),
    ("date_match", ["add_expense_date_a", "add_expense_date_b", "add_expense_date_c", "add_expense_date_d"]),
]:
    print(f"\n{metric}:")
    for v in variants:
        passed = sum(1 for r in data["results"] if r.get("tool_variant") == v and r.get("eval_results", {}).get(metric, {}).get("score", 0) == 1)
        total = sum(1 for r in data["results"] if r.get("tool_variant") == v)
        pct = passed / total * 100 if total else 0
        short = v.replace("add_expense_", "")
        print(f"  {short}: {pct:.1f}% ({passed}/{total})")
