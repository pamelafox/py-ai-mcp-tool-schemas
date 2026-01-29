"""Verify FastMCP tool result format.

Checks that tool call results include both `content` (backwards-compatible)
and `structuredContent` fields per MCP spec 2025-03-26.
"""

import asyncio
import json

from mcp import ClientSession
from mcp.client.streamable_http import streamable_http_client

MCP_SERVER_URL = "http://localhost:8000/mcp"


async def main():
    async with streamable_http_client(MCP_SERVER_URL) as (read_stream, write_stream, _):
        async with ClientSession(read_stream, write_stream) as session:
            await session.initialize()

            # Call get_expenses_c which returns typed data
            print("Calling get_expenses_c...")
            result = await session.call_tool("get_expenses_c", {})

            print(f"\nResult type: {type(result).__name__}")
            print(f"Result fields: {result.model_dump(mode='json').keys()}")

            # Check for content field (backwards-compatible text)
            if result.content:
                print(f"\n✓ content field present ({len(result.content)} items)")
                for i, item in enumerate(result.content):
                    print(f"  [{i}] type={item.type}, ", end="")
                    if hasattr(item, "text"):
                        text_preview = item.text[:100] + "..." if len(item.text) > 100 else item.text
                        print(f"text={text_preview!r}")
                    else:
                        print(f"data={item}")
            else:
                print("\n✗ content field MISSING")

            # Check for structuredContent field (typed data)
            if hasattr(result, "structuredContent") and result.structuredContent:
                print("\n✓ structuredContent field present")
                print(f"  {json.dumps(result.structuredContent, indent=2)[:500]}")
            else:
                print("\n? structuredContent field not present (may be optional)")

            # Full result dump for inspection
            print("\n--- Full result ---")
            print(json.dumps(result.model_dump(mode="json"), indent=2))


if __name__ == "__main__":
    asyncio.run(main())
