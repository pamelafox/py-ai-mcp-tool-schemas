"""Show model output for bus pass refusal."""
import json

with open("evals/runs/gpt41mini_cat_v2/results.json") as f:
    data = json.load(f)

for r in data["results"]:
    if r["case_name"] == "relative_date_day_after_tomorrow_bus_pass" and r["tool_variant"] == "add_expense_cat_b":
        print(f"Output:\n{r['agent_output']}")
        break
