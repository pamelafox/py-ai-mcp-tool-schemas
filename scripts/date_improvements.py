"""Find cases where stricter date schemas helped for gpt-4.1-mini."""
import json

with open("evals/runs/gpt41mini_rerun/results.json") as f:
    data = json.load(f)

cases = {}
for r in data["results"]:
    v = r.get("tool_variant", "")
    if "date_" not in v:
        continue
    c = r.get("case_name", "")
    if c not in cases:
        cases[c] = {}
    cases[c][v] = r

# Find cases where date_d (pattern) succeeded but date_a (str) failed
print("=== Cases where Field(pattern) succeeded but str failed ===\n")
for case_name, variants in sorted(cases.items()):
    date_a = variants.get("add_expense_date_a", {})
    date_d = variants.get("add_expense_date_d", {})
    a_match = date_a.get("eval_results", {}).get("date_match", {}).get("score", 0)
    d_match = date_d.get("eval_results", {}).get("date_match", {}).get("score", 0)
    a_format = date_a.get("eval_results", {}).get("date_format", {}).get("score", 0)
    d_format = date_d.get("eval_results", {}).get("date_format", {}).get("score", 0)
    a_called = date_a.get("eval_results", {}).get("tool_called", {}).get("score", 0)
    d_called = date_d.get("eval_results", {}).get("tool_called", {}).get("score", 0)

    if (d_called == 1 and a_called == 0) or (d_format == 1 and a_format == 0) or (d_match == 1 and a_match == 0):
        tc_a = date_a.get("tool_calls", [])
        tc_d = date_d.get("tool_calls", [])
        got_a = tc_a[0]["arguments"].get("expense_date", "?") if tc_a else "NO CALL"
        got_d = tc_d[0]["arguments"].get("expense_date", "?") if tc_d else "NO CALL"
        print(f"  {case_name}:")
        print(f"    Query: {date_a.get('user_query', '')}")
        print(f"    str: {got_a} (called={a_called} format={a_format} match={a_match})")
        print(f"    pattern: {got_d} (called={d_called} format={d_format} match={d_match})")
        print()
