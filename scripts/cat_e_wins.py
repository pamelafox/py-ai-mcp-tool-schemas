"""Find specific examples where cat_e succeeded but cat_b/c/d failed for gpt-4.1-mini."""
import json

with open("evals/runs/gpt41mini_rerun/results.json") as f:
    data = json.load(f)

# Build lookup: case_name -> {variant: result}
cases = {}
for r in data["results"]:
    v = r.get("tool_variant", "")
    if "cat_" not in v:
        continue
    c = r.get("case_name", "")
    if c not in cases:
        cases[c] = {}
    cases[c][v] = r

# Find cases where cat_e matched but others didn't
print("=== Cases where Enum+Annotated (cat_e) succeeded but others failed ===\n")
for case_name, variants in sorted(cases.items()):
    cat_e = variants.get("add_expense_cat_e", {})
    cat_e_match = cat_e.get("eval_results", {}).get("category_match", {}).get("score", 0)
    if cat_e_match != 1:
        continue

    for v_name in ["add_expense_cat_b", "add_expense_cat_c", "add_expense_cat_d"]:
        other = variants.get(v_name, {})
        other_match = other.get("eval_results", {}).get("category_match", {}).get("score", 0)
        other_called = other.get("eval_results", {}).get("tool_called", {}).get("score", 0)
        if other_match == 0:
            tc = other.get("tool_calls", [])
            got_cat = tc[0]["arguments"].get("category", "?") if tc else "NO CALL"
            tc_e = cat_e.get("tool_calls", [])
            got_e = tc_e[0]["arguments"].get("category", "?") if tc_e else "?"
            short_v = v_name.replace("add_expense_", "")
            print(f"  {case_name} ({short_v}):")
            print(f"    Query: {other.get('user_query', '')}")
            print(f"    {short_v} got: {got_cat} {'(no call)' if not tc else ''}")
            print(f"    cat_e got: {got_e}")
            print()
