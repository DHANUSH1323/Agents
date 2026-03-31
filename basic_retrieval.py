import enable_langfuse_tracing  # noqa: F401
from smolagents import CodeAgent, WebSearchTool, InferenceClientModel

search_tool = WebSearchTool()
model = InferenceClientModel(provider="hf-inference")

agent = CodeAgent(model=model, tools=[search_tool])

response = agent.run("Search for luxury superhero-themed party ideas, including decorations, entertainment, and catering.")
print(response)
