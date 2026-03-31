from pathlib import Path
import sys

_ROOT = Path(__file__).resolve().parent.parent
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

from dotenv import load_dotenv

load_dotenv(_ROOT / ".env")

from smolagents import CodeAgent, GoogleSearchTool, InferenceClientModel, VisitWebpageTool
from tools.cargo_travel_time import cargo_travel_time

model = InferenceClientModel(
    model_id="Qwen/Qwen2.5-Coder-32B-Instruct",
    provider="hf-inference",
)

task = """Find all Batman filming locations in the world, calculate the time to transfer via cargo plane to here (we're in Gotham, 40.7128° N, 74.0060° W), and return them to me as a pandas dataframe.
Also give me some supercar factories with the same cargo plane transfer time."""

agent = CodeAgent(model=model, tools=[GoogleSearchTool(), VisitWebpageTool(), cargo_travel_time])

result = agent.run(task)
print(result)