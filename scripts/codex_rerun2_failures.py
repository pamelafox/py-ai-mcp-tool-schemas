"""Compare category_match failures across models for rerun2."""
import json

runs = {
    "gpt-4o": "evals/runs/gpt4o_rerun/results.json",
    "gpt-4.1-mini": "evals/runs/gpt41mini_rerun/results.json",
    "gpt-5.3-codex": "evals/runs/gpt53codex_rerun2/results.json",
}

# Collect failures per model for cat_e (Enum+Annotated)
for model, path in runs.items():
    with open(path) as f:
        data = json.load(f)
    print(f"\n=== {model} — cat_e category_match failures ===")
    for r in data["results"]:
        if r.get("tool_variant") != "add_expense_cat_e":
            continue
        ev = r.get("eval_results", {})
        cm = ev.get("category_match", {})
        if cm.get("score", 1) == 0:
            tc = r.get("tool_calls", [])
            cat = tc[0]["arguments"].get("category", "?") if tc else "NO CALL"
            print(f"  {r['case_name']}: got={cat} | {cm.get('message','')}")

# Now show ALL cat_b/c/d/e failures for codex only
print(f"\n{'='*60}")
print("  gpt-5.3-codex (rerun2) — ALL category_match failures")
print(f"{'='*60}")
with open("evals/runs/gpt53codex_rerun2/results.json") as f:
    data = json.load(f)
for r in data["results"]:
    variant = r.get("tool_variant", "")
    if "cat_" not in variant:
        continue
    ev = r.get("eval_results", {})
    cm = ev.get("category_match", {})
    if cm.get("score", 1) == 0:
        tc = r.get("tool_calls", [])
        cat = tc[0]["arguments"].get("category", "?") if tc else "NO CALL"
        short_v = variant.replace("add_expense_", "")
        reasoning = r.get("reasoning", "")
        reasoning_snippet = reasoning[:200] if reasoning else "(none)"
        print(f"\n  {short_v} / {r['case_name']}")
        print(f"    Query: {r['user_query']}")
        print(f"    Got: {cat}")
        print(f"    {cm.get('message','')}")
        print(f"    Reasoning: {reasoning_snippet}")
