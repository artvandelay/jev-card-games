"""Compute episode statistics and basic-strategy agreement from logged play.

Reads results/episodes.jsonl and writes results/summary.json.
"""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
RESULTS = ROOT / "results"
LOG_PATH = RESULTS / "episodes.jsonl"
SUMMARY_PATH = RESULTS / "summary.json"

ACTION_STAND = 0
ACTION_HIT = 1


def _dealer_rank(dealer_showing: str) -> int:
    if dealer_showing == "A":
        return 1
    return int(dealer_showing)


def basic_strategy_action(player_sum: int, dealer_showing: str, usable_ace: bool) -> int:
    """Return canonical basic-strategy action: 0 stand, 1 hit."""
    dealer = _dealer_rank(dealer_showing)

    if usable_ace:
        if player_sum >= 19:
            return ACTION_STAND
        if player_sum == 18:
            # Stand vs 2-8; hit vs 9, 10, A
            if dealer in (9, 10, 1):
                return ACTION_HIT
            return ACTION_STAND
        # Soft totals <= 17 hit
        return ACTION_HIT

    # Hard totals
    if player_sum >= 17:
        return ACTION_STAND
    if player_sum <= 11:
        return ACTION_HIT
    if player_sum == 12:
        # Stand vs 4-6; hit vs 2, 3, 7-A
        if dealer in (4, 5, 6):
            return ACTION_STAND
        return ACTION_HIT
    # 13-16: stand vs 2-6; hit vs 7-A
    if dealer in (2, 3, 4, 5, 6):
        return ACTION_STAND
    return ACTION_HIT


def load_episodes(path: Path = LOG_PATH) -> list[dict]:
    if not path.exists():
        raise SystemExit(f"No log at {path}. Run: blackjack-lab play")
    with path.open() as handle:
        return [json.loads(line) for line in handle if line.strip()]


def _percentile(values: list[float], q: float) -> float:
    if not values:
        return 0.0
    return float(np.percentile(values, q))


def analyze(episodes: list[dict]) -> dict:
    rewards = [float(episode["reward"]) for episode in episodes]
    n = len(episodes)
    wins = sum(1 for reward in rewards if reward > 0)
    losses = sum(1 for reward in rewards if reward < 0)
    pushes = sum(1 for reward in rewards if reward == 0)

    mean_reward = float(np.mean(rewards)) if rewards else 0.0
    if n > 1:
        reward_stderr = float(np.std(rewards, ddof=1) / np.sqrt(n))
    elif n == 1:
        reward_stderr = 0.0
    else:
        reward_stderr = 0.0

    latencies: list[float] = []
    costs: list[float] = []
    total_input_tokens = 0
    total_output_tokens = 0
    agreements = 0
    total_decisions = 0

    for episode in episodes:
        for step in episode["steps"]:
            total_decisions += 1
            obs = step["observation"]
            recommended = basic_strategy_action(
                obs["player_sum"],
                obs["dealer_showing"],
                obs["usable_ace"],
            )
            if int(step["action"]) == recommended:
                agreements += 1

            elapsed = step.get("elapsed_ms")
            if elapsed is not None:
                latencies.append(float(elapsed))

            usage = step.get("usage")
            if usage:
                if usage.get("cost") is not None:
                    costs.append(float(usage["cost"]))
                total_input_tokens += int(usage.get("input_tokens") or 0)
                total_output_tokens += int(usage.get("output_tokens") or 0)

    total_cost = float(sum(costs)) if costs else 0.0
    cost_per_decision = (
        total_cost / total_decisions if total_decisions else 0.0
    )
    cost_per_episode = total_cost / n if n else 0.0
    agreement_rate = (
        agreements / total_decisions if total_decisions else 0.0
    )

    summary = {
        "total_episodes": n,
        "total_decisions": total_decisions,
        "wins": wins,
        "losses": losses,
        "pushes": pushes,
        "win_rate": wins / n if n else 0.0,
        "loss_rate": losses / n if n else 0.0,
        "push_rate": pushes / n if n else 0.0,
        "mean_reward": mean_reward,
        "reward_stderr": reward_stderr,
        "latency_ms": {
            "mean": float(np.mean(latencies)) if latencies else 0.0,
            "p50": _percentile(latencies, 50),
            "p90": _percentile(latencies, 90),
            "p95": _percentile(latencies, 95),
            "p99": _percentile(latencies, 99),
            "min": float(min(latencies)) if latencies else 0.0,
            "max": float(max(latencies)) if latencies else 0.0,
        },
        "cost": {
            "total_cost": total_cost,
            "cost_per_decision": cost_per_decision,
            "cost_per_episode": cost_per_episode,
            "total_input_tokens": total_input_tokens,
            "total_output_tokens": total_output_tokens,
        },
        "basic_strategy_agreement_rate": agreement_rate,
    }
    return summary


def print_summary(summary: dict) -> None:
    lat = summary["latency_ms"]
    cost = summary["cost"]
    print("=== Blackjack Lab Summary ===")
    print(f"episodes:   {summary['total_episodes']}")
    print(f"decisions:  {summary['total_decisions']}")
    print(
        f"W/L/P:      {summary['wins']}/{summary['losses']}/{summary['pushes']} "
        f"({summary['win_rate']:.1%} / {summary['loss_rate']:.1%} / {summary['push_rate']:.1%})"
    )
    print(
        f"mean reward: {summary['mean_reward']:+.4f} "
        f"(stderr {summary['reward_stderr']:.4f})"
    )
    print(
        f"latency ms:  mean={lat['mean']:.1f} p50={lat['p50']:.1f} "
        f"p90={lat['p90']:.1f} p95={lat['p95']:.1f} p99={lat['p99']:.1f} "
        f"min={lat['min']:.1f} max={lat['max']:.1f}"
    )
    print(
        f"cost:        total=${cost['total_cost']:.6f} "
        f"per_decision=${cost['cost_per_decision']:.6f} "
        f"per_episode=${cost['cost_per_episode']:.6f} "
        f"tokens in/out={cost['total_input_tokens']}/{cost['total_output_tokens']}"
    )
    print(
        f"basic strategy agreement: {summary['basic_strategy_agreement_rate']:.1%}"
    )


def main() -> None:
    episodes = load_episodes()
    summary = analyze(episodes)
    RESULTS.mkdir(parents=True, exist_ok=True)
    with SUMMARY_PATH.open("w") as handle:
        json.dump(summary, handle, indent=2)
        handle.write("\n")
    print_summary(summary)
    print(f"wrote {SUMMARY_PATH}")


if __name__ == "__main__":
    main()
