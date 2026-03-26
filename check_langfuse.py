import os
from langfuse import get_client
import dotenv

dotenv.load_dotenv()

client = get_client()

if client.auth_check():
    print("Langfuse authentication successful")
else:
    print("Langfuse authentication failed")



from openinference.instrumentation.smolagents import SmolagentsInstrumentor
 
SmolagentsInstrumentor().instrument()

from smolagents import (
    CodeAgent,
    ToolCallingAgent,
    WebSearchTool,
    VisitWebpageTool,
    InferenceClientModel,
)

model = InferenceClientModel(
    model_id="deepseek-ai/DeepSeek-R1-Distill-Qwen-32B"
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