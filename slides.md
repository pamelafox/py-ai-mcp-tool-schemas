# Slide outline

* Start with an MCP for outift picking for fun!?

* Okay now that the outfit is sorted.. on to the real talk!

* Basic MCP server with all strings
(Do we want to talk about annotated with description outside of category, as an ease-in?)
* Show reasoning for how it decides category
(Logfire demo early on)

Word cloud of all the categories chosen across many evals - invented_categories.md

* What if we want to constrain it more?
* We could add a description annotation with the suggested fields
* That works 80% of the time.. but what if we want to be more strict?
* We can use literals or enums! (Same schema)
* Enums are better since we get more type safety later
* Now we get 95% accuracy!
* Okay now let's look at the date field, what does it output when we just use str?
* Sometimes it gets it right, but often it makes mistakes
* Let's try using datetime
* Much better! But datetime objects can be tricky for models
* Let's try using a regex pattern on a str field
* Actually, that's worse! Why? Check the reasoning
* The model got confused by the regex pattern and tried to output something that matched it exactly
* That's why it's so important to evaluate! You might think a stricter schema is always better, but that's not always the case
* Are there any cases where regex patterns are useful?
* Yes! If you have a very specific format you need, like a product code or ID
* But be careful, they can confuse the model if overused
* All of those evals were with model A and PydanticAI, what about other models or frameworks?
* We can try the same evals with model B
* Results are similar, but some differences in how well they handle certain schema features
* We can also try with another framework, like Framework Y
* Framework Y has different capabilities and limitations compared to PydanticAI
* Results show that schema choices can have different impacts depending on the framework used

* How does reasoning effect it? Same model, 5 different reasoning levels

    none tends to ask a clarifying question when a required field is missing/ambiguous (so it often makes no tool call).
    xhigh more often picks a plausible default and proceeds with the tool call (e.g., for ambiguous_no_date it defaulted to today: 2026-01-29), and it can explain that choice in the reasoning summary.

* We can ALSO control the output schema and see how agents handle that
* Show agent running with different schema variants to generate table of results
* Evaluate the results and show how different schema choices impact markdown table
* Summary of findings

* Conclusions
* Using MCPs with structured schemas can greatly improve the accuracy of model outputs
* Stricter schemas aren't always better; it's important to evaluate and find the right balance
* Different models and frameworks may respond differently to schema features
* Always test and validate your schemas with real model outputs to ensure they meet your needs
* Thank you! Any questions?

## Failure cases

ambiguous_relative_date - "Last week I spent $89 on concert tickets."
Model reasoning: "I need to clarify what 'last week' means...It could refer to the previous calendar week or simply the past seven days."

ambiguous_mixed_items - "I bought coffee and a phone case for $55 yesterday."
Model reasoning: "I should ask the user how they'd like to split it...The total is $55, but it's unclear how to split this amount."

# These are intentionally underspecified; a good assistant should ask a clarifying question
# (or apply a consistent, documented default).
ExpenseCase(
    name="ambiguous_no_date",
    prompt="I spent 50 dollars on groceries.",
    expected_category="food",
    expected_amount=50.0,
    difficulty="ambiguous",
    # Date not specified - model should use today or ask
),

# --- Ambiguous requests ---
ExpenseCase(
    name="ambiguous_vague_category",
    prompt="Yesterday I paid $30 for stuff at the store.",
    expected_date=get_yesterday(),
    expected_amount=30.0,
    difficulty="ambiguous",
    # Category unclear - could be shopping or other
),