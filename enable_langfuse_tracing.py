"""Langfuse + OpenInference bootstrap for smolagents.

Import this as the **first** import in any script that uses smolagents so runs are
traced in Langfuse::

    import enable_langfuse_tracing  # noqa: F401

This loads ``.env``, initializes the Langfuse OpenTelemetry tracer (so spans
export to your project), then runs ``SmolagentsInstrumentor``. The OpenTelemetry
instrumentor is a singleton; calling ``instrument()`` again is a no-op.

For code that does not use smolagents (e.g. direct HTTP to Ollama), import this
module first, then use ``from langfuse import observe`` and ``@observe()`` on
functions you want traced.
"""
from __future__ import annotations

import atexit

from dotenv import load_dotenv

load_dotenv()

from langfuse import get_client
from openinference.instrumentation.smolagents import SmolagentsInstrumentor

_client = get_client()
SmolagentsInstrumentor().instrument()


def flush() -> None:
    """Flush pending Langfuse data (also registered on process exit)."""
    _client.flush()


atexit.register(flush)
