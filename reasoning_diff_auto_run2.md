# Reasoning diff

Generated: 2026-01-29T17:54:25.617258Z  
Query: `Yesterday I bought a sandwich for $12.50.`  
Tool: `add_expense_cat_c`  
Reasoning summary: `auto`  
Seed: `42`

## Table

| Reasoning effort | Reasoning (verbatim excerpt) | Full text |
|---|---|---|
| `none` | <none> | [full](#reasoning-none) |
| `low` | I'm working on adding an expense for my food category. I need to make sure I reference the correct date, which is yesterday, January 28, 202… | [full](#reasoning-low) |
| `medium` | **Adding an expense** I need to add an expense from yesterday, specifically from January 28, 2026, to today, January 29, 2026. The category … | [full](#reasoning-medium) |
| `high` | **Adding an expense** I need to add an expense recorded yesterday, which is related to January 29, 2026. It falls under the food category, a… | [full](#reasoning-high) |
| `xhigh` | **Logging an expense** I need to log an expense with a date of yesterday, which is January 28, 2026. The amount is $12.50, belonging to the … | [full](#reasoning-xhigh) |

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
Logged: **$12.50** for **Sandwich** on **2026-01-28** (category: **food**).
```

### reasoning-low

Reasoning (verbatim):
```
I'm working on adding an expense for my food category. I need to make sure I reference the correct date, which is yesterday, January 28, 2026, in relation to today's date of January 29, 2026. I'll use the appropriate tool to record this expense, ensuring that it's logged accurately. Keeping things organized is important to me; I want to make sure I have everything in order!
```

Output (verbatim):
```
Logged: **$12.50** for **Sandwich** on **2026-01-28** (category: **food**).
```

### reasoning-medium

Reasoning (verbatim):
```
**Adding an expense**

I need to add an expense from yesterday, specifically from January 28, 2026, to today, January 29, 2026. The category for this expense is food, and the description is a sandwich. I’ll go ahead and use the appropriate tool to record this. It's essential to keep my records up to date, so let’s make sure everything is accurately logged!
```

Output (verbatim):
```
Logged: **$12.50** on **2026-01-28** — **food** — *Sandwich*.
```

### reasoning-high

Reasoning (verbatim):
```
**Adding an expense**

I need to add an expense recorded yesterday, which is related to January 29, 2026. It falls under the food category, and the description is "sandwich." My plan is to use the tool to add this expense and then confirm it afterward to ensure it's properly logged. It's a straightforward task, and I'll make sure to have everything documented correctly!
```

Output (verbatim):
```
Logged: **$12.50** for **sandwich** on **2026-01-28** (category: **food**).
```

### reasoning-xhigh

Reasoning (verbatim):
```
**Logging an expense**

I need to log an expense with a date of yesterday, which is January 28, 2026. The amount is $12.50, belonging to the food category and the description is "sandwich." I’ll use the tool to add this expense, specifically calling functions.add_expense_cat_c with these fields. After that, I’ll provide a confirmation response to let the user know it’s logged successfully.
```

Output (verbatim):
```
Logged: **$12.50** on **2026-01-28** — **food** (sandwich).
```
