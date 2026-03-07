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
| `add_expense_cat_e` | `Annotated[Enum, Field(description=...)]` | `{"type": "string", "enum": [...], "description": "..."}` — Enum + guidance |

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

### Description Field Variants

Testing pattern constraints on string fields:

| Variant | Python Type | JSON Schema Result |
| ------- | ----------- | ------------------ |
| `add_expense_desc_a` | `str` | `{"type": "string"}` — No constraints |
| `add_expense_desc_b` | `Annotated[str, "Start with capital..."]` | `{"type": "string", "description": "..."}` — Text instruction |
| `add_expense_desc_c` | `Annotated[str, Field(pattern=...)]` | `{"type": "string", "pattern": "^[A-Z].*\\.$"}` — Regex constraint |
| `add_expense_desc_d` | `Annotated[str, Field(pattern=..., description=...)]` | `{"type": "string", "pattern": "...", "description": "..."}` — Both |

**Key finding:** Tests whether text instructions vs regex patterns vs both are more effective at guiding model output format.

### Input Shape Variants

Testing flat arguments vs a single nested Pydantic model input:

| Variant | Python Type | JSON Schema Result |
| ------- | ----------- | ------------------ |
| `add_expense_cat_d` | `expense_date: date, amount: float, category: Enum, description: str` | Flat `properties` at top-level |
| `add_expense_model_a` | `expense: ExpenseInput (BaseModel)` | Single top-level `expense` object with nested `properties` |

**Key finding:** Nested object inputs can trigger different model behavior (e.g., passing a dict vs stringified JSON).

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
+        "description": "Must be one of: Food & drink, Transit and Fuel, Media & streaming, Apparel and Beauty, Electronics & tech, Home and office, Health & Fitness, Arts and hobbies, Fees & services, Misc",
         "type": "string"
       },
       "description": {
```

#### `add_expense_cat_a` → `add_expense_cat_c`

```diff
--- add_expense_cat_a.json+++ add_expense_cat_c.json@@ -8,6 +8,18 @@         "type": "number"
       },
       "category": {
+        "enum": [
+          "Food & drink",
+          "Transit and Fuel",
+          "Media & streaming",
+          "Apparel and Beauty",
+          "Electronics & tech",
+          "Home and office",
+          "Health & Fitness",
+          "Arts and hobbies",
+          "Fees & services",
+          "Misc"
+        ],
         "type": "string"
       },
       "description": {
```

#### `add_expense_cat_a` → `add_expense_cat_d`

```diff
--- add_expense_cat_a.json+++ add_expense_cat_d.json@@ -8,6 +8,18 @@         "type": "number"
       },
       "category": {
+        "enum": [
+          "Food & drink",
+          "Transit and Fuel",
+          "Media & streaming",
+          "Apparel and Beauty",
+          "Electronics & tech",
+          "Home and office",
+          "Health & Fitness",
+          "Arts and hobbies",
+          "Fees & services",
+          "Misc"
+        ],
         "type": "string"
       },
       "description": {
```

#### `add_expense_cat_a` → `add_expense_cat_e`

```diff
--- add_expense_cat_a.json+++ add_expense_cat_e.json@@ -8,6 +8,19 @@         "type": "number"
       },
       "category": {
+        "description": "Choose the closest category for the expense. Do not ask follow-up questions just to disambiguate the category; pick the best fit using the description and common sense. If truly unclear, use Misc.\n\nHeuristics: Food & drink=meals, groceries, coffee, restaurants, snacks; Transit and Fuel=rideshare, taxi, gas, parking, public transit, tolls; Media & streaming=movies, concerts, subscriptions, streaming, games, tickets; Apparel and Beauty=clothing, shoes, cosmetics, haircuts, personal care; Electronics & tech=devices, gadgets, accessories, apps, software; Home and office=furniture, supplies, housewares, decor, cleaning; Health & Fitness=gym, medical, wellness, supplements, pharmacy; Arts and hobbies=crafts, sports equipment, creative supplies, lessons; Fees & services=banking, professional services, insurance, subscriptions; Misc=anything that does not fit well into other categories.",
+        "enum": [
+          "Food & drink",
+          "Transit and Fuel",
+          "Media & streaming",
+          "Apparel and Beauty",
+          "Electronics & tech",
+          "Home and office",
+          "Health & Fitness",
+          "Arts and hobbies",
+          "Fees & services",
+          "Misc"
+        ],
         "type": "string"
       },
       "description": {
```

### Date Variants

#### `add_expense_date_a` → `add_expense_date_b`

```diff
--- add_expense_date_a.json+++ add_expense_date_b.json@@ -26,6 +26,7 @@         "type": "string"
       },
       "expense_date": {
+        "description": "Date in YYYY-MM-DD format",
         "type": "string"
       }
     },
```

#### `add_expense_date_a` → `add_expense_date_c`

```diff
--- add_expense_date_a.json+++ add_expense_date_c.json@@ -26,6 +26,7 @@         "type": "string"
       },
       "expense_date": {
+        "format": "date",
         "type": "string"
       }
     },
```

#### `add_expense_date_a` → `add_expense_date_d`

```diff
--- add_expense_date_a.json+++ add_expense_date_d.json@@ -26,6 +26,7 @@         "type": "string"
       },
       "expense_date": {
+        "pattern": "^\\d{4}-\\d{2}-\\d{2}$",
         "type": "string"
       }
     },
```

### Description Variants

#### `add_expense_desc_a` → `add_expense_desc_b`

```diff
--- add_expense_desc_a.json+++ add_expense_desc_b.json@@ -23,6 +23,7 @@         "type": "string"
       },
       "description": {
+        "description": "Start with a capital letter and end with a period",
         "type": "string"
       },
       "expense_date": {
```

#### `add_expense_desc_a` → `add_expense_desc_c`

```diff
--- add_expense_desc_a.json+++ add_expense_desc_c.json@@ -23,6 +23,7 @@         "type": "string"
       },
       "description": {
+        "pattern": "^[A-Z].*\\.$",
         "type": "string"
       },
       "expense_date": {
```

#### `add_expense_desc_a` → `add_expense_desc_d`

```diff
--- add_expense_desc_a.json+++ add_expense_desc_d.json@@ -23,6 +23,8 @@         "type": "string"
       },
       "description": {
+        "description": "Start with a capital letter and end with a period",
+        "pattern": "^[A-Z].*\\.$",
         "type": "string"
       },
       "expense_date": {
```

### Input Shape Variants

#### `add_expense_cat_d` → `add_expense_model_a`

```diff
--- add_expense_cat_d.json+++ add_expense_model_a.json@@ -4,37 +4,50 @@   "icons": null,
   "inputSchema": {
     "properties": {
-      "amount": {
-        "type": "number"
-      },
-      "category": {
-        "enum": [
-          "Food & drink",
-          "Transit and Fuel",
-          "Media & streaming",
-          "Apparel and Beauty",
-          "Electronics & tech",
-          "Home and office",
-          "Health & Fitness",
-          "Arts and hobbies",
-          "Fees & services",
-          "Misc"
+      "expense": {
+        "description": "Input model for adding a single expense.\n\nThis is used to test how models handle a single nested JSON object argument.",
+        "properties": {
+          "amount": {
+            "description": "Amount spent",
+            "type": "number"
+          },
+          "category": {
+            "description": "Category of expense",
+            "enum": [
+              "Food & drink",
+              "Transit and Fuel",
+              "Media & streaming",
+              "Apparel and Beauty",
+              "Electronics & tech",
+              "Home and office",
+              "Health & Fitness",
+              "Arts and hobbies",
+              "Fees & services",
+              "Misc"
+            ],
+            "type": "string"
+          },
+          "description": {
+            "description": "Description of the expense",
+            "type": "string"
+          },
+          "expense_date": {
+            "description": "Date of the expense",
+            "format": "date",
+            "type": "string"
+          }
+        },
+        "required": [
+          "expense_date",
+          "amount",
+          "category",
+          "description"
         ],
-        "type": "string"
-      },
-      "description": {
-        "type": "string"
-      },
-      "expense_date": {
-        "format": "date",
-        "type": "string"
+        "type": "object"
       }
     },
     "required": [
-      "expense_date",
-      "amount",
-      "category",
-      "description"
+      "expense"
     ],
     "type": "object"
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

Add a new expense.

**Input parameters:**

- `expense_date`: string
- `amount`: number
- `category`: string
- `description`: string

**Output schema:** See `add_expense_cat_a.json`

### add_expense_cat_b

Add a new expense.

**Input parameters:**

- `expense_date`: string
- `amount`: number
- `category`: string — Must be one of: Food & drink, Transit and Fuel, Media & streaming, Apparel and Beauty, Electronics & tech, Home and office, Health & Fitness, Arts and hobbies, Fees & services, Misc
- `description`: string

**Output schema:** See `add_expense_cat_b.json`

### add_expense_cat_c

Add a new expense.

**Input parameters:**

- `expense_date`: string
- `amount`: number
- `category`: enum: ['Food & drink', 'Transit and Fuel', 'Media & streaming', 'Apparel and Beauty', 'Electronics & tech', 'Home and office', 'Health & Fitness', 'Arts and hobbies', 'Fees & services', 'Misc']
- `description`: string

**Output schema:** See `add_expense_cat_c.json`

### add_expense_cat_d

Add a new expense.

**Input parameters:**

- `expense_date`: string
- `amount`: number
- `category`: enum: ['Food & drink', 'Transit and Fuel', 'Media & streaming', 'Apparel and Beauty', 'Electronics & tech', 'Home and office', 'Health & Fitness', 'Arts and hobbies', 'Fees & services', 'Misc']
- `description`: string

**Output schema:** See `add_expense_cat_d.json`

### add_expense_cat_e

Add a new expense.

**Input parameters:**

- `expense_date`: string
- `amount`: number
- `category`: enum: ['Food & drink', 'Transit and Fuel', 'Media & streaming', 'Apparel and Beauty', 'Electronics & tech', 'Home and office', 'Health & Fitness', 'Arts and hobbies', 'Fees & services', 'Misc'] — Choose the closest category for the expense. Do not ask follow-up questions just to disambiguate the category; pick the best fit using the description and common sense. If truly unclear, use Misc.

Heuristics: Food & drink=meals, groceries, coffee, restaurants, snacks; Transit and Fuel=rideshare, taxi, gas, parking, public transit, tolls; Media & streaming=movies, concerts, subscriptions, streaming, games, tickets; Apparel and Beauty=clothing, shoes, cosmetics, haircuts, personal care; Electronics & tech=devices, gadgets, accessories, apps, software; Home and office=furniture, supplies, housewares, decor, cleaning; Health & Fitness=gym, medical, wellness, supplements, pharmacy; Arts and hobbies=crafts, sports equipment, creative supplies, lessons; Fees & services=banking, professional services, insurance, subscriptions; Misc=anything that does not fit well into other categories.
- `description`: string

**Output schema:** See `add_expense_cat_e.json`

### add_expense_date_a

Add a new expense.

**Input parameters:**

- `expense_date`: string
- `amount`: number
- `category`: enum: ['Food & drink', 'Transit and Fuel', 'Media & streaming', 'Apparel and Beauty', 'Electronics & tech', 'Home and office', 'Health & Fitness', 'Arts and hobbies', 'Fees & services', 'Misc']
- `description`: string

**Output schema:** See `add_expense_date_a.json`

### add_expense_date_b

Add a new expense.

**Input parameters:**

- `expense_date`: string — Date in YYYY-MM-DD format
- `amount`: number
- `category`: enum: ['Food & drink', 'Transit and Fuel', 'Media & streaming', 'Apparel and Beauty', 'Electronics & tech', 'Home and office', 'Health & Fitness', 'Arts and hobbies', 'Fees & services', 'Misc']
- `description`: string

**Output schema:** See `add_expense_date_b.json`

### add_expense_date_c

Add a new expense.

**Input parameters:**

- `expense_date`: string
- `amount`: number
- `category`: enum: ['Food & drink', 'Transit and Fuel', 'Media & streaming', 'Apparel and Beauty', 'Electronics & tech', 'Home and office', 'Health & Fitness', 'Arts and hobbies', 'Fees & services', 'Misc']
- `description`: string

**Output schema:** See `add_expense_date_c.json`

### add_expense_date_d

Add a new expense.

**Input parameters:**

- `expense_date`: string (pattern: `^\d{4}-\d{2}-\d{2}$`)
- `amount`: number
- `category`: enum: ['Food & drink', 'Transit and Fuel', 'Media & streaming', 'Apparel and Beauty', 'Electronics & tech', 'Home and office', 'Health & Fitness', 'Arts and hobbies', 'Fees & services', 'Misc']
- `description`: string

**Output schema:** See `add_expense_date_d.json`

### add_expense_desc_a

Add a new expense.

**Input parameters:**

- `expense_date`: string
- `amount`: number
- `category`: enum: ['Food & drink', 'Transit and Fuel', 'Media & streaming', 'Apparel and Beauty', 'Electronics & tech', 'Home and office', 'Health & Fitness', 'Arts and hobbies', 'Fees & services', 'Misc']
- `description`: string

**Output schema:** See `add_expense_desc_a.json`

### add_expense_desc_b

Add a new expense.

**Input parameters:**

- `expense_date`: string
- `amount`: number
- `category`: enum: ['Food & drink', 'Transit and Fuel', 'Media & streaming', 'Apparel and Beauty', 'Electronics & tech', 'Home and office', 'Health & Fitness', 'Arts and hobbies', 'Fees & services', 'Misc']
- `description`: string — Start with a capital letter and end with a period

**Output schema:** See `add_expense_desc_b.json`

### add_expense_desc_c

Add a new expense.

**Input parameters:**

- `expense_date`: string
- `amount`: number
- `category`: enum: ['Food & drink', 'Transit and Fuel', 'Media & streaming', 'Apparel and Beauty', 'Electronics & tech', 'Home and office', 'Health & Fitness', 'Arts and hobbies', 'Fees & services', 'Misc']
- `description`: string (pattern: `^[A-Z].*\.$`)

**Output schema:** See `add_expense_desc_c.json`

### add_expense_desc_d

Add a new expense.

**Input parameters:**

- `expense_date`: string
- `amount`: number
- `category`: enum: ['Food & drink', 'Transit and Fuel', 'Media & streaming', 'Apparel and Beauty', 'Electronics & tech', 'Home and office', 'Health & Fitness', 'Arts and hobbies', 'Fees & services', 'Misc']
- `description`: string (pattern: `^[A-Z].*\.$`) — Start with a capital letter and end with a period

**Output schema:** See `add_expense_desc_d.json`

### add_expense_model_a

Add a new expense.

**Input parameters:**

- `expense`: object — Input model for adding a single expense.

This is used to test how models handle a single nested JSON object argument.

**Output schema:** See `add_expense_model_a.json`

### get_expenses_a

Get all expenses.

**Output schema:** See `get_expenses_a.json`

### get_expenses_b

Get all expenses.

**Output schema:** See `get_expenses_b.json`

### get_expenses_c

Get all expenses.

**Output schema:** See `get_expenses_c.json`

