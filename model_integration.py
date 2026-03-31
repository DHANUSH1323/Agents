"""Hugging Face Inference API model setup for smolagents.

The assessment name ``HfApiModel`` is not a separate class in smolagents; use
``InferenceClientModel``, which wraps ``huggingface_hub.InferenceClient``.
"""
from smolagents import InferenceClientModel

HfApiModel = InferenceClientModel

# Primary: smaller, lower latency / cost for development
model = HfApiModel(
    model_id="Qwen/Qwen2.5-Coder-7B-Instruct",
    provider="hf-inference",
)

# Alternative: larger model when you need more capacity (same router; check HF model card for availability)
alternative_model = HfApiModel(
    model_id="Qwen/Qwen2.5-Coder-32B-Instruct",
    provider="hf-inference",
)

__all__ = ["HfApiModel", "InferenceClientModel", "model", "alternative_model"]
