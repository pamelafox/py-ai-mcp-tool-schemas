"""Compare reasoning traces for cat_e failures across reasoning levels."""
import json

# The two cases that fail at medium/high/xhigh but pass at low
FAILING_CASES = ["edge_large_amount", "edge_unknown_category"]

runs = {
    "low": "evals/runs/gpt53codex_low/results.json",
    "medium": "evals/runs/gpt53codex_medium/results.json",
    "high": "evals/runs/gpt53codex_high/results.json",
    "xhigh": "evals/runs/gpt53codex_xhigh/results.json",
}

for case_name in FAILING_CASES:
    print(f"\n{'='*70}")
    print(f"  Case: {case_name}")
    print(f"{'='*70}")
    for label, path in runs.items():
        with open(path) as f:
            data = json.load(f)
        for r in data["results"]:
            if r.get("tool_variant") == "add_expense_cat_e" and r.get("case_name") == case_name:
                tc = r.get("tool_calls", [])
                cat = tc[0]["arguments"].get("category", "?") if tc else "NO CALL"
                reasoning = r.get("reasoning", "") or ""
                ev = r.get("eval_results", {})
                match = ev.get("category_match", {}).get("score", 0)
                print(f"\n  --- reasoning={label} (match={'PASS' if match == 1 else 'FAIL'}) ---")
                print(f"  Category: {cat}")
                if reasoning:
                    # Show first 400 chars
                    print(f"  Reasoning: {reasoning[:400]}")
                else:
                    print(f"  Reasoning: (none)")
                break
