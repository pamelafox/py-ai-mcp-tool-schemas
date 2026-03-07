"""Get full responses for edge_large_amount across models and schemas."""
import json

runs = {
    "gpt-4o": "evals/runs/gpt4o_rerun/results.json",
    "gpt-4.1-mini": "evals/runs/gpt41mini_rerun/results.json",
    "gpt-5.3-codex": "evals/runs/gpt53codex_rerun/results.json",
}

for variant in ["add_expense_cat_b", "add_expense_cat_e"]:
    print(f"\n{'='*70}")
    print(f"  {variant} / edge_large_amount")
    print(f"  Query: Yesterday I bought a car for 35000 USD.")
    print(f"{'='*70}")
    for model, path in runs.items():
        with open(path) as f:
            data = json.load(f)
        for r in data["results"]:
            if r.get("tool_variant") == variant and r.get("case_name") == "edge_large_amount":
                tc = r.get("tool_calls", [])
                output = r.get("agent_output", "")
                print(f"\n  --- {model} ---")
                if tc:
                    print(f"  Tool call: {json.dumps(tc[0]['arguments'], indent=4)}")
                else:
                    print(f"  No tool call.")
                print(f"  Response: {output[:400]}")
                break
