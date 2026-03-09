# MCP Tool Schema Evaluation Report

## Metadata

- **Timestamp**: 2026-03-09T03:16:13.420598
- **Agent**: pydanticai
- **API Host**: N/A
- **Model**: gpt-5.3-codex
- **Reasoning Effort**: medium
- **Reasoning Summary**: N/A
- **Seed**: 42
- **Temperature**: N/A
- **MCP Server URL**: http://localhost:8000/mcp

## Variant Comparison

| Variant | Description | Avg Score | Avg Latency | Avg Input Tokens | Avg Output Tokens | Avg Tool Response Size | Total |
|---------|-------------|-----------|-------------|------------------|-------------------|------------------------|-------|
| add_expense_cat_b | category: Annotated[str, ...] | 1.00 | 18448ms | 1010 | 328 | 60 chars | 1 |

## Evaluation Breakdown

### category_match

| Variant | Description | Pass Rate | Passed | Total |
|---------|-------------|-----------|--------|-------|
| add_expense_cat_b | category: Annotated[str, ...] | 100.0% | 1 | 1 |

### category_valid

| Variant | Description | Pass Rate | Passed | Total |
|---------|-------------|-----------|--------|-------|
| add_expense_cat_b | category: Annotated[str, ...] | 100.0% | 1 | 1 |

### tool_called

| Variant | Description | Pass Rate | Passed | Total |
|---------|-------------|-----------|--------|-------|
| add_expense_cat_b | category: Annotated[str, ...] | 100.0% | 1 | 1 |

## Detailed Results

<details>
<summary>Click to expand</summary>

### add_expense_cat_b / relative_date_first_monday_this_month: 1.00

**Metrics**: Latency: 18448ms | Input tokens: 1010 | Output tokens: 328 | Tool response size: 60 chars

**User Query**:

> I bought a sandwich on the first Monday of this month for $12.50.

**Tool Calls**:

- Tool: `add_expense_cat_b`

```json
{
  "expense_date": "2026-03-02",
  "amount": 12.5,
  "category": "Food & drink",
  "description": "Sandwich"
}
```


**Assistant Output**:

> Done — I logged **$12.50** for a **sandwich** on **2026-03-02** under **Food & drink**.

**Reasoning Summary**:

```
**Interpreting dates for expenses**

I need to figure out the first Monday of March 2026 in relation to today, March 9. I believe that falls on March 2, since March 1 is likely a Sunday. Confirming, it seems right because January 1, 2026, was a Thursday, meaning February 1 was a Sunday, which makes March 1 a Sunday as well. So March 2 is indeed the first Monday. I’ll add an expense for a sandwich of $12.50, under Food & Drink, on that date.
```

**Evaluations**:

| Result | Evaluator | Message |
|---|---|---|
| ✅ Pass | tool_called | Tool 'add_expense_cat_b' was called |
| ✅ Pass | category_valid | Category 'Food & drink' is valid |
| ✅ Pass | category_match | Category 'Food & drink' matches expected 'Food & drink' |

</details>
