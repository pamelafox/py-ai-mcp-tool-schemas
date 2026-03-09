"""Find cases where tool was called but date was wrong, per date variant."""
import json

with open("evals/runs/gpt41mini_rerun/results.json") as f:
    data = json.load(f)

for variant in ["add_expense_date_a", "add_expense_date_b", "add_expense_date_c", "add_expense_date_d"]:
    short = variant.replace("add_expense_", "")
    wrong = []
    for r in data["results"]:
        if r.get("tool_variant") != variant:
            continue
        ev = r.get("eval_results", {})
        called = ev.get("tool_called", {}).get("score", 0) == 1
        date_match = ev.get("date_match", {}).get("score", 0) == 1
        if called and not date_match:
            calls = r.get("tool_calls", [])
            actual_date = calls[0]["arguments"].get("expense_date", "?") if calls else "?"
            expected = r.get("expected_date", "?")
            wrong.append((r["case_name"], r["user_query"], actual_date, expected))
    
    total_called = sum(1 for r in data["results"] if r.get("tool_variant") == variant and r.get("eval_results", {}).get("tool_called", {}).get("score", 0) == 1)
    wrong_count = len(wrong)
    right_count = total_called - wrong_count
    print(f"\n{short}: {right_count}/{total_called} date correct when called ({right_count/total_called*100:.1f}%)")
    for name, query, actual, expected in wrong:
        print(f"  {name}")
        print(f"    Query: {query}")
        print(f"    Got: {actual}  Expected: {expected}")
