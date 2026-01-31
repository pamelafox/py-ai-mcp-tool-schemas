# MCP Tool Schema Evaluation Report

## Metadata

- **Timestamp**: 2026-01-30T16:05:31.099101
- **Agent**: copilot
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
| add_expense_cat_a | category: str | 0.00 | 1 |
| add_expense_cat_b | category: Annotated[str, ...] | 0.00 | 1 |
| add_expense_cat_c | category: Literal[...] | 0.00 | 1 |

## Evaluation Breakdown

## Detailed Results

<details>
<summary>Click to expand</summary>

### add_expense_cat_a / clear_food_yesterday: 0.00

**User Query**:

> Yesterday I bought a sandwich for $12.50.

**Error**: Timeout after 60.0s waiting for session.idle

### add_expense_cat_b / clear_food_yesterday: 0.00

**User Query**:

> Yesterday I bought a sandwich for $12.50.

**Error**: Timeout after 60.0s waiting for session.idle

### add_expense_cat_c / clear_food_yesterday: 0.00

**User Query**:

> Yesterday I bought a sandwich for $12.50.

**Error**: Timeout after 60.0s waiting for session.idle

</details>
