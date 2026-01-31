# MCP Tool Schema Evaluation Report

## Metadata

- **Timestamp**: 2026-01-30T11:06:31.438218
- **API Host**: N/A
- **Model**: gpt-4.1-mini
- **Reasoning Effort**: N/A
- **Reasoning Summary**: N/A
- **Seed**: 42
- **Temperature**: N/A
- **MCP Server URL**: http://localhost:8000/mcp

## Variant Comparison

| Variant | Description | Avg Score | Total |
|---------|-------------|-----------|-------|
| add_expense_cat_c | category: Literal[...] | 1.00 | 2 |

## Evaluation Breakdown

### category_match

| Variant | Description | Pass Rate | Passed | Total |
|---------|-------------|-----------|--------|-------|
| add_expense_cat_c | category: Literal[...] | 100.0% | 2 | 2 |

### category_valid

| Variant | Description | Pass Rate | Passed | Total |
|---------|-------------|-----------|--------|-------|
| add_expense_cat_c | category: Literal[...] | 100.0% | 2 | 2 |

### tool_called

| Variant | Description | Pass Rate | Passed | Total |
|---------|-------------|-----------|--------|-------|
| add_expense_cat_c | category: Literal[...] | 100.0% | 2 | 2 |

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
  "intent": "Adding expense"
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

> Added your $12.50 sandwich expense from January 29th under Food & drink.

**Reasoning Summary**:

```
The user wants to add an expense for a sandwich they bought yesterday. Yesterday would be 2026-01-29. The amount is $12.50, and a sandwich would fall under "Food & drink" category.
```

**Evaluations**:

| Result | Evaluator | Message |
|---|---|---|
| ✅ Pass | tool_called | Tool 'add_expense_cat_c' was called |
| ✅ Pass | category_valid | Category 'Food & drink' is valid |
| ✅ Pass | category_match | Category 'Food & drink' matches expected 'Food & drink' |

### add_expense_cat_c / clear_transport_today: 1.00

**User Query**:

> I paid $45 for gas today (2026-01-30).

**Tool Calls**:

- Tool: `add_expense_cat_c`

```json
{
  "expense_date": "2026-01-30",
  "amount": 45,
  "category": "Transit and Fuel",
  "description": "Gas"
}
```


**Assistant Output**:

> Done! I've recorded your $45 gas expense for today under "Transit and Fuel."

**Reasoning Summary**:

```
The user wants to add an expense for gas. I have the add_expense tool available. Let me use it with the details provided:
- Date: 2026-01-30
- Amount: 45
- Category: "Transit and Fuel" seems appropriate for gas
- Description: "Gas"
```

**Evaluations**:

| Result | Evaluator | Message |
|---|---|---|
| ✅ Pass | tool_called | Tool 'add_expense_cat_c' was called |
| ✅ Pass | category_valid | Category 'Transit and Fuel' is valid |
| ✅ Pass | category_match | Category 'Transit and Fuel' matches expected 'Transit and Fuel' |

</details>
