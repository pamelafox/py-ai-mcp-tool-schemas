"""Pydantic AI agent for testing MCP tool schema variants.

This module provides reusable functions for running agents against MCP tool servers.
It's used both as a standalone script and as a library by the evaluation runner.

Usage:
    # Start the MCP server first:
    uv run python servers/expenses_mcp.py

    # Run with default tool (add_expense_cat_c):
    uv run python agents/pydanticai_agent.py

    # Run with specific tool variant:
    uv run python agents/pydanticai_agent.py --tools add_expense_cat_a

    # Run with multiple tools:
    uv run python agents/pydanticai_agent.py --tools add_expense_cat_c,get_expenses_c

    # Run with custom query:
    uv run python agents/pydanticai_agent.py --query "I spent $50 on groceries today"
"""

import argparse
import asyncio
import json
import logging
import os
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from pathlib import Path
from urllib.parse import urlencode

import logfire
from azure.identity.aio import DefaultAzureCredential, get_bearer_token_provider
from dotenv import load_dotenv
from openai import AsyncOpenAI
from opentelemetry import trace as otel_trace
from opentelemetry.instrumentation.httpx import HTTPXClientInstrumentor
from opentelemetry.instrumentation.openai import OpenAIInstrumentor
from pydantic_ai import Agent
from pydantic_ai.mcp import MCPServerStreamableHTTP
from pydantic_ai.messages import ModelRequest, ModelResponse, ThinkingPart, ToolCallPart, ToolReturnPart
from pydantic_ai.models.openai import OpenAIResponsesModel
from pydantic_ai.providers.openai import OpenAIProvider
from pydantic_ai.usage import RunUsage

load_dotenv(override=True)  # Default; overridden by --env-file in main()

logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger("pydanticai")
logger.setLevel(logging.INFO)

# Reference: https://logfire.pydantic.dev/docs/integrations/llms/pydanticai/
logfire.configure(console=False)
logfire.instrument_pydantic_ai()

# Instrument HTTP calls to see raw requests to Azure OpenAI.
# This is useful for debugging but can be noisy.
HTTPXClientInstrumentor().instrument()
OpenAIInstrumentor().instrument()

# =============================================================================
# Configuration
# =============================================================================

MCP_SERVER_URL = os.getenv("MCP_SERVER_URL", "http://localhost:8000/mcp")
REASONING_LEVELS = ["none", "minimal", "low", "medium", "high", "xhigh"]
DEFAULT_REASONING: str | None = None


def _supports_openai_reasoning(model_name: str) -> bool:
    """Return True if the deployed model is expected to support `reasoning.*` params.

    Azure OpenAI deployments are referenced by deployment name, so this is
    necessarily heuristic. We keep it conservative to avoid hard failures on
    non-reasoning models (e.g., gpt-4.1-mini).
    """
    name = (model_name or "").lower()
    return name.startswith("gpt-5") or name.startswith("o")


# =============================================================================
# Data Classes
# =============================================================================


@dataclass
class ToolCallInfo:
    """Information about a single tool call."""

    tool_name: str
    arguments: dict


@dataclass
class QueryResult:
    """Result of running a query against the agent."""

    output: str
    tool_calls: list[ToolCallInfo]
    reasoning: str | None = None  # Model-provided reasoning summary text (if returned)
    usage: RunUsage | None = None  # Token usage from the model
    tool_response_content: str | None = None  # Raw content returned by the tool
    error: str | None = None


# =============================================================================
# Model Configuration
# =============================================================================


def get_model(
    reasoning_effort: str | None = DEFAULT_REASONING,
    seed: int | None = None,
    temperature: float | None = None,
    deployment: str | None = None,
) -> tuple[OpenAIResponsesModel, dict, DefaultAzureCredential | None]:
    """Configure the model for Azure OpenAI.

    Args:
        reasoning_effort: Optional reasoning effort level (none, minimal, low, medium, high, xhigh)
        seed: Optional seed for determinism/reproducibility
        temperature: Optional sampling temperature
        deployment: Optional deployment name (defaults to AZURE_OPENAI_CHAT_DEPLOYMENT env var)

    Returns:
        Tuple of (model, model_settings, async_credential)
    """
    api_key = os.environ.get("AZURE_OPENAI_KEY")
    if api_key:
        client = AsyncOpenAI(
            base_url=os.environ["AZURE_OPENAI_ENDPOINT"],
            api_key=api_key,
        )
        async_credential = None
    else:
        async_credential = DefaultAzureCredential()
        token_provider = get_bearer_token_provider(async_credential, "https://cognitiveservices.azure.com/.default")
        client = AsyncOpenAI(
            base_url=os.environ["AZURE_OPENAI_ENDPOINT"],
            api_key=token_provider,
        )
    deployment_name = deployment or os.environ["AZURE_OPENAI_CHAT_DEPLOYMENT"]
    model = OpenAIResponsesModel(deployment_name, provider=OpenAIProvider(openai_client=client))

    model_settings: dict = {}
    if reasoning_effort is not None and _supports_openai_reasoning(deployment_name):
        # Model settings with reasoning enabled
        # Use openai_reasoning_effort and openai_reasoning_summary keys for OpenAIResponsesModel
        # See: https://ai.pydantic.dev/models/openai/#openai-responses
        model_settings.update(
            {
                "openai_reasoning_effort": reasoning_effort,
                # NOTE: For GPT-5 models, OpenAI docs indicate `summary="auto"` is
                # equivalent to the most detailed summarizer available (typically `detailed`).
                # We keep this set to `auto` to match recommended usage.
                "openai_reasoning_summary": "auto",
            }
        )
    elif reasoning_effort is not None:
        logger.info(
            "Model '%s' does not support reasoning params; running without reasoning.*",
            deployment_name,
        )
    # Seed is supported and useful for reproducibility.
    if seed is not None:
        model_settings["seed"] = seed

    # Temperature is supported by many models/deployments (e.g., gpt-4.1-mini).
    # If not provided, we leave it unset to use the provider default.
    if temperature is not None:
        model_settings["temperature"] = temperature
    return model, model_settings, async_credential


def _get_logfire_project_url() -> str | None:
    """Return the Logfire project URL if available.

    This reads the local credentials file created by `logfire auth`.
    """
    try:
        creds_path = Path(".logfire") / "logfire_credentials.json"
        if not creds_path.exists():
            return None
        data = json.loads(creds_path.read_text())
        project_url = data.get("project_url")
        return project_url if isinstance(project_url, str) and project_url else None
    except Exception:
        return None


def _build_logfire_trace_url(trace_id_hex: str) -> str | None:
    """Build a Logfire UI URL that opens a trace.

    Logfire links are query-string based, e.g.:
    `...?q=trace_id%3D%27...%27&traceId=...&since=...&until=...`
    """
    project_url = _get_logfire_project_url()
    if not project_url:
        return None

    # Use a wide time window so the UI can find the span even if clocks differ.
    # The Logfire UI expects RFC3339 timestamps with `Z`.
    now = datetime.now(timezone.utc)
    since = (now - timedelta(hours=1)).isoformat().replace("+00:00", "Z")
    until = (now + timedelta(hours=1)).isoformat().replace("+00:00", "Z")

    q = f"trace_id='{trace_id_hex}'"
    params = {
        "q": q,
        "traceId": trace_id_hex,
        "since": since,
        "until": until,
    }
    return f"{project_url}?{urlencode(params)}"


# =============================================================================
# Tool Call Extraction
# =============================================================================


def extract_tool_calls(result) -> list[ToolCallInfo]:
    """Extract tool call information from agent result.

    Pydantic AI agent results contain message history with tool calls.
    """
    tool_calls = []

    for message in result.all_messages():
        if isinstance(message, ModelResponse):
            for part in message.parts:
                if isinstance(part, ToolCallPart):
                    args = part.args
                    if isinstance(args, str):
                        try:
                            args = json.loads(args)
                        except json.JSONDecodeError:
                            args = {}
                    elif not isinstance(args, dict):
                        args = {}
                    tool_calls.append(
                        ToolCallInfo(
                            tool_name=part.tool_name,
                            arguments=args,
                        )
                    )

    return tool_calls


def extract_tool_response_content(result) -> str | None:
    """Extract the raw content returned by tools from an agent result.

    Concatenates all ToolReturnPart contents into a single string.
    Useful for measuring the size of data returned by different tool variants.
    """
    parts = []
    for message in result.all_messages():
        if isinstance(message, ModelRequest):
            for part in message.parts:
                if isinstance(part, ToolReturnPart):
                    parts.append(str(part.content))
    return "\n".join(parts) if parts else None


def extract_reasoning(result) -> str | None:
    """Extract model-provided reasoning summary text from an agent result.

    For OpenAI's Responses API, reasoning summaries (if returned by the provider)
    arrive as `ResponseReasoningItem.summary` and are mapped by PydanticAI to
    `ThinkingPart` items.

    Notes:
    - This is not full chain-of-thought.
    - Some providers/deployments may not return any reasoning summary even when
      requested via `openai_reasoning_summary`.
    """
    reasoning_parts = []

    for message in result.all_messages():
        if isinstance(message, ModelResponse):
            for part in message.parts:
                if isinstance(part, ThinkingPart):
                    if part.content:
                        reasoning_parts.append(part.content)

    return "\n\n".join(reasoning_parts) if reasoning_parts else None


# =============================================================================
# Agent Factory
# =============================================================================


def create_agent(toolset, model: OpenAIResponsesModel) -> Agent[None, str]:
    """Create an agent with the given toolset.

    Args:
        toolset: The toolset (MCP server or filtered subset)
        model: The model to use
    """
    return Agent(
        model,
        system_prompt=(
            "You help users log expenses. "
            f"Today's date is {datetime.now().strftime('%B %-d, %Y')}."
        ),
        output_type=str,
        toolsets=[toolset],
    )


# =============================================================================
# Query Runner
# =============================================================================


async def run_query(
    tool_name: str,
    query: str,
    model: str | None = None,
    seed: int | None = None,
    temperature: float | None = None,
    reasoning_effort: str | None = None,
) -> QueryResult:
    """Run a single query against the agent with a specific tool.

    Args:
        tool_name: Name of the tool to use (filters to only this tool)
        query: The user query to send
        model: Optional deployment name (defaults to AZURE_OPENAI_CHAT_DEPLOYMENT env var)
        seed: Optional seed for determinism/reproducibility
        temperature: Optional sampling temperature
        reasoning_effort: Optional reasoning effort level

    Returns:
        QueryResult with output, tool calls, and optional reasoning
    """
    pydantic_model, model_settings, async_credential = get_model(
        reasoning_effort=reasoning_effort,
        seed=seed,
        temperature=temperature,
        deployment=model,
    )

    try:
        async with MCPServerStreamableHTTP(url=MCP_SERVER_URL) as server:
            # Filter to only the specified tool
            toolset = server.filtered(lambda ctx, tool, tn=tool_name: tool.name == tn)

            agent = create_agent(toolset, pydantic_model)
            result = await agent.run(query, model_settings=model_settings)

            tool_calls = extract_tool_calls(result)
            reasoning = extract_reasoning(result)
            tool_response_content = extract_tool_response_content(result)

            return QueryResult(
                output=result.output,
                tool_calls=tool_calls,
                reasoning=reasoning,
                usage=result.usage(),
                tool_response_content=tool_response_content,
            )

    except Exception as e:
        logger.exception(f"Error running query with tool {tool_name}")
        return QueryResult(
            output="",
            tool_calls=[],
            error=str(e),
        )
    finally:
        if async_credential:
            await async_credential.close()


# =============================================================================
# Main (CLI)
# =============================================================================

DEFAULT_TOOL = "add_expense_cat_c"
DEFAULT_QUERY = "Yesterday I bought a laptop for $1200."


def parse_args() -> argparse.Namespace:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description="Run Pydantic AI agent with MCP tool schema variants")
    parser.add_argument(
        "--tools",
        type=str,
        default=DEFAULT_TOOL,
        help=f"Comma-separated list of allowed tools (default: {DEFAULT_TOOL})",
    )
    parser.add_argument(
        "--query",
        type=str,
        default=DEFAULT_QUERY,
        help=f"Query to send to the agent (default: '{DEFAULT_QUERY}')",
    )
    parser.add_argument(
        "--reasoning",
        type=str,
        default=DEFAULT_REASONING,
        choices=REASONING_LEVELS,
        help="Reasoning effort level (optional; if omitted, not sent)",
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=42,
        help="Seed for reproducibility (default: 42)",
    )
    parser.add_argument(
        "--temperature",
        type=float,
        default=None,
        help="Sampling temperature (e.g., 0-2). If omitted, provider default is used.",
    )
    parser.add_argument(
        "--show-tool-calls",
        action="store_true",
        help="Print extracted tool calls after the run (default: off)",
    )
    parser.add_argument(
        "--show-reasoning",
        action="store_true",
        help="Print extracted reasoning summary text after the run (default: off)",
    )
    parser.add_argument(
        "--env-file",
        type=str,
        default=None,
        help="Path to .env file (default: .env)",
    )
    return parser.parse_args()


async def main():
    """Run the agent with command line arguments."""
    args = parse_args()

    # Re-load env from specified file if provided
    if args.env_file:
        load_dotenv(args.env_file, override=True)

    allowed_tools = args.tools.split(",")
    logger.info(f"Using tools: {allowed_tools}")
    logger.info(f"Using seed: {args.seed}")
    if args.reasoning is not None:
        logger.info(f"Using reasoning: {args.reasoning}")
    if args.temperature is not None:
        logger.info(f"Using temperature: {args.temperature}")

    model, model_settings, async_credential = get_model(
        args.reasoning,
        seed=args.seed,
        temperature=args.temperature,
    )

    try:
        async with MCPServerStreamableHTTP(url=MCP_SERVER_URL) as server:
            # Filter tools to allowed list
            # Reference: https://ai.pydantic.dev/toolsets/#filtering-tools
            toolset = server.filtered(lambda ctx, tool: tool.name in allowed_tools)

            agent = create_agent(toolset, model)

            logger.info(f"Query: {args.query}")

            tracer = otel_trace.get_tracer(__name__)
            with tracer.start_as_current_span("pydanticai.run") as span:
                ctx = span.get_span_context()
                trace_id_hex = f"{ctx.trace_id:032x}"
                result = await agent.run(args.query, model_settings=model_settings)
                print(f"Result: {result.output}")

                if args.show_tool_calls:
                    tool_calls = extract_tool_calls(result)
                    print("Tool calls:")
                    if tool_calls:
                        for call in tool_calls:
                            print(f"- {call.tool_name}: {call.arguments}")
                    else:
                        print("- (none)")

                if args.show_reasoning:
                    reasoning = extract_reasoning(result)
                    print("Reasoning summary:")
                    print(reasoning if reasoning else "(none returned)")

            trace_url = _build_logfire_trace_url(trace_id_hex)
            if trace_url:
                print("Logfire trace:")
                print(trace_url)
            else:
                print(f"Logfire trace id: {trace_id_hex}")
    finally:
        if async_credential:
            await async_credential.close()


if __name__ == "__main__":
    asyncio.run(main())
