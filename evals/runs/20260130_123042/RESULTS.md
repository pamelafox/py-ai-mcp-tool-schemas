# MCP Tool Schema Evaluation Report

## Metadata

- **Timestamp**: 2026-01-30T12:30:42.175305
- **Agent**: copilot
- **API Host**: N/A
- **Model**: gpt-5.2
- **Reasoning Effort**: low
- **Reasoning Summary**: N/A
- **Seed**: 42
- **Temperature**: N/A
- **MCP Server URL**: http://localhost:8000/mcp

## Variant Comparison

| Variant | Description | Avg Score | Total |
|---------|-------------|-----------|-------|
| add_expense_cat_b | category: Annotated[str, ...] | 1.00 | 2 |
| add_expense_cat_c | category: Literal[...] | 1.00 | 2 |
| add_expense_cat_d | category: ExpenseCategory (Enum) | 1.00 | 2 |
| add_expense_cat_e | category: Annotated[ExpenseCategory, Field(description=...)] | 1.00 | 2 |

## Evaluation Breakdown

### category_match

| Variant | Description | Pass Rate | Passed | Total |
|---------|-------------|-----------|--------|-------|
| add_expense_cat_b | category: Annotated[str, ...] | 100.0% | 2 | 2 |
| add_expense_cat_c | category: Literal[...] | 100.0% | 2 | 2 |
| add_expense_cat_d | category: ExpenseCategory (Enum) | 100.0% | 2 | 2 |
| add_expense_cat_e | category: Annotated[ExpenseCategory, Field(description=...)] | 100.0% | 2 | 2 |

### category_valid

| Variant | Description | Pass Rate | Passed | Total |
|---------|-------------|-----------|--------|-------|
| add_expense_cat_b | category: Annotated[str, ...] | 100.0% | 2 | 2 |
| add_expense_cat_c | category: Literal[...] | 100.0% | 2 | 2 |
| add_expense_cat_d | category: ExpenseCategory (Enum) | 100.0% | 2 | 2 |
| add_expense_cat_e | category: Annotated[ExpenseCategory, Field(description=...)] | 100.0% | 2 | 2 |

### tool_called

| Variant | Description | Pass Rate | Passed | Total |
|---------|-------------|-----------|--------|-------|
| add_expense_cat_b | category: Annotated[str, ...] | 100.0% | 2 | 2 |
| add_expense_cat_c | category: Literal[...] | 100.0% | 2 | 2 |
| add_expense_cat_d | category: ExpenseCategory (Enum) | 100.0% | 2 | 2 |
| add_expense_cat_e | category: Annotated[ExpenseCategory, Field(description=...)] | 100.0% | 2 | 2 |

## Detailed Results

<details>
<summary>Click to expand</summary>

### add_expense_cat_b / hard_category_grocery_delivery_yesterday: 1.00

**User Query**:

> Yesterday I paid $65 for Instacart grocery delivery.

**Tool Calls**:

- Tool: `add_expense_cat_b`

```json
{
  "expense_date": "2026-01-29",
  "amount": 65,
  "category": "Food & drink",
  "description": "Instacart grocery delivery"
}
```


**Assistant Output**:

> Added: **$65** on **2026-01-29** — **Food & drink** — *Instacart grocery delivery*.

**Reasoning Summary**:

```
(none returned)
```

**Evaluations**:

| Result | Evaluator | Message |
|---|---|---|
| ✅ Pass | tool_called | Tool 'add_expense_cat_b' was called |
| ✅ Pass | category_valid | Category 'Food & drink' is valid |
| ✅ Pass | category_match | Category 'Food & drink' matches expected 'Food & drink' |

### add_expense_cat_b / hard_category_headphones_last_day_last_month: 1.00

**User Query**:

> On the last day of last month I bought headphones for $79.99.

**Tool Calls**:

- Tool: `report_intent`

```json
{
  "intent": "Logging expense"
}
```

- Tool: `add_expense_cat_b`

```json
{
  "expense_date": "2025-12-31",
  "amount": 79.99,
  "category": "Electronics & tech",
  "description": "Headphones"
}
```


**Assistant Output**:

> Adding that headphones purchase as an expense dated the last day of last month (2025-12-31).
> Added an expense: **$79.99** for **Headphones** on **2025-12-31** under **Electronics & tech**.

**Reasoning Summary**:

```
I need to add an expense for the last day of December 2025, which is December 31, 2025. This is related to January 30, 2026. The category is likely Electronics & Tech, and the description will be "Headphones." I’ll use a tool to add this expense without requiring a report intent, as that's optional. I’ll call the tool to add the expense amounting to $79.99.
```

**Evaluations**:

| Result | Evaluator | Message |
|---|---|---|
| ✅ Pass | tool_called | Tool 'add_expense_cat_b' was called |
| ✅ Pass | category_valid | Category 'Electronics & tech' is valid |
| ✅ Pass | category_match | Category 'Electronics & tech' matches expected 'Electronics & tech' |

### add_expense_cat_c / hard_category_grocery_delivery_yesterday: 1.00

**User Query**:

> Yesterday I paid $65 for Instacart grocery delivery.

**Tool Calls**:

- Tool: `add_expense_cat_c`

```json
{
  "expense_date": "2026-01-29",
  "amount": 65,
  "category": "Food & drink",
  "description": "Instacart grocery delivery"
}
```


**Assistant Output**:

> Logging this as a Food & drink expense dated yesterday (2026-01-29).
> Added: **$65** on **2026-01-29** — **Food & drink** — “Instacart grocery delivery”.

**Reasoning Summary**:

```
I need to add an expense using the appropriate tool. The date will be set to yesterday, which is January 29, 2026. The category for this expense will likely be Food & Drink, and I'll describe it as an Instacart grocery delivery. It's straightforward; I'll make sure to use the add_expense tool to record this properly. I want to ensure everything gets logged accurately!
```

**Evaluations**:

| Result | Evaluator | Message |
|---|---|---|
| ✅ Pass | tool_called | Tool 'add_expense_cat_c' was called |
| ✅ Pass | category_valid | Category 'Food & drink' is valid |
| ✅ Pass | category_match | Category 'Food & drink' matches expected 'Food & drink' |

### add_expense_cat_c / hard_category_headphones_last_day_last_month: 1.00

**User Query**:

> On the last day of last month I bought headphones for $79.99.

**Tool Calls**:

- Tool: `add_expense_cat_c`

```json
{
  "expense_date": "2025-12-31",
  "amount": 79.99,
  "category": "Electronics & tech",
  "description": "Headphones"
}
```


**Assistant Output**:

> Added: **$79.99** for **Headphones** on **2025-12-31** under **Electronics & tech**.

**Reasoning Summary**:

```
I need to add an expense from the last day of last month, which is December 31, 2025, relative to the current date of January 30, 2026. The category for this expense is likely Electronics & Tech, with a description for headphones. I'll make sure to use the appropriate tool to document this expense correctly. It's important to keep track of these details accurately!
```

**Evaluations**:

| Result | Evaluator | Message |
|---|---|---|
| ✅ Pass | tool_called | Tool 'add_expense_cat_c' was called |
| ✅ Pass | category_valid | Category 'Electronics & tech' is valid |
| ✅ Pass | category_match | Category 'Electronics & tech' matches expected 'Electronics & tech' |

### add_expense_cat_d / hard_category_grocery_delivery_yesterday: 1.00

**User Query**:

> Yesterday I paid $65 for Instacart grocery delivery.

**Tool Calls**:

- Tool: `add_expense_cat_d`

```json
{
  "expense_date": "2026-01-29",
  "amount": 65,
  "category": "Food & drink",
  "description": "Instacart grocery delivery"
}
```


**Assistant Output**:

> Added: **$65** on **2026-01-29** in **Food & drink** — “Instacart grocery delivery”.

**Reasoning Summary**:

```
I need to add an expense using a specific tool. I’ll set the date to "yesterday," which, given today is January 30, 2026, means it should be January 29, 2026. The category will be "Food & drink," and I’ll describe it as "Instacart grocery delivery." Once I have all this information, I’ll go ahead and make the tool call. It seems pretty straightforward!
```

**Evaluations**:

| Result | Evaluator | Message |
|---|---|---|
| ✅ Pass | tool_called | Tool 'add_expense_cat_d' was called |
| ✅ Pass | category_valid | Category 'Food & drink' is valid |
| ✅ Pass | category_match | Category 'Food & drink' matches expected 'Food & drink' |

### add_expense_cat_d / hard_category_headphones_last_day_last_month: 1.00

**User Query**:

> On the last day of last month I bought headphones for $79.99.

**Tool Calls**:

- Tool: `add_expense_cat_d`

```json
{
  "expense_date": "2025-12-31",
  "amount": 79.99,
  "category": "Electronics & tech",
  "description": "Headphones"
}
```


**Assistant Output**:

> Recorded: **$79.99** for **Headphones** on **2025-12-31** under **Electronics & tech**.

**Reasoning Summary**:

```
I need to incorporate a tool call for adding an expense. Since today's date is January 30, 2026, the last day of last month was December 31, 2025. The expense category is Electronics & Tech, and the description will be for headphones. I'll use the tool designed for adding expenses under that category. It's all straightforward, just need to ensure I make the right call!
```

**Evaluations**:

| Result | Evaluator | Message |
|---|---|---|
| ✅ Pass | tool_called | Tool 'add_expense_cat_d' was called |
| ✅ Pass | category_valid | Category 'Electronics & tech' is valid |
| ✅ Pass | category_match | Category 'Electronics & tech' matches expected 'Electronics & tech' |

### add_expense_cat_e / hard_category_grocery_delivery_yesterday: 1.00

**User Query**:

> Yesterday I paid $65 for Instacart grocery delivery.

**Tool Calls**:

- Tool: `add_expense_cat_e`

```json
{
  "expense_date": "2026-01-29",
  "amount": 65,
  "category": "Food & drink",
  "description": "Instacart grocery delivery"
}
```


**Assistant Output**:

> Added: **$65** on **2026-01-29** — **Instacart grocery delivery** (Category: **Food & drink**).

**Reasoning Summary**:

```
I need to add an expense, specifically for yesterday's date, which would be January 29, 2026, in relation to the current date of January 30, 2026. The category is Food & Drink, and the description will be "Instacart grocery delivery." I’ll use the expense tool to make this entry and keep things organized. It feels good to keep track of expenses, so let’s get this done!
```

**Evaluations**:

| Result | Evaluator | Message |
|---|---|---|
| ✅ Pass | tool_called | Tool 'add_expense_cat_e' was called |
| ✅ Pass | category_valid | Category 'Food & drink' is valid |
| ✅ Pass | category_match | Category 'Food & drink' matches expected 'Food & drink' |

### add_expense_cat_e / hard_category_headphones_last_day_last_month: 1.00

**User Query**:

> On the last day of last month I bought headphones for $79.99.

**Tool Calls**:

- Tool: `add_expense_cat_e`

```json
{
  "expense_date": "2025-12-31",
  "amount": 79.99,
  "category": "Electronics & tech",
  "description": "Headphones"
}
```


**Assistant Output**:

> Logging the headphone purchase as an Electronics & tech expense on the last day of last month.
> Added: **$79.99** on **2025-12-31** — **Headphones** (Category: **Electronics & tech**).

**Reasoning Summary**:

```
I need to add an expense for the last day of December 2025, which is December 31, 2025. The category for this expense is electronics & tech, and the description is "headphones." I’ll use the specific tool for adding this expense. I want to make sure it's recorded accurately, so I’ll proceed with calling that tool now. Let's make sure everything is set up correctly!
```

**Evaluations**:

| Result | Evaluator | Message |
|---|---|---|
| ✅ Pass | tool_called | Tool 'add_expense_cat_e' was called |
| ✅ Pass | category_valid | Category 'Electronics & tech' is valid |
| ✅ Pass | category_match | Category 'Electronics & tech' matches expected 'Electronics & tech' |

</details>
