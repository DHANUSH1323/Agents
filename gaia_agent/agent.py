import os
from smolagents import CodeAgent, InferenceClientModel, DuckDuckGoSearchTool
from .tools import GaiaFileReaderTool, CalculatorTool, StringReverseTool

SYSTEM_PROMPT = """You are a precise research assistant solving GAIA benchmark questions.

IMPORTANT RULES:
- Your final answer must be EXACT — no extra words, no explanation, no preamble.
- If the answer is a number, return just the number (e.g., "42" not "The answer is 42").
- If the answer is a name, return just the name (e.g., "Albert Einstein").
- If the answer is a list, return comma-separated values.
- If the answer is a yes/no, return just "Yes" or "No".
- Do NOT include "FINAL ANSWER" or any prefix in your response.
- Use the available tools to search the web, read files, or calculate when needed.
- Think step by step, but your final answer must be concise and exact.
"""


class GaiaAgent:
    def __init__(self):
        model = InferenceClientModel(
            model_id="Qwen/Qwen2.5-72B-Instruct",
            token=os.getenv("HF_TOKEN"),
        )

        tools = [
            DuckDuckGoSearchTool(),
            GaiaFileReaderTool(),
            CalculatorTool(),
            StringReverseTool(),
        ]

        self.agent = CodeAgent(
            tools=tools,
            model=model,
            max_steps=10,
            additional_authorized_imports=[
                "json", "re", "math", "datetime", "collections",
                "itertools", "statistics", "unicodedata",
                "csv", "io", "pandas", "openpyxl",
            ],
        )
        print("GaiaAgent initialized.")

    def __call__(self, question: str, task_id: str | None = None) -> str:
        prompt = question
        if task_id:
            prompt += (
                f"\n\n[This question has an associated file. "
                f"Use the read_task_file tool with task_id='{task_id}' to access it if needed.]"
            )

        prompt += (
            "\n\nRespond with ONLY the exact answer — no explanation, "
            "no extra words, no prefix like 'FINAL ANSWER'."
        )

        try:
            result = self.agent.run(prompt)
            answer = str(result).strip()
            # Clean up common prefixes the model might add
            for prefix in ["FINAL ANSWER:", "Final Answer:", "Answer:", "The answer is "]:
                if answer.startswith(prefix):
                    answer = answer[len(prefix):].strip()
            return answer
        except Exception as e:
            print(f"Agent error: {e}")
            return "Unable to determine answer"
