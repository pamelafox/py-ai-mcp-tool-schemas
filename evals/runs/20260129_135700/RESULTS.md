# MCP Tool Schema Evaluation Report

## Metadata

- **Timestamp**: 2026-01-29T13:57:00.152812
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
| add_expense_model_a | expense: ExpenseInput (Pydantic model) | 0.97 | 6 |

## Evaluation Breakdown

### category_match

| Variant | Description | Pass Rate | Passed | Total |
|---------|-------------|-----------|--------|-------|
| add_expense_model_a | expense: ExpenseInput (Pydantic model) | 100.0% | 6 | 6 |

### category_valid

| Variant | Description | Pass Rate | Passed | Total |
|---------|-------------|-----------|--------|-------|
| add_expense_model_a | expense: ExpenseInput (Pydantic model) | 100.0% | 6 | 6 |

### date_format

| Variant | Description | Pass Rate | Passed | Total |
|---------|-------------|-----------|--------|-------|
| add_expense_model_a | expense: ExpenseInput (Pydantic model) | 100.0% | 6 | 6 |

### date_match

| Variant | Description | Pass Rate | Passed | Total |
|---------|-------------|-----------|--------|-------|
| add_expense_model_a | expense: ExpenseInput (Pydantic model) | 83.3% | 5 | 6 |

### tool_called

| Variant | Description | Pass Rate | Passed | Total |
|---------|-------------|-----------|--------|-------|
| add_expense_model_a | expense: ExpenseInput (Pydantic model) | 100.0% | 6 | 6 |

## Detailed Results

<details>
<summary>Click to expand</summary>

### add_expense_model_a / clear_food_yesterday: 1.00

**User Query**:

> Yesterday I bought a sandwich for $12.50.

**Tool Calls**:

- Tool: `add_expense_model_a`

```json
{
  "expense": {
    "expense_date": "2026-01-28",
    "amount": 12.5,
    "category": "food",
    "description": "sandwich"
  }
}
```


**Assistant Output**:

> I've recorded your expense of $12.50 for the sandwich purchased yesterday. If you have any other expenses to log, feel free to let me know!

**Reasoning Summary**:

```
(none returned)
```

**Evaluations**:

| Result | Evaluator | Message |
|---|---|---|
| ✅ | tool_called | Tool 'add_expense_model_a' was called |
| ✅ | category_valid | Category 'food' is valid |
| ✅ | date_format | Date '2026-01-28' is in correct format |
| ✅ | category_match | Category 'food' matches expected 'food' |
| ✅ | date_match | Date '2026-01-28' matches expected '2026-01-28' |

### add_expense_model_a / clear_transport_today: 1.00

**User Query**:

> I paid $45 for gas today (2026-01-29).

**Tool Calls**:

- Tool: `add_expense_model_a`

```json
{
  "expense": {
    "expense_date": "2026-01-29",
    "amount": 45,
    "category": "transport",
    "description": "gas"
  }
}
```


**Assistant Output**:

> I have logged your $45 expense for gas today. Is there anything else you would like to record?

**Reasoning Summary**:

```
(none returned)
```

**Evaluations**:

| Result | Evaluator | Message |
|---|---|---|
| ✅ | tool_called | Tool 'add_expense_model_a' was called |
| ✅ | category_valid | Category 'transport' is valid |
| ✅ | date_format | Date '2026-01-29' is in correct format |
| ✅ | category_match | Category 'transport' matches expected 'transport' |
| ✅ | date_match | Date '2026-01-29' matches expected '2026-01-29' |

### add_expense_model_a / clear_entertainment: 1.00

**User Query**:

> On 2026-01-15 I spent $25.99 on a movie ticket.

**Tool Calls**:

- Tool: `add_expense_model_a`

```json
{
  "expense": {
    "expense_date": "2026-01-15",
    "amount": 25.99,
    "category": "entertainment",
    "description": "movie ticket"
  }
}
```


**Assistant Output**:

> I have logged your expense of $25.99 on 2026-01-15 for a movie ticket under the entertainment category. Is there anything else you would like to add?

**Reasoning Summary**:

```
(none returned)
```

**Evaluations**:

| Result | Evaluator | Message |
|---|---|---|
| ✅ | tool_called | Tool 'add_expense_model_a' was called |
| ✅ | category_valid | Category 'entertainment' is valid |
| ✅ | date_format | Date '2026-01-15' is in correct format |
| ✅ | category_match | Category 'entertainment' matches expected 'entertainment' |
| ✅ | date_match | Date '2026-01-15' matches expected '2026-01-15' |

### add_expense_model_a / relative_date_last_friday_movie: 0.80

**User Query**:

> Last Friday I spent $18 on a movie ticket.

**Tool Calls**:

- Tool: `add_expense_model_a`

```json
{
  "expense": {
    "expense_date": "2026-01-24",
    "amount": 18,
    "category": "entertainment",
    "description": "Movie ticket"
  }
}
```


**Assistant Output**:

> I've recorded your $18 expense for the movie ticket last Friday, January 24, 2026. Is there anything else you'd like to log?

**Reasoning Summary**:

```
(none returned)
```

**Evaluations**:

| Result | Evaluator | Message |
|---|---|---|
| ✅ | tool_called | Tool 'add_expense_model_a' was called |
| ✅ | category_valid | Category 'entertainment' is valid |
| ✅ | date_format | Date '2026-01-24' is in correct format |
| ✅ | category_match | Category 'entertainment' matches expected 'entertainment' |
| ❌ | date_match | Date '2026-01-24' does not match expected '2026-01-23' |

### add_expense_model_a / hard_category_grocery_delivery_yesterday: 1.00

**User Query**:

> Yesterday I paid $65 for Instacart grocery delivery.

**Tool Calls**:

- Tool: `add_expense_model_a`

```json
{
  "expense": {
    "expense_date": "2026-01-28",
    "amount": 65,
    "category": "food",
    "description": "Instacart grocery delivery"
  }
}
```


**Assistant Output**:

> I have logged your $65 expense for Instacart grocery delivery on January 28, 2026. Is there anything else you would like to add?

**Reasoning Summary**:

```
(none returned)
```

**Evaluations**:

| Result | Evaluator | Message |
|---|---|---|
| ✅ | tool_called | Tool 'add_expense_model_a' was called |
| ✅ | category_valid | Category 'food' is valid |
| ✅ | date_format | Date '2026-01-28' is in correct format |
| ✅ | category_match | Category 'food' matches expected 'food' |
| ✅ | date_match | Date '2026-01-28' matches expected '2026-01-28' |

### add_expense_model_a / spanish_gadget: 1.00

**User Query**:

> Ayer compré una laptop por 1200 dólares.

**Tool Calls**:

- Tool: `add_expense_model_a`

```json
{
  "expense": {
    "expense_date": "2026-01-28",
    "amount": 1200,
    "category": "gadget",
    "description": "Compra de laptop"
  }
}
```


**Assistant Output**:

> He registrado la compra de la laptop por 1200 dólares realizada ayer. ¿Quieres añadir algún otro gasto?

**Reasoning Summary**:

```
(none returned)
```

**Evaluations**:

| Result | Evaluator | Message |
|---|---|---|
| ✅ | tool_called | Tool 'add_expense_model_a' was called |
| ✅ | category_valid | Category 'gadget' is valid |
| ✅ | date_format | Date '2026-01-28' is in correct format |
| ✅ | category_match | Category 'gadget' matches expected 'gadget' |
| ✅ | date_match | Date '2026-01-28' matches expected '2026-01-28' |

</details>
