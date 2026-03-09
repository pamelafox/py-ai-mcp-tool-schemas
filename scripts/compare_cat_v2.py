"""Compare old vs new category results for gpt-4.1-mini."""
import json

old = json.load(open("evals/runs/gpt41mini_rerun/results.json"))
new = json.load(open("evals/runs/gpt41mini_cat_v2/results.json"))

for v in ["add_expense_cat_b", "add_expense_cat_c", "add_expense_cat_d", "add_expense_cat_e"]:
    short = v.replace("add_expense_", "")

    def stats(data):
        results = [r for r in data["results"] if r.get("tool_variant") == v]
        total = len(results)
        if total == 0:
            return 0, 0, 0, 0, 0, []
        called = [r for r in results if r.get("eval_results", {}).get("tool_called", {}).get("score", 0) == 1]
        n_called = len(called)
        cv = sum(1 for r in called if r.get("eval_results", {}).get("category_valid", {}).get("score", 0) == 1)
        cm = sum(1 for r in called if r.get("eval_results", {}).get("category_match", {}).get("score", 0) == 1)
        refusals = [r["case_name"] for r in results if r.get("eval_results", {}).get("tool_called", {}).get("score", 0) == 0]
        return total, n_called, cv, cm, refusals

    pct = lambda n, d: f"{n/d*100:.1f}%" if d > 0 else "N/A"

    ot, oc, ocv, ocm, oref = stats(old)
    nt, nc, ncv, ncm, nref = stats(new)

    print(f"{short}:")
    print(f"  OLD: called={pct(oc,ot)} ({oc}/{ot})  valid(called)={pct(ocv,oc)}  match(called)={pct(ocm,oc)}  refusals={oref}")
    print(f"  NEW: called={pct(nc,nt)} ({nc}/{nt})  valid(called)={pct(ncv,nc)}  match(called)={pct(ncm,nc)}  refusals={nref}")
    print()
