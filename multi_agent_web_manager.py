"""Multi-agent: manager (CodeAgent) delegates web research to a ToolCallingAgent."""
from smolagents import (
    CodeAgent,
    InferenceClientModel,
    ToolCallingAgent,
    VisitWebpageTool,
    WebSearchTool,
)

model = InferenceClientModel(
    model_id="Qwen/Qwen2.5-Coder-7B-Instruct",
    provider="hf-inference",
)

web_agent = ToolCallingAgent(
    tools=[WebSearchTool(), VisitWebpageTool()],
    model=model,
    max_steps=12,
    name="web_search_agent",
    description=(
        "Searches the public web and opens relevant pages to collect current facts, "
        "sources, and details for the manager."
    ),
)

manager_agent = CodeAgent(
    tools=[],
    model=model,
    managed_agents=[web_agent],
    max_steps=15,
)

if __name__ == "__main__":
    print(
        manager_agent.run(
            "What are three notable Python releases in the last two years and one key feature each? "
            "Use the web agent to verify dates from official or reliable sources."
        )
    )
