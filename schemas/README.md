# Tool Schemas

Auto-generated JSON schemas for all MCP tool variants.
Run `uv run python scripts/generate_schemas.py` to regenerate.

## Schema Differences by Variant

This section documents how different Python type annotations translate to JSON Schema,
which affects how LLMs interpret the tool parameters.

### Category Field Variants

Testing constrained value handling:

| Variant | Python Type | JSON Schema Result |
| ------- | ----------- | ------------------ |
| `add_expense_cat_a` | `str` | `{"type": "string"}` — No constraints |
| `add_expense_cat_b` | `Annotated[str, "hint"]` | `{"type": "string", "description": "hint"}` |
| `add_expense_cat_c` | `Literal[...]` | `{"type": "string", "enum": [...]}` — Explicit enum |
| `add_expense_cat_d` | `Enum` | `{"type": "string", "enum": [...]}` — Same as Literal |

**Key finding:** Both `Literal` and `Enum` produce identical JSON Schema with explicit `enum` arrays.

### Date Field Variants

Testing date format handling:

| Variant | Python Type | JSON Schema Result |
| ------- | ----------- | ------------------ |
| `add_expense_date_a` | `str` | `{"type": "string"}` — No format hint |
| `add_expense_date_b` | `Annotated[str, "YYYY-MM-DD"]` | `{"type": "string", "description": "..."}` |
| `add_expense_date_c` | `date` | `{"type": "string", "format": "date"}` — ISO 8601 |
| `add_expense_date_d` | `Annotated[str, Field(pattern=...)]` | `{"type": "string", "pattern": "..."}` |

**Key finding:** Python's `date` type produces `"format": "date"` (ISO 8601).

### Output Schema Variants

Testing return type handling:

| Variant | Python Return Type | outputSchema Result |
| ------- | ----------------- | ------------------- |
| `get_expenses_a` | `str` | `{"result": {"type": "string"}}` |
| `get_expenses_b` | `list[dict]` | `{"result": {"type": "array", "items": {...}}}` |
| `get_expenses_c` | `list[Expense]` | Full Pydantic model schema |

**Key finding:** Typed Pydantic models produce rich schemas with field descriptions.

## Schema Diffs

Unified diffs comparing each variant against the baseline (`_a` variant).

### Category Variants

#### `add_expense_cat_a` → `add_expense_cat_b`

```diff
--- add_expense_cat_a.json+++ add_expense_cat_b.json@@ -8,6 +8,7 @@         "type": "number"
       },
       "category": {
+        "description": "Must be one of: food, transport, entertainment, shopping, gadget, other",
         "type": "string"
       },
       "description": {
```

#### `add_expense_cat_a` → `add_expense_cat_c`

```diff
--- add_expense_cat_a.json+++ add_expense_cat_c.json@@ -8,6 +8,14 @@         "type": "number"
       },
       "category": {
+        "enum": [
+          "food",
+          "transport",
+          "entertainment",
+          "shopping",
+          "gadget",
+          "other"
+        ],
         "type": "string"
       },
       "description": {
```

#### `add_expense_cat_a` → `add_expense_cat_d`

```diff
--- add_expense_cat_a.json+++ add_expense_cat_d.json@@ -8,6 +8,14 @@         "type": "number"
       },
       "category": {
+        "enum": [
+          "food",
+          "transport",
+          "entertainment",
+          "shopping",
+          "gadget",
+          "other"
+        ],
         "type": "string"
       },
       "description": {
```

### Date Variants

#### `add_expense_date_a` → `add_expense_date_b`

```diff
--- add_expense_date_a.json+++ add_expense_date_b.json@@ -22,6 +22,7 @@         "type": "string"
       },
       "expense_date": {
+        "description": "Date in YYYY-MM-DD format",
         "type": "string"
       }
     },
```

#### `add_expense_date_a` → `add_expense_date_c`

```diff
--- add_expense_date_a.json+++ add_expense_date_c.json@@ -22,6 +22,7 @@         "type": "string"
       },
       "expense_date": {
+        "format": "date",
         "type": "string"
       }
     },
```

#### `add_expense_date_a` → `add_expense_date_d`

```diff
--- add_expense_date_a.json+++ add_expense_date_d.json@@ -22,6 +22,7 @@         "type": "string"
       },
       "expense_date": {
+        "pattern": "^\\d{4}-\\d{2}-\\d{2}$",
         "type": "string"
       }
     },
```

### Output Variants

#### `get_expenses_a` → `get_expenses_b`

```diff
--- get_expenses_a.json+++ get_expenses_b.json@@ -14,7 +14,11 @@   "outputSchema": {
     "properties": {
       "result": {
-        "type": "string"
+        "items": {
+          "additionalProperties": true,
+          "type": "object"
+        },
+        "type": "array"
       }
     },
     "required": [
```

#### `get_expenses_a` → `get_expenses_c`

```diff
--- get_expenses_a.json+++ get_expenses_c.json@@ -14,7 +14,36 @@   "outputSchema": {
     "properties": {
       "result": {
-        "type": "string"
+        "items": {
+          "description": "A single expense record.",
+          "properties": {
+            "amount": {
+              "description": "Amount spent",
+              "type": "number"
+            },
+            "category": {
+              "description": "Category of expense",
+              "type": "string"
+            },
+            "date": {
+              "description": "Date of the expense",
+              "format": "date",
+              "type": "string"
+            },
+            "description": {
+              "description": "Description of the expense",
+              "type": "string"
+            }
+          },
+          "required": [
+            "date",
+            "amount",
+            "category",
+            "description"
+          ],
+          "type": "object"
+        },
+        "type": "array"
       }
     },
     "required": [
```

## MCP Backwards Compatibility

FastMCP tool results include both:

- `content`: Text representation (backwards-compatible)
- `structuredContent`: Typed data matching outputSchema

Verified by `scripts/verify_content_field.py`.

## Tools

### add_expense_cat_a

Add a new expense for the given date, amount, category, and description.

**Input parameters:**

- `expense_date`: string
- `amount`: number
- `category`: string
- `description`: string

**Output schema:** See `add_expense_cat_a.json`

### add_expense_cat_b

Add a new expense for the given date, amount, category, and description.

**Input parameters:**

- `expense_date`: string
- `amount`: number
- `category`: string — Must be one of: food, transport, entertainment, shopping, gadget, other
- `description`: string

**Output schema:** See `add_expense_cat_b.json`

### add_expense_cat_c

Add a new expense for the given date, amount, category, and description.

**Input parameters:**

- `expense_date`: string
- `amount`: number
- `category`: enum: ['food', 'transport', 'entertainment', 'shopping', 'gadget', 'other']
- `description`: string

**Output schema:** See `add_expense_cat_c.json`

### add_expense_cat_d

Add a new expense for the given date, amount, category, and description.

**Input parameters:**

- `expense_date`: string
- `amount`: number
- `category`: enum: ['food', 'transport', 'entertainment', 'shopping', 'gadget', 'other']
- `description`: string

**Output schema:** See `add_expense_cat_d.json`

### add_expense_date_a

Add a new expense for the given date, amount, category, and description.

**Input parameters:**

- `expense_date`: string
- `amount`: number
- `category`: enum: ['food', 'transport', 'entertainment', 'shopping', 'gadget', 'other']
- `description`: string

**Output schema:** See `add_expense_date_a.json`

### add_expense_date_b

Add a new expense for the given date, amount, category, and description.

**Input parameters:**

- `expense_date`: string — Date in YYYY-MM-DD format
- `amount`: number
- `category`: enum: ['food', 'transport', 'entertainment', 'shopping', 'gadget', 'other']
- `description`: string

**Output schema:** See `add_expense_date_b.json`

### add_expense_date_c

Add a new expense for the given date, amount, category, and description.

**Input parameters:**

- `expense_date`: string
- `amount`: number
- `category`: enum: ['food', 'transport', 'entertainment', 'shopping', 'gadget', 'other']
- `description`: string

**Output schema:** See `add_expense_date_c.json`

### add_expense_date_d

Add a new expense for the given date, amount, category, and description.

**Input parameters:**

- `expense_date`: string (pattern: `^\d{4}-\d{2}-\d{2}$`)
- `amount`: number
- `category`: enum: ['food', 'transport', 'entertainment', 'shopping', 'gadget', 'other']
- `description`: string

**Output schema:** See `add_expense_date_d.json`

### get_expenses_a

Get all expenses. Returns: formatted text string.

**Output schema:** See `get_expenses_a.json`

### get_expenses_b

Get all expenses. Returns: untyped list of dicts.

**Output schema:** See `get_expenses_b.json`

### get_expenses_c

Get all expenses. Returns: typed list of Expense models.

**Output schema:** See `get_expenses_c.json`

