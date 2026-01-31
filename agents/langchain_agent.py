"""LangChain agent for testing MCP tool schema variants.

This module provides reusable functions for running agents against MCP tool servers
using the LangChain framework.

Usage:
    # Start the MCP server first:
    uv run python servers/expenses_mcp.py

    # Run with default tool (add_expense_cat_c):
    uv run python agents/langchain_agent.py

    # Run with specific tool variant:
    uv run python agents/langchain_agent.py --tools add_expense_cat_a

    # Run with custom query:
    uv run python agents/langchain_agent.py --query "I spent $50 on groceries today"
"""

import argparse
import asyncio
import logging
import os
from dataclasses import dataclass
from datetime import datetime

from azure.identity import DefaultAzureCredential, get_bearer_token_provider
from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_openai import ChatOpenAI

load_dotenv(override=True)

logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger("langchain_agent")
logger.setLevel(logging.INFO)

# =============================================================================
# Configuration
# =============================================================================

MCP_SERVER_URL = os.getenv("MCP_SERVER_URL", "http://localhost:8000/mcp")


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


def get_model(
    temperature: float | None = None,
    deployment: str | None = None,
    reasoning_effort: str | None = None,
) -> ChatOpenAI:
    """Configure the model for Azure OpenAI using Responses API.

    Args:
        temperature: Optional sampling temperature
        deployment: Optional deployment name (defaults to AZURE_OPENAI_CHAT_DEPLOYMENT env var)
        reasoning_effort: Optional reasoning effort level (low, medium, high)

    Returns:
        Configured ChatOpenAI instance using Azure Responses API
    """
    credential = DefaultAzureCredential()
    token_provider = get_bearer_token_provider(credential, "https://cognitiveservices.azure.com/.default")
    deployment_name = deployment or os.environ.get("AZURE_OPENAI_CHAT_DEPLOYMENT", "gpt-4.1-mini")

    # Build reasoning config if specified
    reasoning = None
    if reasoning_effort is not None:
        reasoning = {"effort": reasoning_effort, "summary": "auto"}

    # Use ChatOpenAI with base_url pointing to Azure Responses API
    # (AZURE_OPENAI_ENDPOINT already includes /openai/v1/ path)
    return ChatOpenAI(
        model=deployment_name,
        base_url=os.environ["AZURE_OPENAI_ENDPOINT"],
        api_key=token_provider,
        use_responses_api=True,
        temperature=temperature,
        reasoning=reasoning
    )


# =============================================================================
# Tool Call Extraction
# =============================================================================


def extract_tool_calls(messages: list) -> list[ToolCallInfo]:
    """Extract tool call information from LangChain agent messages.

    Args:
        messages: List of messages from agent response

    Returns:
        List of ToolCallInfo objects
    """
    tool_calls = []

    for message in messages:
        if isinstance(message, AIMessage) and message.tool_calls:
            for tc in message.tool_calls:
                tool_calls.append(
                    ToolCallInfo(
                        tool_name=tc["name"],
                        arguments=tc.get("args", {}),
                    )
                )

    return tool_calls


def extract_reasoning(messages: list) -> str | None:
    """Extract reasoning summary from LangChain agent messages.

    For OpenAI Responses API models with reasoning, the summary appears in
    AIMessage.content_blocks with type='reasoning'.

    Args:
        messages: List of messages from agent response

    Returns:
        Reasoning summary text or None if not available
    """
    reasoning_parts = []

    for message in messages:
        if isinstance(message, AIMessage):
            # Responses API: reasoning is in content_blocks with type='reasoning'
            content_blocks = getattr(message, "content_blocks", None)
            if content_blocks:
                for block in content_blocks:
                    if isinstance(block, dict) and block.get("type") == "reasoning":
                        reasoning_text = block.get("reasoning")
                        if reasoning_text:
                            reasoning_parts.append(reasoning_text)

    return "\n\n".join(reasoning_parts) if reasoning_parts else None


# =============================================================================
# Query Runner
# =============================================================================


async def run_query(
    tool_name: str,
    query: str,
    model: str | None = None,
    temperature: float | None = None,
    reasoning_effort: str | None = None,
) -> QueryResult:
    """Run a single query against the agent with a specific tool.

    Args:
        tool_name: Name of the tool to use (filters to only this tool)
        query: The user query to send
        model: Optional deployment name (defaults to AZURE_OPENAI_CHAT_DEPLOYMENT env var)
        temperature: Optional sampling temperature
        reasoning_effort: Optional reasoning effort level (low, medium, high)

    Returns:
        QueryResult with output, tool calls, and optional error
    """
    try:
        llm = get_model(temperature=temperature, deployment=model, reasoning_effort=reasoning_effort)

        # Initialize MCP client
        client = MultiServerMCPClient(
            {
                "expenses": {
                    "url": MCP_SERVER_URL,
                    "transport": "streamable_http",
                }
            }
        )

        # Get tools and filter to the specified tool
        all_tools = await client.get_tools()
        tools = [t for t in all_tools if t.name == tool_name]

        if not tools:
            return QueryResult(
                output="",
                tool_calls=[],
                error=f"Tool '{tool_name}' not found",
            )

        agent = create_agent(llm, tools)

        # Prepare query with context
        today = datetime.now().strftime("%Y-%m-%d")
        system_prompt = f"You help users log expenses. Today's date is {today}."

        # Invoke agent
        response = await agent.ainvoke(
            {"messages": [SystemMessage(content=system_prompt), HumanMessage(content=query)]}
        )

        # Extract tool calls from messages
        messages = response.get("messages", [])
        tool_calls = extract_tool_calls(messages)
        reasoning = extract_reasoning(messages)

        # Get final response
        final_message = messages[-1] if messages else None
        output = final_message.content if final_message else ""

        return QueryResult(
            output=output,
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
    parser = argparse.ArgumentParser(description="Run LangChain agent with MCP tool schema variants")
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
