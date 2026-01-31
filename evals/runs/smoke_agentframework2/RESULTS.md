# MCP Tool Schema Evaluation Report

## Metadata

- **Timestamp**: 2026-01-30T12:50:53.562883
- **Agent**: agentframework
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

- Tool: `add_expense_date_b`

```json
{
  "expense_date": "2026-01-29",
  "amount": 12.5,
  "category": "Food & drink",
  "description": "Sandwich"
}
```


**Assistant Output**:

> Logged: **$12.50** — *Sandwich* (**Food & drink**) on **2026-01-29**.

**Reasoning Summary**:

```
(none returned)
```

**Evaluations**:

| Result | Evaluator | Message |
|---|---|---|
| ✅ Pass | tool_called | Tool 'add_expense_date_b' was called |
| ✅ Pass | category_valid | Category 'Food & drink' is valid |
| ✅ Pass | category_match | Category 'Food & drink' matches expected 'Food & drink' |

</details>
