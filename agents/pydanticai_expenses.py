"""Pydantic AI agent for testing MCP tool schema variants.

Usage:
    # Start the MCP server first:
    uv run python servers/expenses_mcp.py

    # Run with default tool (add_expense_cat_c):
    uv run python agents/pydanticai_expenses.py

    # Run with specific tool variant:
    uv run python agents/pydanticai_expenses.py --tools add_expense_cat_a

    # Run with multiple tools:
    uv run python agents/pydanticai_expenses.py --tools add_expense_cat_c,get_expenses_c

    # Run with custom query:
    uv run python agents/pydanticai_expenses.py --query "I spent $50 on groceries today"

    # Run with different model provider (via env var):
    API_HOST=azure uv run python agents/pydanticai_expenses.py
"""

import argparse
import asyncio
import logging
import os
from datetime import datetime

import logfire
from azure.identity.aio import DefaultAzureCredential, get_bearer_token_provider
from dotenv import load_dotenv
from openai import AsyncOpenAI
from pydantic_ai import Agent
from pydantic_ai.mcp import MCPServerStreamableHTTP
from pydantic_ai.models.openai import OpenAIChatModel
from pydantic_ai.providers.openai import OpenAIProvider

load_dotenv(override=True)

logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger("pydanticai_expenses")
logger.setLevel(logging.INFO)

# Configure Logfire tracing if LOGFIRE_TOKEN is set
# Reference: https://logfire.pydantic.dev/docs/integrations/llms/pydanticai/
logfire.configure()
logfire.instrument_pydantic_ai()

# =============================================================================
# Model Configuration
# =============================================================================

API_HOST = os.getenv("API_HOST", "github")
MCP_SERVER_URL = os.getenv("MCP_SERVER_URL", "http://localhost:8000/mcp")


def get_model() -> tuple[OpenAIChatModel, DefaultAzureCredential | None]:
    """Configure the model based on API_HOST environment variable."""
    async_credential = None

    if API_HOST == "azure":
        async_credential = DefaultAzureCredential()
        token_provider = get_bearer_token_provider(async_credential, "https://cognitiveservices.azure.com/.default")
        client = AsyncOpenAI(
            base_url=os.environ["AZURE_OPENAI_ENDPOINT"],
            api_key=token_provider,
        )
        model = OpenAIChatModel(
            os.environ["AZURE_OPENAI_CHAT_DEPLOYMENT"], provider=OpenAIProvider(openai_client=client)
        )
    elif API_HOST == "github":
        client = AsyncOpenAI(api_key=os.environ["GITHUB_TOKEN"], base_url="https://models.inference.ai.azure.com")
        model = OpenAIChatModel(os.getenv("GITHUB_MODEL", "gpt-4o"), provider=OpenAIProvider(openai_client=client))
    elif API_HOST == "ollama":
        client = AsyncOpenAI(base_url=os.environ.get("OLLAMA_ENDPOINT", "http://localhost:11434/v1"), api_key="none")
        model = OpenAIChatModel(os.environ["OLLAMA_MODEL"], provider=OpenAIProvider(openai_client=client))
    else:
        client = AsyncOpenAI(api_key=os.environ["OPENAI_API_KEY"])
        model = OpenAIChatModel(os.environ.get("OPENAI_MODEL", "gpt-4o"), provider=OpenAIProvider(openai_client=client))

    return model, async_credential


# =============================================================================
# Agent Factory
# =============================================================================


def create_agent(toolset, model: OpenAIChatModel) -> Agent[None, str]:
    """Create an agent with the given toolset.

    Args:
        toolset: The toolset (MCP server or filtered subset)
        model: The model to use
    """
    return Agent(
        model,
        system_prompt=f"You help users log expenses. Today's date is {datetime.now().strftime('%Y-%m-%d')}.",
        output_type=str,
        toolsets=[toolset],
    )


# =============================================================================
# Main
# =============================================================================


# Default tool to use if none specified
DEFAULT_TOOL = "add_expense_cat_c"
DEFAULT_QUERY = "Yesterday I bought a laptop for $1200."


def parse_args() -> argparse.Namespace:
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
    return parser.parse_args()


async def main():
    args = parse_args()
    allowed_tools = args.tools.split(",")

    logger.info(f"Using tools: {allowed_tools}")

    model, async_credential = get_model()

    async with MCPServerStreamableHTTP(url=MCP_SERVER_URL) as server:
        # Filter tools to allowed list
        # Reference: https://ai.pydantic.dev/toolsets/#filtering-tools
        toolset = server.filtered(lambda ctx, tool: tool.name in allowed_tools)

        agent = create_agent(toolset, model)

        logger.info(f"Query: {args.query}")

        result = await agent.run(args.query)
        print(f"Result: {result.output}")

    if async_credential:
        await async_credential.close()


if __name__ == "__main__":
    asyncio.run(main())
