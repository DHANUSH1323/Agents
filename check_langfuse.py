import enable_langfuse_tracing  # noqa: F401
from langfuse import get_client

from smolagents import (
    CodeAgent,
    ToolCallingAgent,
    WebSearchTool,
    VisitWebpageTool,
    InferenceClientModel,
)

client = get_client()

if client.auth_check():
    print("Langfuse authentication successful")
else:
    print("Langfuse authentication failed")

model = InferenceClientModel(
    model_id="deepseek-ai/DeepSeek-R1-Distill-Qwen-32B",
    provider="hf-inference",
)

search_agent = ToolCallingAgent(
    tools=[WebSearchTool(), VisitWebpageTool()],
    model=model,
    name="search_agent",
    description="This is an agent that can do web search.",
)

manager_agent = CodeAgent(
    tools=[],
    model=model,
    managed_agents=[search_agent],
)
manager_agent.run(
    "How can Langfuse be used to monitor and improve the reasoning and decision-making of smolagents when they execute multi-step tasks, like dynamically adjusting a recipe based on user feedback or available ingredients?"
)
