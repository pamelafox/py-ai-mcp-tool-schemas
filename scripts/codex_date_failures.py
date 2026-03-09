"""Check which date case failed for codex rerun2 across all date variants."""
import json

with open("evals/runs/gpt53codex_rerun2/results.json") as f:
    data = json.load(f)

for variant in ["add_expense_date_a", "add_expense_date_b", "add_expense_date_c", "add_expense_date_d"]:
    short = variant.replace("add_expense_", "")
    failures = []
    for r in data["results"]:
        if r.get("tool_variant") != variant:
            continue
        ev = r.get("eval_results", {})
        dm = ev.get("date_match", {})
        if dm.get("score", 1) == 0:
            tc = r.get("tool_calls", [])
            date_val = tc[0]["arguments"].get("expense_date", "?") if tc else "N/A"
            failures.append(f"{r['case_name']}: got={date_val} | {dm.get('message','')}")
    print(f"{short}: {len(failures)} failure(s)")
    for f2 in failures:
        print(f"  {f2}")
