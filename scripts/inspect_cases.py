"""Inspect specific failure cases across models."""
import json

runs = {
    "gpt-4o": "evals/runs/gpt4o_rerun/results.json",
    "gpt-4.1-mini": "evals/runs/gpt41mini_rerun/results.json",
    "gpt-5.3-codex": "evals/runs/gpt53codex_rerun/results.json",
}

# Cases of interest
CASES = ["edge_large_amount", "edge_unknown_category", "relative_date_last_friday_movie"]

for model, path in runs.items():
    with open(path) as f:
        data = json.load(f)
    print(f"\n{'='*60}")
    print(f"  {model}")
    print(f"{'='*60}")
    for r in data["results"]:
        case = r.get("case_name", "")
        variant = r.get("tool_variant", "")
        if case in CASES and ("cat_e" in variant or "cat_b" in variant):
            tc = r.get("tool_calls", [])
            cat = tc[0]["arguments"].get("category", "?") if tc else "NO CALL"
            output = r.get("agent_output", "")[:200]
            print(f"\n  {case} ({variant}):")
            print(f"    Query: {r['user_query']}")
            print(f"    Category: {cat}")
            print(f"    Output: {output}")
            evals = r.get("eval_results", {})
            cm = evals.get("category_match", {})
            tc_eval = evals.get("tool_called", {})
            print(f"    category_match: {cm.get('message', 'N/A')}")
            print(f"    tool_called: {tc_eval.get('message', 'N/A')}")

    # Also show no-tool-call count by variant
    print(f"\n  No-tool-call summary:")
    from collections import Counter
    no_call_variants = Counter()
    for r in data["results"]:
        variant = r.get("tool_variant", "")
        evals = r.get("eval_results", {})
        tc_eval = evals.get("tool_called", {})
        if tc_eval.get("score", 1) == 0:
            no_call_variants[variant] += 1
    for v, c in sorted(no_call_variants.items()):
        print(f"    {v}: {c} no-calls")
