"""Compare specific failure cases across models."""
import json

runs = {
    "gpt-4o": "evals/runs/gpt4o_rerun/results.json",
    "gpt-4.1-mini": "evals/runs/gpt41mini_rerun/results.json",
    "gpt-5.3-codex": "evals/runs/gpt53codex_rerun/results.json",
}

for model, path in runs.items():
    with open(path) as f:
        data = json.load(f)

    cat_e_fails = []
    cat_b_fails = []
    date_d_fails = []
    no_tool_calls = []

    for r in data["results"]:
        variant = r.get("tool_variant", "")
        case = r.get("case_name", "")
        evals = r.get("eval_results", {})
        tc = r.get("tool_calls", [])

        tool_called = evals.get("tool_called", {}).get("score", 1)
        if tool_called == 0:
            no_tool_calls.append(f"  {variant}/{case}")

        if variant == "add_expense_cat_e":
            cat_match = evals.get("category_match", {})
            if cat_match.get("score", 1) == 0:
                cat_val = tc[0].get("arguments", {}).get("category", "N/A") if tc else "NO CALL"
                cat_e_fails.append(f"  {case}: got={cat_val}")

        if variant == "add_expense_cat_b":
            cat_match = evals.get("category_match", {})
            if cat_match.get("score", 1) == 0:
                cat_val = tc[0].get("arguments", {}).get("category", "N/A") if tc else "NO CALL"
                cat_b_fails.append(f"  {case}: got={cat_val}")

        if variant == "add_expense_date_d":
            date_match = evals.get("date_match", {})
            if date_match.get("score", 0) == 0:
                date_val = tc[0].get("arguments", {}).get("expense_date", "N/A") if tc else "NO CALL"
                date_d_fails.append(f"  {case}: got={date_val}")

    print(f"=== {model} ===")
    print(f"cat_e failures ({len(cat_e_fails)}):")
    for f2 in cat_e_fails:
        print(f2)
    print(f"cat_b failures ({len(cat_b_fails)}):")
    for f2 in cat_b_fails:
        print(f2)
    print(f"date_d failures ({len(date_d_fails)}):")
    for f2 in date_d_fails:
        print(f2)
    print(f"no tool call at all ({len(no_tool_calls)}):")
    for f2 in no_tool_calls:
        print(f2)
    print()
