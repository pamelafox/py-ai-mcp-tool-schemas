# MCP Tool Schema Evaluation Report

## Metadata

- **Timestamp**: 2026-03-06T12:26:55.181815
- **Agent**: pydanticai
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
| get_expenses_a | return: str (formatted text) | 0.00 | 6 |
| get_expenses_b | return: list[dict] (untyped) | 0.00 | 6 |
| get_expenses_c | return: list[Expense] (Pydantic model) | 0.00 | 6 |

## Evaluation Breakdown

## Detailed Results

<details>
<summary>Click to expand</summary>

### get_expenses_a / count_all: 0.00

**User Query**:

> How many expenses are recorded in total? Reply with just the number.

**Error**: status_code: 404, model_name: gpt-5.2, body: {'type': 'invalid_request_error', 'code': 'DeploymentNotFound', 'message': 'The API deployment for this resource does not exist. If you created the deployment within the last 5 minutes, please wait a moment and try again.'}

### get_expenses_a / total_spending: 0.00

**User Query**:

> What is the exact total amount spent across all recorded expenses? Reply with just the number.

**Error**: status_code: 404, model_name: gpt-5.2, body: {'type': 'invalid_request_error', 'code': 'DeploymentNotFound', 'message': 'The API deployment for this resource does not exist. If you created the deployment within the last 5 minutes, please wait a moment and try again.'}

### get_expenses_a / max_expense: 0.00

**User Query**:

> What is the dollar amount of the single most expensive expense? Reply with just the number.

**Error**: status_code: 404, model_name: gpt-5.2, body: {'type': 'invalid_request_error', 'code': 'DeploymentNotFound', 'message': 'The API deployment for this resource does not exist. If you created the deployment within the last 5 minutes, please wait a moment and try again.'}

### get_expenses_a / min_expense: 0.00

**User Query**:

> What is the dollar amount of the cheapest expense? Reply with just the number.

**Error**: status_code: 404, model_name: gpt-5.2, body: {'type': 'invalid_request_error', 'code': 'DeploymentNotFound', 'message': 'The API deployment for this resource does not exist. If you created the deployment within the last 5 minutes, please wait a moment and try again.'}

### get_expenses_a / earliest_date: 0.00

**User Query**:

> What is the date of the earliest recorded expense? Reply in YYYY-MM-DD format.

**Error**: status_code: 404, model_name: gpt-5.2, body: {'type': 'invalid_request_error', 'code': 'DeploymentNotFound', 'message': 'The API deployment for this resource does not exist. If you created the deployment within the last 5 minutes, please wait a moment and try again.'}

### get_expenses_a / average_expense: 0.00

**User Query**:

> What is the average expense amount, rounded to 2 decimal places? Reply with just the number.

**Error**: status_code: 404, model_name: gpt-5.2, body: {'type': 'invalid_request_error', 'code': 'DeploymentNotFound', 'message': 'The API deployment for this resource does not exist. If you created the deployment within the last 5 minutes, please wait a moment and try again.'}

### get_expenses_b / count_all: 0.00

**User Query**:

> How many expenses are recorded in total? Reply with just the number.

**Error**: status_code: 404, model_name: gpt-5.2, body: {'type': 'invalid_request_error', 'code': 'DeploymentNotFound', 'message': 'The API deployment for this resource does not exist. If you created the deployment within the last 5 minutes, please wait a moment and try again.'}

### get_expenses_b / total_spending: 0.00

**User Query**:

> What is the exact total amount spent across all recorded expenses? Reply with just the number.

**Error**: status_code: 404, model_name: gpt-5.2, body: {'type': 'invalid_request_error', 'code': 'DeploymentNotFound', 'message': 'The API deployment for this resource does not exist. If you created the deployment within the last 5 minutes, please wait a moment and try again.'}

### get_expenses_b / max_expense: 0.00

**User Query**:

> What is the dollar amount of the single most expensive expense? Reply with just the number.

**Error**: status_code: 404, model_name: gpt-5.2, body: {'type': 'invalid_request_error', 'code': 'DeploymentNotFound', 'message': 'The API deployment for this resource does not exist. If you created the deployment within the last 5 minutes, please wait a moment and try again.'}

### get_expenses_b / min_expense: 0.00

**User Query**:

> What is the dollar amount of the cheapest expense? Reply with just the number.

**Error**: status_code: 404, model_name: gpt-5.2, body: {'type': 'invalid_request_error', 'code': 'DeploymentNotFound', 'message': 'The API deployment for this resource does not exist. If you created the deployment within the last 5 minutes, please wait a moment and try again.'}

### get_expenses_b / earliest_date: 0.00

**User Query**:

> What is the date of the earliest recorded expense? Reply in YYYY-MM-DD format.

**Error**: status_code: 404, model_name: gpt-5.2, body: {'type': 'invalid_request_error', 'code': 'DeploymentNotFound', 'message': 'The API deployment for this resource does not exist. If you created the deployment within the last 5 minutes, please wait a moment and try again.'}

### get_expenses_b / average_expense: 0.00

**User Query**:

> What is the average expense amount, rounded to 2 decimal places? Reply with just the number.

**Error**: status_code: 404, model_name: gpt-5.2, body: {'type': 'invalid_request_error', 'code': 'DeploymentNotFound', 'message': 'The API deployment for this resource does not exist. If you created the deployment within the last 5 minutes, please wait a moment and try again.'}

### get_expenses_c / count_all: 0.00

**User Query**:

> How many expenses are recorded in total? Reply with just the number.

**Error**: status_code: 404, model_name: gpt-5.2, body: {'type': 'invalid_request_error', 'code': 'DeploymentNotFound', 'message': 'The API deployment for this resource does not exist. If you created the deployment within the last 5 minutes, please wait a moment and try again.'}

### get_expenses_c / total_spending: 0.00

**User Query**:

> What is the exact total amount spent across all recorded expenses? Reply with just the number.

**Error**: status_code: 404, model_name: gpt-5.2, body: {'type': 'invalid_request_error', 'code': 'DeploymentNotFound', 'message': 'The API deployment for this resource does not exist. If you created the deployment within the last 5 minutes, please wait a moment and try again.'}

### get_expenses_c / max_expense: 0.00

**User Query**:

> What is the dollar amount of the single most expensive expense? Reply with just the number.

**Error**: status_code: 404, model_name: gpt-5.2, body: {'type': 'invalid_request_error', 'code': 'DeploymentNotFound', 'message': 'The API deployment for this resource does not exist. If you created the deployment within the last 5 minutes, please wait a moment and try again.'}

### get_expenses_c / min_expense: 0.00

**User Query**:

> What is the dollar amount of the cheapest expense? Reply with just the number.

**Error**: status_code: 404, model_name: gpt-5.2, body: {'type': 'invalid_request_error', 'code': 'DeploymentNotFound', 'message': 'The API deployment for this resource does not exist. If you created the deployment within the last 5 minutes, please wait a moment and try again.'}

### get_expenses_c / earliest_date: 0.00

**User Query**:

> What is the date of the earliest recorded expense? Reply in YYYY-MM-DD format.

**Error**: status_code: 404, model_name: gpt-5.2, body: {'type': 'invalid_request_error', 'code': 'DeploymentNotFound', 'message': 'The API deployment for this resource does not exist. If you created the deployment within the last 5 minutes, please wait a moment and try again.'}

### get_expenses_c / average_expense: 0.00

**User Query**:

> What is the average expense amount, rounded to 2 decimal places? Reply with just the number.

**Error**: status_code: 404, model_name: gpt-5.2, body: {'type': 'invalid_request_error', 'code': 'DeploymentNotFound', 'message': 'The API deployment for this resource does not exist. If you created the deployment within the last 5 minutes, please wait a moment and try again.'}

</details>
