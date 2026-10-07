"""Nash equilibrium policies for Kuhn Poker via OpenSpiel."""

from __future__ import annotations

import pyspiel
from open_spiel.python import policy as os_policy
from open_spiel.python.algorithms import expected_game_score, exploitability

from kuhn_lab.kuhn import ALL_INFOSETS, ALPHAS, INFOSETS_P0, NASH_VALUE_P0


def nash_p_bet_table(alpha: float) -> dict[str, float]:
    """P(action Bet=1) per infoset from the closed-form Nash family."""
    if alpha < 0 or alpha > 1.0 / 3.0:
        raise ValueError("alpha must be in [0, 1/3]")
    three_alpha = 3 * alpha
    table = {
        "0": alpha,
        "0pb": 0.0,
        "1": 0.0,
        "1pb": 1.0 / 3.0 + alpha,
        "2": three_alpha,
        "2pb": 1.0,
        "0p": 1.0 / 3.0,
        "0b": 0.0,
        "1p": 0.0,
        "1b": 1.0 / 3.0,
        "2p": 1.0,
        "2b": 1.0,
    }
    return table


def nash_policy(game, alpha: float):
    pyspiel_tp = pyspiel.kuhn_poker.get_optimal_policy(alpha)
    return os_policy.pyspiel_policy_to_python_policy(game, pyspiel_tp)


def run_sanity_gates() -> None:
    game = pyspiel.load_game("kuhn_poker")
    print("=== Nash sanity gates ===")
    for alpha in ALPHAS:
        nash = nash_policy(game, alpha)
        exp = exploitability.exploitability(game, nash)
        root = game.new_initial_state()
        value = expected_game_score.policy_value(root, [nash, nash])[0]
        print(f"alpha={alpha:.6f} exploitability={exp:.2e} value_p0={value:.12f}")
        if exp >= 1e-9:
            raise SystemExit(f"Nash exploitability too high at alpha={alpha}: {exp}")
        if abs(value - NASH_VALUE_P0) >= 1e-9:
            raise SystemExit(
                f"Nash value mismatch at alpha={alpha}: {value} vs {NASH_VALUE_P0}"
            )
        table = nash_p_bet_table(alpha)
        for key in ALL_INFOSETS:
            got = float(nash.policy_for_key(key)[1])
            want = table[key]
            if abs(got - want) >= 1e-9:
                raise SystemExit(
                    f"Table mismatch {key} alpha={alpha}: got {got} want {want}"
                )
    print("All Nash sanity gates passed.")


if __name__ == "__main__":
    run_sanity_gates()
