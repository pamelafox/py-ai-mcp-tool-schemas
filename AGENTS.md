# Instructions for coding agents

## Markdown files

Always check for markdownlint issues and resolve them.

## Updating Python dependencies

When updating or adding Python dependencies:

1. Edit `pyproject.toml` with the new or updated version constraints.
2. Run `uv lock` to re-resolve dependencies (use `uv lock -P <package>` to upgrade only a specific package).
3. Run `uv sync` to install the updated lockfile into the virtual environment.

## Testing agents

First, start the MCP server in the background:

```bash
uv run python servers/expenses_mcp.py &
```

### Pydantic AI agent

```bash
# Basic run with default tool and query
uv run python agents/pydanticai_agent.py

# Specify tool variant and custom query
uv run python agents/pydanticai_agent.py --tools add_expense_cat_a --query "I bought coffee for $5"

# With reasoning and show outputs
uv run python agents/pydanticai_agent.py --reasoning xhigh --show-tool-calls --show-reasoning

# With specific model deployment
uv run python agents/pydanticai_agent.py --model gpt-5.2 --reasoning low
```

### Agent Framework agent

```bash
# Basic run
uv run python agents/agentframework_agent.py

# With tool variant and reasoning
uv run python agents/agentframework_agent.py --tools add_expense_cat_c --reasoning high

# Show tool calls and reasoning output
uv run python agents/agentframework_agent.py --model gpt-5.2 --reasoning xhigh --show-tool-calls --show-reasoning
```

### LangChain agent

```bash
# Basic run
uv run python agents/langchain_agent.py

# With tool variant and custom query
uv run python agents/langchain_agent.py --tools add_expense_cat_a --query "Coffee for $5"

# With reasoning and show tool calls
uv run python agents/langchain_agent.py --model gpt-5.2 --reasoning low --show-tool-calls
```

### Copilot SDK agent

```bash
# Basic run (requires GITHUB_TOKEN or Azure OpenAI)
uv run python agents/copilotsdk_agent.py

# With specific model
uv run python agents/copilotsdk_agent.py --model gpt-5 --show-tool-calls

# Available models: gpt-5, claude-sonnet-4, claude-sonnet-4.5, claude-haiku-4.5
uv run python agents/copilotsdk_agent.py --model claude-sonnet-4 --show-reasoning
```

### Common options

| Option | Description |
|--------|-------------|
| `--tools` | Tool variant to use (e.g., `add_expense_cat_c`) |
| `--query` | Custom query to send |
| `--model` | Model deployment name |
| `--seed` | Seed for reproducibility (default: 42) |
| `--temperature` | Sampling temperature |
| `--reasoning` | Reasoning effort: none, minimal, low, medium, high, xhigh |
| `--show-tool-calls` | Print extracted tool calls |
| `--show-reasoning` | Print reasoning summary |

## Running evals

**Important:** For gpt-5 level models (gpt-5.2, gpt-5.3-codex, etc.), always specify `--reasoning medium` (or another explicit level) when running evals. Without an explicit reasoning effort, these models might default to no reasoning or might use an unpredictable amount of reasoning, which can lead to inconsistent results.

**Reproducibility:** Always specify `--seed 42 --temperature 0` when the model supports it. This minimizes run-to-run variance and makes results comparable across runs.

```bash
# Run all default variants (category + date) with default .env
uv run python evals/runner.py --output evals/runs/my_run

# Run only category variants
uv run python evals/runner.py --variants add_expense_cat_b,add_expense_cat_c,add_expense_cat_d,add_expense_cat_e --output evals/runs/my_cat_run

# Run only date variants
uv run python evals/runner.py --variants add_expense_date_a,add_expense_date_b,add_expense_date_c,add_expense_date_d --output evals/runs/my_date_run

# Run with a specific model via env file
uv run python evals/runner.py --env-file .env.gpt4o --output evals/runs/gpt4o_run

# Run with specific seed and temperature
uv run python evals/runner.py --seed 42 --temperature 0 --output evals/runs/deterministic_run

# Run with reasoning effort (required for gpt-5 level models)
uv run python evals/runner.py --env-file .env.gpt53codex --reasoning medium --output evals/runs/gpt53codex_med

# Run output schema evals (get_expenses variants)
uv run python evals/runner.py --eval-type output --output evals/runs/output_run

# Run with a different agent framework
uv run python evals/runner.py --agent copilot --output evals/runs/copilot_run

# Run specific test cases only
uv run python evals/runner.py --cases clear_food_yesterday,edge_large_amount --output evals/runs/subset_run
```

When you are done running evals, inform the developer by using the "say" command in the terminal:

```bash
say "Evals complete! Return to laptop!"
```
