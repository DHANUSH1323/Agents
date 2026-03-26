# agent.py – models and model handling; other files import from here

import enable_langfuse_tracing  # noqa: F401
from langfuse import observe
import requests

OLLAMA_BASE_URL = "http://127.0.0.1:11434"
OLLAMA_CHAT_URL = f"{OLLAMA_BASE_URL}/api/chat"

DEFAULT_MODEL = "qwen2.5:3b"

MODELS = {
    "default": "qwen2.5:3b",
    "small": "qwen2.5:3b",
    "medium": "qwen2.5:7b",
    "large": "llama3.2:latest",
}


@observe(name="ollama_chat", as_type="generation")
def chat(messages, model=None, stream=False):
    """Call the model with the given messages. Other files use this only."""
    payload = {
        "model": model or DEFAULT_MODEL,
        "messages": messages,
        "stream": stream,
    }
    r = requests.post(OLLAMA_CHAT_URL, json=payload, timeout=60)
    r.raise_for_status()
    data = r.json()
    return data["message"]["content"]