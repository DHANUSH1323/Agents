"""CodeAgent with E2B sandbox execution and a restricted import allowlist.

Requires:
  pip install e2b-code-interpreter  (listed in requirements.txt)
  E2B_API_KEY in the environment or ``.env`` — https://e2b.dev/dashboard

Smolagents merges ``additional_authorized_imports`` with a safe builtin set
(``math``, ``re``, ``datetime``, …). Do not use ``"*"`` unless you accept
arbitrary third-party imports.
"""
from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv

from smolagents import CodeAgent, InferenceClientModel

load_dotenv(Path(__file__).resolve().parent / ".env")


def create_secure_agent() -> CodeAgent:
    """Build a CodeAgent that runs generated code in an E2B sandbox."""
    if not os.environ.get("E2B_API_KEY"):
        raise EnvironmentError(
            "E2B_API_KEY is required for E2B execution. "
            "Create a key at https://e2b.dev/dashboard and set E2B_API_KEY in .env or your shell."
        )

    model = InferenceClientModel(
        model_id="Qwen/Qwen2.5-Coder-7B-Instruct",
        provider="hf-inference",
    )

    # Only these *extra* modules beyond smolagents' BASE_BUILTIN_MODULES.
    additional_authorized_imports = ["json"]

    return CodeAgent(
        tools=[],
        model=model,
        executor_type="e2b",
        executor_kwargs={"api_key": os.environ["E2B_API_KEY"]},
        additional_authorized_imports=additional_authorized_imports,
        max_print_outputs_length=10_000,
    )


if __name__ == "__main__":
    agent = create_secure_agent()
    try:
        print(
            agent.run(
                "Compute the sum of integers from 1 to 100 using Python code and return the result."
            )
        )
    finally:
        agent.cleanup()
