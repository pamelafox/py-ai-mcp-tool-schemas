"""Find category_valid failures across models."""
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
    print(f"  {label} — category_valid failures")
    print(f"{'='*60}")

    found = False
    for r in data["results"]:
        v = r.get("tool_variant", "")
        if not v.startswith("add_expense_cat_"):
            continue
        ev = r.get("eval_results", {})
        cv = ev.get("category_valid", {}).get("score", 1)
        tc = ev.get("tool_called", {}).get("score", 1)
        if cv == 0 or tc == 0:
            found = True
            short_v = v.replace("add_expense_", "")
            calls = r.get("tool_calls", [])
            if calls:
                cat = calls[0]["arguments"].get("category", "?")
                print(f"\n  {short_v} / {r['case_name']}")
                print(f"    Query: {r['user_query']}")
                print(f"    Category sent: '{cat}'")
                print(f"    category_valid={cv}, tool_called={tc}")
            else:
                print(f"\n  {short_v} / {r['case_name']}")
                print(f"    Query: {r['user_query']}")
                print(f"    NO TOOL CALL")
                print(f"    Output: {r['agent_output'][:200]}")

    if not found:
        print("  (no failures)")
