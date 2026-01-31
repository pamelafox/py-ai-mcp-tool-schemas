# MCP Tool Schema Evaluation Report

## Metadata

- **Timestamp**: 2026-01-30T15:52:11.668088
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
| add_expense_cat_a | category: str | 0.33 | 1 |
| add_expense_cat_b | category: Annotated[str, ...] | 1.00 | 1 |
| add_expense_cat_c | category: Literal[...] | 1.00 | 1 |
| add_expense_cat_d | category: ExpenseCategory (Enum) | 1.00 | 1 |
| add_expense_cat_e | category: Annotated[ExpenseCategory, Field(description=...)] | 1.00 | 1 |
| add_expense_date_a | expense_date: str | 1.00 | 1 |
| add_expense_date_b | expense_date: Annotated[str, ...] | 1.00 | 1 |
| add_expense_date_c | expense_date: date | 1.00 | 1 |
| add_expense_date_d | expense_date: Annotated[str, Field(pattern=...)] | 1.00 | 1 |
| add_expense_model_a | expense: ExpenseInput (Pydantic model) | 1.00 | 1 |
| add_expense_reimb_e | reimbursable: bool \| Literal["unknown"] | 1.00 | 1 |

## Evaluation Breakdown

### category_match

| Variant | Description | Pass Rate | Passed | Total |
|---------|-------------|-----------|--------|-------|
| add_expense_cat_a | category: str | 0.0% | 0 | 1 |
| add_expense_cat_b | category: Annotated[str, ...] | 100.0% | 1 | 1 |
| add_expense_cat_c | category: Literal[...] | 100.0% | 1 | 1 |
| add_expense_cat_d | category: ExpenseCategory (Enum) | 100.0% | 1 | 1 |
| add_expense_cat_e | category: Annotated[ExpenseCategory, Field(description=...)] | 100.0% | 1 | 1 |
| add_expense_model_a | expense: ExpenseInput (Pydantic model) | 100.0% | 1 | 1 |

### category_valid

| Variant | Description | Pass Rate | Passed | Total |
|---------|-------------|-----------|--------|-------|
| add_expense_cat_a | category: str | 0.0% | 0 | 1 |
| add_expense_cat_b | category: Annotated[str, ...] | 100.0% | 1 | 1 |
| add_expense_cat_c | category: Literal[...] | 100.0% | 1 | 1 |
| add_expense_cat_d | category: ExpenseCategory (Enum) | 100.0% | 1 | 1 |
| add_expense_cat_e | category: Annotated[ExpenseCategory, Field(description=...)] | 100.0% | 1 | 1 |
| add_expense_model_a | expense: ExpenseInput (Pydantic model) | 100.0% | 1 | 1 |

### date_format

| Variant | Description | Pass Rate | Passed | Total |
|---------|-------------|-----------|--------|-------|
| add_expense_date_a | expense_date: str | 100.0% | 1 | 1 |
| add_expense_date_b | expense_date: Annotated[str, ...] | 100.0% | 1 | 1 |
| add_expense_date_c | expense_date: date | 100.0% | 1 | 1 |
| add_expense_date_d | expense_date: Annotated[str, Field(pattern=...)] | 100.0% | 1 | 1 |
| add_expense_model_a | expense: ExpenseInput (Pydantic model) | 100.0% | 1 | 1 |

### date_match

| Variant | Description | Pass Rate | Passed | Total |
|---------|-------------|-----------|--------|-------|
| add_expense_date_a | expense_date: str | 100.0% | 1 | 1 |
| add_expense_date_b | expense_date: Annotated[str, ...] | 100.0% | 1 | 1 |
| add_expense_date_c | expense_date: date | 100.0% | 1 | 1 |
| add_expense_date_d | expense_date: Annotated[str, Field(pattern=...)] | 100.0% | 1 | 1 |
| add_expense_model_a | expense: ExpenseInput (Pydantic model) | 100.0% | 1 | 1 |

### tool_called

| Variant | Description | Pass Rate | Passed | Total |
|---------|-------------|-----------|--------|-------|
| add_expense_cat_a | category: str | 100.0% | 1 | 1 |
| add_expense_cat_b | category: Annotated[str, ...] | 100.0% | 1 | 1 |
| add_expense_cat_c | category: Literal[...] | 100.0% | 1 | 1 |
| add_expense_cat_d | category: ExpenseCategory (Enum) | 100.0% | 1 | 1 |
| add_expense_cat_e | category: Annotated[ExpenseCategory, Field(description=...)] | 100.0% | 1 | 1 |
| add_expense_date_a | expense_date: str | 100.0% | 1 | 1 |
| add_expense_date_b | expense_date: Annotated[str, ...] | 100.0% | 1 | 1 |
| add_expense_date_c | expense_date: date | 100.0% | 1 | 1 |
| add_expense_date_d | expense_date: Annotated[str, Field(pattern=...)] | 100.0% | 1 | 1 |
| add_expense_model_a | expense: ExpenseInput (Pydantic model) | 100.0% | 1 | 1 |
| add_expense_reimb_e | reimbursable: bool \| Literal["unknown"] | 100.0% | 1 | 1 |

## Detailed Results

<details>
<summary>Click to expand</summary>

### add_expense_cat_a / clear_food_yesterday: 0.33

**User Query**:

> Yesterday I bought a sandwich for $12.50.

**Tool Calls**:

- Tool: `add_expense_cat_a`

```json
{
  "expense_date": "2026-01-29",
  "amount": 12.5,
  "category": "Food",
  "description": "Sandwich"
}
```


**Assistant Output**:

> Logged: **$12.50** — **Sandwich** (**Food**) on **2026-01-29**.

**Reasoning Summary**:

```
(none returned)
```

**Evaluations**:

| Result | Evaluator | Message |
|---|---|---|
| ✅ Pass | tool_called | Tool 'add_expense_cat_a' was called |
| ❌ Fail | category_valid | Category 'Food' is not a valid enum value |
| ❌ Fail | category_match | Category 'Food' does not match expected 'Food & drink' |

### add_expense_cat_b / clear_food_yesterday: 1.00

**User Query**:

> Yesterday I bought a sandwich for $12.50.

**Tool Calls**:

- Tool: `add_expense_cat_b`

```json
{
  "expense_date": "2026-01-29",
  "amount": 12.5,
  "category": "Food & drink",
  "description": "Sandwich"
}
```


**Assistant Output**:

> Logged: **$12.50** — **Sandwich** (**Food & drink**) on **2026-01-29**.

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

### add_expense_cat_c / clear_food_yesterday: 1.00

**User Query**:

> Yesterday I bought a sandwich for $12.50.

**Tool Calls**:

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

> Logged: **$12.50** for **Sandwich** on **2026-01-29** under **Food & drink**.

**Reasoning Summary**:

```
(none returned)
```

**Evaluations**:

| Result | Evaluator | Message |
|---|---|---|
| ✅ Pass | tool_called | Tool 'add_expense_cat_c' was called |
| ✅ Pass | category_valid | Category 'Food & drink' is valid |
| ✅ Pass | category_match | Category 'Food & drink' matches expected 'Food & drink' |

### add_expense_cat_d / clear_food_yesterday: 1.00

**User Query**:

> Yesterday I bought a sandwich for $12.50.

**Tool Calls**:

- Tool: `add_expense_cat_d`

```json
{
  "expense_date": "2026-01-29",
  "amount": 12.5,
  "category": "Food & drink",
  "description": "Sandwich"
}
```


**Assistant Output**:

> Logged: **$12.50** on **2026-01-29** — **Food & drink** (Sandwich).

**Reasoning Summary**:

```
(none returned)
```

**Evaluations**:

| Result | Evaluator | Message |
|---|---|---|
| ✅ Pass | tool_called | Tool 'add_expense_cat_d' was called |
| ✅ Pass | category_valid | Category 'Food & drink' is valid |
| ✅ Pass | category_match | Category 'Food & drink' matches expected 'Food & drink' |

### add_expense_cat_e / clear_food_yesterday: 1.00

**User Query**:

> Yesterday I bought a sandwich for $12.50.

**Tool Calls**:

- Tool: `add_expense_cat_e`

```json
{
  "expense_date": "2026-01-29",
  "amount": 12.5,
  "category": "Food & drink",
  "description": "Sandwich"
}
```


**Assistant Output**:

> Logged: **$12.50** for **Sandwich** on **2026-01-29** (Food & drink).

**Reasoning Summary**:

```
(none returned)
```

**Evaluations**:

| Result | Evaluator | Message |
|---|---|---|
| ✅ Pass | tool_called | Tool 'add_expense_cat_e' was called |
| ✅ Pass | category_valid | Category 'Food & drink' is valid |
| ✅ Pass | category_match | Category 'Food & drink' matches expected 'Food & drink' |

### add_expense_date_a / clear_food_yesterday: 1.00

**User Query**:

> Yesterday I bought a sandwich for $12.50.

**Tool Calls**:

- Tool: `add_expense_date_a`

```json
{
  "expense_date": "2026-01-29",
  "amount": 12.5,
  "category": "Food & drink",
  "description": "Sandwich"
}
```


**Assistant Output**:

> Logged: **$12.50** — **Sandwich** (**Food & drink**) on **2026-01-29**.

**Reasoning Summary**:

```
(none returned)
```

**Evaluations**:

| Result | Evaluator | Message |
|---|---|---|
| ✅ Pass | tool_called | Tool 'add_expense_date_a' was called |
| ✅ Pass | date_format | Date '2026-01-29' is in correct format |
| ✅ Pass | date_match | Date '2026-01-29' matches expected '2026-01-29' |

### add_expense_date_b / clear_food_yesterday: 1.00

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

> Logged: **$12.50** for **Sandwich** on **2026-01-29** under **Food & drink**.

**Reasoning Summary**:

```
(none returned)
```

**Evaluations**:

| Result | Evaluator | Message |
|---|---|---|
| ✅ Pass | tool_called | Tool 'add_expense_date_b' was called |
| ✅ Pass | date_format | Date '2026-01-29' is in correct format |
| ✅ Pass | date_match | Date '2026-01-29' matches expected '2026-01-29' |

### add_expense_date_c / clear_food_yesterday: 1.00

**User Query**:

> Yesterday I bought a sandwich for $12.50.

**Tool Calls**:

- Tool: `add_expense_date_c`

```json
{
  "expense_date": "2026-01-29",
  "amount": 12.5,
  "category": "Food & drink",
  "description": "Sandwich"
}
```


**Assistant Output**:

> Logged: **$12.50** — **Sandwich** (**Food & drink**) on **2026-01-29**.

**Reasoning Summary**:

```
(none returned)
```

**Evaluations**:

| Result | Evaluator | Message |
|---|---|---|
| ✅ Pass | tool_called | Tool 'add_expense_date_c' was called |
| ✅ Pass | date_format | Date '2026-01-29' is in correct format |
| ✅ Pass | date_match | Date '2026-01-29' matches expected '2026-01-29' |

### add_expense_date_d / clear_food_yesterday: 1.00

**User Query**:

> Yesterday I bought a sandwich for $12.50.

**Tool Calls**:

- Tool: `add_expense_date_d`

```json
{
  "expense_date": "2026-01-29",
  "amount": 12.5,
  "category": "Food & drink",
  "description": "Sandwich"
}
```


**Assistant Output**:

> Logged: **$12.50** — **Sandwich** (**Food & drink**) on **2026-01-29**.

**Reasoning Summary**:

```
(none returned)
```

**Evaluations**:

| Result | Evaluator | Message |
|---|---|---|
| ✅ Pass | tool_called | Tool 'add_expense_date_d' was called |
| ✅ Pass | date_format | Date '2026-01-29' is in correct format |
| ✅ Pass | date_match | Date '2026-01-29' matches expected '2026-01-29' |

### add_expense_model_a / clear_food_yesterday: 1.00

**User Query**:

> Yesterday I bought a sandwich for $12.50.

**Tool Calls**:

- Tool: `add_expense_model_a`

```json
{
  "expense": {
    "expense_date": "2026-01-29",
    "amount": 12.5,
    "category": "Food & drink",
    "description": "Sandwich"
  }
}
```


**Assistant Output**:

> Logged: **$12.50** — **Sandwich** (**Food & drink**) on **2026-01-29**.

**Reasoning Summary**:

```
(none returned)
```

**Evaluations**:

| Result | Evaluator | Message |
|---|---|---|
| ✅ Pass | tool_called | Tool 'add_expense_model_a' was called |
| ✅ Pass | category_valid | Category 'Food & drink' is valid |
| ✅ Pass | category_match | Category 'Food & drink' matches expected 'Food & drink' |
| ✅ Pass | date_format | Date '2026-01-29' is in correct format |
| ✅ Pass | date_match | Date '2026-01-29' matches expected '2026-01-29' |

### add_expense_reimb_e / clear_food_yesterday: 1.00

**User Query**:

> Yesterday I bought a sandwich for $12.50.

**Tool Calls**:

- Tool: `add_expense_reimb_e`

```json
{
  "expense_date": "2026-01-29",
  "amount": 12.5,
  "category": "Food & drink",
  "description": "Sandwich",
  "reimbursable": "unknown"
}
```


**Assistant Output**:

> Logged: **$12.50** for **Sandwich** on **2026-01-29** (Food & drink).

**Reasoning Summary**:

```
(none returned)
```

**Evaluations**:

| Result | Evaluator | Message |
|---|---|---|
| ✅ Pass | tool_called | Tool 'add_expense_reimb_e' was called |

</details>
