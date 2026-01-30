# Reasoning diff

Generated: 2026-01-29T17:41:29.388423Z  
Query: `Yesterday I bought a sandwich for $12.50.`  
Tool: `add_expense_cat_c`  
Seed: `42`

## Table

| Reasoning effort | Reasoning (verbatim excerpt) | Full text |
|---|---|---|
| `none` | <none> | [full](#reasoning-none) |
| `low` | I need to add an expense for food on January 28, 2026, specifically for a sandwich. I’ll use the appropriate tool to enter this information.… | [full](#reasoning-low) |
| `medium` | I need to add an expense from yesterday's date, which is January 28, 2026, in relation to today, January 29, 2026. The category for this exp… | [full](#reasoning-medium) |
| `high` | **Adding expense details** I need to add an expense from yesterday, which is 2026-01-28, relative to the date of 2026-01-29. The category fo… | [full](#reasoning-high) |
| `xhigh` | **Logging user expense** I need to help the user log an expense for yesterday, which was January 28, 2026. The category is food, with the ex… | [full](#reasoning-xhigh) |

## Noted differences

- `none` returns no `ThinkingPart` content (empty reasoning).
- `low`/`medium`/`high` are very similar: they compute "yesterday" as `2026-01-28`, choose category `food`, and use a short description like "sandwich".
- `xhigh` differs most: different heading ("Logging expenses"), explicitly mentions tool name/date format, and uses a more verbose description ("Bought a sandwich.").
- Non-`none` levels appear to be summaries (not full chain-of-thought), consistent with `openai_reasoning_summary="auto"`.

## Full reasoning text

### reasoning-none

Reasoning (verbatim):
```
<no reasoning returned>
```

Output (verbatim):
```
Logged: **$12.50** on **2026-01-28** — **Food** (sandwich).
```

### reasoning-low

Reasoning (verbatim):
```
I need to add an expense for food on January 28, 2026, specifically for a sandwich. I’ll use the appropriate tool to enter this information. It’s straightforward, but I want to make sure I get all the details correct to keep everything organized. Keeping track of expenses is important, and I’m making sure everything’s noted properly! Alright, let’s move forward with that!
```

Output (verbatim):
```
Logged: **$12.50** on **2026-01-28** — **food** (*sandwich*).
```

### reasoning-medium

Reasoning (verbatim):
```
I need to add an expense from yesterday's date, which is January 28, 2026, in relation to today, January 29, 2026. The category for this expense is food, and the description is simply "sandwich." So, I’ll make sure to call the appropriate tool to get this added. It feels straightforward, but I want to ensure I get all the details right for accurate tracking!
```

Output (verbatim):
```
Logged: **$12.50** for **Sandwich** under **food** on **2026-01-28**.
```

### reasoning-high

Reasoning (verbatim):
```
**Adding expense details**

I need to add an expense from yesterday, which is 2026-01-28, relative to the date of 2026-01-29. The category for this expense is food, so I’ll include that in the entry. To do this, I'll be using the appropriate tool to ensure everything is recorded correctly. It’s important to keep track of these expenses accurately, so I want to make sure I get this right!
```

Output (verbatim):
```
Logged: **$12.50** on **2026-01-28** — **Food** (Sandwich).
```

### reasoning-xhigh

Reasoning (verbatim):
```
**Logging user expense**

I need to help the user log an expense for yesterday, which was January 28, 2026. The category is food, with the expense being a sandwich for $12.50. I’ll use the add_expense_cat_c tool to record this by specifying the date, amount, category, and description. Once I’ve done that, I’ll confirm back to the user that it’s all logged. Okay, let’s make that tool call!
```

Output (verbatim):
```
Logged: **$12.50** for **sandwich** on **2026-01-28** (category: **food**).
```
