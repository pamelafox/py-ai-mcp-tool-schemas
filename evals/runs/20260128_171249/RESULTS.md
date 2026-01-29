# MCP Tool Schema Evaluation Report

## Metadata

- **Timestamp**: 2026-01-28T17:12:49.067725
- **API Host**: azure
- **Model**: gpt-5.2
- **Temperature**: 0
- **Seed**: 42
- **MCP Server URL**: http://localhost:8000/mcp

## Variant Comparison

| Variant | Description | Pass Rate | Avg Score | Passed | Total |
|---------|-------------|-----------|-----------|--------|-------|
| add_expense_cat_a | category: str | 14.3% | 0.54 | 2 | 14 |
| add_expense_cat_b | category: Annotated[str, ...] | 78.6% | 0.77 | 11 | 14 |
| add_expense_cat_c | category: Literal[...] | 85.7% | 0.86 | 12 | 14 |
| add_expense_cat_d | category: ExpenseCategory (Enum) | 85.7% | 0.86 | 12 | 14 |
| add_expense_date_a | expense_date: str | 78.6% | 0.77 | 11 | 14 |
| add_expense_date_b | expense_date: Annotated[str, ...] | 78.6% | 0.79 | 11 | 14 |
| add_expense_date_c | expense_date: date | 92.9% | 0.91 | 13 | 14 |
| add_expense_date_d | expense_date: Annotated[str, Field(pattern=...)] | 71.4% | 0.70 | 10 | 14 |

## Evaluation Breakdown

### category_match

| Variant | Description | Pass Rate | Passed | Total |
|---------|-------------|-----------|--------|-------|
| add_expense_cat_a | category: str | 20.0% | 2 | 10 |
| add_expense_cat_b | category: Annotated[str, ...] | 70.0% | 7 | 10 |
| add_expense_cat_c | category: Literal[...] | 90.0% | 9 | 10 |
| add_expense_cat_d | category: ExpenseCategory (Enum) | 90.0% | 9 | 10 |

### category_valid

| Variant | Description | Pass Rate | Passed | Total |
|---------|-------------|-----------|--------|-------|
| add_expense_cat_a | category: str | 14.3% | 2 | 14 |
| add_expense_cat_b | category: Annotated[str, ...] | 78.6% | 11 | 14 |
| add_expense_cat_c | category: Literal[...] | 85.7% | 12 | 14 |
| add_expense_cat_d | category: ExpenseCategory (Enum) | 85.7% | 12 | 14 |

### date_format

| Variant | Description | Pass Rate | Passed | Total |
|---------|-------------|-----------|--------|-------|
| add_expense_date_a | expense_date: str | 78.6% | 11 | 14 |
| add_expense_date_b | expense_date: Annotated[str, ...] | 78.6% | 11 | 14 |
| add_expense_date_c | expense_date: date | 92.9% | 13 | 14 |
| add_expense_date_d | expense_date: Annotated[str, Field(pattern=...)] | 71.4% | 10 | 14 |

### date_match

| Variant | Description | Pass Rate | Passed | Total |
|---------|-------------|-----------|--------|-------|
| add_expense_date_a | expense_date: str | 91.7% | 11 | 12 |
| add_expense_date_b | expense_date: Annotated[str, ...] | 91.7% | 11 | 12 |
| add_expense_date_c | expense_date: date | 100.0% | 12 | 12 |
| add_expense_date_d | expense_date: Annotated[str, Field(pattern=...)] | 83.3% | 10 | 12 |

### tool_called

| Variant | Description | Pass Rate | Passed | Total |
|---------|-------------|-----------|--------|-------|
| add_expense_cat_a | category: str | 78.6% | 11 | 14 |
| add_expense_cat_b | category: Annotated[str, ...] | 78.6% | 11 | 14 |
| add_expense_cat_c | category: Literal[...] | 85.7% | 12 | 14 |
| add_expense_cat_d | category: ExpenseCategory (Enum) | 85.7% | 12 | 14 |
| add_expense_date_a | expense_date: str | 78.6% | 11 | 14 |
| add_expense_date_b | expense_date: Annotated[str, ...] | 78.6% | 11 | 14 |
| add_expense_date_c | expense_date: date | 92.9% | 13 | 14 |
| add_expense_date_d | expense_date: Annotated[str, Field(pattern=...)] | 71.4% | 10 | 14 |

## Detailed Results

<details>
<summary>Click to expand</summary>

### add_expense_cat_a / clear_food_yesterday: PASS (1.00)

**Tool Calls**:

- `add_expense_cat_a`
  ```json
  {
  "expense_date": "2026-01-27",
  "amount": 12.5,
  "category": "Food",
  "description": "Sandwich"
}
  ```

**Evaluations**:

- [+] tool_called: Tool 'add_expense_cat_a' was called
- [+] category_valid: Category 'Food' is valid
- [+] date_format: Date '2026-01-27' is in correct format
- [+] category_match: Category 'Food' matches expected 'food'
- [+] date_match: Date '2026-01-27' matches expected '2026-01-27'

### add_expense_cat_a / clear_transport_today: FAIL (0.60)

**Tool Calls**:

- `add_expense_cat_a`
  ```json
  {
  "expense_date": "2026-01-28",
  "amount": 45,
  "category": "Gas",
  "description": "Gas"
}
  ```

**Evaluations**:

- [+] tool_called: Tool 'add_expense_cat_a' was called
- [-] category_valid: Category 'Gas' is not a valid enum value
- [+] date_format: Date '2026-01-28' is in correct format
- [-] category_match: Category 'Gas' does not match expected 'transport'
- [+] date_match: Date '2026-01-28' matches expected '2026-01-28'

### add_expense_cat_a / clear_entertainment: PASS (1.00)

**Tool Calls**:

- `add_expense_cat_a`
  ```json
  {
  "expense_date": "2026-01-15",
  "amount": 25.99,
  "category": "Entertainment",
  "description": "Movie ticket"
}
  ```

**Evaluations**:

- [+] tool_called: Tool 'add_expense_cat_a' was called
- [+] category_valid: Category 'Entertainment' is valid
- [+] date_format: Date '2026-01-15' is in correct format
- [+] category_match: Category 'Entertainment' matches expected 'entertainment'
- [+] date_match: Date '2026-01-15' matches expected '2026-01-15'

### add_expense_cat_a / clear_shopping: FAIL (0.60)

**Tool Calls**:

- `add_expense_cat_a`
  ```json
  {
  "expense_date": "2026-01-20",
  "amount": 125,
  "category": "Clothing",
  "description": "New shoes"
}
  ```

**Evaluations**:

- [+] tool_called: Tool 'add_expense_cat_a' was called
- [-] category_valid: Category 'Clothing' is not a valid enum value
- [+] date_format: Date '2026-01-20' is in correct format
- [-] category_match: Category 'Clothing' does not match expected 'shopping'
- [+] date_match: Date '2026-01-20' matches expected '2026-01-20'

### add_expense_cat_a / clear_gadget: FAIL (0.60)

**Tool Calls**:

- `add_expense_cat_a`
  ```json
  {
  "expense_date": "2026-01-27",
  "amount": 1200,
  "category": "Electronics",
  "description": "Laptop purchase"
}
  ```

**Evaluations**:

- [+] tool_called: Tool 'add_expense_cat_a' was called
- [-] category_valid: Category 'Electronics' is not a valid enum value
- [+] date_format: Date '2026-01-27' is in correct format
- [-] category_match: Category 'Electronics' does not match expected 'gadget'
- [+] date_match: Date '2026-01-27' matches expected '2026-01-27'

### add_expense_cat_a / ambiguous_no_date: FAIL (0.50)

**Tool Calls**:

- `add_expense_cat_a`
  ```json
  {
  "expense_date": "2026-01-28",
  "amount": 50,
  "category": "Groceries",
  "description": "Groceries"
}
  ```

**Evaluations**:

- [+] tool_called: Tool 'add_expense_cat_a' was called
- [-] category_valid: Category 'Groceries' is not a valid enum value
- [+] date_format: Date '2026-01-28' is in correct format
- [-] category_match: Category 'Groceries' does not match expected 'food'

### add_expense_cat_a / ambiguous_vague_category: FAIL (0.00)

**No tool calls made**

**Evaluations**:

- [-] tool_called: No tool starting with 'add_expense' was called
- [-] category_valid: No add_expense tool call found
- [-] date_format: No add_expense tool call found
- [-] date_match: No add_expense tool call found

### add_expense_cat_a / ambiguous_relative_date: FAIL (0.00)

**No tool calls made**

**Evaluations**:

- [-] tool_called: No tool starting with 'add_expense' was called
- [-] category_valid: No add_expense tool call found
- [-] date_format: No add_expense tool call found
- [-] category_match: No add_expense tool call found

### add_expense_cat_a / ambiguous_mixed_items: FAIL (0.00)

**No tool calls made**

**Evaluations**:

- [-] tool_called: No tool starting with 'add_expense' was called
- [-] category_valid: No add_expense tool call found
- [-] date_format: No add_expense tool call found
- [-] date_match: No add_expense tool call found

### add_expense_cat_a / edge_future_date: FAIL (0.75)

**Tool Calls**:

- `add_expense_cat_a`
  ```json
  {
  "expense_date": "2026-01-29",
  "amount": 100,
  "category": "Hotel",
  "description": "Hotel"
}
  ```

**Evaluations**:

- [+] tool_called: Tool 'add_expense_cat_a' was called
- [-] category_valid: Category 'Hotel' is not a valid enum value
- [+] date_format: Date '2026-01-29' is in correct format
- [+] date_match: Date '2026-01-29' matches expected '2026-01-29'

### add_expense_cat_a / edge_large_amount: FAIL (0.60)

**Tool Calls**:

- `add_expense_cat_a`
  ```json
  {
  "expense_date": "2026-01-27",
  "amount": 35000,
  "category": "Car",
  "description": "Bought a car"
}
  ```

**Evaluations**:

- [+] tool_called: Tool 'add_expense_cat_a' was called
- [-] category_valid: Category 'Car' is not a valid enum value
- [+] date_format: Date '2026-01-27' is in correct format
- [-] category_match: Category 'Car' does not match expected 'other'
- [+] date_match: Date '2026-01-27' matches expected '2026-01-27'

### add_expense_cat_a / edge_small_amount: FAIL (0.60)

**Tool Calls**:

- `add_expense_cat_a`
  ```json
  {
  "expense_date": "2026-01-27",
  "amount": 0.99,
  "category": "Apps/Software",
  "description": "App purchase"
}
  ```

**Evaluations**:

- [+] tool_called: Tool 'add_expense_cat_a' was called
- [-] category_valid: Category 'Apps/Software' is not a valid enum value
- [+] date_format: Date '2026-01-27' is in correct format
- [-] category_match: Category 'Apps/Software' does not match expected 'gadget'
- [+] date_match: Date '2026-01-27' matches expected '2026-01-27'

### add_expense_cat_a / edge_unknown_category: FAIL (0.75)

**Tool Calls**:

- `add_expense_cat_a`
  ```json
  {
  "expense_date": "2026-01-27",
  "amount": 200,
  "category": "Spa",
  "description": "Spa treatment"
}
  ```

**Evaluations**:

- [+] tool_called: Tool 'add_expense_cat_a' was called
- [-] category_valid: Category 'Spa' is not a valid enum value
- [+] date_format: Date '2026-01-27' is in correct format
- [+] date_match: Date '2026-01-27' matches expected '2026-01-27'

### add_expense_cat_a / edge_currency_symbol: FAIL (0.60)

**Tool Calls**:

- `add_expense_cat_a`
  ```json
  {
  "expense_date": "2026-01-27",
  "amount": 50,
  "category": "Dinner",
  "description": "Dinner"
}
  ```

**Evaluations**:

- [+] tool_called: Tool 'add_expense_cat_a' was called
- [-] category_valid: Category 'Dinner' is not a valid enum value
- [+] date_format: Date '2026-01-27' is in correct format
- [-] category_match: Category 'Dinner' does not match expected 'food'
- [+] date_match: Date '2026-01-27' matches expected '2026-01-27'

### add_expense_cat_b / clear_food_yesterday: PASS (1.00)

**Tool Calls**:

- `add_expense_cat_b`
  ```json
  {
  "expense_date": "2026-01-27",
  "amount": 12.5,
  "category": "food",
  "description": "sandwich"
}
  ```

**Evaluations**:

- [+] tool_called: Tool 'add_expense_cat_b' was called
- [+] category_valid: Category 'food' is valid
- [+] date_format: Date '2026-01-27' is in correct format
- [+] category_match: Category 'food' matches expected 'food'
- [+] date_match: Date '2026-01-27' matches expected '2026-01-27'

### add_expense_cat_b / clear_transport_today: PASS (1.00)

**Tool Calls**:

- `add_expense_cat_b`
  ```json
  {
  "expense_date": "2026-01-28",
  "amount": 45,
  "category": "transport",
  "description": "Gas"
}
  ```

**Evaluations**:

- [+] tool_called: Tool 'add_expense_cat_b' was called
- [+] category_valid: Category 'transport' is valid
- [+] date_format: Date '2026-01-28' is in correct format
- [+] category_match: Category 'transport' matches expected 'transport'
- [+] date_match: Date '2026-01-28' matches expected '2026-01-28'

### add_expense_cat_b / clear_entertainment: PASS (1.00)

**Tool Calls**:

- `add_expense_cat_b`
  ```json
  {
  "expense_date": "2026-01-15",
  "amount": 25.99,
  "category": "entertainment",
  "description": "Movie ticket"
}
  ```

**Evaluations**:

- [+] tool_called: Tool 'add_expense_cat_b' was called
- [+] category_valid: Category 'entertainment' is valid
- [+] date_format: Date '2026-01-15' is in correct format
- [+] category_match: Category 'entertainment' matches expected 'entertainment'
- [+] date_match: Date '2026-01-15' matches expected '2026-01-15'

### add_expense_cat_b / clear_shopping: PASS (1.00)

**Tool Calls**:

- `add_expense_cat_b`
  ```json
  {
  "expense_date": "2026-01-20",
  "amount": 125,
  "category": "shopping",
  "description": "New shoes"
}
  ```

**Evaluations**:

- [+] tool_called: Tool 'add_expense_cat_b' was called
- [+] category_valid: Category 'shopping' is valid
- [+] date_format: Date '2026-01-20' is in correct format
- [+] category_match: Category 'shopping' matches expected 'shopping'
- [+] date_match: Date '2026-01-20' matches expected '2026-01-20'

### add_expense_cat_b / clear_gadget: PASS (1.00)

**Tool Calls**:

- `add_expense_cat_b`
  ```json
  {
  "expense_date": "2026-01-27",
  "amount": 1200,
  "category": "gadget",
  "description": "Laptop purchase"
}
  ```

**Evaluations**:

- [+] tool_called: Tool 'add_expense_cat_b' was called
- [+] category_valid: Category 'gadget' is valid
- [+] date_format: Date '2026-01-27' is in correct format
- [+] category_match: Category 'gadget' matches expected 'gadget'
- [+] date_match: Date '2026-01-27' matches expected '2026-01-27'

### add_expense_cat_b / ambiguous_no_date: FAIL (0.00)

**No tool calls made**

**Evaluations**:

- [-] tool_called: No tool starting with 'add_expense' was called
- [-] category_valid: No add_expense tool call found
- [-] date_format: No add_expense tool call found
- [-] category_match: No add_expense tool call found

### add_expense_cat_b / ambiguous_vague_category: FAIL (0.00)

**No tool calls made**

**Evaluations**:

- [-] tool_called: No tool starting with 'add_expense' was called
- [-] category_valid: No add_expense tool call found
- [-] date_format: No add_expense tool call found
- [-] date_match: No add_expense tool call found

### add_expense_cat_b / ambiguous_relative_date: FAIL (0.00)

**No tool calls made**

**Evaluations**:

- [-] tool_called: No tool starting with 'add_expense' was called
- [-] category_valid: No add_expense tool call found
- [-] date_format: No add_expense tool call found
- [-] category_match: No add_expense tool call found

### add_expense_cat_b / ambiguous_mixed_items: PASS (1.00)

**Tool Calls**:

- `add_expense_cat_b`
  ```json
  {
  "expense_date": "2026-01-27",
  "amount": 55,
  "category": "shopping",
  "description": "Coffee and phone case"
}
  ```

**Evaluations**:

- [+] tool_called: Tool 'add_expense_cat_b' was called
- [+] category_valid: Category 'shopping' is valid
- [+] date_format: Date '2026-01-27' is in correct format
- [+] date_match: Date '2026-01-27' matches expected '2026-01-27'

### add_expense_cat_b / edge_future_date: PASS (1.00)

**Tool Calls**:

- `add_expense_cat_b`
  ```json
  {
  "expense_date": "2026-01-29",
  "amount": 100,
  "category": "other",
  "description": "Hotel"
}
  ```

**Evaluations**:

- [+] tool_called: Tool 'add_expense_cat_b' was called
- [+] category_valid: Category 'other' is valid
- [+] date_format: Date '2026-01-29' is in correct format
- [+] date_match: Date '2026-01-29' matches expected '2026-01-29'

### add_expense_cat_b / edge_large_amount: PASS (0.80)

**Tool Calls**:

- `add_expense_cat_b`
  ```json
  {
  "expense_date": "2026-01-27",
  "amount": 35000,
  "category": "transport",
  "description": "Bought a car"
}
  ```

**Evaluations**:

- [+] tool_called: Tool 'add_expense_cat_b' was called
- [+] category_valid: Category 'transport' is valid
- [+] date_format: Date '2026-01-27' is in correct format
- [-] category_match: Category 'transport' does not match expected 'other'
- [+] date_match: Date '2026-01-27' matches expected '2026-01-27'

### add_expense_cat_b / edge_small_amount: PASS (1.00)

**Tool Calls**:

- `add_expense_cat_b`
  ```json
  {
  "expense_date": "2026-01-27",
  "amount": 0.99,
  "category": "gadget",
  "description": "App purchase"
}
  ```

**Evaluations**:

- [+] tool_called: Tool 'add_expense_cat_b' was called
- [+] category_valid: Category 'gadget' is valid
- [+] date_format: Date '2026-01-27' is in correct format
- [+] category_match: Category 'gadget' matches expected 'gadget'
- [+] date_match: Date '2026-01-27' matches expected '2026-01-27'

### add_expense_cat_b / edge_unknown_category: PASS (1.00)

**Tool Calls**:

- `add_expense_cat_b`
  ```json
  {
  "expense_date": "2026-01-27",
  "amount": 200,
  "category": "entertainment",
  "description": "Spa treatment"
}
  ```

**Evaluations**:

- [+] tool_called: Tool 'add_expense_cat_b' was called
- [+] category_valid: Category 'entertainment' is valid
- [+] date_format: Date '2026-01-27' is in correct format
- [+] date_match: Date '2026-01-27' matches expected '2026-01-27'

### add_expense_cat_b / edge_currency_symbol: PASS (1.00)

**Tool Calls**:

- `add_expense_cat_b`
  ```json
  {
  "expense_date": "2026-01-27",
  "amount": 50,
  "category": "food",
  "description": "Dinner"
}
  ```

**Evaluations**:

- [+] tool_called: Tool 'add_expense_cat_b' was called
- [+] category_valid: Category 'food' is valid
- [+] date_format: Date '2026-01-27' is in correct format
- [+] category_match: Category 'food' matches expected 'food'
- [+] date_match: Date '2026-01-27' matches expected '2026-01-27'

### add_expense_cat_c / clear_food_yesterday: PASS (1.00)

**Tool Calls**:

- `add_expense_cat_c`
  ```json
  {
  "expense_date": "2026-01-27",
  "amount": 12.5,
  "category": "food",
  "description": "Sandwich"
}
  ```

**Evaluations**:

- [+] tool_called: Tool 'add_expense_cat_c' was called
- [+] category_valid: Category 'food' is valid
- [+] date_format: Date '2026-01-27' is in correct format
- [+] category_match: Category 'food' matches expected 'food'
- [+] date_match: Date '2026-01-27' matches expected '2026-01-27'

### add_expense_cat_c / clear_transport_today: PASS (1.00)

**Tool Calls**:

- `add_expense_cat_c`
  ```json
  {
  "expense_date": "2026-01-28",
  "amount": 45,
  "category": "transport",
  "description": "Gas"
}
  ```

**Evaluations**:

- [+] tool_called: Tool 'add_expense_cat_c' was called
- [+] category_valid: Category 'transport' is valid
- [+] date_format: Date '2026-01-28' is in correct format
- [+] category_match: Category 'transport' matches expected 'transport'
- [+] date_match: Date '2026-01-28' matches expected '2026-01-28'

### add_expense_cat_c / clear_entertainment: PASS (1.00)

**Tool Calls**:

- `add_expense_cat_c`
  ```json
  {
  "expense_date": "2026-01-15",
  "amount": 25.99,
  "category": "entertainment",
  "description": "Movie ticket"
}
  ```

**Evaluations**:

- [+] tool_called: Tool 'add_expense_cat_c' was called
- [+] category_valid: Category 'entertainment' is valid
- [+] date_format: Date '2026-01-15' is in correct format
- [+] category_match: Category 'entertainment' matches expected 'entertainment'
- [+] date_match: Date '2026-01-15' matches expected '2026-01-15'

### add_expense_cat_c / clear_shopping: PASS (1.00)

**Tool Calls**:

- `add_expense_cat_c`
  ```json
  {
  "expense_date": "2026-01-20",
  "amount": 125,
  "category": "shopping",
  "description": "New shoes"
}
  ```

**Evaluations**:

- [+] tool_called: Tool 'add_expense_cat_c' was called
- [+] category_valid: Category 'shopping' is valid
- [+] date_format: Date '2026-01-20' is in correct format
- [+] category_match: Category 'shopping' matches expected 'shopping'
- [+] date_match: Date '2026-01-20' matches expected '2026-01-20'

### add_expense_cat_c / clear_gadget: PASS (1.00)

**Tool Calls**:

- `add_expense_cat_c`
  ```json
  {
  "expense_date": "2026-01-27",
  "amount": 1200,
  "category": "gadget",
  "description": "Laptop purchase"
}
  ```

**Evaluations**:

- [+] tool_called: Tool 'add_expense_cat_c' was called
- [+] category_valid: Category 'gadget' is valid
- [+] date_format: Date '2026-01-27' is in correct format
- [+] category_match: Category 'gadget' matches expected 'gadget'
- [+] date_match: Date '2026-01-27' matches expected '2026-01-27'

### add_expense_cat_c / ambiguous_no_date: PASS (1.00)

**Tool Calls**:

- `add_expense_cat_c`
  ```json
  {
  "expense_date": "2026-01-28",
  "amount": 50,
  "category": "food",
  "description": "groceries"
}
  ```

**Evaluations**:

- [+] tool_called: Tool 'add_expense_cat_c' was called
- [+] category_valid: Category 'food' is valid
- [+] date_format: Date '2026-01-28' is in correct format
- [+] category_match: Category 'food' matches expected 'food'

### add_expense_cat_c / ambiguous_vague_category: FAIL (0.00)

**No tool calls made**

**Evaluations**:

- [-] tool_called: No tool starting with 'add_expense' was called
- [-] category_valid: No add_expense tool call found
- [-] date_format: No add_expense tool call found
- [-] date_match: No add_expense tool call found

### add_expense_cat_c / ambiguous_relative_date: FAIL (0.00)

**No tool calls made**

**Evaluations**:

- [-] tool_called: No tool starting with 'add_expense' was called
- [-] category_valid: No add_expense tool call found
- [-] date_format: No add_expense tool call found
- [-] category_match: No add_expense tool call found

### add_expense_cat_c / ambiguous_mixed_items: PASS (1.00)

**Tool Calls**:

- `add_expense_cat_c`
  ```json
  {
  "expense_date": "2026-01-27",
  "amount": 55,
  "category": "shopping",
  "description": "Coffee and phone case"
}
  ```

**Evaluations**:

- [+] tool_called: Tool 'add_expense_cat_c' was called
- [+] category_valid: Category 'shopping' is valid
- [+] date_format: Date '2026-01-27' is in correct format
- [+] date_match: Date '2026-01-27' matches expected '2026-01-27'

### add_expense_cat_c / edge_future_date: PASS (1.00)

**Tool Calls**:

- `add_expense_cat_c`
  ```json
  {
  "expense_date": "2026-01-29",
  "amount": 100,
  "category": "other",
  "description": "Hotel"
}
  ```

**Evaluations**:

- [+] tool_called: Tool 'add_expense_cat_c' was called
- [+] category_valid: Category 'other' is valid
- [+] date_format: Date '2026-01-29' is in correct format
- [+] date_match: Date '2026-01-29' matches expected '2026-01-29'

### add_expense_cat_c / edge_large_amount: PASS (1.00)

**Tool Calls**:

- `add_expense_cat_c`
  ```json
  {
  "expense_date": "2026-01-27",
  "amount": 35000,
  "category": "other",
  "description": "Bought a car"
}
  ```

**Evaluations**:

- [+] tool_called: Tool 'add_expense_cat_c' was called
- [+] category_valid: Category 'other' is valid
- [+] date_format: Date '2026-01-27' is in correct format
- [+] category_match: Category 'other' matches expected 'other'
- [+] date_match: Date '2026-01-27' matches expected '2026-01-27'

### add_expense_cat_c / edge_small_amount: PASS (1.00)

**Tool Calls**:

- `add_expense_cat_c`
  ```json
  {
  "expense_date": "2026-01-27",
  "amount": 0.99,
  "category": "gadget",
  "description": "App purchase"
}
  ```

**Evaluations**:

- [+] tool_called: Tool 'add_expense_cat_c' was called
- [+] category_valid: Category 'gadget' is valid
- [+] date_format: Date '2026-01-27' is in correct format
- [+] category_match: Category 'gadget' matches expected 'gadget'
- [+] date_match: Date '2026-01-27' matches expected '2026-01-27'

### add_expense_cat_c / edge_unknown_category: PASS (1.00)

**Tool Calls**:

- `add_expense_cat_c`
  ```json
  {
  "expense_date": "2026-01-27",
  "amount": 200,
  "category": "entertainment",
  "description": "Spa treatment"
}
  ```

**Evaluations**:

- [+] tool_called: Tool 'add_expense_cat_c' was called
- [+] category_valid: Category 'entertainment' is valid
- [+] date_format: Date '2026-01-27' is in correct format
- [+] date_match: Date '2026-01-27' matches expected '2026-01-27'

### add_expense_cat_c / edge_currency_symbol: PASS (1.00)

**Tool Calls**:

- `add_expense_cat_c`
  ```json
  {
  "expense_date": "2026-01-27",
  "amount": 50,
  "category": "food",
  "description": "Dinner"
}
  ```

**Evaluations**:

- [+] tool_called: Tool 'add_expense_cat_c' was called
- [+] category_valid: Category 'food' is valid
- [+] date_format: Date '2026-01-27' is in correct format
- [+] category_match: Category 'food' matches expected 'food'
- [+] date_match: Date '2026-01-27' matches expected '2026-01-27'

### add_expense_cat_d / clear_food_yesterday: PASS (1.00)

**Tool Calls**:

- `add_expense_cat_d`
  ```json
  {
  "expense_date": "2026-01-27",
  "amount": 12.5,
  "category": "food",
  "description": "Sandwich"
}
  ```

**Evaluations**:

- [+] tool_called: Tool 'add_expense_cat_d' was called
- [+] category_valid: Category 'food' is valid
- [+] date_format: Date '2026-01-27' is in correct format
- [+] category_match: Category 'food' matches expected 'food'
- [+] date_match: Date '2026-01-27' matches expected '2026-01-27'

### add_expense_cat_d / clear_transport_today: PASS (1.00)

**Tool Calls**:

- `add_expense_cat_d`
  ```json
  {
  "expense_date": "2026-01-28",
  "amount": 45,
  "category": "transport",
  "description": "Gas"
}
  ```

**Evaluations**:

- [+] tool_called: Tool 'add_expense_cat_d' was called
- [+] category_valid: Category 'transport' is valid
- [+] date_format: Date '2026-01-28' is in correct format
- [+] category_match: Category 'transport' matches expected 'transport'
- [+] date_match: Date '2026-01-28' matches expected '2026-01-28'

### add_expense_cat_d / clear_entertainment: PASS (1.00)

**Tool Calls**:

- `add_expense_cat_d`
  ```json
  {
  "expense_date": "2026-01-15",
  "amount": 25.99,
  "category": "entertainment",
  "description": "Movie ticket"
}
  ```

**Evaluations**:

- [+] tool_called: Tool 'add_expense_cat_d' was called
- [+] category_valid: Category 'entertainment' is valid
- [+] date_format: Date '2026-01-15' is in correct format
- [+] category_match: Category 'entertainment' matches expected 'entertainment'
- [+] date_match: Date '2026-01-15' matches expected '2026-01-15'

### add_expense_cat_d / clear_shopping: PASS (1.00)

**Tool Calls**:

- `add_expense_cat_d`
  ```json
  {
  "expense_date": "2026-01-20",
  "amount": 125,
  "category": "shopping",
  "description": "New shoes"
}
  ```

**Evaluations**:

- [+] tool_called: Tool 'add_expense_cat_d' was called
- [+] category_valid: Category 'shopping' is valid
- [+] date_format: Date '2026-01-20' is in correct format
- [+] category_match: Category 'shopping' matches expected 'shopping'
- [+] date_match: Date '2026-01-20' matches expected '2026-01-20'

### add_expense_cat_d / clear_gadget: PASS (1.00)

**Tool Calls**:

- `add_expense_cat_d`
  ```json
  {
  "expense_date": "2026-01-27",
  "amount": 1200,
  "category": "gadget",
  "description": "Laptop purchase"
}
  ```

**Evaluations**:

- [+] tool_called: Tool 'add_expense_cat_d' was called
- [+] category_valid: Category 'gadget' is valid
- [+] date_format: Date '2026-01-27' is in correct format
- [+] category_match: Category 'gadget' matches expected 'gadget'
- [+] date_match: Date '2026-01-27' matches expected '2026-01-27'

### add_expense_cat_d / ambiguous_no_date: PASS (1.00)

**Tool Calls**:

- `add_expense_cat_d`
  ```json
  {
  "expense_date": "2026-01-28",
  "amount": 50,
  "category": "food",
  "description": "groceries"
}
  ```

**Evaluations**:

- [+] tool_called: Tool 'add_expense_cat_d' was called
- [+] category_valid: Category 'food' is valid
- [+] date_format: Date '2026-01-28' is in correct format
- [+] category_match: Category 'food' matches expected 'food'

### add_expense_cat_d / ambiguous_vague_category: FAIL (0.00)

**No tool calls made**

**Evaluations**:

- [-] tool_called: No tool starting with 'add_expense' was called
- [-] category_valid: No add_expense tool call found
- [-] date_format: No add_expense tool call found
- [-] date_match: No add_expense tool call found

### add_expense_cat_d / ambiguous_relative_date: FAIL (0.00)

**No tool calls made**

**Evaluations**:

- [-] tool_called: No tool starting with 'add_expense' was called
- [-] category_valid: No add_expense tool call found
- [-] date_format: No add_expense tool call found
- [-] category_match: No add_expense tool call found

### add_expense_cat_d / ambiguous_mixed_items: PASS (1.00)

**Tool Calls**:

- `add_expense_cat_d`
  ```json
  {
  "expense_date": "2026-01-27",
  "amount": 55,
  "category": "shopping",
  "description": "Coffee and phone case"
}
  ```

**Evaluations**:

- [+] tool_called: Tool 'add_expense_cat_d' was called
- [+] category_valid: Category 'shopping' is valid
- [+] date_format: Date '2026-01-27' is in correct format
- [+] date_match: Date '2026-01-27' matches expected '2026-01-27'

### add_expense_cat_d / edge_future_date: PASS (1.00)

**Tool Calls**:

- `add_expense_cat_d`
  ```json
  {
  "expense_date": "2026-01-29",
  "amount": 100,
  "category": "other",
  "description": "Hotel"
}
  ```

**Evaluations**:

- [+] tool_called: Tool 'add_expense_cat_d' was called
- [+] category_valid: Category 'other' is valid
- [+] date_format: Date '2026-01-29' is in correct format
- [+] date_match: Date '2026-01-29' matches expected '2026-01-29'

### add_expense_cat_d / edge_large_amount: PASS (1.00)

**Tool Calls**:

- `add_expense_cat_d`
  ```json
  {
  "expense_date": "2026-01-27",
  "amount": 35000,
  "category": "other",
  "description": "Bought a car"
}
  ```

**Evaluations**:

- [+] tool_called: Tool 'add_expense_cat_d' was called
- [+] category_valid: Category 'other' is valid
- [+] date_format: Date '2026-01-27' is in correct format
- [+] category_match: Category 'other' matches expected 'other'
- [+] date_match: Date '2026-01-27' matches expected '2026-01-27'

### add_expense_cat_d / edge_small_amount: PASS (1.00)

**Tool Calls**:

- `add_expense_cat_d`
  ```json
  {
  "expense_date": "2026-01-27",
  "amount": 0.99,
  "category": "gadget",
  "description": "App purchase"
}
  ```

**Evaluations**:

- [+] tool_called: Tool 'add_expense_cat_d' was called
- [+] category_valid: Category 'gadget' is valid
- [+] date_format: Date '2026-01-27' is in correct format
- [+] category_match: Category 'gadget' matches expected 'gadget'
- [+] date_match: Date '2026-01-27' matches expected '2026-01-27'

### add_expense_cat_d / edge_unknown_category: PASS (1.00)

**Tool Calls**:

- `add_expense_cat_d`
  ```json
  {
  "expense_date": "2026-01-27",
  "amount": 200,
  "category": "entertainment",
  "description": "Spa treatment"
}
  ```

**Evaluations**:

- [+] tool_called: Tool 'add_expense_cat_d' was called
- [+] category_valid: Category 'entertainment' is valid
- [+] date_format: Date '2026-01-27' is in correct format
- [+] date_match: Date '2026-01-27' matches expected '2026-01-27'

### add_expense_cat_d / edge_currency_symbol: PASS (1.00)

**Tool Calls**:

- `add_expense_cat_d`
  ```json
  {
  "expense_date": "2026-01-27",
  "amount": 50,
  "category": "food",
  "description": "Dinner"
}
  ```

**Evaluations**:

- [+] tool_called: Tool 'add_expense_cat_d' was called
- [+] category_valid: Category 'food' is valid
- [+] date_format: Date '2026-01-27' is in correct format
- [+] category_match: Category 'food' matches expected 'food'
- [+] date_match: Date '2026-01-27' matches expected '2026-01-27'

### add_expense_date_a / clear_food_yesterday: PASS (1.00)

**Tool Calls**:

- `add_expense_date_a`
  ```json
  {
  "expense_date": "2026-01-27",
  "amount": 12.5,
  "category": "food",
  "description": "Sandwich"
}
  ```

**Evaluations**:

- [+] tool_called: Tool 'add_expense_date_a' was called
- [+] category_valid: Category 'food' is valid
- [+] date_format: Date '2026-01-27' is in correct format
- [+] category_match: Category 'food' matches expected 'food'
- [+] date_match: Date '2026-01-27' matches expected '2026-01-27'

### add_expense_date_a / clear_transport_today: PASS (1.00)

**Tool Calls**:

- `add_expense_date_a`
  ```json
  {
  "expense_date": "2026-01-28",
  "amount": 45,
  "category": "transport",
  "description": "Gas"
}
  ```

**Evaluations**:

- [+] tool_called: Tool 'add_expense_date_a' was called
- [+] category_valid: Category 'transport' is valid
- [+] date_format: Date '2026-01-28' is in correct format
- [+] category_match: Category 'transport' matches expected 'transport'
- [+] date_match: Date '2026-01-28' matches expected '2026-01-28'

### add_expense_date_a / clear_entertainment: PASS (1.00)

**Tool Calls**:

- `add_expense_date_a`
  ```json
  {
  "expense_date": "2026-01-15",
  "amount": 25.99,
  "category": "entertainment",
  "description": "Movie ticket"
}
  ```

**Evaluations**:

- [+] tool_called: Tool 'add_expense_date_a' was called
- [+] category_valid: Category 'entertainment' is valid
- [+] date_format: Date '2026-01-15' is in correct format
- [+] category_match: Category 'entertainment' matches expected 'entertainment'
- [+] date_match: Date '2026-01-15' matches expected '2026-01-15'

### add_expense_date_a / clear_shopping: PASS (1.00)

**Tool Calls**:

- `add_expense_date_a`
  ```json
  {
  "expense_date": "2026-01-20",
  "amount": 125,
  "category": "shopping",
  "description": "New shoes"
}
  ```

**Evaluations**:

- [+] tool_called: Tool 'add_expense_date_a' was called
- [+] category_valid: Category 'shopping' is valid
- [+] date_format: Date '2026-01-20' is in correct format
- [+] category_match: Category 'shopping' matches expected 'shopping'
- [+] date_match: Date '2026-01-20' matches expected '2026-01-20'

### add_expense_date_a / clear_gadget: PASS (1.00)

**Tool Calls**:

- `add_expense_date_a`
  ```json
  {
  "expense_date": "2026-01-27",
  "amount": 1200,
  "category": "gadget",
  "description": "Laptop purchase"
}
  ```

**Evaluations**:

- [+] tool_called: Tool 'add_expense_date_a' was called
- [+] category_valid: Category 'gadget' is valid
- [+] date_format: Date '2026-01-27' is in correct format
- [+] category_match: Category 'gadget' matches expected 'gadget'
- [+] date_match: Date '2026-01-27' matches expected '2026-01-27'

### add_expense_date_a / ambiguous_no_date: FAIL (0.00)

**No tool calls made**

**Evaluations**:

- [-] tool_called: No tool starting with 'add_expense' was called
- [-] category_valid: No add_expense tool call found
- [-] date_format: No add_expense tool call found
- [-] category_match: No add_expense tool call found

### add_expense_date_a / ambiguous_vague_category: FAIL (0.00)

**No tool calls made**

**Evaluations**:

- [-] tool_called: No tool starting with 'add_expense' was called
- [-] category_valid: No add_expense tool call found
- [-] date_format: No add_expense tool call found
- [-] date_match: No add_expense tool call found

### add_expense_date_a / ambiguous_relative_date: FAIL (0.00)

**No tool calls made**

**Evaluations**:

- [-] tool_called: No tool starting with 'add_expense' was called
- [-] category_valid: No add_expense tool call found
- [-] date_format: No add_expense tool call found
- [-] category_match: No add_expense tool call found

### add_expense_date_a / ambiguous_mixed_items: PASS (1.00)

**Tool Calls**:

- `add_expense_date_a`
  ```json
  {
  "expense_date": "2026-01-27",
  "amount": 55,
  "category": "shopping",
  "description": "Coffee and phone case"
}
  ```

**Evaluations**:

- [+] tool_called: Tool 'add_expense_date_a' was called
- [+] category_valid: Category 'shopping' is valid
- [+] date_format: Date '2026-01-27' is in correct format
- [+] date_match: Date '2026-01-27' matches expected '2026-01-27'

### add_expense_date_a / edge_future_date: PASS (1.00)

**Tool Calls**:

- `add_expense_date_a`
  ```json
  {
  "expense_date": "2026-01-29",
  "amount": 100,
  "category": "other",
  "description": "Hotel"
}
  ```

**Evaluations**:

- [+] tool_called: Tool 'add_expense_date_a' was called
- [+] category_valid: Category 'other' is valid
- [+] date_format: Date '2026-01-29' is in correct format
- [+] date_match: Date '2026-01-29' matches expected '2026-01-29'

### add_expense_date_a / edge_large_amount: PASS (0.80)

**Tool Calls**:

- `add_expense_date_a`
  ```json
  {
  "expense_date": "2026-01-27",
  "amount": 35000,
  "category": "transport",
  "description": "Bought a car"
}
  ```

**Evaluations**:

- [+] tool_called: Tool 'add_expense_date_a' was called
- [+] category_valid: Category 'transport' is valid
- [+] date_format: Date '2026-01-27' is in correct format
- [-] category_match: Category 'transport' does not match expected 'other'
- [+] date_match: Date '2026-01-27' matches expected '2026-01-27'

### add_expense_date_a / edge_small_amount: PASS (1.00)

**Tool Calls**:

- `add_expense_date_a`
  ```json
  {
  "expense_date": "2026-01-27",
  "amount": 0.99,
  "category": "gadget",
  "description": "App purchase"
}
  ```

**Evaluations**:

- [+] tool_called: Tool 'add_expense_date_a' was called
- [+] category_valid: Category 'gadget' is valid
- [+] date_format: Date '2026-01-27' is in correct format
- [+] category_match: Category 'gadget' matches expected 'gadget'
- [+] date_match: Date '2026-01-27' matches expected '2026-01-27'

### add_expense_date_a / edge_unknown_category: PASS (1.00)

**Tool Calls**:

- `add_expense_date_a`
  ```json
  {
  "expense_date": "2026-01-27",
  "amount": 200,
  "category": "entertainment",
  "description": "Spa treatment"
}
  ```

**Evaluations**:

- [+] tool_called: Tool 'add_expense_date_a' was called
- [+] category_valid: Category 'entertainment' is valid
- [+] date_format: Date '2026-01-27' is in correct format
- [+] date_match: Date '2026-01-27' matches expected '2026-01-27'

### add_expense_date_a / edge_currency_symbol: PASS (1.00)

**Tool Calls**:

- `add_expense_date_a`
  ```json
  {
  "expense_date": "2026-01-27",
  "amount": 50,
  "category": "food",
  "description": "Dinner"
}
  ```

**Evaluations**:

- [+] tool_called: Tool 'add_expense_date_a' was called
- [+] category_valid: Category 'food' is valid
- [+] date_format: Date '2026-01-27' is in correct format
- [+] category_match: Category 'food' matches expected 'food'
- [+] date_match: Date '2026-01-27' matches expected '2026-01-27'

### add_expense_date_b / clear_food_yesterday: PASS (1.00)

**Tool Calls**:

- `add_expense_date_b`
  ```json
  {
  "expense_date": "2026-01-27",
  "amount": 12.5,
  "category": "food",
  "description": "Sandwich"
}
  ```

**Evaluations**:

- [+] tool_called: Tool 'add_expense_date_b' was called
- [+] category_valid: Category 'food' is valid
- [+] date_format: Date '2026-01-27' is in correct format
- [+] category_match: Category 'food' matches expected 'food'
- [+] date_match: Date '2026-01-27' matches expected '2026-01-27'

### add_expense_date_b / clear_transport_today: PASS (1.00)

**Tool Calls**:

- `add_expense_date_b`
  ```json
  {
  "expense_date": "2026-01-28",
  "amount": 45,
  "category": "transport",
  "description": "Gas"
}
  ```

**Evaluations**:

- [+] tool_called: Tool 'add_expense_date_b' was called
- [+] category_valid: Category 'transport' is valid
- [+] date_format: Date '2026-01-28' is in correct format
- [+] category_match: Category 'transport' matches expected 'transport'
- [+] date_match: Date '2026-01-28' matches expected '2026-01-28'

### add_expense_date_b / clear_entertainment: PASS (1.00)

**Tool Calls**:

- `add_expense_date_b`
  ```json
  {
  "expense_date": "2026-01-15",
  "amount": 25.99,
  "category": "entertainment",
  "description": "Movie ticket"
}
  ```

**Evaluations**:

- [+] tool_called: Tool 'add_expense_date_b' was called
- [+] category_valid: Category 'entertainment' is valid
- [+] date_format: Date '2026-01-15' is in correct format
- [+] category_match: Category 'entertainment' matches expected 'entertainment'
- [+] date_match: Date '2026-01-15' matches expected '2026-01-15'

### add_expense_date_b / clear_shopping: PASS (1.00)

**Tool Calls**:

- `add_expense_date_b`
  ```json
  {
  "expense_date": "2026-01-20",
  "amount": 125,
  "category": "shopping",
  "description": "New shoes"
}
  ```

**Evaluations**:

- [+] tool_called: Tool 'add_expense_date_b' was called
- [+] category_valid: Category 'shopping' is valid
- [+] date_format: Date '2026-01-20' is in correct format
- [+] category_match: Category 'shopping' matches expected 'shopping'
- [+] date_match: Date '2026-01-20' matches expected '2026-01-20'

### add_expense_date_b / clear_gadget: PASS (1.00)

**Tool Calls**:

- `add_expense_date_b`
  ```json
  {
  "expense_date": "2026-01-27",
  "amount": 1200,
  "category": "gadget",
  "description": "Laptop purchase"
}
  ```

**Evaluations**:

- [+] tool_called: Tool 'add_expense_date_b' was called
- [+] category_valid: Category 'gadget' is valid
- [+] date_format: Date '2026-01-27' is in correct format
- [+] category_match: Category 'gadget' matches expected 'gadget'
- [+] date_match: Date '2026-01-27' matches expected '2026-01-27'

### add_expense_date_b / ambiguous_no_date: FAIL (0.00)

**No tool calls made**

**Evaluations**:

- [-] tool_called: No tool starting with 'add_expense' was called
- [-] category_valid: No add_expense tool call found
- [-] date_format: No add_expense tool call found
- [-] category_match: No add_expense tool call found

### add_expense_date_b / ambiguous_vague_category: FAIL (0.00)

**No tool calls made**

**Evaluations**:

- [-] tool_called: No tool starting with 'add_expense' was called
- [-] category_valid: No add_expense tool call found
- [-] date_format: No add_expense tool call found
- [-] date_match: No add_expense tool call found

### add_expense_date_b / ambiguous_relative_date: FAIL (0.00)

**No tool calls made**

**Evaluations**:

- [-] tool_called: No tool starting with 'add_expense' was called
- [-] category_valid: No add_expense tool call found
- [-] date_format: No add_expense tool call found
- [-] category_match: No add_expense tool call found

### add_expense_date_b / ambiguous_mixed_items: PASS (1.00)

**Tool Calls**:

- `add_expense_date_b`
  ```json
  {
  "expense_date": "2026-01-27",
  "amount": 55,
  "category": "food",
  "description": "Coffee and phone case"
}
  ```

**Evaluations**:

- [+] tool_called: Tool 'add_expense_date_b' was called
- [+] category_valid: Category 'food' is valid
- [+] date_format: Date '2026-01-27' is in correct format
- [+] date_match: Date '2026-01-27' matches expected '2026-01-27'

### add_expense_date_b / edge_future_date: PASS (1.00)

**Tool Calls**:

- `add_expense_date_b`
  ```json
  {
  "expense_date": "2026-01-29",
  "amount": 100,
  "category": "other",
  "description": "Hotel"
}
  ```

**Evaluations**:

- [+] tool_called: Tool 'add_expense_date_b' was called
- [+] category_valid: Category 'other' is valid
- [+] date_format: Date '2026-01-29' is in correct format
- [+] date_match: Date '2026-01-29' matches expected '2026-01-29'

### add_expense_date_b / edge_large_amount: PASS (1.00)

**Tool Calls**:

- `add_expense_date_b`
  ```json
  {
  "expense_date": "2026-01-27",
  "amount": 35000,
  "category": "other",
  "description": "Bought a car"
}
  ```

**Evaluations**:

- [+] tool_called: Tool 'add_expense_date_b' was called
- [+] category_valid: Category 'other' is valid
- [+] date_format: Date '2026-01-27' is in correct format
- [+] category_match: Category 'other' matches expected 'other'
- [+] date_match: Date '2026-01-27' matches expected '2026-01-27'

### add_expense_date_b / edge_small_amount: PASS (1.00)

**Tool Calls**:

- `add_expense_date_b`
  ```json
  {
  "expense_date": "2026-01-27",
  "amount": 0.99,
  "category": "gadget",
  "description": "App purchase"
}
  ```

**Evaluations**:

- [+] tool_called: Tool 'add_expense_date_b' was called
- [+] category_valid: Category 'gadget' is valid
- [+] date_format: Date '2026-01-27' is in correct format
- [+] category_match: Category 'gadget' matches expected 'gadget'
- [+] date_match: Date '2026-01-27' matches expected '2026-01-27'

### add_expense_date_b / edge_unknown_category: PASS (1.00)

**Tool Calls**:

- `add_expense_date_b`
  ```json
  {
  "expense_date": "2026-01-27",
  "amount": 200,
  "category": "entertainment",
  "description": "Spa treatment"
}
  ```

**Evaluations**:

- [+] tool_called: Tool 'add_expense_date_b' was called
- [+] category_valid: Category 'entertainment' is valid
- [+] date_format: Date '2026-01-27' is in correct format
- [+] date_match: Date '2026-01-27' matches expected '2026-01-27'

### add_expense_date_b / edge_currency_symbol: PASS (1.00)

**Tool Calls**:

- `add_expense_date_b`
  ```json
  {
  "expense_date": "2026-01-27",
  "amount": 50,
  "category": "food",
  "description": "Dinner"
}
  ```

**Evaluations**:

- [+] tool_called: Tool 'add_expense_date_b' was called
- [+] category_valid: Category 'food' is valid
- [+] date_format: Date '2026-01-27' is in correct format
- [+] category_match: Category 'food' matches expected 'food'
- [+] date_match: Date '2026-01-27' matches expected '2026-01-27'

### add_expense_date_c / clear_food_yesterday: PASS (1.00)

**Tool Calls**:

- `add_expense_date_c`
  ```json
  {
  "expense_date": "2026-01-27",
  "amount": 12.5,
  "category": "food",
  "description": "Sandwich"
}
  ```

**Evaluations**:

- [+] tool_called: Tool 'add_expense_date_c' was called
- [+] category_valid: Category 'food' is valid
- [+] date_format: Date '2026-01-27' is in correct format
- [+] category_match: Category 'food' matches expected 'food'
- [+] date_match: Date '2026-01-27' matches expected '2026-01-27'

### add_expense_date_c / clear_transport_today: PASS (1.00)

**Tool Calls**:

- `add_expense_date_c`
  ```json
  {
  "expense_date": "2026-01-28",
  "amount": 45,
  "category": "transport",
  "description": "Gas"
}
  ```

**Evaluations**:

- [+] tool_called: Tool 'add_expense_date_c' was called
- [+] category_valid: Category 'transport' is valid
- [+] date_format: Date '2026-01-28' is in correct format
- [+] category_match: Category 'transport' matches expected 'transport'
- [+] date_match: Date '2026-01-28' matches expected '2026-01-28'

### add_expense_date_c / clear_entertainment: PASS (1.00)

**Tool Calls**:

- `add_expense_date_c`
  ```json
  {
  "expense_date": "2026-01-15",
  "amount": 25.99,
  "category": "entertainment",
  "description": "Movie ticket"
}
  ```

**Evaluations**:

- [+] tool_called: Tool 'add_expense_date_c' was called
- [+] category_valid: Category 'entertainment' is valid
- [+] date_format: Date '2026-01-15' is in correct format
- [+] category_match: Category 'entertainment' matches expected 'entertainment'
- [+] date_match: Date '2026-01-15' matches expected '2026-01-15'

### add_expense_date_c / clear_shopping: PASS (1.00)

**Tool Calls**:

- `add_expense_date_c`
  ```json
  {
  "expense_date": "2026-01-20",
  "amount": 125,
  "category": "shopping",
  "description": "New shoes"
}
  ```

**Evaluations**:

- [+] tool_called: Tool 'add_expense_date_c' was called
- [+] category_valid: Category 'shopping' is valid
- [+] date_format: Date '2026-01-20' is in correct format
- [+] category_match: Category 'shopping' matches expected 'shopping'
- [+] date_match: Date '2026-01-20' matches expected '2026-01-20'

### add_expense_date_c / clear_gadget: PASS (1.00)

**Tool Calls**:

- `add_expense_date_c`
  ```json
  {
  "expense_date": "2026-01-27",
  "amount": 1200,
  "category": "gadget",
  "description": "Laptop purchase"
}
  ```

**Evaluations**:

- [+] tool_called: Tool 'add_expense_date_c' was called
- [+] category_valid: Category 'gadget' is valid
- [+] date_format: Date '2026-01-27' is in correct format
- [+] category_match: Category 'gadget' matches expected 'gadget'
- [+] date_match: Date '2026-01-27' matches expected '2026-01-27'

### add_expense_date_c / ambiguous_no_date: PASS (1.00)

**Tool Calls**:

- `add_expense_date_c`
  ```json
  {
  "expense_date": "2026-01-28",
  "amount": 50,
  "category": "food",
  "description": "groceries"
}
  ```

**Evaluations**:

- [+] tool_called: Tool 'add_expense_date_c' was called
- [+] category_valid: Category 'food' is valid
- [+] date_format: Date '2026-01-28' is in correct format
- [+] category_match: Category 'food' matches expected 'food'

### add_expense_date_c / ambiguous_vague_category: PASS (1.00)

**Tool Calls**:

- `add_expense_date_c`
  ```json
  {
  "expense_date": "2026-01-27",
  "amount": 30,
  "category": "shopping",
  "description": "Stuff at the store"
}
  ```

**Evaluations**:

- [+] tool_called: Tool 'add_expense_date_c' was called
- [+] category_valid: Category 'shopping' is valid
- [+] date_format: Date '2026-01-27' is in correct format
- [+] date_match: Date '2026-01-27' matches expected '2026-01-27'

### add_expense_date_c / ambiguous_relative_date: FAIL (0.00)

**No tool calls made**

**Evaluations**:

- [-] tool_called: No tool starting with 'add_expense' was called
- [-] category_valid: No add_expense tool call found
- [-] date_format: No add_expense tool call found
- [-] category_match: No add_expense tool call found

### add_expense_date_c / ambiguous_mixed_items: PASS (1.00)

**Tool Calls**:

- `add_expense_date_c`
  ```json
  {
  "expense_date": "2026-01-27",
  "amount": 55,
  "category": "shopping",
  "description": "Coffee and phone case"
}
  ```

**Evaluations**:

- [+] tool_called: Tool 'add_expense_date_c' was called
- [+] category_valid: Category 'shopping' is valid
- [+] date_format: Date '2026-01-27' is in correct format
- [+] date_match: Date '2026-01-27' matches expected '2026-01-27'

### add_expense_date_c / edge_future_date: PASS (1.00)

**Tool Calls**:

- `add_expense_date_c`
  ```json
  {
  "expense_date": "2026-01-29",
  "amount": 100,
  "category": "other",
  "description": "Hotel"
}
  ```

**Evaluations**:

- [+] tool_called: Tool 'add_expense_date_c' was called
- [+] category_valid: Category 'other' is valid
- [+] date_format: Date '2026-01-29' is in correct format
- [+] date_match: Date '2026-01-29' matches expected '2026-01-29'

### add_expense_date_c / edge_large_amount: PASS (0.80)

**Tool Calls**:

- `add_expense_date_c`
  ```json
  {
  "expense_date": "2026-01-27",
  "amount": 35000,
  "category": "transport",
  "description": "Bought a car"
}
  ```

**Evaluations**:

- [+] tool_called: Tool 'add_expense_date_c' was called
- [+] category_valid: Category 'transport' is valid
- [+] date_format: Date '2026-01-27' is in correct format
- [-] category_match: Category 'transport' does not match expected 'other'
- [+] date_match: Date '2026-01-27' matches expected '2026-01-27'

### add_expense_date_c / edge_small_amount: PASS (1.00)

**Tool Calls**:

- `add_expense_date_c`
  ```json
  {
  "expense_date": "2026-01-27",
  "amount": 0.99,
  "category": "gadget",
  "description": "App purchase"
}
  ```

**Evaluations**:

- [+] tool_called: Tool 'add_expense_date_c' was called
- [+] category_valid: Category 'gadget' is valid
- [+] date_format: Date '2026-01-27' is in correct format
- [+] category_match: Category 'gadget' matches expected 'gadget'
- [+] date_match: Date '2026-01-27' matches expected '2026-01-27'

### add_expense_date_c / edge_unknown_category: PASS (1.00)

**Tool Calls**:

- `add_expense_date_c`
  ```json
  {
  "expense_date": "2026-01-27",
  "amount": 200,
  "category": "entertainment",
  "description": "Spa treatment"
}
  ```

**Evaluations**:

- [+] tool_called: Tool 'add_expense_date_c' was called
- [+] category_valid: Category 'entertainment' is valid
- [+] date_format: Date '2026-01-27' is in correct format
- [+] date_match: Date '2026-01-27' matches expected '2026-01-27'

### add_expense_date_c / edge_currency_symbol: PASS (1.00)

**Tool Calls**:

- `add_expense_date_c`
  ```json
  {
  "expense_date": "2026-01-27",
  "amount": 50,
  "category": "food",
  "description": "Dinner"
}
  ```

**Evaluations**:

- [+] tool_called: Tool 'add_expense_date_c' was called
- [+] category_valid: Category 'food' is valid
- [+] date_format: Date '2026-01-27' is in correct format
- [+] category_match: Category 'food' matches expected 'food'
- [+] date_match: Date '2026-01-27' matches expected '2026-01-27'

### add_expense_date_d / clear_food_yesterday: PASS (1.00)

**Tool Calls**:

- `add_expense_date_d`
  ```json
  {
  "expense_date": "2026-01-27",
  "amount": 12.5,
  "category": "food",
  "description": "Sandwich"
}
  ```

**Evaluations**:

- [+] tool_called: Tool 'add_expense_date_d' was called
- [+] category_valid: Category 'food' is valid
- [+] date_format: Date '2026-01-27' is in correct format
- [+] category_match: Category 'food' matches expected 'food'
- [+] date_match: Date '2026-01-27' matches expected '2026-01-27'

### add_expense_date_d / clear_transport_today: PASS (1.00)

**Tool Calls**:

- `add_expense_date_d`
  ```json
  {
  "expense_date": "2026-01-28",
  "amount": 45,
  "category": "transport",
  "description": "Gas"
}
  ```

**Evaluations**:

- [+] tool_called: Tool 'add_expense_date_d' was called
- [+] category_valid: Category 'transport' is valid
- [+] date_format: Date '2026-01-28' is in correct format
- [+] category_match: Category 'transport' matches expected 'transport'
- [+] date_match: Date '2026-01-28' matches expected '2026-01-28'

### add_expense_date_d / clear_entertainment: PASS (1.00)

**Tool Calls**:

- `add_expense_date_d`
  ```json
  {
  "expense_date": "2026-01-15",
  "amount": 25.99,
  "category": "entertainment",
  "description": "Movie ticket"
}
  ```

**Evaluations**:

- [+] tool_called: Tool 'add_expense_date_d' was called
- [+] category_valid: Category 'entertainment' is valid
- [+] date_format: Date '2026-01-15' is in correct format
- [+] category_match: Category 'entertainment' matches expected 'entertainment'
- [+] date_match: Date '2026-01-15' matches expected '2026-01-15'

### add_expense_date_d / clear_shopping: PASS (1.00)

**Tool Calls**:

- `add_expense_date_d`
  ```json
  {
  "expense_date": "2026-01-20",
  "amount": 125,
  "category": "shopping",
  "description": "New shoes"
}
  ```

**Evaluations**:

- [+] tool_called: Tool 'add_expense_date_d' was called
- [+] category_valid: Category 'shopping' is valid
- [+] date_format: Date '2026-01-20' is in correct format
- [+] category_match: Category 'shopping' matches expected 'shopping'
- [+] date_match: Date '2026-01-20' matches expected '2026-01-20'

### add_expense_date_d / clear_gadget: PASS (1.00)

**Tool Calls**:

- `add_expense_date_d`
  ```json
  {
  "expense_date": "2026-01-27",
  "amount": 1200,
  "category": "gadget",
  "description": "Laptop purchase"
}
  ```

**Evaluations**:

- [+] tool_called: Tool 'add_expense_date_d' was called
- [+] category_valid: Category 'gadget' is valid
- [+] date_format: Date '2026-01-27' is in correct format
- [+] category_match: Category 'gadget' matches expected 'gadget'
- [+] date_match: Date '2026-01-27' matches expected '2026-01-27'

### add_expense_date_d / ambiguous_no_date: FAIL (0.00)

**No tool calls made**

**Evaluations**:

- [-] tool_called: No tool starting with 'add_expense' was called
- [-] category_valid: No add_expense tool call found
- [-] date_format: No add_expense tool call found
- [-] category_match: No add_expense tool call found

### add_expense_date_d / ambiguous_vague_category: FAIL (0.00)

**No tool calls made**

**Evaluations**:

- [-] tool_called: No tool starting with 'add_expense' was called
- [-] category_valid: No add_expense tool call found
- [-] date_format: No add_expense tool call found
- [-] date_match: No add_expense tool call found

### add_expense_date_d / ambiguous_relative_date: FAIL (0.00)

**No tool calls made**

**Evaluations**:

- [-] tool_called: No tool starting with 'add_expense' was called
- [-] category_valid: No add_expense tool call found
- [-] date_format: No add_expense tool call found
- [-] category_match: No add_expense tool call found

### add_expense_date_d / ambiguous_mixed_items: FAIL (0.00)

**No tool calls made**

**Evaluations**:

- [-] tool_called: No tool starting with 'add_expense' was called
- [-] category_valid: No add_expense tool call found
- [-] date_format: No add_expense tool call found
- [-] date_match: No add_expense tool call found

### add_expense_date_d / edge_future_date: PASS (1.00)

**Tool Calls**:

- `add_expense_date_d`
  ```json
  {
  "expense_date": "2026-01-29",
  "amount": 100,
  "category": "other",
  "description": "Hotel"
}
  ```

**Evaluations**:

- [+] tool_called: Tool 'add_expense_date_d' was called
- [+] category_valid: Category 'other' is valid
- [+] date_format: Date '2026-01-29' is in correct format
- [+] date_match: Date '2026-01-29' matches expected '2026-01-29'

### add_expense_date_d / edge_large_amount: PASS (0.80)

**Tool Calls**:

- `add_expense_date_d`
  ```json
  {
  "expense_date": "2026-01-27",
  "amount": 35000,
  "category": "transport",
  "description": "Bought a car"
}
  ```

**Evaluations**:

- [+] tool_called: Tool 'add_expense_date_d' was called
- [+] category_valid: Category 'transport' is valid
- [+] date_format: Date '2026-01-27' is in correct format
- [-] category_match: Category 'transport' does not match expected 'other'
- [+] date_match: Date '2026-01-27' matches expected '2026-01-27'

### add_expense_date_d / edge_small_amount: PASS (1.00)

**Tool Calls**:

- `add_expense_date_d`
  ```json
  {
  "expense_date": "2026-01-27",
  "amount": 0.99,
  "category": "gadget",
  "description": "App purchase"
}
  ```

**Evaluations**:

- [+] tool_called: Tool 'add_expense_date_d' was called
- [+] category_valid: Category 'gadget' is valid
- [+] date_format: Date '2026-01-27' is in correct format
- [+] category_match: Category 'gadget' matches expected 'gadget'
- [+] date_match: Date '2026-01-27' matches expected '2026-01-27'

### add_expense_date_d / edge_unknown_category: PASS (1.00)

**Tool Calls**:

- `add_expense_date_d`
  ```json
  {
  "expense_date": "2026-01-27",
  "amount": 200,
  "category": "entertainment",
  "description": "Spa treatment"
}
  ```

**Evaluations**:

- [+] tool_called: Tool 'add_expense_date_d' was called
- [+] category_valid: Category 'entertainment' is valid
- [+] date_format: Date '2026-01-27' is in correct format
- [+] date_match: Date '2026-01-27' matches expected '2026-01-27'

### add_expense_date_d / edge_currency_symbol: PASS (1.00)

**Tool Calls**:

- `add_expense_date_d`
  ```json
  {
  "expense_date": "2026-01-27",
  "amount": 50,
  "category": "food",
  "description": "Dinner"
}
  ```

**Evaluations**:

- [+] tool_called: Tool 'add_expense_date_d' was called
- [+] category_valid: Category 'food' is valid
- [+] date_format: Date '2026-01-27' is in correct format
- [+] category_match: Category 'food' matches expected 'food'
- [+] date_match: Date '2026-01-27' matches expected '2026-01-27'

</details>
