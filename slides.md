# Talk: **Improving MCP tool schemas to increase agent reliability**

Talk abstract:

As agents increasingly stitch together tools from many MCP servers, schema quality has become a critical factor in whether tool calls succeed at all. Agents rely entirely on tool schemas—not server code—to choose tools, construct arguments, and interpret results, making clear, expressive schemas essential for reliability. In this talk, we build MCP servers with FastMCP and Pydantic, consume them with Pydantic AI agents, and instrument runs with Logfire to observe tool selection and parsing in detail. We then evaluate tool-calling reliability and output correctness across models at scale using the Pydantic AI evaluation framework. Well-designed input and output schemas can both improve agent reliability, while also making our code more robust and type-safe. Win-win!

## Slide draft

#### Intro slide

#### About me

#### But first... let's have fun with MCP!

What if I could use MCP to pick my outfit for today?
What if I DID use MCP to pick my outfit for today...?

Add screenshot of demo
http://github.com/Azure-samples/iamge-search-mcp (update that link)

Speaker notes:
* Demo it in VS Code
* Now that the outfit is sorted.. on to the real talk!

#### A bare bones FastMCP server

Code: (left side of slide)

```python
@mcp.tool
async def add_expense(
    expense_date: str,
    amount: float,
    category: str,
    description: str,
) -> str:
    """Add a new expense."""
    ...
```

becomes this schema: (right side of slide)

```json
{
  "name": "add_expense",
  "description": "Add a new expense.",
  "inputSchema": {
    "properties": {
      "expense_date": {
        "type": "string"
      },
      "amount": {
        "type": "number"
      },
      "category": {
        "type": "string"
      },
      "description": {
        "type": "string"
      }
    },
    "required": [
      "expense_date", "amount",
      "category", "description"
    ],
    "type": "object"
  }
}
```

File: basic_server.py

Speaker notes:

* Demo the server in VS Code
* Show in Logfire with reasoning and tool calls highlighted

### LLMs can be so/too creative!

What does the model pick for the category? Across N runs:

// Insert a word cloud of all the categories chosen across many evals - invented_categories.md

## SECTION: Reign those LLMs in with better schemas!

### Annotate tool arguments with descriptions

Left side:
```python
    category: Annotated[
        str,
        Field(
            description="Must be one of: Food & drink, "
            "Transit and Fuel, Media & streaming, "
            "Apparel and Beauty, Electronics & tech, "
            "Home and office, ..."
        ),
    ],
```

Schema:
```json
"category": {
    "type": "string",
    "description": "Must be one of: Food & drink, Transit and Fuel, Media & streaming, Apparel and Beauty, Electronics & tech, Home and office, ..."
}
```

### Use constrained types like Literal or Enum

Left side:
```python
CATEGORY_LITERAL = Literal[
    "Food & drink", "Transit and Fuel",
    "Media & streaming", ...
]
    category: CATEGORY_LITERAL,
```

```python
class Category(Enum):
    FOOD_AND_DRINK = "Food & drink"
    TRANSIT_AND_FUEL = "Transit and Fuel"
    ...

    category: Category,
```

becomes:

```json
"category": {
    "type": "string",
    "enum": [
        "Food & drink", "Transit and Fuel",
        "Media & streaming", ...
    ]
}
```

### Why not both? Descriptions + constrained values!

Left side:
```python
    category: Annotated[
        Category,
        Field(
            description=(
                "Choose the closest category. "
                "If truly unclear, use Misc.\n\n"
                "Heuristics: "
                "Food & drink=meals, groceries, coffee; "
                "Transit and Fuel=rideshare, gas, parking; "
                "..."
            )
        ),
    ],
```

becomes:

```json
"category": {
    "type": "string",
    "enum": [
        "Food & drink", "Transit and Fuel",
        "Media & streaming", ...
    ],
    "description": "Choose the closest category. If truly unclear, use Misc. Heuristics: Food & drink=meals, groceries, coffee; Transit and Fuel=rideshare, gas, parking; ..."
}
```

## SECTION: Evaluating schema improvements

### PydanticAI agent with MCP server

```python
server = MCPServerStreamableHTTP(url="http://localhost:8000/mcp")

model = OpenAIResponsesModel(
    "gpt-5.3-codex",
    provider=OpenAIProvider(openai_client=azure_openai_client))

agent = Agent(
    model,
    system_prompt=(
        "You help users log expenses. "
        f"Today's date is {datetime.now().strftime('%Y-%m-%d')}."
    ),
    output_type=str,
    toolsets=[server],
)

result = await agent.run("I bought a sandwich for $12.50.")
```

Speaker notes:

* The agent connects to the MCP server over Streamable HTTP — it only sees the tool schemas, not the server code
* We set today's date in the system prompt so the model can resolve relative dates like "yesterday"
* `output_type=str` means the agent returns a plain text response after calling tools

### Filtering to one tool variant at a time

```python
server = MCPServerStreamableHTTP(url="http://localhost:8000/mcp")

for variant in ["cat_b", "cat_c", "cat_d", "cat_e"]:
    toolset = server.filtered(
        lambda ctx, tool: tool.name == f"add_expense_{variant}")
    agent = Agent(model, toolsets=[toolset], ...)
    result = await agent.run(case.prompt)
```

Speaker notes:

* `server.filtered()` takes a lambda that selects which tools the agent can see
* This lets us test one schema variant at a time against the same prompts — isolating the effect of the schema
* The MCP server exposes all variants simultaneously; filtering happens client-side

### So... which schema is the best?

Let's use Pydantic-AI evals to find out!


```python
EXPENSE_CASES = [
    ExpenseCase(
        name="clear_food_yesterday",
        prompt="Yesterday I bought a sandwich for $12.50.",
        expected_category="Food & drink",
        expected_date=get_yesterday(),
        expected_amount=12.50,
    ),
    ...  # 17 cases: clear, relative dates, edge cases
]

def evaluate_category_valid(tool_calls) -> EvalResult:
    """Is the category one of the valid enum values?"""

def evaluate_category_match(tool_calls, expected) -> EvalResult:
    """Does the category match what we expected?"""

def evaluate_date_format(tool_calls) -> EvalResult:
    """Is the date in YYYY-MM-DD format?"""

for variant in ["cat_b", "cat_c", "cat_d", "cat_e"]:
    for case in EXPENSE_CASES:
        result = await agent.run(case.prompt, tools=[variant])
        evals = run_all_evaluations(result.tool_calls, case)
```

File: evaluators.py

Speaker notes:

* We run the same set of 17 test cases across multiple schema variants to see which leads to the most accurate category and date outputs
* We can also analyze the reasoning traces to understand why certain schemas perform better or worse

### Evals: Which category schema did best?

gpt-5.3-codex, 17 cases each, with a Pydantic-AI agent:

| Schema | Category Match | Category Valid | Tool Called | Avg Input Tokens |
|--------|---------------|----------------|------------|------------------|
| `Annotated[str, ...]` | 52.9% | 64.7% | 64.7% | 286 |
| `Literal[...]` | 47.1% | 52.9% | 52.9% | 282 |
| `Enum` | 47.1% | 58.8% | 58.8% | 295 |
| 🏆 **Enum + description** | **82.4%** | **94.1%** | **94.1%** | **757** |

Speaker notes:

* **Enum + description is the clear winner** at 94% valid categories — the rich Field description gives the model the context it needs
* Bare `Literal`/`Enum` alone actually performs *worse* than an annotated string — constraint without explanation confuses the model
* `cat_e` uses ~757 avg input tokens vs ~282-295 for other variants, but that extra context pays for itself in 30+ percentage point accuracy gains
* Enums are better than Literal since we get more type safety later

## SECTION: Using schemas to guide formatting

### Bare string date

Our original `str` schema gives no guidance on the expected date format:

```python
    expense_date: str,
```

Schema:
```json
"expense_date": {
    "type": "string"
}
```

### Description hint for date format

```python
    expense_date: Annotated[
        str, "Date in YYYY-MM-DD format"
    ],
```

Schema:
```json
"expense_date": {
    "description": "Date in YYYY-MM-DD format",
    "type": "string"
}
```

### Using a Python `date` type

```python
    expense_date: date,
```

Schema:
```json
"expense_date": {
    "format": "date",
    "type": "string"
}
```

### Constraining with a Regex pattern

```python
    expense_date: Annotated[
        str,
        Field(pattern=r"^\d{4}-\d{2}-\d{2}$"),
    ],
```

Schema:
```json
"expense_date": {
    "pattern": "^\\d{4}-\\d{2}-\\d{2}$",
    "type": "string"
}
```

### Evals time! Which date schema did best?

| Schema | Date Match | Date Format | Tool Called | Avg Input Tokens |
|--------|-----------|-------------|------------|------------------|
| 🏆 `str` | 64.7% | 64.7% | 64.7% | 298 |
| 🏆 `Annotated[str, ...]` | 64.7% | 64.7% | 64.7% | 311 |
| 🏆 `date` | 64.7% | 64.7% | 64.7% | 309 |
| `Field(pattern=...)` | 50.0% | 50.0% | 50.0% | 277 |

Stricter schemas are *not* always better! But you don't know that until you evaluate.

Speaker notes:

* `str`, `Annotated[str]`, and `date` all perform identically — the model handles dates fine without extra constraints
* The **regex pattern variant is the worst performer** — it actually *hurts* accuracy
* The model gets confused by the regex and tries to match it literally instead of reasoning about the date
* That's why it's so important to evaluate! Stricter schemas are NOT always better
* Regex patterns can be useful for very specific formats (product codes, IDs), but be careful — they can confuse the model if overused

## SECTION: Do all models think alike?

### Cross-model category results

Same 17 test cases, same Pydantic AI agent, different models:

#### Category valid

| Schema | gpt-4o | gpt-4.1-mini | gpt-5.3-codex (medium) |
|--------|--------|-------------|---------------|
| `Annotated[str]` | 94.1% | 88.2% | 64.7% |
| `Literal` | 100% | 94.1% | 52.9% |
| `Enum` | 100% | 100% | 58.8% |
| 🏆 Enum + desc | 100% | 100% | 94.1% |

#### Category match

| Schema | gpt-4o | gpt-4.1-mini | gpt-5.3-codex (medium) |
|--------|--------|-------------|---------------|
| `Annotated[str]` | 94.1% | 76.5% | 52.9% |
| `Literal` | 88.2% | 76.5% | 47.1% |
| `Enum` | 82.4% | 82.4% | 47.1% |
| 🏆 Enum + desc | 100% | 88.2% | 82.4% |

#### Date format

| Schema | gpt-4o | gpt-4.1-mini | gpt-5.3-codex (medium) |
|--------|--------|-------------|---------------|
| `str` | 94.1% | 82.4% | 64.7% |
| `Annotated[str]` | 100% | 94.1% | 64.7% |
| `date` | 100% | 94.1% | 64.7% |
| `Field(pattern)` | 100% | 100% | 47.1% |

#### Date match

| Schema | gpt-4o | gpt-4.1-mini | gpt-5.3-codex (medium) |
|--------|--------|-------------|---------------|
| `str` | 76.5% | 58.8% | 64.7% |
| `Annotated[str]` | 76.5% | 64.7% | 64.7% |
| `date` | 82.4% | 64.7% | 64.7% |
| `Field(pattern)` | 82.4% | 70.6% | 47.1% |

Speaker notes:

* **cat_e (Enum + description) is the best or tied-best across every model** — the pattern holds universally
* gpt-4o with cat_e hits 100% match — but drops to 82-94% with weaker schemas, showing even strong models benefit from good schemas
* gpt-4.1-mini is interesting: with cat_b (just a description), it picks "Arts and hobbies" for a movie ticket — without the enum list to guide it, it guesses a plausible but wrong category. With cat_e it gets it right.
* gpt-4.1-mini cat_e fails on edge cases: it picks "Transit and Fuel" for a $35K car (should be Misc) and "Apparel and Beauty" for a spa treatment (should be Health & Fitness). gpt-4o gets both right.
* gpt-4.1-mini is also more cautious — 11 total no-tool-calls across variants vs only 3 for gpt-4o vs **zero** for gpt-5.3-codex. Smaller models hesitate more on ambiguous inputs.
* Both gpt-4o and gpt-4.1-mini get 100% category_valid with Enum types (cat_d, cat_e) — constrained types prevent invalid categories even when the *match* isn't right
* **Date results tell a different story**: date_d (regex) is best for gpt-4o (82.4%) and gpt-4.1-mini (70.6%), but **worst** for gpt-5.3-codex (47.1%) — the same schema can help one model and hurt another!
* gpt-4.1-mini gets 100% date format with regex (date_d) — it's more rule-following with explicit patterns
* gpt-4o is the most consistent across date variants — date_c and date_d tied at 82.4% match
* gpt-5.3-codex has identical date results for date_a/b/c (64.7%) — it doesn't benefit from hints or types, but regex actively confuses it
* gpt-5.3-codex struggles much more without rich schemas — the gap between cat_e and weaker variants *widens* as the model gets weaker
* Data sources: `evals/runs/gpt4o_rerun`, `evals/runs/gpt41mini_rerun`, `evals/runs/gpt53codex_rerun`

### Same prompt, different models, different behavior

**"Yesterday I bought a car for 35000 USD."**

With `Annotated[str]` (no enum list) — all three models **refuse to call the tool**:

**gpt-4o**: *"Buying a car is typically considered a major purchase rather than a regular expense. However, if you'd like to log it, you can categorize it under 'Transit and Fuel.' Would you like me to proceed?"*

**gpt-4.1-mini**: *"Buying a car is typically considered a major purchase or an asset rather than a regular expense... Could you please confirm how you'd like to categorize this?"*

**gpt-5.3-codex**: *"Got it — I can log that. Before I do, which category should I use? A car purchase could fit best under Misc."*

With **Enum + description** (includes heuristic: *"If truly unclear, use Misc"*):

**gpt-4o**: ✅ Calls tool → `category: "Misc"` — followed the heuristic

**gpt-4.1-mini**: ❌ Calls tool → `category: "Transit and Fuel"` — car ≈ transit?

**gpt-5.3-codex**: ❌ Calls tool → `category: "Transit and Fuel"` — same wrong reasoning

Speaker notes:

* Great example of how the description heuristic ("If truly unclear, use Misc") helps gpt-4o make the right call, but gpt-4.1-mini and codex both default to Transit and Fuel (car = vehicle = transit)
* Without any enum, ALL models hesitate — but they hesitate differently: gpt-4o and gpt-4.1-mini ask for confirmation, while codex narrates what it would do
* The Enum + description schema gives the model permission to act — it reduces clarification questions and increases tool calls
* But it doesn't guarantee the *right* category — that still depends on the model's reasoning about the heuristics

### Just THINK HARDER, models!

New reasoning models let you set the effort level — does that help with ambiguous cases?

gpt-5.2 with cat_b, same prompt: *"I spent 50 dollars on groceries."* (no date given)

**reasoning=none**: No tool call — asks a clarifying question instead

> What date should I log this for? (If it was today, I'll record **2026-01-29**.)

**reasoning=xhigh**: Picks a plausible default and proceeds

```json
{"expense_date": "2026-01-29", "amount": 50,
 "category": "food", "description": "groceries"}
```

> Logged: **$50** on **2026-01-29** under **food** (groceries).

Reasoning trace: *"The date defaults to today, 2026-01-29. The category is groceries, which falls under food..."*

Speaker notes:

* Overall accuracy was similar across reasoning levels — the main difference was in how they handled **ambiguous** cases
* `none` tends to ask the user for clarification when a required field is missing or ambiguous — it often makes no tool call at all
* `xhigh` more often picks a plausible default (e.g., today's date) and proceeds with the tool call, then explains its reasoning
* Neither behavior is inherently wrong — it depends on whether you want an assistant that asks or one that acts
* The reasoning trace from `xhigh` is useful for auditing — you can see *why* the model chose that default

## SECTION: Are all agent frameworks the same?

### Framework showdown!

Same model (gpt-5.3-codex), same 17 cases, same MCP server — different agent framework:

**Category Match %**

| Schema | Pydantic AI | Copilot SDK |
|--------|-------------|-------------|
| `Annotated[str]` | 52.9% | 76.5% |
| `Literal` | 47.1% | 76.5% |
| `Enum` | 47.1% | 81.2% |
| 🏆 Enum + desc | 82.4% | **94.1%** |

**Tool Called %**

| Schema | Pydantic AI | Copilot SDK |
|--------|-------------|-------------|
| `Annotated[str]` | 64.7% | **100%** |
| `Literal` | 52.9% | **100%** |
| `Enum` | 58.8% | **100%** |
| Enum + desc | 94.1% | **100%** |

**Date Match %**

| Schema | Pydantic AI | Copilot SDK |
|--------|-------------|-------------|
| `str` | 64.7% | 25.0% |
| `Annotated[str]` | 64.7% | 31.2% |
| `date` | 64.7% | 29.4% |
| `Field(pattern)` | 47.1% | 37.5% |

Speaker notes:

* **Copilot SDK gets 100% tool-calling** — the same model that refused to call tools 48 times via PydanticAI always calls them via Copilot SDK. Framework matters!
* Category accuracy is significantly better via Copilot SDK (76-94%) vs PydanticAI (47-82%) — possibly because the framework enforces more structured interactions
* **But date accuracy is much worse** via Copilot SDK (25-37%) vs PydanticAI (47-65%) — the model consistently picks dates off-by-one (e.g., "yesterday" → today's date instead of yesterday's). This suggests the system prompt with today's date may not be reaching the model as effectively through the Copilot SDK.
* Enum + description is still the best category schema in both frameworks — the pattern is universal
* Data sources: PydanticAI = `evals/runs/gpt53codex_rerun`, Copilot SDK = `evals/runs/copilot_53codex`

## SECTION: Tools have return schemas too!

### Return a plain string

```python
@mcp.tool
def get_expenses_a() -> str:
    """Get all expenses."""
    return "\n".join(
        f"Date: {e['date']}, Amount: ${e['amount']}, "
        f"Category: {e['category']}, ..."
        for e in expenses
    )
```

Example output:

```text
Expense data (68 entries):
Date: 2025-01-02, Amount: $4.50, Category: Food & drink, Description: Morning coffee
Date: 2025-01-02, Amount: $12.99, Category: Food & drink, Description: Lunch sandwich
Date: 2025-01-03, Amount: $45.00, Category: Transit and Fuel, Description: Gas station fill-up
...
```

Schema:

```json
"outputSchema": {
    "result": {"type": "string"}
}
```

### Return a list of dicts

```python
@mcp.tool
def get_expenses_b() -> list[dict]:
    """Get all expenses."""
    return expenses  # list of dicts
```

Example output:

```json
[
  {"date": "2025-01-02", "amount": "4.50",
   "category": "Food & drink",
   "description": "Morning coffee"},
  {"date": "2025-01-02", "amount": "12.99",
   "category": "Food & drink",
   "description": "Lunch sandwich"},
  ...
]
```

Schema:

```json
"outputSchema": {
    "result": {
        "type": "array",
        "items": {
            "type": "object",
            "additionalProperties": true
        }
    }
}
```

### Return a list of Pydantic models

```python
class Expense(BaseModel):
    """A single expense record."""
    expense_date: date = Field(
        alias="date",
        description="Date of the expense")
    amount: float = Field(
        description="Amount spent")
    category: str = Field(
        description="Category of expense")
    description: str = Field(
        description="Description of the expense")

@mcp.tool
def get_expenses_c() -> list[Expense]:
    """Get all expenses."""
    return [Expense(**e) for e in expenses]
```

Example output:

```json
[
  {"date": "2025-01-02", "amount": 4.5,
   "category": "Food & drink",
   "description": "Morning coffee"},
  {"date": "2025-01-02", "amount": 12.99,
   "category": "Food & drink",
   "description": "Lunch sandwich"},
  ...
]
```

Schema:

```json
"outputSchema": {
    "result": {
        "type": "array",
        "items": {
            "description": "A single expense record.",
            "properties": {
                "date": {"type": "string",
                    "format": "date",
                    "description": "Date of the expense"},
                "amount": {"type": "number",
                    "description": "Amount spent"},
                ...
            }
        }
    }
}
```


Speaker notes:

* Notice the amounts are now **numbers** (`4.5`) not **strings** (`"4.50"`) — Pydantic coerces the CSV string values to proper floats. I didn't even notice the difference at first! That's a hidden benefit of typed return models.

#### Eval time: Output schemas

gpt-5.3-codex, 7 cases each


| Variant | Avg Score | Avg Input Tokens | Avg Output Tokens | Avg Tool Response Size |
|---------|-----------|------------------|-------------------|------------------------|
| `get_expenses_a` (str) | 1.00 | 2155 | 53 | 6,297 chars |
| `get_expenses_b` (list[dict]) | 1.00 | 2037 | 53 | 7,494 chars |
| `get_expenses_c` (list[Expense]) | 1.00 | 2037 | 52 | 7,306 chars |

Speaker notes:

* Accuracy is identical across all three output formats — the model answers correctly regardless
* Structured variants (list[dict], Pydantic) cost **~16-19% more** in tool response size due to JSON overhead (braces, quotes, repeated keys)
* Input tokens are slightly *lower* for structured variants (schema is more concise), but the tool response size increase outweighs it
* Output tokens are nearly identical — the model generates the same answer regardless of format
* So why use structured output? For consumption by other MCPs or agents downstream — structured data is much easier to work with than unstructured text

### Conclusions

* Using MCPs with structured schemas may improve the accuracy of model outputs
* Stricter schemas aren't always better; it's important to EVALUATE and find the right balance
  * Hamel's tweet: do evalsTM
* Different models and frameworks may respond differently to schema features
* Always test and validate your schemas with real model outputs to ensure they meet your needs
* Thank you! Any questions?


## Appendix: Failure cases

### Failure cases

ambiguous_relative_date - "Last week I spent $89 on concert tickets."
Model reasoning: "I need to clarify what 'last week' means...It could refer to the previous calendar week or simply the past seven days."

ambiguous_mixed_items - "I bought coffee and a phone case for $55 yesterday."
Model reasoning: "I should ask the user how they'd like to split it...The total is $55, but it's unclear how to split this amount."

### These are intentionally underspecified; a good assistant should ask a clarifying question
#### (or apply a consistent, documented default).

ExpenseCase(
    name="ambiguous_no_date",
    prompt="I spent 50 dollars on groceries.",
    expected_category="food",
    expected_amount=50.0,
    difficulty="ambiguous",
    # Date not specified - model should use today or ask
),

### --- Ambiguous requests ---
ExpenseCase(
    name="ambiguous_vague_category",
    prompt="Yesterday I paid $30 for stuff at the store.",
    expected_date=get_yesterday(),
    expected_amount=30.0,
    difficulty="ambiguous",
    # Category unclear - could be shopping or other
),