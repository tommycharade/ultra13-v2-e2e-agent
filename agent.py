"""Small, provider-free OpenAI Agents SDK application used for Ultra13 V2 acceptance."""

from agents import Agent, InputGuardrail, Runner, function_tool


@function_tool
def read_status(service: str) -> str:
    """Return a bounded health value from the local fixture."""
    return f"{service}: healthy"


@function_tool
def read_metrics(service: str) -> str:
    """Return a bounded, read-only metric summary for the requested service."""
    return f"{service}: requests=42 errors=0"


owner_gate = InputGuardrail(guardrail_function=lambda value: value)
root = Agent(
    name="v2_release_agent",
    instructions="Read deployment status only. Never mutate infrastructure.",
    model="gpt-5-mini",
    tools=[read_status, read_metrics],
    input_guardrails=[owner_gate],
)


def handle(user_input: str):
    """Native SDK input boundary; provider execution is not used by the deployment test."""
    return Runner.run_sync(root, user_input)


if __name__ == "__main__":
    print("Ultra13 V2 acceptance agent; provider execution is disabled.")
