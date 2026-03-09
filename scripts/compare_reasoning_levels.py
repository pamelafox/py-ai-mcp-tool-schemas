"""Compare all reasoning levels for gpt-5.3-codex."""
import json

runs = {
    "low": "evals/runs/gpt53codex_low/results.json",
    "medium": "evals/runs/gpt53codex_medium/results.json",
    "high": "evals/runs/gpt53codex_high/results.json",
    "xhigh": "evals/runs/gpt53codex_xhigh/results.json",
}

for label, path in runs.items():
    with open(path) as f:
        data = json.load(f)
    print(f"\n=== reasoning={label} ===")

    # Category
    for v in ["add_expense_cat_b", "add_expense_cat_e"]:
        results = [r for r in data["results"] if r.get("tool_variant") == v]
        total = len(results)
        match = sum(1 for r in results if r.get("eval_results", {}).get("category_match", {}).get("score", 0) == 1)
        valid = sum(1 for r in results if r.get("eval_results", {}).get("category_valid", {}).get("score", 0) == 1)
        called = sum(1 for r in results if r.get("eval_results", {}).get("tool_called", {}).get("score", 0) == 1)
        avg_in = sum(r.get("input_tokens", 0) or 0 for r in results) / total if total else 0
        short = v.replace("add_expense_", "")
        print(f"  {short}: match={match/total*100:.1f}% valid={valid/total*100:.1f}% called={called/total*100:.1f}% tokens={avg_in:.0f}")

    # Date (just date_c as representative)
    for v in ["add_expense_date_c"]:
        results = [r for r in data["results"] if r.get("tool_variant") == v]
        total = len(results)
        match = sum(1 for r in results if r.get("eval_results", {}).get("date_match", {}).get("score", 0) == 1)
        fmt = sum(1 for r in results if r.get("eval_results", {}).get("date_format", {}).get("score", 0) == 1)
        called = sum(1 for r in results if r.get("eval_results", {}).get("tool_called", {}).get("score", 0) == 1)
        short = v.replace("add_expense_", "")
        print(f"  {short}: match={match/total*100:.1f}% format={fmt/total*100:.1f}% called={called/total*100:.1f}%")

    # Overall avg score
    all_results = data["results"]
    total = len(all_results)
    avg_score = sum(r.get("overall_score", 0) for r in all_results) / total if total else 0
    errors = sum(1 for r in all_results if r.get("error"))
    avg_latency = sum(r.get("latency_ms", 0) or 0 for r in all_results) / total if total else 0
    print(f"  Overall: avg_score={avg_score:.3f} errors={errors} avg_latency={avg_latency:.0f}ms")
