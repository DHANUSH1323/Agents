from smolagents import CodeAgent, DuckDuckGoSearchTool, InferenceClientModel

HfApiModel = InferenceClientModel  # alias for HF Inference API (tutorial name)

model = HfApiModel(
    model_id="Qwen/Qwen2.5-Coder-7B-Instruct",
    provider="hf-inference",
)

agent = CodeAgent(
    tools=[DuckDuckGoSearchTool()],
    model=model,
)

if __name__ == "__main__":
    print(agent.run("What is the latest stable Python 3 release? Search the web briefly."))
