"""Compare old (cat_d) vs new (cat_e) date variant results."""
import json
import sys

old_path = sys.argv[1] if len(sys.argv) > 1 else "evals/runs/gpt41mini_rerun/results.json"
new_path = sys.argv[2] if len(sys.argv) > 2 else "evals/runs/gpt41mini_date_v2/results.json"

old = json.load(open(old_path))
new = json.load(open(new_path))

print(f"OLD: {old_path}")
print(f"NEW: {new_path}")
print()

for v in ["add_expense_date_a", "add_expense_date_b", "add_expense_date_c", "add_expense_date_d"]:
    short = v.replace("add_expense_", "")

    def stats(data):
        results = [r for r in data["results"] if r.get("tool_variant") == v]
        total = len(results)
        if total == 0:
            return 0, 0, 0, 0, []
        called = [r for r in results if r.get("eval_results", {}).get("tool_called", {}).get("score", 0) == 1]
        n_called = len(called)
        dm_all = sum(1 for r in results if r.get("eval_results", {}).get("date_match", {}).get("score", 0) == 1)
        dm_called = sum(1 for r in called if r.get("eval_results", {}).get("date_match", {}).get("score", 0) == 1)
        refusals = [r["case_name"] for r in results if r.get("eval_results", {}).get("tool_called", {}).get("score", 0) == 0]
        return total, n_called, dm_all, dm_called, refusals

    ot, oc, oda, odc, oref = stats(old)
    nt, nc, nda, ndc, nref = stats(new)

    pct = lambda n, d: f"{n/d*100:.1f}%" if d > 0 else "N/A"

    print(f"{short}:")
    if ot > 0:
        print(f"  OLD (cat_d): called={pct(oc,ot)} ({oc}/{ot})  date_match(all)={pct(oda,ot)}  date_match(called)={pct(odc,oc)}  refusals={oref}")
    print(f"  NEW (cat_e): called={pct(nc,nt)} ({nc}/{nt})  date_match(all)={pct(nda,nt)}  date_match(called)={pct(ndc,nc)}  refusals={nref}")
    print()
