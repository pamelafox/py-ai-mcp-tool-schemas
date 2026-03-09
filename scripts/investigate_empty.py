"""Investigate the empty output for date_c / edge_currency_symbol."""
import json

with open("evals/runs/gpt41mini_date_v2b/results.json") as f:
    data = json.load(f)

for r in data["results"]:
    if r["case_name"] == "edge_currency_symbol" and r["tool_variant"] == "add_expense_date_c":
        print("Full result:")
        print(json.dumps({
            "case_name": r["case_name"],
            "tool_variant": r["tool_variant"],
            "user_query": r["user_query"],
            "agent_output": r["agent_output"],
            "tool_calls": r.get("tool_calls", []),
            "eval_results": r.get("eval_results", {}),
            "error": r.get("error"),
            "latency_ms": r.get("latency_ms"),
            "input_tokens": r.get("input_tokens"),
            "output_tokens": r.get("output_tokens"),
            "reasoning": r.get("reasoning", ""),
        }, indent=2))
        break
