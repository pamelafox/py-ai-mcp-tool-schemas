# Failure analysis (gpt41mini)

This file summarizes the most notable failure patterns in the `gpt-4.1-mini` run located in this folder.

## Run context

- Date the eval ran: 2026-01-29
- Model: `gpt-4.1-mini`
- Dataset size: 27 cases
- Key headline: category schemas mostly hold up; relative-date reasoning is the primary weakness.

For the overall metrics, see [RESULTS.md](RESULTS.md).

## Notable failure patterns

### 1) Relative-date reasoning failures (wrong date, but tool was called)

The biggest cluster of failures is the model computing the wrong absolute date for certain relative expressions, especially:

- **"last day of last month"**
  - Frequent wrong value observed: `2026-01-31` (end of *this* month) instead of the last day of last month (`2025-12-31`), given the run date is 2026-01-29.

This shows up heavily in:

- `relative_date_last_day_last_month`
- `hard_category_headphones_last_day_last_month`

Smaller but recurring relative-date issues:

- `relative_date_monday_before_this_one`
- `relative_date_last_friday_movie`
- `relative_date_last_business_day_last_month`

Impact by tool variant group:

- Date typing/validation helps *format* but not the *inference*.
- This is reflected in the `date_match` table where all date variants are below 100%, with `add_expense_date_b` / `add_expense_date_d` the lowest in this run.

### 2) "Asks for confirmation" → no tool call (tool_called failures)

A second notable behavior is that for some prompts, the model chooses to ask the user for confirmation rather than logging the expense, resulting in **no tool call** and thus a `tool_called` eval failure.

The clearest repeated case is:

- `edge_large_amount` (e.g., a large purchase like a car)

In this run, several variants responded with a confirmation question instead of calling the tool. This is particularly important because it’s not a schema/typing failure—it's a policy/behavioral choice by the model.

### 3) Category errors: mostly "cat_a", with one meaningful exception

As expected, `add_expense_cat_a` (free-form `str`) fails broadly by inventing new categories (e.g., capitalization differences, novel labels, Spanish labels not in the allowed set).

The constrained category variants (`cat_b/c/d/e`) are much more stable, but there is **one meaningful non-`cat_a` mismatch** to note:

- `add_expense_cat_e / edge_large_amount` categorized as `shopping` when expected `other`.

This suggests that even with the richer `cat_e` description guidance, the model may map “car purchase” to `shopping` instead of treating it as a large irregular purchase best placed into `other`.

Also worth noting: the prompt `ambiguous_reimbursable_unknown_mixed_outing` (“drinks after work with coworkers and friends”) is category-taxonomy ambiguous (food vs entertainment). The dataset now leaves `expected_category=None` for that case, so `category_match` is not evaluated there.

## High-signal cases (worth keeping)

If you’re pruning the dataset, these cases appear to provide the most unique signal on a weaker model:

- Relative date inference edge cases:
  - `relative_date_last_day_last_month`
  - `hard_category_headphones_last_day_last_month`
  - `relative_date_last_business_day_last_month`
  - `relative_date_monday_before_this_one`
- Behavior/no-tool-call:
  - `edge_large_amount`

These expose failures that are not just “`cat_a` is unconstrained”, and they stress behaviors that differ across models.

## Possible next tweaks (optional)

- Consider refining the `add_expense_cat_e` guidance to explicitly steer **large durable goods (e.g., car purchase)** toward `other` (or make the expected label `transport` if you prefer that taxonomy).
- If you want the eval to measure “tool call even when uncertain”, consider adding a system instruction in the agent prompt like: *"If the user provides sufficient info, log the expense without asking for confirmation."* (That would change what the harness is testing, though.)
