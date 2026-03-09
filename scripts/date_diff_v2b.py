"""Find cases where date_a (str) got it right but other date variants got it wrong."""
import json

with open("evals/runs/gpt41mini_date_v2b/results.json") as f:
    data = json.load(f)

# Build a map of (case_name, variant) -> date_match score
scores = {}
for r in data["results"]:
    v = r.get("tool_variant", "")
    if not v.startswith("add_expense_date_"):
        continue
    case = r["case_name"]
    dm = r.get("eval_results", {}).get("date_match", {}).get("score", 0)
    scores[(case, v)] = dm

# Find cases where date_a passes but others fail
cases = set(c for c, v in scores.keys())
for case in sorted(cases):
    a = scores.get((case, "add_expense_date_a"), 0)
    b = scores.get((case, "add_expense_date_b"), 0)
    c = scores.get((case, "add_expense_date_c"), 0)
    d = scores.get((case, "add_expense_date_d"), 0)
    if a != b or a != c or a != d:
        # Find the actual dates
        dates = {}
        for r in data["results"]:
            if r["case_name"] == case and r["tool_variant"].startswith("add_expense_date_"):
                v_short = r["tool_variant"].replace("add_expense_", "")
                tc = r.get("tool_calls", [])
                dt = tc[0]["arguments"].get("expense_date", "?") if tc else "?"
                dates[v_short] = dt
        
        print(f"{case}: a={a} b={b} c={c} d={d}")
        # Find query
        for r in data["results"]:
            if r["case_name"] == case and r["tool_variant"] == "add_expense_date_a":
                print(f"  Query: {r['user_query']}")
                break
        for v_short, dt in sorted(dates.items()):
            print(f"  {v_short}: {dt}")
        print()
