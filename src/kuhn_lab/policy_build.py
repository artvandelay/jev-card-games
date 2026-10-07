"""Build OpenSpiel TabularPolicy from probe logs."""

from __future__ import annotations

import json
from collections import defaultdict
from pathlib import Path

import numpy as np
from open_spiel.python import policy as os_policy

from kuhn_lab.kuhn import ALL_INFOSETS


def load_probe(path: Path) -> list[dict]:
    if not path.exists():
        raise SystemExit(f"No probe log at {path}. Run: kuhn-lab probe")
    with path.open() as handle:
        return [json.loads(line) for line in handle if line.strip()]


def jev_p_bet_table(records: list[dict]) -> dict[str, float]:
    buckets: dict[str, list[float]] = defaultdict(list)
    for row in records:
        buckets[row["infoset"]].append(float(row["p_bet"]))
    return {key: float(np.mean(values)) for key, values in buckets.items()}


def determinism(records: list[dict]) -> dict[str, dict]:
    buckets: dict[str, list[float]] = defaultdict(list)
    for row in records:
        buckets[row["infoset"]].append(float(row["p_bet"]))
    out: dict[str, dict] = {}
    for key, values in buckets.items():
        arr = np.array(values, dtype=float)
        out[key] = {
            "n": len(values),
            "min": float(arr.min()) if len(arr) else 0.0,
            "max": float(arr.max()) if len(arr) else 0.0,
            "spread": float(arr.max() - arr.min()) if len(arr) else 0.0,
            "mean": float(arr.mean()) if len(arr) else 0.0,
        }
    return out


def jev_policy(game, table: dict[str, float]):
    tp = os_policy.TabularPolicy(game)
    if set(tp.state_lookup) != set(ALL_INFOSETS):
        raise SystemExit(
            f"TabularPolicy keys {set(tp.state_lookup)} != ALL_INFOSETS {set(ALL_INFOSETS)}"
        )
    for key in ALL_INFOSETS:
        p_bet = float(table[key])
        tp.policy_for_key(key)[:] = [1.0 - p_bet, p_bet]
    return tp
