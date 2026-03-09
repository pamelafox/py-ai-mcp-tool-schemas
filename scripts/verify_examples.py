"""Verify slide examples against latest eval data."""
import json

with open("evals/runs/gpt41mini_cat_v2/results.json") as f:
    data = json.load(f)

examples = [
    ("edge_small_amount", "I paid $0.99 for an app"),
    ("relative_date_last_friday_movie", "Last Friday I spent $18 on a movie ticket"),
    ("edge_large_amount", "Yesterday I bought a car for 35000 USD"),
]

for case_name, query in examples:
    print(f"\n{case_name}: {query}")
    for v in ["add_expense_cat_b", "add_expense_cat_c", "add_expense_cat_d", "add_expense_cat_e"]:
        short = v.replace("add_expense_", "")
        for r in data["results"]:
            if r.get("tool_variant") == v and r.get("case_name") == case_name:
                ev = r.get("eval_results", {})
                tc = ev.get("tool_called", {}).get("score", 0)
                cm = ev.get("category_match", {}).get("score", 0)
                calls = r.get("tool_calls", [])
                cat = calls[0]["arguments"].get("category", "?") if calls else "NO CALL"
                print(f"  {short}: tc={tc} cm={cm} category={cat}")
                break
