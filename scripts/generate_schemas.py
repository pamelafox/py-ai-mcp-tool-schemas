"""Generate JSON schemas for all MCP tool variants.

Usage:
    # Start the MCP server first:
    uv run python servers/expenses_mcp.py

    # Generate schemas:
    uv run python scripts/generate_schemas.py

Saves schemas to schemas/ directory, one JSON file per tool.
"""

import asyncio
import difflib
import json
from pathlib import Path

from mcp import ClientSession
from mcp.client.streamable_http import streamable_http_client

MCP_SERVER_URL = "http://localhost:8000/mcp"
SCHEMAS_DIR = Path(__file__).parent.parent / "schemas"

# Variant groups for diff generation (baseline is first in each list)
VARIANT_GROUPS = {
    "category": [
        "add_expense_cat_a",
        "add_expense_cat_b",
        "add_expense_cat_c",
        "add_expense_cat_d",
        "add_expense_cat_e",
    ],
    "date": ["add_expense_date_a", "add_expense_date_b", "add_expense_date_c", "add_expense_date_d"],
    "description": ["add_expense_desc_a", "add_expense_desc_b", "add_expense_desc_c", "add_expense_desc_d"],
    # Compare a flat-args baseline against a nested-object Pydantic model input.
    "input_shape": ["add_expense_cat_d", "add_expense_model_a"],
    "output": ["get_expenses_a", "get_expenses_b", "get_expenses_c"],
}


async def fetch_tools() -> list[dict]:
    """Fetch tool definitions from the MCP server."""
    async with streamable_http_client(MCP_SERVER_URL) as (read_stream, write_stream, _):
        async with ClientSession(read_stream, write_stream) as session:
            await session.initialize()
            result = await session.list_tools()
            # Convert Tool objects to dicts
            return [tool.model_dump(mode="json") for tool in result.tools]


def generate_diff(baseline: dict, variant: dict, baseline_name: str, variant_name: str) -> str:
    """Generate unified diff between two schemas."""
    # Remove fields that are always different or not informative for comparison
    exclude_keys = {"name", "description"}
    baseline_filtered = {k: v for k, v in baseline.items() if k not in exclude_keys}
    variant_filtered = {k: v for k, v in variant.items() if k not in exclude_keys}

    baseline_json = json.dumps(baseline_filtered, indent=2, sort_keys=True).splitlines(keepends=True)
    variant_json = json.dumps(variant_filtered, indent=2, sort_keys=True).splitlines(keepends=True)

    diff = difflib.unified_diff(
        baseline_json,
        variant_json,
        fromfile=f"{baseline_name}.json",
        tofile=f"{variant_name}.json",
        lineterm="",
    )
    return "".join(diff)


def generate_group_diffs(tools_by_name: dict[str, dict], group_name: str, variant_names: list[str]) -> str:
    """Generate diffs for a variant group, comparing all to baseline (first variant)."""
    if not variant_names or variant_names[0] not in tools_by_name:
        return ""

    baseline_name = variant_names[0]
    baseline = tools_by_name[baseline_name]

    output = []
    for variant_name in variant_names[1:]:
        if variant_name not in tools_by_name:
            continue

        variant = tools_by_name[variant_name]
        diff = generate_diff(baseline, variant, baseline_name, variant_name)

        if diff:
            output.append(f"#### `{baseline_name}` → `{variant_name}`\n\n")
            output.append("```diff\n")
            output.append(diff)
            if not diff.endswith("\n"):
                output.append("\n")
            output.append("```\n\n")

    return "".join(output)


async def main():
    # Create schemas directory
    SCHEMAS_DIR.mkdir(exist_ok=True)

    print(f"Fetching tools from {MCP_SERVER_URL}...")
    tools = await fetch_tools()
    print(f"Found {len(tools)} tools")

    for tool in tools:
        name = tool["name"]
        schema_file = SCHEMAS_DIR / f"{name}.json"

        # Extract the full tool definition (name, description, inputSchema, outputSchema if present)
        tool_schema = {
            "name": name,
            "description": tool.get("description", ""),
            "inputSchema": tool.get("inputSchema", {}),
        }

        # Include outputSchema if present (MCP 2025-03-26 spec)
        if "outputSchema" in tool:
            tool_schema["outputSchema"] = tool["outputSchema"]

        # Check for annotations (including content field for backwards compatibility)
        if "annotations" in tool:
            tool_schema["annotations"] = tool["annotations"]

        with open(schema_file, "w") as f:
            json.dump(tool_schema, f, indent=2)

        print(f"  Saved {schema_file.name}")

    # Generate summary markdown
    summary_file = SCHEMAS_DIR / "README.md"
    with open(summary_file, "w") as f:
        f.write("# Tool Schemas\n\n")
        f.write("Auto-generated JSON schemas for all MCP tool variants.\n")
        f.write("Run `uv run python scripts/generate_schemas.py` to regenerate.\n\n")

        # Schema differences documentation
        f.write("## Schema Differences by Variant\n\n")
        f.write("This section documents how different Python type annotations translate to JSON Schema,\n")
        f.write("which affects how LLMs interpret the tool parameters.\n\n")

        f.write("### Category Field Variants\n\n")
        f.write("Testing constrained value handling:\n\n")
        f.write("| Variant | Python Type | JSON Schema Result |\n")
        f.write("| ------- | ----------- | ------------------ |\n")
        f.write('| `add_expense_cat_a` | `str` | `{"type": "string"}` — No constraints |\n')
        f.write('| `add_expense_cat_b` | `Annotated[str, "hint"]` | `{"type": "string", "description": "hint"}` |\n')
        f.write('| `add_expense_cat_c` | `Literal[...]` | `{"type": "string", "enum": [...]}` — Explicit enum |\n')
        f.write('| `add_expense_cat_d` | `Enum` | `{"type": "string", "enum": [...]}` — Same as Literal |\n')
        f.write(
            '| `add_expense_cat_e` | `Annotated[Enum, Field(description=...)]` '
            '| `{"type": "string", "enum": [...], "description": "..."}` — Enum + guidance |\n\n'
        )
        f.write(
            "**Key finding:** Both `Literal` and `Enum` produce identical JSON Schema "
            "with explicit `enum` arrays.\n\n"
        )

        f.write("### Date Field Variants\n\n")
        f.write("Testing date format handling:\n\n")
        f.write("| Variant | Python Type | JSON Schema Result |\n")
        f.write("| ------- | ----------- | ------------------ |\n")
        f.write('| `add_expense_date_a` | `str` | `{"type": "string"}` — No format hint |\n')
        f.write(
            '| `add_expense_date_b` | `Annotated[str, "YYYY-MM-DD"]` '
            '| `{"type": "string", "description": "..."}` |\n'
        )
        f.write('| `add_expense_date_c` | `date` | `{"type": "string", "format": "date"}` — ISO 8601 |\n')
        f.write(
            '| `add_expense_date_d` | `Annotated[str, Field(pattern=...)]` '
            '| `{"type": "string", "pattern": "..."}` |\n\n'
        )
        f.write("**Key finding:** Python's `date` type produces `\"format\": \"date\"` (ISO 8601).\n\n")

        f.write("### Description Field Variants\n\n")
        f.write("Testing pattern constraints on string fields:\n\n")
        f.write("| Variant | Python Type | JSON Schema Result |\n")
        f.write("| ------- | ----------- | ------------------ |\n")
        f.write('| `add_expense_desc_a` | `str` | `{"type": "string"}` — No constraints |\n')
        f.write(
            '| `add_expense_desc_b` | `Annotated[str, "Start with capital..."]` '
            '| `{"type": "string", "description": "..."}` — Text instruction |\n'
        )
        f.write(
            '| `add_expense_desc_c` | `Annotated[str, Field(pattern=...)]` '
            '| `{"type": "string", "pattern": "^[A-Z].*\\\\.$"}` — Regex constraint |\n'
        )
        f.write(
            '| `add_expense_desc_d` | `Annotated[str, Field(pattern=..., description=...)]` '
            '| `{"type": "string", "pattern": "...", "description": "..."}` — Both |\n\n'
        )
        f.write(
            "**Key finding:** Tests whether text instructions vs regex patterns vs both "
            "are more effective at guiding model output format.\n\n"
        )

        f.write("### Input Shape Variants\n\n")
        f.write("Testing flat arguments vs a single nested Pydantic model input:\n\n")
        f.write("| Variant | Python Type | JSON Schema Result |\n")
        f.write("| ------- | ----------- | ------------------ |\n")
        f.write('| `add_expense_cat_d` | `expense_date: date, amount: float, category: Enum, description: str` | Flat `properties` at top-level |\n')
        f.write('| `add_expense_model_a` | `expense: ExpenseInput (BaseModel)` | Single top-level `expense` object with nested `properties` |\n\n')
        f.write(
            "**Key finding:** Nested object inputs can trigger different model behavior (e.g., passing a dict vs stringified JSON).\n\n"
        )

        f.write("### Output Schema Variants\n\n")
        f.write("Testing return type handling:\n\n")
        f.write("| Variant | Python Return Type | outputSchema Result |\n")
        f.write("| ------- | ----------------- | ------------------- |\n")
        f.write('| `get_expenses_a` | `str` | `{"result": {"type": "string"}}` |\n')
        f.write('| `get_expenses_b` | `list[dict]` | `{"result": {"type": "array", "items": {...}}}` |\n')
        f.write("| `get_expenses_c` | `list[Expense]` | Full Pydantic model schema |\n\n")
        f.write("**Key finding:** Typed Pydantic models produce rich schemas with field descriptions.\n\n")

        # Generate diffs section
        tools_by_name = {t["name"]: t for t in tools}

        f.write("## Schema Diffs\n\n")
        f.write("Unified diffs comparing each variant against the baseline (`_a` variant).\n\n")

        f.write("### Category Variants\n\n")
        f.write(generate_group_diffs(tools_by_name, "category", VARIANT_GROUPS["category"]))

        f.write("### Date Variants\n\n")
        f.write(generate_group_diffs(tools_by_name, "date", VARIANT_GROUPS["date"]))

        f.write("### Description Variants\n\n")
        f.write(generate_group_diffs(tools_by_name, "description", VARIANT_GROUPS["description"]))

        f.write("### Input Shape Variants\n\n")
        f.write(generate_group_diffs(tools_by_name, "input_shape", VARIANT_GROUPS["input_shape"]))

        f.write("### Output Variants\n\n")
        f.write(generate_group_diffs(tools_by_name, "output", VARIANT_GROUPS["output"]))

        f.write("## MCP Backwards Compatibility\n\n")
        f.write("FastMCP tool results include both:\n\n")
        f.write("- `content`: Text representation (backwards-compatible)\n")
        f.write("- `structuredContent`: Typed data matching outputSchema\n\n")
        f.write("Verified by `scripts/verify_content_field.py`.\n\n")

        f.write("## Tools\n\n")

        for tool in sorted(tools, key=lambda t: t["name"]):
            name = tool["name"]
            desc = tool.get("description", "")
            f.write(f"### {name}\n\n")
            f.write(f"{desc}\n\n")

            # Input schema summary
            input_schema = tool.get("inputSchema", {})
            props = input_schema.get("properties", {})
            if props:
                f.write("**Input parameters:**\n\n")
                for param_name, param_def in props.items():
                    param_type = param_def.get("type", "unknown")
                    param_desc = param_def.get("description", "")

                    # Show enum values if present
                    if "enum" in param_def:
                        param_type = f"enum: {param_def['enum']}"
                    elif "pattern" in param_def:
                        param_type = f"string (pattern: `{param_def['pattern']}`)"

                    f.write(f"- `{param_name}`: {param_type}")
                    if param_desc:
                        f.write(f" — {param_desc}")
                    f.write("\n")
                f.write("\n")

            # Output schema if present
            if "outputSchema" in tool:
                f.write(f"**Output schema:** See `{name}.json`\n\n")

    print(f"  Saved {summary_file.name}")
    print("\nDone!")


if __name__ == "__main__":
    asyncio.run(main())
