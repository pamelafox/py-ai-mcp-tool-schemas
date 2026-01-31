# MCP Tool Schema Evaluation Report

## Metadata

- **Timestamp**: 2026-01-30T16:25:27.914101
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
| add_expense_cat_a | category: str | 0.33 | 1 |
| add_expense_cat_b | category: Annotated[str, ...] | 1.00 | 1 |
| add_expense_cat_c | category: Literal[...] | 1.00 | 1 |
| add_expense_cat_d | category: ExpenseCategory (Enum) | 1.00 | 1 |
| add_expense_cat_e | category: Annotated[ExpenseCategory, Field(description=...)] | 1.00 | 1 |
| add_expense_date_a | expense_date: str | 0.67 | 1 |
| add_expense_date_b | expense_date: Annotated[str, ...] | 0.67 | 1 |
| add_expense_date_c | expense_date: date | 0.67 | 1 |
| add_expense_date_d | expense_date: Annotated[str, Field(pattern=...)] | 0.67 | 1 |
| add_expense_model_a | expense: ExpenseInput (Pydantic model) | 0.80 | 1 |
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
| add_expense_date_a | expense_date: str | 0.0% | 0 | 1 |
| add_expense_date_b | expense_date: Annotated[str, ...] | 0.0% | 0 | 1 |
| add_expense_date_c | expense_date: date | 0.0% | 0 | 1 |
| add_expense_date_d | expense_date: Annotated[str, Field(pattern=...)] | 0.0% | 0 | 1 |
| add_expense_model_a | expense: ExpenseInput (Pydantic model) | 0.0% | 0 | 1 |

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
  "expense_date": "2026-01-30",
  "amount": 12.5,
  "category": "Food",
  "description": "Sandwich"
}
```


**Assistant Output**:

> Done! I've added your sandwich expense of $12.50 for January 30th to the Food category.

**Reasoning Summary**:

```
The user wants to add an expense for a sandwich that cost $12.50 bought yesterday. Let me figure out the date:
- Current date: 2026-01-31
- Yesterday: 2026-01-30

I need to use the 0-add_expense_cat_a function with:
- expense_date: 2026-01-30 (yesterday)
- amount: 12.50
- category: (need to infer something reasonable for a sandwich... probably "Food" or similar)
- description: "Sandwich"

Let me call the function to add this expense.
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
  "expense_date": "2026-01-30",
  "amount": 12.5,
  "category": "Food & drink",
  "description": "Sandwich"
}
```


**Assistant Output**:

> Done! I've added your sandwich expense for $12.50 to the Food & drink category on January 30th.

**Reasoning Summary**:

```
The user is telling me they bought a sandwich for $12.50 yesterday. This sounds like they want to add an expense to their expense tracker. Looking at the available tools, I can see there's a function called `0-add_expense_cat_b` which allows adding expenses.

The function takes:
- expense_date (required, format: date)
- amount (required, number)
- category (required, must be one of the listed categories)
- description (required, string)

The current datetime is 2026-01-31T00:22:25.633Z, so yesterday would be 2026-01-30.

The amount is $12.50, which is 12.50.

The description is "sandwich".

For the category, looking at the available options: "Food & drink, Transit and Fuel, Media & streaming, Apparel and Beauty, Electronics & tech, Home and office, Health & Fitness, Arts and hobbies, Fees & services, Misc"

A sandwich would fall under "Food & drink".

I should add this expense for them.
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
  "expense_date": "2026-01-30",
  "amount": 12.5,
  "category": "Food & drink",
  "description": "Sandwich"
}
```


**Assistant Output**:

> Done! Added your $12.50 sandwich purchase to Food & drink for yesterday (January 30).

**Reasoning Summary**:

```
The user is telling me they bought a sandwich for $12.50 yesterday. This seems like they want to add an expense to their system. Looking at the available tools, I can see there's a tool called `0-add_expense_cat_c` which can add expenses.

The tool requires:
- expense_date (format: date)
- amount (number)
- category (enum with options including "Food & drink", "Transit and Fuel", "Media & streaming", "Apparel and Beauty", "Electronics & tech", "Home and office", "Health & Fitness", "Arts and hobbies", "Fees & services", "Misc")
- description (string)

The current datetime is 2026-01-31T00:22:45.105Z, so yesterday would be 2026-01-30.

For the sandwich:
- expense_date: 2026-01-30
- amount: 12.50
- category: "Food & drink" (sandwich is clearly food)
- description: "Sandwich"

Let me add this expense.
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
  "expense_date": "2026-01-30",
  "amount": 12.5,
  "category": "Food & drink",
  "description": "Sandwich"
}
```


**Assistant Output**:

> Done! Added your $12.50 sandwich expense for yesterday (Jan 30).

**Reasoning Summary**:

```
The user is telling me they bought a sandwich for $12.50 yesterday. This sounds like they want to add an expense. Looking at the available tools, I have an "add_expense_cat_d" function that can add expenses.

Let me check the parameters needed:
- expense_date: format "date" (required)
- amount: number (required)
- category: enum with options like "Food & drink", "Transit and Fuel", etc. (required)
- description: string (required)

The user said "Yesterday" and the current date/time is 2026-01-31T00:23:03.703Z, so yesterday would be 2026-01-30.

The amount is $12.50.
For category, "Food & drink" seems appropriate for a sandwich.
For description, I can use something like "Sandwich".

I should add this expense.
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
  "expense_date": "2026-01-30",
  "amount": 12.5,
  "category": "Food & drink",
  "description": "Sandwich"
}
```


**Assistant Output**:

> Done! Added $12.50 sandwich expense to Food & drink for January 30th.

**Reasoning Summary**:

```
The user is asking me to add an expense for a sandwich they bought yesterday for $12.50. 

Looking at the available tools, I have the `0-add_expense_cat_e` function which allows me to add an expense with the following parameters:
- expense_date: format "date" (YYYY-MM-DD)
- amount: number
- category: enum with options like "Food & drink", "Transit and Fuel", "Media & streaming", etc.
- description: string

Given information:
- Amount: $12.50
- Description: sandwich
- Category: "Food & drink" (the description says "Choose the closest category for the expense. Do not ask follow-up questions just to disambiguate the category; pick the best fit using the description and common sense." Food includes "meals, groceries, coffee, restaurants, snacks")
- Date: Yesterday. Current datetime is 2026-01-31T00:23:23.025Z, so yesterday would be 2026-01-30

I should call the add_expense_cat_e function with these parameters.
```

**Evaluations**:

| Result | Evaluator | Message |
|---|---|---|
| ✅ Pass | tool_called | Tool 'add_expense_cat_e' was called |
| ✅ Pass | category_valid | Category 'Food & drink' is valid |
| ✅ Pass | category_match | Category 'Food & drink' matches expected 'Food & drink' |

### add_expense_date_a / clear_food_yesterday: 0.67

**User Query**:

> Yesterday I bought a sandwich for $12.50.

**Tool Calls**:

- Tool: `add_expense_date_a`

```json
{
  "expense_date": "2026-01-30",
  "amount": 12.5,
  "category": "Food & drink",
  "description": "Sandwich"
}
```


**Assistant Output**:

> Done! I've recorded your sandwich purchase for $12.50 yesterday (2026-01-30) in the Food & drink category.

**Reasoning Summary**:

```
The user is asking me to add an expense. They bought a sandwich for $12.50 yesterday. 

Current datetime is 2026-01-31T00:23:42.149Z, so yesterday would be 2026-01-30.

Looking at the available functions, I have `0-add_expense_date_a` which takes:
- expense_date: string (required)
- amount: number (required)
- category: enum (required) - one of ["Food & drink", "Transit and Fuel", "Media & streaming", "Apparel and Beauty", "Electronics & tech", "Home and office", "Health & Fitness", "Arts and hobbies", "Fees & services", "Misc"]
- description: string (required)

For a sandwich:
- expense_date: "2026-01-30"
- amount: 12.50
- category: "Food & drink"
- description: "Sandwich"

I should add this expense using the function call.
```

**Evaluations**:

| Result | Evaluator | Message |
|---|---|---|
| ✅ Pass | tool_called | Tool 'add_expense_date_a' was called |
| ✅ Pass | date_format | Date '2026-01-30' is in correct format |
| ❌ Fail | date_match | Date '2026-01-30' does not match expected '2026-01-29' |

### add_expense_date_b / clear_food_yesterday: 0.67

**User Query**:

> Yesterday I bought a sandwich for $12.50.

**Tool Calls**:

- Tool: `add_expense_date_b`

```json
{
  "expense_date": "2026-01-30",
  "amount": 12.5,
  "category": "Food & drink",
  "description": "Sandwich"
}
```


**Assistant Output**:

> Done! I've recorded your sandwich purchase for $12.50 on January 30th in the Food & drink category.

**Reasoning Summary**:

```
The user is asking me to add an expense. They bought a sandwich for $12.50 yesterday. The current datetime is 2026-01-31, so yesterday would be 2026-01-30.

I need to use the 0-add_expense_date_b tool with:
- expense_date: "2026-01-30"
- amount: 12.50
- category: This should be "Food & drink" based on the available categories
- description: "Sandwich" or something similar

Let me call the tool to add this expense.
```

**Evaluations**:

| Result | Evaluator | Message |
|---|---|---|
| ✅ Pass | tool_called | Tool 'add_expense_date_b' was called |
| ✅ Pass | date_format | Date '2026-01-30' is in correct format |
| ❌ Fail | date_match | Date '2026-01-30' does not match expected '2026-01-29' |

### add_expense_date_c / clear_food_yesterday: 0.67

**User Query**:

> Yesterday I bought a sandwich for $12.50.

**Tool Calls**:

- Tool: `add_expense_date_c`

```json
{
  "expense_date": "2026-01-30",
  "amount": 12.5,
  "category": "Food & drink",
  "description": "Sandwich"
}
```


**Assistant Output**:

> Done! I've recorded your $12.50 sandwich purchase from yesterday in the Food & drink category.

**Reasoning Summary**:

```
The user is asking me to add an expense for a sandwich that they bought yesterday for $12.50.

Looking at the available tools, I can see there's a function called "0-add_expense_date_c" which allows me to add expenses with parameters:
- expense_date (format: date)
- amount (number)
- category (enum with options including "Food & drink")
- description (string)

The current date/time is: 2026-01-31T00:24:18.680Z
So yesterday would be: 2026-01-30

I need to:
1. Date: 2026-01-30 (yesterday)
2. Amount: 12.50
3. Category: "Food & drink" (sandwich is food)
4. Description: "Sandwich" or "Bought a sandwich"

Let me make the function call to add this expense.
```

**Evaluations**:

| Result | Evaluator | Message |
|---|---|---|
| ✅ Pass | tool_called | Tool 'add_expense_date_c' was called |
| ✅ Pass | date_format | Date '2026-01-30' is in correct format |
| ❌ Fail | date_match | Date '2026-01-30' does not match expected '2026-01-29' |

### add_expense_date_d / clear_food_yesterday: 0.67

**User Query**:

> Yesterday I bought a sandwich for $12.50.

**Tool Calls**:

- Tool: `add_expense_date_d`

```json
{
  "expense_date": "2026-01-30",
  "amount": 12.5,
  "category": "Food & drink",
  "description": "Sandwich"
}
```


**Assistant Output**:

> Done! Added your $12.50 sandwich expense for yesterday.

**Reasoning Summary**:

```
The user is asking me to add an expense. They bought a sandwich for $12.50 yesterday. The current date is 2026-01-31, so yesterday would be 2026-01-30.

Looking at the available tools, I have `0-add_expense_date_d` which takes:
- expense_date (required): in format YYYY-MM-DD
- amount (required): number
- category (required): enum of specific categories
- description (required): string

The sandwich would likely fall under "Food & drink" category.

Let me prepare the call:
- expense_date: 2026-01-30 (yesterday)
- amount: 12.50
- category: Food & drink
- description: sandwich (or something more descriptive like "Sandwich")

I should make this call directly without explanation, keeping it concise.
```

**Evaluations**:

| Result | Evaluator | Message |
|---|---|---|
| ✅ Pass | tool_called | Tool 'add_expense_date_d' was called |
| ✅ Pass | date_format | Date '2026-01-30' is in correct format |
| ❌ Fail | date_match | Date '2026-01-30' does not match expected '2026-01-29' |

### add_expense_model_a / clear_food_yesterday: 0.80

**User Query**:

> Yesterday I bought a sandwich for $12.50.

**Tool Calls**:

- Tool: `add_expense_model_a`

```json
{
  "expense": {
    "expense_date": "2026-01-30",
    "amount": 12.5,
    "category": "Food & drink",
    "description": "Sandwich"
  }
}
```


**Assistant Output**:

> Done! I've added your sandwich expense ($12.50) to the Food & drink category for yesterday.

**Reasoning Summary**:

```
The user is telling me they bought a sandwich for $12.50 yesterday. This looks like they want to add an expense to the system. 

Looking at the available functions, I can see there's a function called `0-add_expense_model_a` that can add an expense.

The function requires:
- expense_date (format: date, YYYY-MM-DD)
- amount (number)
- category (enum with specific values)
- description (string)

Current datetime is: 2026-01-31T00:24:54.835Z
So yesterday would be: 2026-01-30

Amount: $12.50 = 12.50
Category: Looking at the enum, a sandwich would fall under "Food & drink"
Description: "Sandwich"

Let me call the function to add this expense.
```

**Evaluations**:

| Result | Evaluator | Message |
|---|---|---|
| ✅ Pass | tool_called | Tool 'add_expense_model_a' was called |
| ✅ Pass | category_valid | Category 'Food & drink' is valid |
| ✅ Pass | category_match | Category 'Food & drink' matches expected 'Food & drink' |
| ✅ Pass | date_format | Date '2026-01-30' is in correct format |
| ❌ Fail | date_match | Date '2026-01-30' does not match expected '2026-01-29' |

### add_expense_reimb_e / clear_food_yesterday: 1.00

**User Query**:

> Yesterday I bought a sandwich for $12.50.

**Tool Calls**:

- Tool: `add_expense_reimb_e`

```json
{
  "expense_date": "2026-01-30",
  "amount": 12.5,
  "category": "Food & drink",
  "description": "Sandwich",
  "reimbursable": false
}
```


**Assistant Output**:

> Done! Added your $12.50 sandwich expense for yesterday.

**Reasoning Summary**:

```
The user is telling me they bought a sandwich for $12.50 yesterday. They're likely asking me to add this as an expense. Let me use the add_expense tool to record this.

The current datetime is 2026-01-31T00:25:12.722Z, so yesterday would be 2026-01-30.

The sandwich is food, so the category should be "Food & drink".

I need to determine if this is reimbursable. Since they just mentioned it as a personal purchase without any indication of it being work-related, I should assume it's personal (reimbursable: false).

Let me add this expense:
- expense_date: 2026-01-30
- amount: 12.50
- category: Food & drink
- description: Sandwich
- reimbursable: false
```

**Evaluations**:

| Result | Evaluator | Message |
|---|---|---|
| ✅ Pass | tool_called | Tool 'add_expense_reimb_e' was called |

</details>
