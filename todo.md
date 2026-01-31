# Implementation TODO for Talk

Talk: **Improving MCP tool schemas to increase agent reliability**

## Architecture

Single MCP server (`servers/expenses_mcp.py`) exposes multiple tool variants with different schemas. All tools call a shared implementation. Agent selects which variant to use via `allowed_tools`.

**Tool naming**: Use opaque names like `add_expense_a`, `add_expense_b`, etc. to avoid biasing the model. If a tool is named `add_expense_enum`, the model might infer from the name that it should send enum values — defeating the purpose of testing whether the schema itself guides correct behavior.

```python
# Server: all variants exposed with opaque names
@mcp.tool
async def add_expense_a(category: str, ...): ...      # str variant

@mcp.tool  
async def add_expense_b(category: Category, ...): ... # enum variant

@mcp.tool
async def add_expense_c(category: Literal["food", ...], ...): ... # literal variant

# Agent: select variant per test
agent = Agent(model, toolsets=[server], allowed_tools=["add_expense_b"])
```

## MCP Server Tool Variants

### Category Field Variants (constrained values)

| Tool Name | Category Type | Notes |
| --- | --- | --- |
| `add_expense_cat_a` | `str` | No constraints |
| `add_expense_cat_b` | `Annotated[str, "food, transport, ..."]` | Description hints valid values |
| `add_expense_cat_c` | `Literal["food", "transport", ...]` | Inline allowed values |
| `add_expense_cat_d` | `Enum` | Python enum |

### Date Field Variants

| Tool Name | Date Type | Notes |
| --- | --- | --- |
| `add_expense_date_a` | `str` | No format hint |
| `add_expense_date_b` | `Annotated[str, "YYYY-MM-DD"]` | Description hint |
| `add_expense_date_c` | `date` | Python date type |
| `add_expense_date_d` | `Annotated[str, Field(pattern=r"\d{4}-\d{2}-\d{2}")]` | Regex constraint |

### Output Variations (`get_expenses_data`)

Output schema tests belong on `get_expenses_data` — it returns actual data the agent needs to interpret, unlike `add_expense` which just returns confirmation text.

| Tool Name | Return Type | Notes |
| --- | --- | --- |
| `get_expenses_a` | `str` | Formatted text (hard for agent to parse) |
| `get_expenses_b` | `list[dict]` | Untyped list of dicts |
| `get_expenses_c` | `list[Expense]` | Typed Pydantic models |

## Pydantic AI Agents

Reference: [pydanticai_mcp_http.py](https://github.com/Azure-Samples/python-ai-agent-frameworks-demos/blob/main/examples/pydanticai_mcp_http.py)

- [x] Create `agents/pydanticai.py` based on reference above
- [x] Use `MCPServerStreamableHTTP(url="http://localhost:8000/mcp")`
- [x] Add `allowed_tools` parameter to select which schema variant to test (not in reference — we add this)
- [x] Multi-provider setup already in reference (Azure, GitHub, Ollama, OpenAI)
- [x] Add Logfire instrumentation to observe:
  - [x] Tool selection decisions
  - [x] Argument construction
  - [x] Output parsing
- [x] Add `--reasoning` arg to test different reasoning levels

## Evaluation Framework

Reference: [Pydantic Evals - Evaluators Overview](https://ai.pydantic.dev/evals/evaluators/overview)

Uses `pydantic_evals` library with `Dataset`, `Case`, and evaluators.

- [x] Create `evals/` directory for evaluation code
- [x] Define test dataset with varied expense-logging prompts:
  - [x] Clear, unambiguous requests
  - [x] Ambiguous requests (missing date, vague categories)
  - [x] Edge cases
  - [x] Non-English language coverage (Spanish)
  - [x] Amount wording/currency variability (e.g., bucks, USD, dólares, pesos)
- [x] Implement evaluators:
  - [x] `tool_called` — verify an `add_expense_*` tool was called
  - [x] `category_valid` / `category_match`
  - [x] `date_format` / `date_match`
- [x] Implement evaluation runner that loops over schema variants and cases
- [x] Generate comparison metrics between schema variants (JSON + markdown report)

## Schemas

- [x] Generate JSON schemas for all tool variants and save to `schemas/` directory
- [x] Verify FastMCP includes backwards-compatible `content` field alongside `structuredContent` (per MCP spec)
- [x] Document schema differences between variants (e.g., `list[dict]` vs `list[Expense]` outputSchema)

## Logfire Integration

References:

- [Logfire MCP Integration](https://logfire.pydantic.dev/docs/integrations/llms/mcp/)
- [Logfire Pydantic AI Integration](https://logfire.pydantic.dev/docs/integrations/llms/pydanticai/)

Simple setup — just `logfire.configure()` + `logfire.instrument_mcp()` (no custom middleware needed).

- [x] Add Logfire support to MCP server
- [x] Add Logfire instrumentation to Pydantic AI agent (`logfire.instrument_pydantic_ai()`)
- [ ] Create example traces showing good vs bad tool calls
- [x] Delete `servers/opentelemetry_middleware.py` (no longer needed)

## Documentation

- [ ] Update README.md for new focus
- [ ] Document how to run evaluations
- [ ] Add example Logfire screenshots
- [ ] Write up findings on schema features vs model support

## Future Ideas

- [x] Add evaluation for non-English languages
- [x] Compare different reasoning effort levels for GPT-5.2
- [x] Experiment with a way to describe what things go in which category, like for ambiguous situations (transport/shopping/gadget)
- [x] Add a tool variant that accepts a Pydantic model input (e.g., `expense: ExpenseInput`) to test nested JSON/object-shape adherence
- [x] Add a tool variant that uses a `Union`/`Literal` sentinel for missing values (e.g., `reimbursable: bool | Literal["unknown"]`) to test “proceed vs ask” behavior
- [ ] Add another argument type that tests regex/gt constraints
- [ ] Add comparison with other models (Opus, awaiting access)
- [x] Add comparison with Copilot SDK, Microsoft Agent Framework
- [x] Make runner.py work generically with any agent script
- [ ] Remove `--seed` from agents if Responses API confirmed not to support it (already removed from langchain_agent.py)

## Evaluation matrix

Once all is done, we should re-run fresh evaluations for:

- [ ] GPT-5.2: none, low, medium, high, xhigh
- [ ] GPT-4.1-mini: temperature=0
- [ ] GPT-4.0: temperature=0
- [ ] Anthropic Opus 4.5
- [ ] Anthropic Sonnet 4.5

Each evals should be stored in its own folder under `evals/runs/` with clear folder names, e.g., `gpt52_xhigh`, `gpt41mini`, etc.