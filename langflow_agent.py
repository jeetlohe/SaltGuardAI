"""
langflow_agent.py — Langflow pipeline runner for SaltGuard AI.
Sends prompts to a local Langflow endpoint and falls back to IBM Granite
if Langflow is unreachable.
"""

import requests
from ibm_granite import GraniteAgent

LANGFLOW_URL = "http://127.0.0.1:7860/api/v1/run/saltguard-agent"
TIMEOUT      = 10  # seconds to wait for Langflow before giving up


def run_langflow_pipeline(user_prompt: str) -> str:
    """
    Send user_prompt to the local Langflow pipeline.

    Returns the output text from Langflow.
    Falls back to IBM Granite via GraniteAgent if Langflow is offline
    or returns an unexpected response.
    """
    try:
        response = requests.post(
            LANGFLOW_URL,
            json={
                "input_value": user_prompt,
                "input_type": "chat",
                "output_type": "chat",
            },
            timeout=TIMEOUT,
        )
        response.raise_for_status()
        data = response.json()

        # Langflow v1 response shape:
        # { "outputs": [ { "outputs": [ { "results": { "message": { "text": "..." } } } ] } ] }
        return (
            data["outputs"][0]["outputs"][0]["results"]["message"]["text"].strip()
        )

    except (requests.ConnectionError, requests.Timeout):
        # Langflow is offline — fall back to Granite
        return _granite_fallback(user_prompt, reason="Langflow is offline")

    except (requests.HTTPError, KeyError, IndexError, ValueError) as exc:
        # Langflow returned an error or unexpected shape — fall back to Granite
        return _granite_fallback(user_prompt, reason=str(exc))


def _granite_fallback(prompt: str, reason: str) -> str:
    """Invoke IBM Granite directly when Langflow is unavailable."""
    print(f"[SaltGuard] Langflow unavailable ({reason}). Falling back to IBM Granite.")
    try:
        agent = GraniteAgent()
        return agent.generate_response(prompt)
    except Exception as exc:
        return f"[Error] Both Langflow and IBM Granite are unavailable: {exc}"


if __name__ == "__main__":
    result = run_langflow_pipeline(
        "What are the recommended hydration guidelines for salt pan workers during extreme heat?"
    )
    print(result)
