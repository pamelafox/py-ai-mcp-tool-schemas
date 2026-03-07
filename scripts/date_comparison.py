"""Get date eval results for cross-model comparison."""
import json

runs = {
    "gpt-4o": "evals/runs/gpt4o_rerun/results.json",
    "gpt-4.1-mini": "evals/runs/gpt41mini_rerun/results.json",
    "gpt-5.3-codex": "evals/runs/gpt53codex_rerun/results.json",
}

for model, path in runs.items():
    with open(path) as f:
        data = json.load(f)
    print(f"=== {model} ===")
    for variant in ["add_expense_date_a", "add_expense_date_b", "add_expense_date_c", "add_expense_date_d"]:
        match_pass = 0
        format_pass = 0
        tool_pass = 0
        total = 0
        for r in data["results"]:
            if r.get("tool_variant", "") == variant:
                total += 1
                ev = r.get("eval_results", {})
                if ev.get("date_match", {}).get("score", 0) == 1:
                    match_pass += 1
                if ev.get("date_format", {}).get("score", 0) == 1:
                    format_pass += 1
                if ev.get("tool_called", {}).get("score", 0) == 1:
                    tool_pass += 1
        short = variant.replace("add_expense_", "")
        m_pct = f"{match_pass/total*100:.1f}%" if total else "N/A"
        f_pct = f"{format_pass/total*100:.1f}%" if total else "N/A"
        t_pct = f"{tool_pass/total*100:.1f}%" if total else "N/A"
        print(f"  {short}: match={m_pct} format={f_pct} tool={t_pct} ({match_pass}/{total})")
    print()
