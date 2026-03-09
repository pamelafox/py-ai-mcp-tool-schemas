"""Compare date_d failures across the two v2b runs to see what changed."""
import json

# Previous run (with YYYY-MM-DD prompt, AnnotatedCategory)
# This was the first v2b run before the prompt change
old = json.load(open("evals/runs/gpt41mini_date_v2/results.json"))  # first run with cat_e, old prompt

# Current run (with natural language prompt, AnnotatedCategory) 
new = json.load(open("evals/runs/gpt41mini_date_v2b/results.json"))

for v in ["add_expense_date_d"]:
    short = v.replace("add_expense_", "")
    print(f"\n=== {short} ===")
    
    for label, data in [("OLD (YYYY-MM-DD prompt)", old), ("NEW (natural lang prompt)", new)]:
        results = [r for r in data["results"] if r.get("tool_variant") == v]
        print(f"\n  {label}:")
        for r in results:
            ev = r.get("eval_results", {})
            dm = ev.get("date_match", {}).get("score", 0)
            tc = ev.get("tool_called", {}).get("score", 0)
            if dm == 0:
                calls = r.get("tool_calls", [])
                dt = calls[0]["arguments"].get("expense_date", "?") if calls else "NO CALL"
                print(f"    FAIL: {r['case_name']}: got={dt}  tc={tc}")
