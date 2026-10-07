"""OpenRouter Decisions API client for Kuhn Poker."""

from __future__ import annotations

import json
import os
import urllib.error
import urllib.request
from pathlib import Path

from dotenv import load_dotenv

from kuhn_lab.kuhn import ACTION_BET, jev_instructions

MODEL = "typesafe/jev-1.13"
DECISIONS_URL = "https://openrouter.ai/api/alpha/decisions"
ROOT = Path(__file__).resolve().parents[2]

def load_key() -> str:
    load_dotenv(ROOT / ".env")
    key = os.environ.get("OPENROUTER_API_KEY", "").strip()
    if not key:
        raise SystemExit(
            "OPENROUTER_API_KEY is missing. Put it in .env at the project root."
        )
    return key


def _p_bet(probabilities: dict[str, float], action_names: dict[str, int]) -> float:
    bet_label = next(name for name, aid in action_names.items() if aid == ACTION_BET)
    p_bet = float(probabilities.get(bet_label, 0.0))
    total = sum(float(probabilities.get(n, 0.0)) for n in action_names)
    if abs(total - 1.0) > 1e-6 and total > 0:
        p_bet /= total
    return p_bet


def decide(
    state: dict,
    action_names: dict[str, int],
    facing_bet: bool,
) -> dict:
    """Ask Jev for action probabilities and auxiliary Nouls."""
    history = state["history"]
    questions: dict = {
        "action": {
            "type": "choice",
            "instructions": jev_instructions(history),
            "criteria": {name: name for name in action_names},
        },
        "you_hold_higher_card": {
            "type": "noul",
            "instructions": (
                "Is `your_card` the higher of the two cards dealt in this hand?"
            ),
        },
    }
    if facing_bet:
        questions["opponent_is_bluffing"] = {
            "type": "noul",
            "instructions": (
                "Given the betting so far, is the opponent betting without the "
                "stronger card?"
            ),
        }

    body = {"model": MODEL, "state": state, "questions": questions}
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
        with urllib.request.urlopen(request, timeout=60) as response:
            payload = json.load(response)
    except urllib.error.HTTPError as error:
        detail = error.read().decode("utf-8", errors="replace")
        raise SystemExit(f"Jev request failed ({error.code}): {detail}") from error

    action_answer = payload["answers"]["action"]
    choice = action_answer["choice"]
    if choice not in action_names:
        raise SystemExit(f"Jev returned an unknown action: {choice}")
    probabilities = {
        name: float(action_answer.get("probabilities", {}).get(name, 0.0))
        for name in action_names
    }
    p_bet = _p_bet(probabilities, action_names)
    higher = float(payload["answers"]["you_hold_higher_card"]["noul"])
    bluff = None
    if facing_bet:
        bluff = float(payload["answers"]["opponent_is_bluffing"]["noul"])

    return {
        "model": payload.get("model", MODEL),
        "action": action_names[choice],
        "action_name": choice,
        "probabilities": probabilities,
        "p_bet": p_bet,
        "confidence": action_answer.get("confidence"),
        "you_hold_higher_card": higher,
        "opponent_is_bluffing": bluff,
        "usage": payload.get("usage"),
    }
