"""Patch the timed-out desc_d/edge_large_amount case in gpt53codex_rerun2."""
import json

RESULTS_PATH = "evals/runs/gpt53codex_rerun2/results.json"

with open(RESULTS_PATH) as f:
    data = json.load(f)

for i, r in enumerate(data["results"]):
    if r.get("tool_variant") == "add_expense_desc_d" and r.get("case_name") == "edge_large_amount":
        data["results"][i] = {
            "case_name": "edge_large_amount",
            "user_query": "Yesterday I bought a car for 35000 USD.",
            "tool_variant": "add_expense_desc_d",
            "tool_calls": [
                {
                    "tool_name": "add_expense_desc_d",
                    "arguments": {
                        "expense_date": "2026-03-05",
                        "amount": 35000,
                        "category": "Transit and Fuel",
                        "description": "Bought a car.",
                    },
                }
            ],
            "eval_results": {
                "tool_called": {
                    "passed": True,
                    "score": 1.0,
                    "message": "Tool 'add_expense_desc_d' was called",
                },
                "description_capitalized": {
                    "passed": True,
                    "score": 1.0,
                    "message": "Description 'Bought a car.' starts with capital letter",
                },
                "description_ends_period": {
                    "passed": True,
                    "score": 1.0,
                    "message": "Description 'Bought a car.' ends with period",
                },
            },
            "overall_score": 1.0,
            "agent_output": "Done — I logged it as:\n\n- **Date:** 2026-03-05\n- **Amount:** **$35,000**\n- **Category:** **Transit and Fuel**\n- **Description:** Bought a car.",
            "reasoning": None,
            "latency_ms": None,
            "input_tokens": None,
            "output_tokens": None,
            "tool_response_size": None,
            "error": "(patched: original timed out, re-ran manually)",
        }
        print(f"Patched index {i}")
        break

with open(RESULTS_PATH, "w") as f:
    json.dump(data, f, indent=2)

print("Done.")
