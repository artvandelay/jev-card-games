"""Exact exploitability and policy metrics from probe logs."""

from __future__ import annotations

import json
from collections import defaultdict

import numpy as np
import pyspiel
from open_spiel.python import policy as os_policy
from open_spiel.python.algorithms import expected_game_score, exploitability

from kuhn_lab.kuhn import (
    ALPHAS,
    HIGHER_CARD_TRUTH,
    INFOSETS_P0,
    METRICS_PATH,
    PROBE_PATH,
)
from kuhn_lab.nash import nash_p_bet_table, nash_policy, run_sanity_gates
from kuhn_lab.policy_build import (
    determinism,
    jev_p_bet_table,
    jev_policy,
    load_probe,
)


def _closest_alpha(p0_table: dict[str, float]) -> dict:
    best_alpha = 0.0
    best_residual = float("inf")
    grid = np.arange(0.0, 1.0 / 3.0 + 0.0005, 0.001)
    for alpha in grid:
        nash = nash_p_bet_table(alpha)
        residual = 0.0
        for key in INFOSETS_P0:
            residual += (p0_table[key] - nash[key]) ** 2
        if residual < best_residual:
            best_residual = residual
            best_alpha = float(alpha)
    return {
        "alpha": best_alpha,
        "residual_sse": float(best_residual),
    }


def compute_metrics(probe_path=PROBE_PATH, game=None) -> dict:
    if game is None:
        game = pyspiel.load_game("kuhn_poker")
    records = load_probe(probe_path)
    table = jev_p_bet_table(records)
    jev = jev_policy(game, table)

    nash_conv = exploitability.nash_conv(game, jev, return_only_nash_conv=False)
    metrics: dict = {
        "exploitability": float(exploitability.exploitability(game, jev)),
        "player_improvements": [
            float(x) for x in nash_conv.player_improvements
        ],
        "reference_exploitability": {},
        "expected_value": {},
        "infoset_deltas": {},
        "closest_alpha": _closest_alpha({k: table[k] for k in INFOSETS_P0}),
        "calibration_higher_card": {},
        "determinism": determinism(records),
        "jev_p_bet": table,
    }

    uniform = os_policy.UniformRandomPolicy(game)
    metrics["reference_exploitability"]["uniform_random"] = float(
        exploitability.exploitability(game, uniform)
    )
    for alpha in ALPHAS:
        nash = nash_policy(game, alpha)
        metrics["reference_exploitability"][str(alpha)] = float(
            exploitability.exploitability(game, nash)
        )
        merged_jev_first = os_policy.merge_tabular_policies([jev, nash], game)
        merged_nash_first = os_policy.merge_tabular_policies([nash, jev], game)
        root = game.new_initial_state()
        metrics["expected_value"][str(alpha)] = {
            "jev_seat_0": float(
                expected_game_score.policy_value(root, [merged_jev_first, merged_jev_first])[0]
            ),
            "jev_seat_1": float(
                expected_game_score.policy_value(root, [merged_nash_first, merged_nash_first])[1]
            ),
        }
        deltas = {}
        nash_table = nash_p_bet_table(alpha)
        for key in table:
            deltas[key] = float(table[key] - nash_table[key])
        metrics["infoset_deltas"][str(alpha)] = deltas

    by_card: dict[str, list[float]] = defaultdict(list)
    for row in records:
        by_card[row["card"]].append(float(row["you_hold_higher_card"]))
    cal = {}
    for card, truth in HIGHER_CARD_TRUTH.items():
        mean_noul = float(np.mean(by_card[card])) if by_card[card] else float("nan")
        cal[card] = {
            "mean_noul": mean_noul,
            "truth": truth,
            "abs_error": abs(mean_noul - truth) if by_card[card] else float("nan"),
        }
    metrics["calibration_higher_card"] = cal
    metrics["note_p1_alpha_independent"] = (
        "Player 1 Nash betting frequencies are unique (alpha-independent)."
    )
    return metrics


def print_summary(metrics: dict) -> None:
    print("=== Kuhn Lab Metrics ===")
    print(f"exploitability (chips/hand): {metrics['exploitability']:.6f}")
    pi = metrics["player_improvements"]
    print(f"player improvements: P0={pi[0]:.6f} P1={pi[1]:.6f}")
    ca = metrics["closest_alpha"]
    print(f"closest_alpha (P0 only): {ca['alpha']:.4f} sse={ca['residual_sse']:.6f}")
    print("reference exploitability:", metrics["reference_exploitability"])


def main() -> None:
    run_sanity_gates()
    metrics = compute_metrics()
    METRICS_PATH.parent.mkdir(parents=True, exist_ok=True)
    with METRICS_PATH.open("w") as handle:
        json.dump(metrics, handle, indent=2)
        handle.write("\n")
    print_summary(metrics)
    print(f"wrote {METRICS_PATH}")


if __name__ == "__main__":
    main()
