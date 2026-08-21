"""
ibm_granite.py — IBM Granite LLM wrapper for SaltGuard AI.
Loads credentials from .env and exposes a simple generate_response() method.
"""

import os
import time
from pathlib import Path
from dotenv import load_dotenv
from ibm_watsonx_ai import Credentials
from ibm_watsonx_ai.foundation_models import ModelInference

# Always load .env from the same directory as this file, regardless of cwd
load_dotenv(dotenv_path=Path(__file__).parent / ".env", override=True)

# Retry config for 429 rate-limit errors
_MAX_RETRIES = 4
_RETRY_DELAYS = [5, 15, 30, 60]  # seconds between each attempt


class GraniteAgent:
    """Thin wrapper around IBM watsonx.ai ModelInference for Granite models."""

    def __init__(self):
        api_key    = os.getenv("IBM_API_KEY")
        project_id = os.getenv("IBM_PROJECT_ID")
        wml_url    = os.getenv("IBM_WML_URL", "https://us-south.ml.cloud.ibm.com")
        model_id   = os.getenv("WATSONX_MODEL_ID", "ibm/granite-3-2-8b-instruct")

        if not api_key:
            raise ValueError("IBM_API_KEY is not set in .env")
        if not project_id:
            raise ValueError("IBM_PROJECT_ID is not set in .env")

        credentials = Credentials(url=wml_url, api_key=api_key)

        self.model = ModelInference(
            model_id=model_id,
            credentials=credentials,
            project_id=project_id,
            params={
                "max_new_tokens": 512,
                "temperature": 0.3,
                "repetition_penalty": 1.1,
            },
        )

    def generate_response(self, prompt: str) -> str:
        """Send prompt to IBM model with retry on 429 rate-limit errors."""
        last_error = None
        for attempt, delay in enumerate(
            [0] + _RETRY_DELAYS, start=1
        ):
            if delay:
                print(f"[SaltGuard] Rate limited. Retrying in {delay}s (attempt {attempt}/{_MAX_RETRIES})…")
                time.sleep(delay)
            try:
                result = self.model.generate_text(prompt=prompt)
                return result.strip()
            except Exception as exc:
                last_error = exc
                if "429" not in str(exc) and "consumption_limit_reached" not in str(exc):
                    # Not a rate-limit error — fail immediately
                    raise
        return f"⚠️ IBM watsonx.ai rate limit reached after {_MAX_RETRIES} retries. Please wait a minute and try again.\n\nDetail: {last_error}"


if __name__ == "__main__":
    agent = GraniteAgent()
    response = agent.generate_response(
        "What are the top 3 heat safety tips for outdoor salt pan workers?"
    )
    print(response)
