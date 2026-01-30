# Reasoning diff

Generated: 2026-01-29T17:51:11.271089Z  
Query: `Yesterday I bought a sandwich for $12.50.`  
Tool: `add_expense_cat_c`  
Reasoning summary: `detailed`  
Seed: `42`

## Table

| Reasoning effort | Reasoning (verbatim excerpt) | Full text |
|---|---|---|
| `none` | <none> | [full](#reasoning-none) |
| `low` | I need to add an expense from yesterday, which was January 28, 2026. It falls under the food category, and the description is for a sandwich… | [full](#reasoning-low) |
| `medium` | **Adding expense detail** I need to add an expense for food, specifically a sandwich, with the date of yesterday relative to today's date, w… | [full](#reasoning-medium) |
| `high` | **Adding an expense** I need to add an expense for yesterday, which is 2026-01-28. The category will be food, and the description is a "sand… | [full](#reasoning-high) |
| `xhigh` | **Logging an expense** I need to log an expense for yesterday, which is January 28, 2026, relative to today’s date. The likely category is f… | [full](#reasoning-xhigh) |

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
I need to add an expense from yesterday, which was January 28, 2026. It falls under the food category, and the description is for a sandwich. I’ll go ahead and call the tool to make this entry. It's important to keep track of these details to stay organized! I just want to ensure I get everything logged accurately. So let's get that tool activated!
```

Output (verbatim):
```
Logged: **$12.50** on **2026-01-28** under **food** — *Sandwich*.
```

### reasoning-medium

Reasoning (verbatim):
```
**Adding expense detail**

I need to add an expense for food, specifically a sandwich, with the date of yesterday relative to today's date, which is January 29, 2026. That would make it January 28, 2026. It’s pretty straightforward — I just need to use the appropriate tool to log this expense properly. I'll make sure to do it correctly to keep everything organized!
```

Output (verbatim):
```
Logged: **$12.50** on **2026-01-28** — **Food** (Sandwich).
```

### reasoning-high

Reasoning (verbatim):
```
**Adding an expense**

I need to add an expense for yesterday, which is 2026-01-28. The category will be food, and the description is a "sandwich." I'll use the appropriate tool to log this expense. It's straightforward, but I want to make sure everything is correctly entered! It's important for keeping track of my spending. Alright, let's get this done quickly and accurately! I don't want to miss any details.
```

Output (verbatim):
```
Logged: **$12.50** for **sandwich** under **food** on **2026-01-28**.
```

### reasoning-xhigh

Reasoning (verbatim):
```
**Logging an expense**

I need to log an expense for yesterday, which is January 28, 2026, relative to today’s date. The likely category is food, and the expense description is "sandwich" with an amount of $12.50. I’ll use the tool to add this expense and make sure the date format is correct as "YYYY-MM-DD". So, I'll call the function with the specified date, amount, category, and description, then confirm it to the user.
```

Output (verbatim):
```
Logged: **$12.50** on **2026-01-28** — **food** (sandwich).
```
