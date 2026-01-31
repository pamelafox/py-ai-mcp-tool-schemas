# MCP Tool Schema Evaluation Report

## Metadata

- **Timestamp**: 2026-01-29T16:56:24.127099
- **API Host**: N/A
- **Model**: gpt-4o
- **Reasoning Effort**: N/A
- **Reasoning Summary**: N/A
- **Seed**: 42
- **Temperature**: 0.0
- **MCP Server URL**: http://localhost:8000/mcp

## Variant Comparison

| Variant | Description | Avg Score | Total |
|---------|-------------|-----------|-------|
| add_expense_cat_b | category: Annotated[str, ...] | 1.00 | 1 |
| add_expense_cat_c | category: Literal[...] | 1.00 | 1 |

## Evaluation Breakdown

### category_match

| Variant | Description | Pass Rate | Passed | Total |
|---------|-------------|-----------|--------|-------|
| add_expense_cat_b | category: Annotated[str, ...] | 100.0% | 1 | 1 |
| add_expense_cat_c | category: Literal[...] | 100.0% | 1 | 1 |

### category_valid

| Variant | Description | Pass Rate | Passed | Total |
|---------|-------------|-----------|--------|-------|
| add_expense_cat_b | category: Annotated[str, ...] | 100.0% | 1 | 1 |
| add_expense_cat_c | category: Literal[...] | 100.0% | 1 | 1 |

### tool_called

| Variant | Description | Pass Rate | Passed | Total |
|---------|-------------|-----------|--------|-------|
| add_expense_cat_b | category: Annotated[str, ...] | 100.0% | 1 | 1 |
| add_expense_cat_c | category: Literal[...] | 100.0% | 1 | 1 |

## Detailed Results

<details>
<summary>Click to expand</summary>

### add_expense_cat_b / clear_food_yesterday: 1.00

**User Query**:

> Yesterday I bought a sandwich for $12.50.

**Tool Calls**:

- Tool: `add_expense_cat_b`

```json
{
  "expense_date": "2026-01-28",
  "amount": 12.5,
  "category": "food & drink",
  "description": "Sandwich"
}
```


**Assistant Output**:

> Your expense of $12.50 for a sandwich on January 28, 2026, has been recorded under "Food & Drink."

**Reasoning Summary**:

```
(none returned)
```

**Evaluations**:

| Result | Evaluator | Message |
|---|---|---|
| ✅ Pass | tool_called | Tool 'add_expense_cat_b' was called |
| ✅ Pass | category_valid | Category 'food & drink' is valid |
| ✅ Pass | category_match | Category 'food & drink' matches expected 'food & drink' |

### add_expense_cat_c / clear_food_yesterday: 1.00

**User Query**:

> Yesterday I bought a sandwich for $12.50.

**Tool Calls**:

- Tool: `add_expense_cat_c`

```json
{
  "expense_date": "2026-01-28",
  "amount": 12.5,
  "category": "food & drink",
  "description": "Sandwich purchase"
}
```


**Assistant Output**:

> Your expense of $12.50 for a sandwich on 2026-01-28 has been successfully recorded under "Food & Drink."

**Reasoning Summary**:

```
(none returned)
```

**Evaluations**:

| Result | Evaluator | Message |
|---|---|---|
| ✅ Pass | tool_called | Tool 'add_expense_cat_c' was called |
| ✅ Pass | category_valid | Category 'food & drink' is valid |
| ✅ Pass | category_match | Category 'food & drink' matches expected 'food & drink' |

</details>
