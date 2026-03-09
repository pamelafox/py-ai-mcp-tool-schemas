# Invented Categories (from add_expense_cat_a)

This report lists **invalid / invented** `category` values produced by the free-form tool variant `add_expense_cat_a`.
A category is counted as *invented* if its lowercased form is not in the allowed set:

- entertainment, food, gadget, other, shopping, transport

Notes:

- This only covers runs/cases where the tool was actually called (no tool call → no category to inspect).
- Other category variants (`cat_b/c/d/e`) constrain categories, so they usually won’t invent invalid values.

## Summary

- Runs analyzed: gpt52_none, gpt52_xhigh, gpt41mini
- Total invented category occurrences: 57
- Unique invented categories (normalized): 25
- Unique invented categories (raw strings): 28

Context (how often `add_expense_cat_a` guessed correctly):

| Run | Total cases | Tool called | Category match (guessed expected) | Category valid (allowed set) | Invented invalid (from this report) |
| --- | ---: | ---: | ---: | ---: | ---: |
| gpt52_none | 29 | 29/29 (100.0%) | 9/27 (33.3%) | 10/29 (34.5%) | 19/29 (65.5%) |
| gpt52_xhigh | 29 | 28/29 (96.6%) | 8/27 (29.6%) | 8/29 (27.6%) | 20/28 (71.4%) |
| gpt41mini | 27 | 26/27 (96.3%) | 8/26 (30.8%) | 8/27 (29.6%) | 18/26 (69.2%) |
| **Overall** | 85 | 83/85 (97.6%) | 25/80 (31.2%) | 26/85 (30.6%) | 57/83 (68.7%) |

Notes:

- “Category match” only applies to cases that define an expected category, so its denominator can be smaller than total cases.
- “Invented invalid” is counted only when the tool was called and its `category` was outside the allowed set.

## View A: Frequency table (normalized)

| Normalized category | Count |
| --- | ---: |
| gas | 6 |
| electronics | 6 |
| coffee | 6 |
| transportation | 5 |
| groceries | 4 |
| comida | 3 |
| gasolina | 3 |
| electrónica | 3 |
| clothing | 2 |
| apps | 2 |
| spa | 2 |
| entretenimiento | 2 |
| car purchase | 1 |
| ropa y calzado | 1 |
| apps & software | 1 |
| personal care | 1 |
| dining | 1 |
| calzado | 1 |
| shoes | 1 |
| grocery delivery | 1 |
| lunch | 1 |
| car | 1 |
| dinner | 1 |
| ocio | 1 |
| zapatos | 1 |

## View B: Frequency table (raw strings)

| Raw category | Count |
| --- | ---: |
| Gas | 6 |
| Electronics | 5 |
| Transportation | 5 |
| Coffee | 4 |
| Comida | 3 |
| Gasolina | 3 |
| Electrónica | 3 |
| Clothing | 2 |
| groceries | 2 |
| Groceries | 2 |
| Apps | 2 |
| Spa | 2 |
| Entretenimiento | 2 |
| coffee | 2 |
| Car purchase | 1 |
| Ropa y calzado | 1 |
| Apps & Software | 1 |
| Personal Care | 1 |
| Dining | 1 |
| Calzado | 1 |
| Shoes | 1 |
| electronics | 1 |
| Grocery Delivery | 1 |
| lunch | 1 |
| car | 1 |
| dinner | 1 |
| ocio | 1 |
| zapatos | 1 |

## View C: Per-run breakdown (normalized)

### gpt52_none (n=19)

| Normalized category | Count |
| --- | ---: |
| gas | 2 |
| electronics | 2 |
| groceries | 2 |
| coffee | 2 |
| transportation | 2 |
| clothing | 1 |
| car purchase | 1 |
| apps | 1 |
| spa | 1 |
| comida | 1 |
| gasolina | 1 |
| entretenimiento | 1 |
| ropa y calzado | 1 |
| electrónica | 1 |

### gpt52_xhigh (n=20)

| Normalized category | Count |
| --- | ---: |
| transportation | 3 |
| gas | 2 |
| electronics | 2 |
| groceries | 2 |
| coffee | 2 |
| clothing | 1 |
| apps & software | 1 |
| personal care | 1 |
| dining | 1 |
| comida | 1 |
| gasolina | 1 |
| entretenimiento | 1 |
| calzado | 1 |
| electrónica | 1 |

### gpt41mini (n=18)

| Normalized category | Count |
| --- | ---: |
| gas | 2 |
| electronics | 2 |
| coffee | 2 |
| shoes | 1 |
| grocery delivery | 1 |
| lunch | 1 |
| car | 1 |
| apps | 1 |
| spa | 1 |
| dinner | 1 |
| comida | 1 |
| gasolina | 1 |
| ocio | 1 |
| zapatos | 1 |
| electrónica | 1 |

## View D: By case (what it invented where)

| Case | Invented categories (normalized) | Runs |
| --- | --- | --- |
| ambiguous_no_date | groceries | gpt52_none, gpt52_xhigh |
| clear_gadget | electronics | gpt41mini, gpt52_none, gpt52_xhigh |
| clear_shopping | clothing, shoes | gpt41mini, gpt52_none, gpt52_xhigh |
| clear_transport_today | gas | gpt41mini, gpt52_none, gpt52_xhigh |
| edge_currency_symbol | dining, dinner | gpt41mini, gpt52_xhigh |
| edge_large_amount | car, car purchase, transportation | gpt41mini, gpt52_none, gpt52_xhigh |
| edge_small_amount | apps, apps & software | gpt41mini, gpt52_none, gpt52_xhigh |
| edge_unknown_category | personal care, spa | gpt41mini, gpt52_none, gpt52_xhigh |
| hard_amount_fraction_yesterday_lunch | lunch | gpt41mini |
| hard_category_grocery_delivery_yesterday | groceries, grocery delivery | gpt41mini, gpt52_none, gpt52_xhigh |
| hard_category_headphones_last_day_last_month | electronics | gpt41mini, gpt52_none, gpt52_xhigh |
| relative_date_day_after_tomorrow_bus_pass | transportation | gpt52_none, gpt52_xhigh |
| relative_date_day_before_yesterday_coffee | coffee | gpt41mini, gpt52_none, gpt52_xhigh |
| relative_date_last_business_day_last_month | gas | gpt41mini, gpt52_none, gpt52_xhigh |
| relative_date_three_days_ago_rideshare | transportation | gpt52_none, gpt52_xhigh |
| relative_date_two_mondays_ago | coffee | gpt41mini, gpt52_none, gpt52_xhigh |
| spanish_entertainment | entretenimiento, ocio | gpt41mini, gpt52_none, gpt52_xhigh |
| spanish_food | comida | gpt41mini, gpt52_none, gpt52_xhigh |
| spanish_gadget | electrónica | gpt41mini, gpt52_none, gpt52_xhigh |
| spanish_shopping | calzado, ropa y calzado, zapatos | gpt41mini, gpt52_none, gpt52_xhigh |
| spanish_transport | gasolina | gpt41mini, gpt52_none, gpt52_xhigh |

## View E: One detailed example per invented category

Useful when you want “story” examples with the full tool args context.

### gas

- Run: gpt52_none
- Case: clear_transport_today
- Raw category: Gas
- Description: Gas
- Amount: 45
- Date: 2026-01-29

### clothing

- Run: gpt52_none
- Case: clear_shopping
- Raw category: Clothing
- Description: New shoes
- Amount: 125
- Date: 2026-01-20

### electronics

- Run: gpt52_none
- Case: clear_gadget
- Raw category: Electronics
- Description: Laptop purchase
- Amount: 1200
- Date: 2026-01-28

### groceries

- Run: gpt52_none
- Case: ambiguous_no_date
- Raw category: groceries
- Description: groceries
- Amount: 50
- Date: 2026-01-29

### coffee

- Run: gpt52_none
- Case: relative_date_two_mondays_ago
- Raw category: Coffee
- Description: Coffee
- Amount: 8.75
- Date: 2026-01-19

### transportation

- Run: gpt52_none
- Case: relative_date_three_days_ago_rideshare
- Raw category: Transportation
- Description: Uber to the airport
- Amount: 38
- Date: 2026-01-26

### car purchase

- Run: gpt52_none
- Case: edge_large_amount
- Raw category: Car purchase
- Description: Bought a car
- Amount: 35000
- Date: 2026-01-28

### apps

- Run: gpt52_none
- Case: edge_small_amount
- Raw category: Apps
- Description: App purchase
- Amount: 0.99
- Date: 2026-01-28

### spa

- Run: gpt52_none
- Case: edge_unknown_category
- Raw category: Spa
- Description: Spa treatment
- Amount: 200
- Date: 2026-01-28

### comida

- Run: gpt52_none
- Case: spanish_food
- Raw category: Comida
- Description: Sándwich
- Amount: 12.5
- Date: 2026-01-28

### gasolina

- Run: gpt52_none
- Case: spanish_transport
- Raw category: Gasolina
- Description: Gasolina
- Amount: 45
- Date: 2026-01-29

### entretenimiento

- Run: gpt52_none
- Case: spanish_entertainment
- Raw category: Entretenimiento
- Description: Entrada de cine
- Amount: 25.99
- Date: 2026-01-15

### ropa y calzado

- Run: gpt52_none
- Case: spanish_shopping
- Raw category: Ropa y calzado
- Description: Zapatos nuevos
- Amount: 125
- Date: 2026-01-20

### electrónica

- Run: gpt52_none
- Case: spanish_gadget
- Raw category: Electrónica
- Description: Compra de laptop
- Amount: 1200
- Date: 2026-01-28

### apps & software

- Run: gpt52_xhigh
- Case: edge_small_amount
- Raw category: Apps & Software
- Description: App purchase
- Amount: 0.99
- Date: 2026-01-28

### personal care

- Run: gpt52_xhigh
- Case: edge_unknown_category
- Raw category: Personal Care
- Description: Spa treatment
- Amount: 200
- Date: 2026-01-28

### dining

- Run: gpt52_xhigh
- Case: edge_currency_symbol
- Raw category: Dining
- Description: Dinner
- Amount: 50
- Date: 2026-01-28

### calzado

- Run: gpt52_xhigh
- Case: spanish_shopping
- Raw category: Calzado
- Description: Zapatos nuevos
- Amount: 125
- Date: 2026-01-20

### shoes

- Run: gpt41mini
- Case: clear_shopping
- Raw category: Shoes
- Description: New shoes
- Amount: 125
- Date: 2026-01-20

### grocery delivery

- Run: gpt41mini
- Case: hard_category_grocery_delivery_yesterday
- Raw category: Grocery Delivery
- Description: Instacart grocery delivery
- Amount: 65
- Date: 2026-01-28

### lunch

- Run: gpt41mini
- Case: hard_amount_fraction_yesterday_lunch
- Raw category: lunch
- Description: Lunch
- Amount: 12.5
- Date: 2026-01-28

### car

- Run: gpt41mini
- Case: edge_large_amount
- Raw category: car
- Description: Bought a car
- Amount: 35000
- Date: 2026-01-28

### dinner

- Run: gpt41mini
- Case: edge_currency_symbol
- Raw category: dinner
- Description: dinner
- Amount: 50
- Date: 2026-01-28

### ocio

- Run: gpt41mini
- Case: spanish_entertainment
- Raw category: ocio
- Description: entrada de cine
- Amount: 25.99
- Date: 2026-01-15

### zapatos

- Run: gpt41mini
- Case: spanish_shopping
- Raw category: zapatos
- Description: zapatos nuevos
- Amount: 125
- Date: 2026-01-20

