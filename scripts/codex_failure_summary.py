"""Summarize codex failure reasons."""
import json

with open("evals/runs/gpt53codex_rerun/results.json") as f:
    data = json.load(f)

no_call_with_correct_output = 0
no_call_asks_clarification = 0
no_call_total = 0
wrong_category = 0
wrong_date = 0
total_failures = 0

for r in data["results"]:
    variant = r.get("tool_variant", "")
    if "cat_" not in variant and "date_" not in variant:
        continue

    ev = r.get("eval_results", {})
    tc = r.get("tool_calls", [])
    output = r.get("agent_output", "")

    tool_called = ev.get("tool_called", {}).get("score", 1)
    cat_match = ev.get("category_match", {}).get("score", 1)
    date_match = ev.get("date_match", {}).get("score", 1)

    if tool_called == 1 and cat_match == 1 and date_match == 1:
        continue

    total_failures += 1

    if tool_called == 0:
        no_call_total += 1
        # Check if the output contains the right info (model "responded" correctly but didn't call tool)
        if "log" in output.lower() or "date:" in output.lower() or "amount:" in output.lower():
            no_call_with_correct_output += 1
        if "confirm" in output.lower() or "which" in output.lower() or "would you" in output.lower():
            no_call_asks_clarification += 1

    if tool_called == 1:
        if cat_match == 0:
            wrong_category += 1
        if date_match == 0:
            wrong_date += 1

print(f"Total failures (cat + date variants): {total_failures}")
print(f"  Tool NOT called: {no_call_total}")
print(f"    ...but showed correct info in text: {no_call_with_correct_output}")
print(f"    ...asked for clarification: {no_call_asks_clarification}")
print(f"  Tool called but wrong category: {wrong_category}")
print(f"  Tool called but wrong date: {wrong_date}")
