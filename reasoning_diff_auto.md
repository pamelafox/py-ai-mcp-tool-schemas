# Reasoning diff

Generated: 2026-01-29T17:50:33.554839Z  
Query: `Yesterday I bought a sandwich for $12.50.`  
Tool: `add_expense_cat_c`  
Reasoning summary: `auto`  
Seed: `42`

## Table

| Reasoning effort | Reasoning (verbatim excerpt) | Full text |
|---|---|---|
| `none` | <none> | [full](#reasoning-none) |
| `low` | **Adding expense details** I need to add an expense from yesterday, which is January 28, 2026. The category is food, but I haven't filled in… | [full](#reasoning-low) |
| `medium` | **Logging an expense** I need to log an expense from yesterday, which is January 28, 2026, in relation to today's date. The category will be… | [full](#reasoning-medium) |
| `high` | I need to add an expense for a food item. Yesterday's expense is related to today's date, which is January 29, 2026, making the expense date… | [full](#reasoning-high) |
| `xhigh` | **Logging an expense** I need to log an expense for food, specifically a sandwich. Today’s date is January 29, 2026, and I’ll use the previo… | [full](#reasoning-xhigh) |

## Noted differences

- `none` returns no `ThinkingPart` content (empty reasoning).
- `low`/`medium`/`high` are very similar: they compute "yesterday" as `2026-01-28`, choose category `food`, and use a short description like "sandwich".
- `xhigh` differs most: different heading ("Logging expenses"), explicitly mentions tool name/date format, and uses a more verbose description ("Bought a sandwich.").
- Non-`none` levels reflect the configured reasoning summary level (not full chain-of-thought).

## Full reasoning text

### reasoning-none

Reasoning (verbatim):
```
<no reasoning returned>
```

Output (verbatim):
```
Logged: **$12.50** on **2026-01-28** — **food** — *Sandwich*.
```

### reasoning-low

Reasoning (verbatim):
```
**Adding expense details**

I need to add an expense from yesterday, which is January 28, 2026. The category is food, but I haven't filled in the description yet. I should use the appropriate tool to enter this information. I want to make sure I get it right, so I'll double-check the details before I proceed. It's important to keep track of these things properly! Let’s go ahead and input that.
```

Output (verbatim):
```
Logged: **$12.50** on **2026-01-28** — **food** (Sandwich).
```

### reasoning-medium

Reasoning (verbatim):
```
**Logging an expense**

I need to log an expense from yesterday, which is January 28, 2026, in relation to today's date. The category will be "food" and the description is simply "sandwich." I'll call the appropriate tool to record this. It feels good to keep track of expenses accurately! It's easy to overlook these small details, but they are important for managing my budget. Alright, let's get that logged!
```

Output (verbatim):
```
Logged: **$12.50** on **2026-01-28** — **food** (Sandwich).
```

### reasoning-high

Reasoning (verbatim):
```
I need to add an expense for a food item. Yesterday's expense is related to today's date, which is January 29, 2026, making the expense date January 28, 2026. The category will be food, and the description of the expense is simply "sandwich." So, I'll go ahead and use the tool to add this expense to my records. It's important to keep track of these things accurately!
```

Output (verbatim):
```
Logged: **$12.50** on **2026-01-28** — **Food** (Sandwich).
```

### reasoning-xhigh

Reasoning (verbatim):
```
**Logging an expense**

I need to log an expense for food, specifically a sandwich. Today’s date is January 29, 2026, and I’ll use the previous day’s date, January 28, 2026. I’ll input an amount of $12.50 for this expense. I think the description could be something like "Bought a sandwich." My next step will be to call the tool to add this expense and then confirm that it’s logged.
```

Output (verbatim):
```
Logged: **$12.50** on **2026-01-28** — **food** (Sandwich).
```
