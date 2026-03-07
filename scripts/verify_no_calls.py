"""Verify whether tool_calls is truly empty on 'no call' failures."""
import json

with open("evals/runs/gpt53codex_rerun/results.json") as f:
    data = json.load(f)

empty_tc = 0
has_other_tools = 0
examples = []

for r in data["results"]:
    variant = r.get("tool_variant", "")
    if "cat_" not in variant and "date_" not in variant:
        continue

    ev = r.get("eval_results", {})
    tc = r.get("tool_calls", [])
    tool_called = ev.get("tool_called", {}).get("score", 1)

    if tool_called == 0:
        if len(tc) == 0:
            empty_tc += 1
        else:
            has_other_tools += 1
            examples.append({
                "case": r.get("case_name"),
                "variant": variant,
                "tool_calls": [t["tool_name"] for t in tc],
            })

print(f"No-tool-call failures: {empty_tc + has_other_tools}")
print(f"  Truly empty tool_calls list: {empty_tc}")
print(f"  Had tool calls but wrong name: {has_other_tools}")
if examples:
    print("  Examples of wrong-name calls:")
    for ex in examples:
        print(f"    {ex['variant']}/{ex['case']}: called {ex['tool_calls']}")
