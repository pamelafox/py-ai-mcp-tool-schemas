# MCP Tool Schema Evaluation Report

## Metadata

- **Timestamp**: 2026-01-30T11:05:15.338459
- **API Host**: N/A
- **Model**: gpt-5.2
- **Reasoning Effort**: N/A
- **Reasoning Summary**: N/A
- **Seed**: 42
- **Temperature**: N/A
- **MCP Server URL**: http://localhost:8000/mcp

## Variant Comparison

| Variant | Description | Avg Score | Total |
|---------|-------------|-----------|-------|
| add_expense_cat_c | category: Literal[...] | 1.00 | 1 |

## Evaluation Breakdown

### category_match

| Variant | Description | Pass Rate | Passed | Total |
|---------|-------------|-----------|--------|-------|
| add_expense_cat_c | category: Literal[...] | 100.0% | 1 | 1 |

### category_valid

| Variant | Description | Pass Rate | Passed | Total |
|---------|-------------|-----------|--------|-------|
| add_expense_cat_c | category: Literal[...] | 100.0% | 1 | 1 |

### tool_called

| Variant | Description | Pass Rate | Passed | Total |
|---------|-------------|-----------|--------|-------|
| add_expense_cat_c | category: Literal[...] | 100.0% | 1 | 1 |

## Detailed Results

<details>
<summary>Click to expand</summary>

### add_expense_cat_c / clear_food_yesterday: 1.00

**User Query**:

> Yesterday I bought a sandwich for $12.50.

**Tool Calls**:

- Tool: `report_intent`

```json
{
  "intent": "Recording expense"
}
```

- Tool: `add_expense_cat_c`

```json
{
  "expense_date": "2026-01-29",
  "amount": 12.5,
  "category": "Food & drink",
  "description": "Sandwich"
}
```


**Assistant Output**:

> Logging this purchase as an expense with yesterday’s date.
> Added: **$12.50** on **2026-01-29** — **Food & drink** (“Sandwich”).

**Reasoning Summary**:

```
I need to add an expense using the tool. First, I have to find yesterday's date relative to the current date, which is January 30, 2026, making yesterday January 29, 2026. The expense category is Food & Drink, and the description is "sandwich," with an amount of $12.50. I’ll use the tool for this. Additionally, I have to generate a report at the same time, so I’ll call both actions in parallel.
```

**Evaluations**:

| Result | Evaluator | Message |
|---|---|---|
| ✅ Pass | tool_called | Tool 'add_expense_cat_c' was called |
| ✅ Pass | category_valid | Category 'Food & drink' is valid |
| ✅ Pass | category_match | Category 'Food & drink' matches expected 'Food & drink' |

</details>
