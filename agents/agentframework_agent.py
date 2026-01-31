"""Microsoft Agent Framework agent for testing MCP tool schema variants.

This module provides reusable functions for running agents against MCP tool servers
using the Microsoft Agent Framework.

Usage:
    # Start the MCP server first:
    uv run python servers/expenses_mcp.py

    # Run with default tool (add_expense_cat_c):
    uv run python agents/agentframework_agent.py

    # Run with specific tool variant:
    uv run python agents/agentframework_agent.py --tools add_expense_cat_a

    # Run with custom query:
    uv run python agents/agentframework_agent.py --query "I spent $50 on groceries today"
"""

import argparse
import asyncio
import json
import logging
import os
from dataclasses import dataclass
from datetime import datetime

from agent_framework import ChatAgent, MCPStreamableHTTPTool
from agent_framework.azure import AzureOpenAIResponsesClient
from azure.identity import DefaultAzureCredential, get_bearer_token_provider
from dotenv import load_dotenv
from rich.logging import RichHandler

load_dotenv(override=True)

# Configure logging
logging.basicConfig(level=logging.WARNING, format="%(message)s", datefmt="[%X]", handlers=[RichHandler()])
logger = logging.getLogger("agentframework")
logger.setLevel(logging.INFO)

# =============================================================================
# Configuration
# =============================================================================

MCP_SERVER_URL = os.getenv("MCP_SERVER_URL", "http://localhost:8000/mcp/")


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
    reasoning: str | None = None
    error: str | None = None


# =============================================================================
# Model Configuration
# =============================================================================


def get_client(deployment: str | None = None):
    """Configure the Azure OpenAI Responses client.

    Args:
        deployment: Optional deployment name override (defaults to AZURE_OPENAI_CHAT_DEPLOYMENT env var)

    Returns:
        Configured AzureOpenAIResponsesClient instance.
    """
    credential = DefaultAzureCredential()
    token_provider = get_bearer_token_provider(credential, "https://cognitiveservices.azure.com/.default")

    return AzureOpenAIResponsesClient(
        ad_token_provider=token_provider,
        deployment_name=deployment or os.environ.get("AZURE_OPENAI_CHAT_DEPLOYMENT"),
        endpoint=os.environ.get("AZURE_OPENAI_ENDPOINT"),
        api_version=None,
    )


def build_chat_options(
    seed: int | None = None,
    temperature: float | None = None,
    reasoning_effort: str | None = None,
) -> dict:
    """Build chat options dict for ChatAgent.

    Args:
        seed: Optional seed for determinism/reproducibility
        temperature: Optional sampling temperature
        reasoning_effort: Optional reasoning effort level (low, medium, high)

    Returns:
        Dict of chat options to pass to ChatAgent's default_options.
    """
    options: dict = {}
    if seed is not None:
        options["seed"] = seed
    if temperature is not None:
        options["temperature"] = temperature
    if reasoning_effort is not None:
        # Request both reasoning effort and summary (to get text_reasoning content back)
        options["reasoning"] = {"effort": reasoning_effort, "summary": "auto"}
    return options


# =============================================================================
# Tool Call Extraction
# =============================================================================


def extract_tool_calls(result) -> list[ToolCallInfo]:
    """Extract tool call information from agent result.

    Agent Framework stores tool calls as Content objects in message.contents
    with type='function_call' or 'mcp_server_tool_call'.
    """
    tool_calls = []

    if hasattr(result, "messages"):
        for message in result.messages:
            if hasattr(message, "contents"):
                for content in message.contents:
                    content_type = getattr(content, "type", None)

                    if content_type == "function_call":
                        # Standard function calls
                        name = getattr(content, "name", None)
                        args = getattr(content, "arguments", {})
                        if isinstance(args, str):
                            try:
                                args = json.loads(args)
                            except json.JSONDecodeError:
                                args = {}
                        if name:
                            tool_calls.append(ToolCallInfo(tool_name=name, arguments=args or {}))

                    elif content_type == "mcp_server_tool_call":
                        # MCP tool calls
                        name = getattr(content, "tool_name", None)
                        args = getattr(content, "arguments", {})
                        if isinstance(args, str):
                            try:
                                args = json.loads(args)
                            except json.JSONDecodeError:
                                args = {}
                        if name:
                            tool_calls.append(ToolCallInfo(tool_name=name, arguments=args or {}))

    return tool_calls


def extract_reasoning(result) -> str | None:
    """Extract model-provided reasoning summary text from agent result.

    Agent Framework stores reasoning as Content objects in message.contents
    with type='text_reasoning'. The reasoning text is in the 'text' attribute.
    """
    reasoning_parts = []

    if hasattr(result, "messages"):
        for message in result.messages:
            if hasattr(message, "contents"):
                for content in message.contents:
                    content_type = getattr(content, "type", None)
                    if content_type == "text_reasoning":
                        text = getattr(content, "text", None)
                        if text:
                            reasoning_parts.append(text)

    return "\n\n".join(reasoning_parts) if reasoning_parts else None


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
        reasoning_effort: Optional reasoning effort level (low, medium, high)

    Returns:
        QueryResult with output, tool calls, and optional error.
    """
    client = get_client(model)
    chat_options = build_chat_options(seed=seed, temperature=temperature, reasoning_effort=reasoning_effort)

    try:
        async with (
            MCPStreamableHTTPTool(
                name="Expenses MCP Server",
                url=MCP_SERVER_URL,
                allowed_tools=[tool_name],
            ) as mcp_server,
            ChatAgent(
                chat_client=client,
                name="Expenses Agent",
                instructions=(
                    "You help users log expenses. "
                    f"Today's date is {datetime.now().strftime('%Y-%m-%d')}."
                ),
                default_options=chat_options if chat_options else None,
            ) as agent,
        ):
            result = await agent.run(query, tools=mcp_server)

            tool_calls = extract_tool_calls(result)
            reasoning = extract_reasoning(result)

            return QueryResult(
                output=result.text,
                tool_calls=tool_calls,
                reasoning=reasoning,
            )

    except Exception as e:
        logger.exception(f"Error running query with tool {tool_name}")
        return QueryResult(
            output="",
            tool_calls=[],
            error=str(e),
        )


# =============================================================================
# Main (CLI)
# =============================================================================

DEFAULT_TOOL = "add_expense_cat_c"
DEFAULT_QUERY = "Yesterday I bought a laptop for $1200."


def parse_args() -> argparse.Namespace:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description="Run Agent Framework agent with MCP tool schema variants")
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
        "--model",
        type=str,
        default=None,
        help="Model deployment name (defaults to AZURE_OPENAI_CHAT_DEPLOYMENT env var)",
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
        "--reasoning",
        type=str,
        default=None,
        choices=["none", "minimal", "low", "medium", "high", "xhigh"],
        help="Reasoning effort level (none, minimal, low, medium, high, xhigh). If omitted, provider default is used.",
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
    return parser.parse_args()


async def main():
    """Run the agent with command line arguments."""
    args = parse_args()
    allowed_tools = args.tools.split(",")
    logger.info(f"Using tools: {allowed_tools}")

    # For now, run with first tool if multiple specified
    tool_name = allowed_tools[0]

    result = await run_query(
        tool_name=tool_name,
        query=args.query,
        model=args.model,
        seed=args.seed,
        temperature=args.temperature,
        reasoning_effort=args.reasoning,
    )

    if result.error:
        print(f"Error: {result.error}")
    else:
        print(f"Result: {result.output}")

        if args.show_tool_calls:
            print("Tool calls:")
            if result.tool_calls:
                for call in result.tool_calls:
                    print(f"- {call.tool_name}: {call.arguments}")
            else:
                print("- (none)")

        if args.show_reasoning:
            print("Reasoning summary:")
            print(result.reasoning if result.reasoning else "(none returned)")


if __name__ == "__main__":
    asyncio.run(main())
