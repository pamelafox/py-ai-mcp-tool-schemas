"""Find cases where date_d (regex) is worse than date_a (str)."""
import json

with open("evals/runs/gpt41mini_date_v2b/results.json") as f:
    data = json.load(f)

cases = {}
for r in data["results"]:
    v = r.get("tool_variant", "")
    if not v.startswith("add_expense_date_"):
        continue
    case = r["case_name"]
    if case not in cases:
        cases[case] = {"query": r["user_query"]}
    ev = r.get("eval_results", {})
    dm = ev.get("date_match", {}).get("score", 0)
    tc = r.get("tool_calls", [])
    dt = tc[0]["arguments"].get("expense_date", "?") if tc else "NO CALL"
    cases[case][v.replace("add_expense_", "")] = (dm, dt)

print("Cases where date_d (regex) fails but date_a (str) passes:\n")
for case in sorted(cases):
    vals = cases[case]
    a_score = vals.get("date_a", (0, "?"))[0]
    d_score = vals.get("date_d", (0, "?"))[0]
    if d_score == 0 and a_score == 1:
        print(f"  {case}: {vals['query']}")
        for vs in ["date_a", "date_b", "date_c", "date_d"]:
            score, dt = vals.get(vs, (0, "?"))
            print(f"    {vs}: {dt} ({'PASS' if score else 'FAIL'})")
        print()

print("\nAll date_d failures:\n")
for case in sorted(cases):
    vals = cases[case]
    d_score, d_dt = vals.get("date_d", (0, "?"))
    if d_score == 0:
        print(f"  {case}: {vals['query']}")
        for vs in ["date_a", "date_b", "date_c", "date_d"]:
            score, dt = vals.get(vs, (0, "?"))
            print(f"    {vs}: {dt} ({'PASS' if score else 'FAIL'})")
        print()
