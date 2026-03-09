"""Compare gpt53codex_low (reasoning=low) vs gpt53codex_rerun2 (reasoning=medium)."""
import json

runs = {
    "low": "evals/runs/gpt53codex_low/results.json",
    "medium": "evals/runs/gpt53codex_rerun2/results.json",
}

for label, path in runs.items():
    with open(path) as f:
        data = json.load(f)
    print(f"\n=== reasoning={label} ===")
    for metric, variants in [
        ("category_match", ["add_expense_cat_b", "add_expense_cat_c", "add_expense_cat_d", "add_expense_cat_e"]),
        ("category_valid", ["add_expense_cat_b", "add_expense_cat_c", "add_expense_cat_d", "add_expense_cat_e"]),
        ("date_match", ["add_expense_date_a", "add_expense_date_b", "add_expense_date_c", "add_expense_date_d"]),
        ("tool_called", ["add_expense_cat_b", "add_expense_cat_c", "add_expense_cat_d", "add_expense_cat_e"]),
    ]:
        print(f"  {metric}:")
        for v in variants:
            passed = sum(1 for r in data["results"] if r.get("tool_variant") == v and r.get("eval_results", {}).get(metric, {}).get("score", 0) == 1)
            total = sum(1 for r in data["results"] if r.get("tool_variant") == v)
            short = v.replace("add_expense_", "")
            pct = f"{passed/total*100:.1f}%" if total else "N/A"
            print(f"    {short}: {pct} ({passed}/{total})")
