# MCP Tool Schema Variant Testing (Expenses)

This repo is a small, focused testbed for a talk on **improving MCP tool schemas to increase agent reliability**.

It contains:

- A FastMCP HTTP server that exposes multiple **tool schema variants** for the same underlying expense-tracking actions.
- A PydanticAI agent runner that can be restricted to a specific tool variant and run at different **reasoning effort** levels.
- An evaluation harness that runs a dataset of prompts across variants and writes comparable results.

## Repository layout

| Path | What it is |
| --- | --- |
| [servers/expenses_mcp.py](servers/expenses_mcp.py) | MCP server (streamable HTTP) exposing schema variants |
| [agents/pydanticai_agent.py](agents/pydanticai_agent.py) | Agent runner used standalone and by evals |
| [evals/](evals/) | Dataset, evaluators, runner, report generator |
| [schemas/](schemas/) | Auto-generated JSON schemas + diffs |

## Setup

### Install dependencies

This repo uses `uv`:

```bash
uv sync
```

### Configure environment variables

Copy the sample file:

```bash
cp .env-sample .env
```

For the PydanticAI-based agent + evals, the key variables are:

- `AZURE_OPENAI_ENDPOINT` (example: `https://<resource>.openai.azure.com/`)
- `AZURE_OPENAI_CHAT_DEPLOYMENT` (your deployed model name)

Optional variables:

- `MCP_SERVER_URL` (defaults to `http://localhost:8000/mcp`)
- `LOGFIRE_TOKEN` (enables sending traces to Logfire)

You also need Azure credentials that work with `DefaultAzureCredential` (for local dev, `az login` is usually the easiest).

## Run the MCP server

Start the HTTP MCP server (streamable HTTP on port 8000):

```bash
uv run python servers/expenses_mcp.py
```

This server exposes multiple variants of the same logical operations (e.g., category as `str` vs `Literal[...]` vs `Enum`).

## Run the agent

The agent in [agents/pydanticai_agent.py](agents/pydanticai_agent.py) connects to the MCP server and can be limited to specific tools.

Examples:

```bash
# default tool variant
uv run python agents/pydanticai_agent.py

# single variant
uv run python agents/pydanticai_agent.py --tools add_expense_cat_c \
  --query "Yesterday I purchased a laptop for 1200 bucks." \
  --reasoning medium

# multiple allowed tools
uv run python agents/pydanticai_agent.py --tools add_expense_cat_c,get_expenses_c
```

Reasoning effort levels supported by the CLI:

- `none`, `minimal`, `low`, `medium`, `high`, `xhigh`

## Run evaluations

The evaluation harness runs a fixed dataset of prompts against tool variants and writes results to a timestamped folder under [evals/runs/](evals/runs/).

```bash
uv run python evals/runner.py --reasoning medium
```

By default, the runner evaluates all variants (category + date).

Useful options:

- `--variants add_expense_cat_a,add_expense_cat_c`
- `--cases clear_food_yesterday,spanish_food`
- `--output /path/to/output-folder`

Each run produces:

- `results.json` (machine-readable)
- `RESULTS.md` (human-readable report)

## Schemas

Generate JSON schemas for the tool variants:

```bash
uv run python scripts/generate_schemas.py
```

See [schemas/README.md](schemas/README.md) for a summary of how Python typing differences translate into JSON Schema differences.

## Tracing (Logfire)

Tracing is supported via Logfire:

- The MCP server enables Logfire instrumentation if `LOGFIRE_TOKEN` is set.
- The PydanticAI agent configures Logfire and emits traces for model calls and MCP requests.

To enable sending traces to Logfire, set `LOGFIRE_TOKEN` in `.env`.
