"""Find examples for date slide: tool refusal, and date_d wrong but date_a right."""
import json

with open("evals/runs/gpt41mini_date_v2b/results.json") as f:
    data = json.load(f)

# 1. Tool refusal example (date_c has one)
print("=== Tool refusal (date_c) ===")
for r in data["results"]:
    if r.get("tool_variant") == "add_expense_date_c":
        ev = r.get("eval_results", {})
        if ev.get("tool_called", {}).get("score", 0) == 0:
            print(f"  Case: {r['case_name']}")
            print(f"  Query: {r['user_query']}")
            print(f"  Output: {r['agent_output'][:300]}")
            print()

# 2. Cases where date_a got it right but date_d got it wrong
print("=== date_a right, date_d wrong ===")
cases = set(r["case_name"] for r in data["results"])
for case in sorted(cases):
    a = next((r for r in data["results"] if r["case_name"] == case and r["tool_variant"] == "add_expense_date_a"), None)
    d = next((r for r in data["results"] if r["case_name"] == case and r["tool_variant"] == "add_expense_date_d"), None)
    if not a or not d:
        continue
    a_dm = a.get("eval_results", {}).get("date_match", {}).get("score", 0)
    d_dm = d.get("eval_results", {}).get("date_match", {}).get("score", 0)
    a_tc = a.get("eval_results", {}).get("tool_called", {}).get("score", 0)
    d_tc = d.get("eval_results", {}).get("tool_called", {}).get("score", 0)
    if a_dm == 1 and d_dm == 0 and a_tc == 1 and d_tc == 1:
        a_dt = a["tool_calls"][0]["arguments"].get("expense_date", "?")
        d_dt = d["tool_calls"][0]["arguments"].get("expense_date", "?")
        print(f"  Case: {case}")
        print(f"  Query: {a['user_query']}")
        print(f"  date_a (str): {a_dt} (PASS)")
        print(f"  date_d (pattern): {d_dt} (FAIL)")
        print()

# 3. Also show all shared failures (same wrong date everywhere)
print("=== Shared failures (all variants wrong) ===")
for case in sorted(cases):
    results_for_case = [r for r in data["results"] if r["case_name"] == case]
    all_fail = all(
        r.get("eval_results", {}).get("date_match", {}).get("score", 0) == 0
        for r in results_for_case
        if r.get("eval_results", {}).get("tool_called", {}).get("score", 0) == 1
    )
    any_called = any(
        r.get("eval_results", {}).get("tool_called", {}).get("score", 0) == 1
        for r in results_for_case
    )
    if all_fail and any_called:
        r0 = results_for_case[0]
        dates = {}
        for r in results_for_case:
            v = r["tool_variant"].replace("add_expense_", "")
            tc = r.get("tool_calls", [])
            dt = tc[0]["arguments"].get("expense_date", "?") if tc else "NO CALL"
            dates[v] = dt
        print(f"  {case}: {r0['user_query']}")
        for v, dt in sorted(dates.items()):
            print(f"    {v}: {dt}")
        print()
