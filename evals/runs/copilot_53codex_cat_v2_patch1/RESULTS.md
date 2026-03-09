# MCP Tool Schema Evaluation Report

## Metadata

- **Timestamp**: 2026-03-09T03:24:09.803222
- **Agent**: copilot
- **API Host**: N/A
- **Model**: gpt-5.3-codex
- **Reasoning Effort**: N/A
- **Reasoning Summary**: N/A
- **Seed**: 42
- **Temperature**: N/A
- **MCP Server URL**: http://localhost:8000/mcp

## Variant Comparison

| Variant | Description | Avg Score | Avg Latency | Avg Input Tokens | Avg Output Tokens | Avg Tool Response Size | Total |
|---------|-------------|-----------|-------------|------------------|-------------------|------------------------|-------|
| add_expense_cat_d | category: ExpenseCategory (Enum) | 1.00 | 13376ms | N/A | N/A | N/A | 2 |

## Evaluation Breakdown

### category_match

| Variant | Description | Pass Rate | Passed | Total |
|---------|-------------|-----------|--------|-------|
| add_expense_cat_d | category: ExpenseCategory (Enum) | 100.0% | 2 | 2 |

### category_valid

| Variant | Description | Pass Rate | Passed | Total |
|---------|-------------|-----------|--------|-------|
| add_expense_cat_d | category: ExpenseCategory (Enum) | 100.0% | 2 | 2 |

### tool_called

| Variant | Description | Pass Rate | Passed | Total |
|---------|-------------|-----------|--------|-------|
| add_expense_cat_d | category: ExpenseCategory (Enum) | 100.0% | 2 | 2 |

## Detailed Results

<details>
<summary>Click to expand</summary>

### add_expense_cat_d / hard_category_grocery_delivery_yesterday: 1.00

**Metrics**: Latency: 13517ms

**User Query**:

> Yesterday I paid $65 for Instacart grocery delivery.

**Tool Calls**:

- Tool: `report_intent`

```json
{
  "intent": "Logging expense"
}
```

- Tool: `add_expense_cat_d`

```json
{
  "expense_date": "2026-03-08",
  "amount": 65,
  "category": "Food & drink",
  "description": "Instacart grocery delivery"
}
```


**Assistant Output**:

> Done — I logged it as:
>
> - **Date:** 2026-03-08 (yesterday)
> - **Amount:** **$65.00**
> - **Category:** Food & drink
> - **Description:** Instacart grocery delivery

**Reasoning Summary**:

```
**Planning sequential tool calls**
```

**Evaluations**:

| Result | Evaluator | Message |
|---|---|---|
| ✅ Pass | tool_called | Tool 'add_expense_cat_d' was called |
| ✅ Pass | category_valid | Category 'Food & drink' is valid |
| ✅ Pass | category_match | Category 'Food & drink' matches expected 'Food & drink' |

### add_expense_cat_d / hard_category_headphones_last_day_last_month: 1.00

**Metrics**: Latency: 13236ms

**User Query**:

> On the last day of last month I bought headphones for $79.99.

**Tool Calls**:

- Tool: `report_intent`

```json
{
  "intent": "Logging expense entry"
}
```

- Tool: `add_expense_cat_d`

```json
{
  "expense_date": "2026-02-28",
  "amount": 79.99,
  "category": "Electronics & tech",
  "description": "Headphones"
}
```


**Assistant Output**:

> Logged ✅
>
> - **Date:** 2026-02-28 (last day of last month)
> - **Amount:** $79.99
> - **Category:** Electronics & tech
> - **Description:** Headphones

**Reasoning Summary**:

```
**Sequencing tool calls with intent report**
```

**Evaluations**:

| Result | Evaluator | Message |
|---|---|---|
| ✅ Pass | tool_called | Tool 'add_expense_cat_d' was called |
| ✅ Pass | category_valid | Category 'Electronics & tech' is valid |
| ✅ Pass | category_match | Category 'Electronics & tech' matches expected 'Electronics & tech' |

</details>
