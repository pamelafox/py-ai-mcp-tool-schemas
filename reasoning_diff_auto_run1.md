# Reasoning diff

Generated: 2026-01-29T17:53:44.520140Z  
Query: `Yesterday I bought a sandwich for $12.50.`  
Tool: `add_expense_cat_c`  
Reasoning summary: `auto`  
Seed: `42`

## Table

| Reasoning effort | Reasoning (verbatim excerpt) | Full text |
|---|---|---|
| `none` | <none> | [full](#reasoning-none) |
| `low` | **Adding an expense** I need to add an expense related to food. It looks like I'm referencing yesterday's date, which is 2026-01-28. The ite… | [full](#reasoning-low) |
| `medium` | **Adding expense details** I need to add an expense entry for yesterday, which is January 28, 2026. The category for this entry will be food… | [full](#reasoning-medium) |
| `high` | **Adding expense for sandwich** I'm looking to add an expense from yesterday, which is January 28, 2026. The category will be food, and the … | [full](#reasoning-high) |
| `xhigh` | **Logging expense** I need to log an expense for yesterday, which is 2026-01-28. The category is food and the description is for a sandwich … | [full](#reasoning-xhigh) |

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
Logged: **$12.50** — **food** — *Sandwich* on **2026-01-28**.
```

### reasoning-low

Reasoning (verbatim):
```
**Adding an expense**

I need to add an expense related to food. It looks like I'm referencing yesterday's date, which is 2026-01-28. The item is a sandwich. I'll use the appropriate tool to log this expense. It’s important for me to keep track of these details accurately! I'm on it, making sure everything is correctly entered into the system. Let's get this expense recorded!
```

Output (verbatim):
```
Logged: **$12.50** for **Sandwich** on **2026-01-28** (category: **food**).
```

### reasoning-medium

Reasoning (verbatim):
```
**Adding expense details**

I need to add an expense entry for yesterday, which is January 28, 2026. The category for this entry will be food, with a description saying "sandwich." To do this, I’ll use the designated tool to input the information accurately and ensure it's recorded properly. I'll make sure everything is in place and in the correct format!
```

Output (verbatim):
```
Logged: **$12.50** on **2026-01-28** — **food** (Sandwich).
```

### reasoning-high

Reasoning (verbatim):
```
**Adding expense for sandwich**

I'm looking to add an expense from yesterday, which is January 28, 2026. The category will be food, and the description for this expense is "sandwich." I'll use the function to add this expense correctly. Once that’s done, I should remember to respond with a confirmation to ensure everything goes smoothly. It's all about keeping my records accurate!
```

Output (verbatim):
```
Logged: **$12.50** for **sandwich** under **food** on **2026-01-28**.
```

### reasoning-xhigh

Reasoning (verbatim):
```
**Logging expense**

I need to log an expense for yesterday, which is 2026-01-28. The category is food and the description is for a sandwich that costs $12.50. I’m planning to use the tool add_expense_cat_c and will input the date, amount, category, and description. I wonder if I should confirm the currency again, but since the user specified $12.50, I think that should be clear. Now, I’ll proceed to log this expense!
```

Output (verbatim):
```
Logged: **$12.50** on **2026-01-28** — **Food** (“Sandwich”).
```
