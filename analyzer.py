"""Single Gemini call -> ScamReport."""
import os
from typing import Optional

from dotenv import load_dotenv
from google import genai
from google.genai import types

from prompts import SYSTEM_PROMPT
from schema import ScamReport

load_dotenv()

DEFAULT_MODEL = "gemini-3.8-flash"


class AnalysisError(Exception):
    """Friendly, user-safe error."""


def _get_client() -> genai.Client:
    key = os.getenv("GEMINI_API_KEY")
    if not key or key == "your_key_here":
        raise AnalysisError(
            "Missing GEMINI_API_KEY. Copy .env.example to .env and add your key."
        )
    return genai.Client(api_key=key)


def analyze(
    text: Optional[str],
    image_bytes: Optional[bytes] = None,
    image_mime: Optional[str] = None,
) -> ScamReport:
    """Analyze a message and/or screenshot. Retries once on failure."""
    text = (text or "").strip()
    if not text and not image_bytes:
        raise AnalysisError("Please paste a message or upload a screenshot.")

    client = _get_client()
    model = os.getenv("GEMINI_MODEL") or DEFAULT_MODEL

    contents = []
    if text:
        contents.append(f"Analyze this message:\n\n{text}")
    if image_bytes:
        contents.append(
            types.Part.from_bytes(data=image_bytes, mime_type=image_mime or "image/png")
        )
        if not text:
            contents.append("Analyze the message shown in this screenshot.")

    config = types.GenerateContentConfig(
        system_instruction=SYSTEM_PROMPT,
        response_mime_type="application/json",
        response_schema=ScamReport,
        temperature=0.2,
    )

    last_err: Optional[Exception] = None
    for _ in range(2):  # initial try + one retry
        try:
            resp = client.models.generate_content(
                model=model, contents=contents, config=config
            )
            parsed = getattr(resp, "parsed", None)
            if isinstance(parsed, ScamReport):
                return parsed
            return ScamReport.model_validate_json(resp.text)
        except Exception as e:  # noqa: BLE001 - never leak raw traces to the UI
            last_err = e
    # Log to console only (not the UI)
    print(f"[ScamShield] analysis failed: {type(last_err).__name__}: {last_err}")
    raise AnalysisError("Couldn't analyze. Please try again.")
