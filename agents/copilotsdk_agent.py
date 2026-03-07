"""GitHub Copilot SDK agent for testing MCP tool schema variants.

This module provides reusable functions for running agents against MCP tool servers
using the GitHub Copilot SDK.

Usage:
    # Start the MCP server first:
    uv run python servers/expenses_mcp.py

    # Run with default tool (add_expense_cat_c):
    uv run python agents/copilotsdk_agent.py

    # Run with specific tool variant:
    uv run python agents/copilotsdk_agent.py --tools add_expense_cat_a

    # Run with custom query:
    uv run python agents/copilotsdk_agent.py --query "I spent $50 on groceries today"
"""

import argparse
import asyncio
import logging
import os
from dataclasses import dataclass
from datetime import datetime

from copilot import CopilotClient, PermissionHandler, SessionConfig
from copilot.generated.session_events import SessionEvent, SessionEventType
from copilot.types import CopilotClientOptions, MCPRemoteServerConfig
from dotenv import load_dotenv

load_dotenv(override=True)

logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger("copilot_expenses")
logger.setLevel(logging.INFO)

# =============================================================================
# Configuration
# =============================================================================

MCP_SERVER_URL = os.getenv("MCP_SERVER_URL", "http://localhost:8000/mcp")

# Available models for Copilot SDK
COPILOT_MODELS = ["gpt-5", "gpt-5.3-codex", "claude-sonnet-4", "claude-sonnet-4.5", "claude-haiku-4.5"]
DEFAULT_COPILOT_MODEL = "claude-haiku-4.5"


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
# Query Runner
# =============================================================================


async def run_query(
    tool_name: str,
    query: str,
    model: str | None = None,
) -> QueryResult:
    """Run a single query against the agent with a specific tool.

    Args:
        tool_name: Name of the tool to use (filters to only this tool)
        query: The user query to send
        model: Model name to use. Available: 'gpt-5', 'claude-sonnet-4', 
               'claude-sonnet-4.5', 'claude-haiku-4.5'. Defaults to 'gpt-5'.

    Returns:
        QueryResult with output, tool calls, and optional reasoning
    """
    deployment = model or DEFAULT_COPILOT_MODEL

    tool_calls: list[ToolCallInfo] = []
    output_parts: list[str] = []
    reasoning_parts: list[str] = []

    def handle_event(event: SessionEvent):
        """Handle events from the Copilot session."""
        nonlocal tool_calls, output_parts, reasoning_parts

        if event.type == SessionEventType.TOOL_EXECUTION_START:
            # Extract tool call info from START event (has tool_name and arguments)
            if hasattr(event, "data") and event.data:
                data = event.data
                # Use mcp_tool_name for the actual tool name (without server prefix)
                tool_name_val = getattr(data, "mcp_tool_name", None) or getattr(data, "tool_name", None)
                args = getattr(data, "arguments", None)
                if tool_name_val:
                    tool_calls.append(ToolCallInfo(
                        tool_name=tool_name_val,
                        arguments=args if isinstance(args, dict) else {}
                    ))

        elif event.type == SessionEventType.ASSISTANT_MESSAGE:
            # Capture full message content
            if hasattr(event, "data") and event.data and hasattr(event.data, "content"):
                content = event.data.content
                if content:
                    output_parts.append(str(content))

        elif event.type == SessionEventType.ASSISTANT_REASONING:
            # Capture reasoning if available
            if hasattr(event, "data") and event.data and hasattr(event.data, "content"):
                content = event.data.content
                if content:
                    reasoning_parts.append(str(content))

    client = None
    session = None
    try:
        client = CopilotClient(
            options=CopilotClientOptions(
                github_token=os.getenv("GITHUB_TOKEN"),  # Set if using GitHub auth
                azure_openai_endpoint=os.environ.get("AZURE_OPENAI_ENDPOINT"),
                azure_openai_deployment=deployment,
            )
        )

        session_config = SessionConfig(
            model=deployment,
            mcp_servers={
                "expenses": MCPRemoteServerConfig(
                    type="http",
                    url=MCP_SERVER_URL,
                    tools=[tool_name],  # Filter to specific tool
                )
            },
            system_message={
                "mode": "replace",
                "content": (
                    "You help users log expenses. "
                    f"Today's date is {datetime.now().strftime('%Y-%m-%d')}."
                ),
            },
            on_permission_request=PermissionHandler.approve_all,
        )

        session = await client.create_session(session_config)
        session.on(handle_event)

        await session.send_and_wait({"prompt": query})

        output = "\n".join(output_parts) if output_parts else ""
        reasoning = "\n\n".join(reasoning_parts) if reasoning_parts else None

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
    finally:
        # Clean up session and client to prevent memory leaks
        if session is not None:
            await session.destroy()
        if client is not None:
            await client.stop()


# =============================================================================
# Main (CLI)
# =============================================================================

DEFAULT_TOOL = "add_expense_cat_c"
DEFAULT_QUERY = "Yesterday I bought a laptop for $1200."


def parse_args() -> argparse.Namespace:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description="Run Copilot SDK agent with MCP tool schema variants")
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
        choices=COPILOT_MODELS,
        help=f"Model to use (default: {DEFAULT_COPILOT_MODEL})",
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
