"""Find cases where tool calling improved from cat_b to cat_e."""
import json

with open("evals/runs/gpt41mini_cat_v2/results.json") as f:
    data = json.load(f)

cases = set(r["case_name"] for r in data["results"])
for case in sorted(cases):
    b = next((r for r in data["results"] if r["case_name"] == case and r["tool_variant"] == "add_expense_cat_b"), None)
    e = next((r for r in data["results"] if r["case_name"] == case and r["tool_variant"] == "add_expense_cat_e"), None)
    if not b or not e:
        continue
    b_tc = b.get("eval_results", {}).get("tool_called", {}).get("score", 0)
    e_tc = e.get("eval_results", {}).get("tool_called", {}).get("score", 0)
    e_cm = e.get("eval_results", {}).get("category_match", {}).get("score", 0)
    if b_tc == 0 and e_tc == 1:
        e_cat = e["tool_calls"][0]["arguments"].get("category", "?")
        print(f"{case}: {b['user_query']}")
        print(f"  cat_b: NO CALL")
        print(f"  cat_e: {e_cat} (match={'PASS' if e_cm else 'FAIL'})")
        print()
