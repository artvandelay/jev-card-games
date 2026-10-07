"""Summarize Kuhn play logs."""

from __future__ import annotations

import json
from collections import defaultdict
from pathlib import Path

import numpy as np

from kuhn_lab.kuhn import EPISODES_PATH, METRICS_PATH, SUMMARY_PATH


def load_episodes(path: Path = EPISODES_PATH) -> list[dict]:
    if not path.exists():
        raise SystemExit(f"No log at {path}. Run: kuhn-lab play")
    with path.open() as handle:
        return [json.loads(line) for line in handle if line.strip()]


def _percentile(values: list[float], q: float) -> float:
    if not values:
        return 0.0
    return float(np.percentile(values, q))


def _group_stats(episodes: list[dict], metrics: dict | None) -> dict:
    returns = [float(ep["jev_return"]) for ep in episodes]
    n = len(returns)
    mean_return = float(np.mean(returns)) if returns else 0.0
    if n > 1:
        stderr = float(np.std(returns, ddof=1) / np.sqrt(n))
    elif n == 1:
        stderr = 0.0
    else:
        stderr = 0.0

    wins = sum(1 for r in returns if r > 0)
    losses = sum(1 for r in returns if r < 0)
    zeros = sum(1 for r in returns if r == 0)

    latencies: list[float] = []
    costs: list[float] = []
    total_input_tokens = 0
    total_output_tokens = 0
    for ep in episodes:
        for step in ep["steps"]:
            if step.get("actor") != "jev":
                continue
            if step.get("elapsed_ms") is not None:
                latencies.append(float(step["elapsed_ms"]))
            usage = step.get("usage")
            if usage:
                if usage.get("cost") is not None:
                    costs.append(float(usage["cost"]))
                total_input_tokens += int(usage.get("input_tokens") or 0)
                total_output_tokens += int(usage.get("output_tokens") or 0)

    total_cost = float(sum(costs)) if costs else 0.0
    jev_decisions = sum(
        1 for ep in episodes for step in ep["steps"] if step.get("actor") == "jev"
    )

    out = {
        "hands": n,
        "mean_jev_return": mean_return,
        "jev_return_stderr": stderr,
        "wins": wins,
        "losses": losses,
        "zeros": zeros,
        "win_rate": wins / n if n else 0.0,
        "loss_rate": losses / n if n else 0.0,
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
            "cost_per_decision": total_cost / jev_decisions if jev_decisions else 0.0,
            "cost_per_hand": total_cost / n if n else 0.0,
            "total_input_tokens": total_input_tokens,
            "total_output_tokens": total_output_tokens,
        },
        "gap_vs_exact_value": None,
    }
    if metrics and episodes:
        alpha = episodes[0].get("alpha")
        seat = episodes[0].get("jev_seat")
        if alpha is not None and seat is not None:
            key = "jev_seat_0" if seat == 0 else "jev_seat_1"
            exact = metrics.get("expected_value", {}).get(str(alpha), {}).get(key)
            if exact is not None:
                out["gap_vs_exact_value"] = mean_return - float(exact)
    return out


def analyze(episodes: list[dict]) -> dict:
    metrics = None
    if METRICS_PATH.exists():
        with METRICS_PATH.open() as handle:
            metrics = json.load(handle)

    by_config: dict[str, list[dict]] = defaultdict(list)
    for ep in episodes:
        label = f"alpha={ep['alpha']}_seat={ep['jev_seat']}"
        by_config[label].append(ep)

    groups = {
        label: _group_stats(eps, metrics) for label, eps in sorted(by_config.items())
    }
    summary = {
        "overall": _group_stats(episodes, None),
        "by_config": groups,
    }
    return summary


def print_summary(summary: dict) -> None:
    print("=== Kuhn Lab Summary ===")
    overall = summary["overall"]
    print(f"hands: {overall['hands']}")
    print(
        f"mean jev return: {overall['mean_jev_return']:+.4f} "
        f"(stderr {overall['jev_return_stderr']:.4f})"
    )
    lat = overall["latency_ms"]
    print(
        f"latency ms: mean={lat['mean']:.1f} p50={lat['p50']:.1f} "
        f"p90={lat['p90']:.1f}"
    )
    cost = overall["cost"]
    print(f"cost: total=${cost['total_cost']:.6f}")


def main() -> None:
    episodes = load_episodes()
    summary = analyze(episodes)
    SUMMARY_PATH.parent.mkdir(parents=True, exist_ok=True)
    with SUMMARY_PATH.open("w") as handle:
        json.dump(summary, handle, indent=2)
        handle.write("\n")
    print_summary(summary)
    print(f"wrote {SUMMARY_PATH}")


if __name__ == "__main__":
    main()
