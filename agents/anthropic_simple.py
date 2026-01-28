# Anthropic API - doesn't require Entra auth
import os

from anthropic import AnthropicFoundry
from dotenv import load_dotenv

load_dotenv(override=True)
FOUNDRY_ENDPOINT = "https://foundry-iq-knowledge.services.ai.azure.com/anthropic"
 
anthropic_client = AnthropicFoundry(
    api_key=os.environ["ANTHROPIC_KEY"],
    base_url=FOUNDRY_ENDPOINT
)
 
for model in ["claude-sonnet-4-5", "claude-opus-4-5", "claude-haiku-4-5"]:
    message = anthropic_client.messages.create(
        model=model,
        messages=[
            {"role": "user", "content": "What is the capital of France?"}
        ],
        max_tokens=1024,
    )

    print(model, ":", message.content[0].text)