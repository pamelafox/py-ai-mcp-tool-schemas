"""Get specific case examples for the cross-model comparison slide."""
import json

runs = {
    "gpt-4o": "evals/runs/gpt4o_rerun/results.json",
    "gpt-4.1-mini": "evals/runs/gpt41mini_rerun/results.json",
    "gpt-5.3-codex": "evals/runs/gpt53codex_rerun/results.json",
}

CASES = [
    ("add_expense_cat_b", "edge_large_amount"),
    ("add_expense_cat_b", "relative_date_last_friday_movie"),
    ("add_expense_cat_e", "edge_large_amount"),
    ("add_expense_cat_e", "edge_unknown_category"),
]

for variant, case in CASES:
    print(f"\n{'='*60}")
    print(f"  {variant} / {case}")
    print(f"{'='*60}")
    for model, path in runs.items():
        with open(path) as f:
            data = json.load(f)
        for r in data["results"]:
            if r.get("tool_variant") == variant and r.get("case_name") == case:
                tc = r.get("tool_calls", [])
                ev = r.get("eval_results", {})
                output = r.get("agent_output", "")
                if tc:
                    cat = tc[0]["arguments"].get("category", "?")
                    print(f"  {model}: called tool, category={cat}")
                else:
                    # Show first line of output
                    first_line = output.split("\n")[0][:120]
                    print(f"  {model}: NO CALL -> {first_line}")
                break
