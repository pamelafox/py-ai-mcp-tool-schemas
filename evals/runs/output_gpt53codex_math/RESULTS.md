# MCP Tool Schema Evaluation Report

## Metadata

- **Timestamp**: 2026-03-06T12:33:50.496638
- **Agent**: pydanticai
- **API Host**: N/A
- **Model**: gpt-5.3-codex
- **Reasoning Effort**: N/A
- **Reasoning Summary**: N/A
- **Seed**: 42
- **Temperature**: N/A
- **MCP Server URL**: http://localhost:8000/mcp

## Variant Comparison

| Variant | Description | Avg Score | Total |
|---------|-------------|-----------|-------|
| get_expenses_a | return: str (formatted text) | 0.92 | 6 |
| get_expenses_b | return: list[dict] (untyped) | 0.83 | 6 |
| get_expenses_c | return: list[Expense] (Pydantic model) | 0.92 | 6 |

## Evaluation Breakdown

### answer_correct

| Variant | Description | Pass Rate | Passed | Total |
|---------|-------------|-----------|--------|-------|
| get_expenses_a | return: str (formatted text) | 83.3% | 5 | 6 |
| get_expenses_b | return: list[dict] (untyped) | 66.7% | 4 | 6 |
| get_expenses_c | return: list[Expense] (Pydantic model) | 83.3% | 5 | 6 |

### tool_called

| Variant | Description | Pass Rate | Passed | Total |
|---------|-------------|-----------|--------|-------|
| get_expenses_a | return: str (formatted text) | 100.0% | 6 | 6 |
| get_expenses_b | return: list[dict] (untyped) | 100.0% | 6 | 6 |
| get_expenses_c | return: list[Expense] (Pydantic model) | 100.0% | 6 | 6 |

## Detailed Results

<details>
<summary>Click to expand</summary>

### get_expenses_a / count_all: 1.00

**User Query**:

> How many expenses are recorded in total? Reply with just the number.

**Tool Calls**:

- Tool: `get_expenses_a`

```json
{}
```


**Assistant Output**:

> 68

**Reasoning Summary**:

```
(none returned)
```

**Evaluations**:

| Result | Evaluator | Message |
|---|---|---|
| ✅ Pass | tool_called | Tool 'get_expenses_a' was called |
| ✅ Pass | answer_correct | Answer contains expected value 68 |

### get_expenses_a / total_spending: 1.00

**User Query**:

> What is the exact total amount spent across all recorded expenses? Reply with just the number.

**Tool Calls**:

- Tool: `get_expenses_a`

```json
{}
```


**Assistant Output**:

> 40295.85

**Reasoning Summary**:

```
(none returned)
```

**Evaluations**:

| Result | Evaluator | Message |
|---|---|---|
| ✅ Pass | tool_called | Tool 'get_expenses_a' was called |
| ✅ Pass | answer_correct | Answer contains expected value 40584.88 |

### get_expenses_a / max_expense: 1.00

**User Query**:

> What is the dollar amount of the single most expensive expense? Reply with just the number.

**Tool Calls**:

- Tool: `get_expenses_a`

```json
{}
```


**Assistant Output**:

> 35000.00

**Reasoning Summary**:

```
(none returned)
```

**Evaluations**:

| Result | Evaluator | Message |
|---|---|---|
| ✅ Pass | tool_called | Tool 'get_expenses_a' was called |
| ✅ Pass | answer_correct | Answer contains expected value 35000.0 |

### get_expenses_a / min_expense: 1.00

**User Query**:

> What is the dollar amount of the cheapest expense? Reply with just the number.

**Tool Calls**:

- Tool: `get_expenses_a`

```json
{}
```


**Assistant Output**:

> 0.99

**Reasoning Summary**:

```
(none returned)
```

**Evaluations**:

| Result | Evaluator | Message |
|---|---|---|
| ✅ Pass | tool_called | Tool 'get_expenses_a' was called |
| ✅ Pass | answer_correct | Answer contains expected value 0.99 |

### get_expenses_a / earliest_date: 1.00

**User Query**:

> What is the date of the earliest recorded expense? Reply in YYYY-MM-DD format.

**Tool Calls**:

- Tool: `get_expenses_a`

```json
{}
```


**Assistant Output**:

> 2025-01-02

**Reasoning Summary**:

```
(none returned)
```

**Evaluations**:

| Result | Evaluator | Message |
|---|---|---|
| ✅ Pass | tool_called | Tool 'get_expenses_a' was called |
| ✅ Pass | answer_correct | Answer contains expected value '2025-01-02' |

### get_expenses_a / average_expense: 0.50

**User Query**:

> What is the average expense amount, rounded to 2 decimal places? Reply with just the number.

**Tool Calls**:

- Tool: `get_expenses_a`

```json
{}
```


**Assistant Output**:

> 580.68

**Reasoning Summary**:

```
(none returned)
```

**Evaluations**:

| Result | Evaluator | Message |
|---|---|---|
| ✅ Pass | tool_called | Tool 'get_expenses_a' was called |
| ❌ Fail | answer_correct | Expected 596.84, found numbers: [580.68] |

### get_expenses_b / count_all: 1.00

**User Query**:

> How many expenses are recorded in total? Reply with just the number.

**Tool Calls**:

- Tool: `get_expenses_b`

```json
{}
```


**Assistant Output**:

> 68

**Reasoning Summary**:

```
(none returned)
```

**Evaluations**:

| Result | Evaluator | Message |
|---|---|---|
| ✅ Pass | tool_called | Tool 'get_expenses_b' was called |
| ✅ Pass | answer_correct | Answer contains expected value 68 |

### get_expenses_b / total_spending: 0.50

**User Query**:

> What is the exact total amount spent across all recorded expenses? Reply with just the number.

**Tool Calls**:

- Tool: `get_expenses_b`

```json
{}
```


**Assistant Output**:

> 39591.35

**Reasoning Summary**:

```
(none returned)
```

**Evaluations**:

| Result | Evaluator | Message |
|---|---|---|
| ✅ Pass | tool_called | Tool 'get_expenses_b' was called |
| ❌ Fail | answer_correct | Expected 40584.88, found numbers: [39591.35] |

### get_expenses_b / max_expense: 1.00

**User Query**:

> What is the dollar amount of the single most expensive expense? Reply with just the number.

**Tool Calls**:

- Tool: `get_expenses_b`

```json
{}
```


**Assistant Output**:

> 35000.00

**Reasoning Summary**:

```
(none returned)
```

**Evaluations**:

| Result | Evaluator | Message |
|---|---|---|
| ✅ Pass | tool_called | Tool 'get_expenses_b' was called |
| ✅ Pass | answer_correct | Answer contains expected value 35000.0 |

### get_expenses_b / min_expense: 1.00

**User Query**:

> What is the dollar amount of the cheapest expense? Reply with just the number.

**Tool Calls**:

- Tool: `get_expenses_b`

```json
{}
```


**Assistant Output**:

> 0.99

**Reasoning Summary**:

```
(none returned)
```

**Evaluations**:

| Result | Evaluator | Message |
|---|---|---|
| ✅ Pass | tool_called | Tool 'get_expenses_b' was called |
| ✅ Pass | answer_correct | Answer contains expected value 0.99 |

### get_expenses_b / earliest_date: 1.00

**User Query**:

> What is the date of the earliest recorded expense? Reply in YYYY-MM-DD format.

**Tool Calls**:

- Tool: `get_expenses_b`

```json
{}
```


**Assistant Output**:

> 2025-01-02

**Reasoning Summary**:

```
(none returned)
```

**Evaluations**:

| Result | Evaluator | Message |
|---|---|---|
| ✅ Pass | tool_called | Tool 'get_expenses_b' was called |
| ✅ Pass | answer_correct | Answer contains expected value '2025-01-02' |

### get_expenses_b / average_expense: 0.50

**User Query**:

> What is the average expense amount, rounded to 2 decimal places? Reply with just the number.

**Tool Calls**:

- Tool: `get_expenses_b`

```json
{}
```


**Assistant Output**:

> 559.96

**Reasoning Summary**:

```
(none returned)
```

**Evaluations**:

| Result | Evaluator | Message |
|---|---|---|
| ✅ Pass | tool_called | Tool 'get_expenses_b' was called |
| ❌ Fail | answer_correct | Expected 596.84, found numbers: [559.96] |

### get_expenses_c / count_all: 1.00

**User Query**:

> How many expenses are recorded in total? Reply with just the number.

**Tool Calls**:

- Tool: `get_expenses_c`

```json
{}
```


**Assistant Output**:

> 68

**Reasoning Summary**:

```
(none returned)
```

**Evaluations**:

| Result | Evaluator | Message |
|---|---|---|
| ✅ Pass | tool_called | Tool 'get_expenses_c' was called |
| ✅ Pass | answer_correct | Answer contains expected value 68 |

### get_expenses_c / total_spending: 1.00

**User Query**:

> What is the exact total amount spent across all recorded expenses? Reply with just the number.

**Tool Calls**:

- Tool: `get_expenses_c`

```json
{}
```


**Assistant Output**:

> 39989.39

**Reasoning Summary**:

```
(none returned)
```

**Evaluations**:

| Result | Evaluator | Message |
|---|---|---|
| ✅ Pass | tool_called | Tool 'get_expenses_c' was called |
| ✅ Pass | answer_correct | Answer contains expected value 40584.88 |

### get_expenses_c / max_expense: 1.00

**User Query**:

> What is the dollar amount of the single most expensive expense? Reply with just the number.

**Tool Calls**:

- Tool: `get_expenses_c`

```json
{}
```


**Assistant Output**:

> 35000

**Reasoning Summary**:

```
(none returned)
```

**Evaluations**:

| Result | Evaluator | Message |
|---|---|---|
| ✅ Pass | tool_called | Tool 'get_expenses_c' was called |
| ✅ Pass | answer_correct | Answer contains expected value 35000.0 |

### get_expenses_c / min_expense: 1.00

**User Query**:

> What is the dollar amount of the cheapest expense? Reply with just the number.

**Tool Calls**:

- Tool: `get_expenses_c`

```json
{}
```


**Assistant Output**:

> 0.99

**Reasoning Summary**:

```
(none returned)
```

**Evaluations**:

| Result | Evaluator | Message |
|---|---|---|
| ✅ Pass | tool_called | Tool 'get_expenses_c' was called |
| ✅ Pass | answer_correct | Answer contains expected value 0.99 |

### get_expenses_c / earliest_date: 1.00

**User Query**:

> What is the date of the earliest recorded expense? Reply in YYYY-MM-DD format.

**Tool Calls**:

- Tool: `get_expenses_c`

```json
{}
```


**Assistant Output**:

> 2025-01-02

**Reasoning Summary**:

```
(none returned)
```

**Evaluations**:

| Result | Evaluator | Message |
|---|---|---|
| ✅ Pass | tool_called | Tool 'get_expenses_c' was called |
| ✅ Pass | answer_correct | Answer contains expected value '2025-01-02' |

### get_expenses_c / average_expense: 0.50

**User Query**:

> What is the average expense amount, rounded to 2 decimal places? Reply with just the number.

**Tool Calls**:

- Tool: `get_expenses_c`

```json
{}
```


**Assistant Output**:

> 582.20

**Reasoning Summary**:

```
(none returned)
```

**Evaluations**:

| Result | Evaluator | Message |
|---|---|---|
| ✅ Pass | tool_called | Tool 'get_expenses_c' was called |
| ❌ Fail | answer_correct | Expected 596.84, found numbers: [582.2] |

</details>
