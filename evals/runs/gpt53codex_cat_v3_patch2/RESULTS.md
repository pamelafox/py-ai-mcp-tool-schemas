# MCP Tool Schema Evaluation Report

## Metadata

- **Timestamp**: 2026-03-09T03:17:53.695261
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
| add_expense_cat_c | category: Literal[...] | 1.00 | 10693ms | 463 | 162 | 60 chars | 1 |

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

### add_expense_cat_c / spanish_gadget: 1.00

**Metrics**: Latency: 10693ms | Input tokens: 463 | Output tokens: 162 | Tool response size: 60 chars

**User Query**:

> Ayer compré una laptop por 1200 dólares.

**Tool Calls**:

- Tool: `add_expense_cat_c`

```json
{
  "expense_date": "2026-03-08",
  "amount": 1200,
  "category": "Electronics & tech",
  "description": "Laptop"
}
```


**Assistant Output**:

> ¡Listo! Registré tu gasto de **$1200** de **laptop** en la categoría **Electronics & tech** con fecha de **2026-03-08** (ayer).

**Reasoning Summary**:

```
**Parsing expense in Spanish**

I need to extract details from the Spanish text. It mentions buying a laptop for $1,200. I should also add a date, which seems to be yesterday, meaning March 8, 2026. The category will be "electronics & tech," and I can use "Laptop" as the description. Since the user stated an expense, I’ll need to call the relevant tool to process this. Alright, I’ll get on it!
```

**Evaluations**:

| Result | Evaluator | Message |
|---|---|---|
| ✅ Pass | tool_called | Tool 'add_expense_cat_c' was called |
| ✅ Pass | category_valid | Category 'Electronics & tech' is valid |
| ✅ Pass | category_match | Category 'Electronics & tech' matches expected 'Electronics & tech' |

</details>
