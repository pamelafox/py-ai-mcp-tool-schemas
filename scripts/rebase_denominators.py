"""Compare category/date metrics using two denominators:
1. All cases (current)
2. Only cases where tool was called (proposed)
"""
import json

runs = {
    "gpt-4o": "evals/runs/gpt4o_rerun/results.json",
    "gpt-4.1-mini": "evals/runs/gpt41mini_rerun/results.json",
    "gpt-5.3-codex (med)": "evals/runs/gpt53codex_medium/results.json",
}

for label, path in runs.items():
    with open(path) as f:
        data = json.load(f)

    print(f"\n{'='*60}")
    print(f"  {label}")
    print(f"{'='*60}")

    for variant in ["add_expense_cat_b", "add_expense_cat_c", "add_expense_cat_d", "add_expense_cat_e"]:
        short = variant.replace("add_expense_", "")
        results = [r for r in data["results"] if r.get("tool_variant") == variant]
        total = len(results)
        called = [r for r in results if r.get("eval_results", {}).get("tool_called", {}).get("score", 0) == 1]
        n_called = len(called)
        
        # Current: out of all
        valid_all = sum(1 for r in results if r.get("eval_results", {}).get("category_valid", {}).get("score", 0) == 1)
        match_all = sum(1 for r in results if r.get("eval_results", {}).get("category_match", {}).get("score", 0) == 1)
        
        # Proposed: out of called only
        valid_called = sum(1 for r in called if r.get("eval_results", {}).get("category_valid", {}).get("score", 0) == 1)
        match_called = sum(1 for r in called if r.get("eval_results", {}).get("category_match", {}).get("score", 0) == 1)
        
        pct = lambda n, d: f"{n/d*100:.1f}%" if d > 0 else "N/A"
        
        print(f"\n  {short}: tool_called={pct(n_called, total)} ({n_called}/{total})")
        print(f"    cat_valid:  {pct(valid_all, total)} (all) → {pct(valid_called, n_called)} (of called)")
        print(f"    cat_match:  {pct(match_all, total)} (all) → {pct(match_called, n_called)} (of called)")

    print()
    for variant in ["add_expense_date_a", "add_expense_date_b", "add_expense_date_c", "add_expense_date_d"]:
        short = variant.replace("add_expense_", "")
        results = [r for r in data["results"] if r.get("tool_variant") == variant]
        total = len(results)
        called = [r for r in results if r.get("eval_results", {}).get("tool_called", {}).get("score", 0) == 1]
        n_called = len(called)
        
        fmt_all = sum(1 for r in results if r.get("eval_results", {}).get("date_format", {}).get("score", 0) == 1)
        match_all = sum(1 for r in results if r.get("eval_results", {}).get("date_match", {}).get("score", 0) == 1)
        
        fmt_called = sum(1 for r in called if r.get("eval_results", {}).get("date_format", {}).get("score", 0) == 1)
        match_called = sum(1 for r in called if r.get("eval_results", {}).get("date_match", {}).get("score", 0) == 1)
        
        pct = lambda n, d: f"{n/d*100:.1f}%" if d > 0 else "N/A"
        
        print(f"  {short}: tool_called={pct(n_called, total)} ({n_called}/{total})")
        print(f"    date_fmt:   {pct(fmt_all, total)} (all) → {pct(fmt_called, n_called)} (of called)")
        print(f"    date_match: {pct(match_all, total)} (all) → {pct(match_called, n_called)} (of called)")
