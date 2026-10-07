"""OpenRouter Decisions API client for typesafe/jev-1.13."""

from __future__ import annotations

import json
import os
import urllib.error
import urllib.request
from pathlib import Path

from dotenv import load_dotenv

MODEL = "typesafe/jev-1.13"
DECISIONS_URL = "https://openrouter.ai/api/alpha/decisions"
ROOT = Path(__file__).resolve().parents[2]

# Gymnasium Blackjack-v1: 0 stand, 1 hit.
ACTION_TO_ID = {"stand": 0, "hit": 1}


def load_key() -> str:
    load_dotenv(ROOT / ".env")
    key = os.environ.get("OPENROUTER_API_KEY", "").strip()
    if not key:
        raise SystemExit(
            "OPENROUTER_API_KEY is missing. Put it in .env at the project root."
        )
    return key


def decide(state: dict) -> dict:
    """Ask Jev for one stand/hit Choice. Returns the raw answer plus the gym action id."""
    body = {
        "model": MODEL,
        "state": state,
        "questions": {
            "action": {
                "type": "choice",
                "instructions": "Choose the action.",
                "criteria": {
                    "stand": "stand",
                    "hit": "hit",
                },
            }
        },
    }
    request = urllib.request.Request(
        DECISIONS_URL,
        data=json.dumps(body).encode(),
        headers={
            "Authorization": f"Bearer {load_key()}",
            "Content-Type": "application/json",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            payload = json.load(response)
    except urllib.error.HTTPError as error:
        detail = error.read().decode("utf-8", errors="replace")
        raise SystemExit(f"Jev request failed ({error.code}): {detail}") from error

    answer = payload["answers"]["action"]
    choice = answer["choice"]
    if choice not in ACTION_TO_ID:
        raise SystemExit(f"Jev returned an unknown action: {choice}")
    return {
        "model": payload.get("model", MODEL),
        "action": ACTION_TO_ID[choice],
        "action_name": choice,
        "probabilities": answer.get("probabilities"),
        "confidence": answer.get("confidence"),
        "usage": payload.get("usage"),
    }
