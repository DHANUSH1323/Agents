"""ToolCallingAgent: JSON-style tool calls with web search (smolagents)."""
from smolagents import DuckDuckGoSearchTool, InferenceClientModel, ToolCallingAgent

model = InferenceClientModel(
    model_id="Qwen/Qwen2.5-Coder-7B-Instruct",
    provider="hf-inference",
)

agent = ToolCallingAgent(
    tools=[DuckDuckGoSearchTool()],
    model=model,
    max_steps=12,
    name="web_research_assistant",
    description=(
        "Answers questions by calling web search when fresh or factual information is needed."
    ),
)

if __name__ == "__main__":
    print(
        agent.run(
            "What is the second stable release in the Python 3.13 series? Reply with the version number only."
        )
    )
