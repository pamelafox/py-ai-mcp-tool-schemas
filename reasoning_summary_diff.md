# Reasoning summary diff

This compares the extracted `ThinkingPart.content` text for the same query/tool/seed while varying `openai_reasoning_summary`.

- Query: `Yesterday I bought a sandwich for $12.50.`
- Tool: `add_expense_cat_c`
- Seed: `42`
- Reasoning effort levels tested: `none`, `low`, `medium`, `high`, `xhigh`

## Outputs

- Summary = `auto`: [reasoning_diff_auto.md](reasoning_diff_auto.md)
- Summary = `detailed`: [reasoning_diff_detailed.md](reasoning_diff_detailed.md)

## What changed

- The returned reasoning text does change with `openai_reasoning_summary=detailed`.
- The changes are mostly stylistic/verbosity/structure (headings and extra sentences), not different factual interpretation:
  - Both runs still compute “yesterday” as `2026-01-28`.
  - Both still choose category `food` and description like “sandwich”.
- `none` still returns no extracted reasoning.

If you want, I can extend the generator to output a per-level side-by-side table (auto vs detailed in columns) in a single file.
