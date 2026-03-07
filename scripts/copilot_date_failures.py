"""Analyze date failures in copilot SDK run - what dates did it pick?"""
import json
from datetime import date, timedelta

today = date(2026, 3, 6)

with open("evals/runs/copilot_53codex/results.json") as f:
    data = json.load(f)

for r in data["results"]:
    variant = r.get("tool_variant", "")
    if "date_c" not in variant:  # just check one date variant
        continue

    case = r.get("case_name", "")
    ev = r.get("eval_results", {})
    tc = r.get("tool_calls", [])
    dm = ev.get("date_match", {})

    if dm.get("score", 1) == 0:
        got_date = tc[0]["arguments"].get("expense_date", "?") if tc else "N/A"
        expected_msg = dm.get("message", "")
        print(f"{case}:")
        print(f"  Query: {r['user_query']}")
        print(f"  Got: {got_date}")
        print(f"  Eval: {expected_msg}")
        print()
