"""Charts and HTML report for Kuhn Poker evaluation."""

from __future__ import annotations

import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

from kuhn_lab.kuhn import (
    ALL_INFOSETS,
    METRICS_PATH,
    RESULTS,
    SUMMARY_PATH,
    EPISODES_PATH,
)
from kuhn_lab.nash import nash_p_bet_table


def _load_json(path: Path) -> dict:
    if not path.exists():
        raise SystemExit(f"Missing {path}")
    with path.open() as handle:
        return json.load(handle)


def write_policy_chart(metrics: dict, path: Path) -> None:
    jev = metrics["jev_p_bet"]
    alpha_close = metrics["closest_alpha"]["alpha"]
    nash_third = nash_p_bet_table(1.0 / 3.0)
    nash_close = nash_p_bet_table(alpha_close)
    x = np.arange(len(ALL_INFOSETS))
    width = 0.25
    fig, ax = plt.subplots(figsize=(14, 5))
    ax.bar(x - width, [jev[k] for k in ALL_INFOSETS], width, label="Jev P(bet)")
    ax.bar(x, [nash_third[k] for k in ALL_INFOSETS], width, label="Nash α=1/3")
    ax.bar(
        x + width,
        [nash_close[k] for k in ALL_INFOSETS],
        width,
        label=f"Nash α≈{alpha_close:.3f}",
    )
    ax.set_xticks(x)
    ax.set_xticklabels(ALL_INFOSETS, rotation=45, ha="right")
    ax.set_ylabel("P(bet)")
    ax.set_title("Jev vs Nash betting frequencies by infoset")
    ax.legend()
    fig.tight_layout()
    fig.savefig(path, dpi=120)
    plt.close(fig)


def write_exploitability_chart(metrics: dict, path: Path) -> None:
    labels = ["Jev"]
    values = [metrics["exploitability"]]
    for key, val in metrics["reference_exploitability"].items():
        labels.append(f"ref {key}")
        values.append(val)
    fig, ax = plt.subplots(figsize=(8, 4))
    y = np.arange(len(labels))
    ax.barh(y, values)
    ax.set_yticks(y)
    ax.set_yticklabels(labels)
    ax.set_xlabel("Exploitability (chips/hand)")
    ax.set_title("Exploitability comparison")
    fig.tight_layout()
    fig.savefig(path, dpi=120)
    plt.close(fig)


def write_calibration_chart(metrics: dict, path: Path) -> None:
    cal = metrics["calibration_higher_card"]
    cards = ["J", "Q", "K"]
    pred = [cal[c]["mean_noul"] for c in cards]
    truth = [cal[c]["truth"] for c in cards]
    fig, ax = plt.subplots(figsize=(5, 5))
    ax.scatter(truth, pred)
    ax.plot([0, 1], [0, 1], linestyle="--", color="gray")
    for i, card in enumerate(cards):
        ax.annotate(card, (truth[i], pred[i]))
    ax.set_xlabel("Truth P(higher card)")
    ax.set_ylabel("Jev mean Noul")
    ax.set_title("Higher-card calibration")
    fig.tight_layout()
    fig.savefig(path, dpi=120)
    plt.close(fig)


def write_latency_chart(episodes: list[dict], path: Path) -> None:
    latencies = [
        step["elapsed_ms"]
        for ep in episodes
        for step in ep["steps"]
        if step.get("actor") == "jev" and step.get("elapsed_ms") is not None
    ]
    returns = [ep["jev_return"] for ep in episodes]
    fig, axs = plt.subplots(ncols=2, figsize=(10, 4))
    if latencies:
        axs[0].hist(latencies, bins=30)
    axs[0].set_title("Jev decision latency (ms)")
    window = min(50, max(1, len(returns) // 10))
    if returns and window:
        kernel = np.ones(window)
        line = np.convolve(returns, kernel, mode="valid") / window
        axs[1].plot(line)
    axs[1].set_title(f"Rolling mean jev_return (window {window})")
    fig.tight_layout()
    fig.savefig(path, dpi=120)
    plt.close(fig)


def _html(metrics: dict, summary: dict, episodes: list[dict]) -> str:
    overall = summary["overall"]
    exploit = metrics["exploitability"]
    lat = overall["latency_ms"]
    cost = overall["cost"]
    rows = []
    for ep in episodes[:200]:
        rows.append(
            "<tr>"
            f"<td>{ep['episode']}</td>"
            f"<td>{ep['alpha']:.4f}</td>"
            f"<td>{ep['jev_seat']}</td>"
            f"<td>{ep['jev_return']:+.0f}</td>"
            "</tr>"
        )
    policy_rows = []
    jev = metrics["jev_p_bet"]
    nash = nash_p_bet_table(1.0 / 3.0)
    for key in ALL_INFOSETS:
        policy_rows.append(
            "<tr>"
            f"<td>{key}</td>"
            f"<td>{jev[key]:.3f}</td>"
            f"<td>{nash[key]:.3f}</td>"
            f"<td>{jev[key] - nash[key]:+.3f}</td>"
            "</tr>"
        )
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>Kuhn lab</title>
<style>
body {{ font: 15px/1.4 sans-serif; margin: 2rem; max-width: 1100px; }}
img {{ max-width: 100%; height: auto; }}
table {{ border-collapse: collapse; }}
td, th {{ border: 1px solid #ccc; padding: 0.3rem 0.6rem; text-align: left; }}
.metrics {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 0.75rem; margin: 1rem 0; }}
.card {{ border: 1px solid #ccc; padding: 0.75rem; border-radius: 6px; }}
.card strong {{ display: block; font-size: 1.1rem; }}
</style>
</head>
<body>
<h1>Kuhn Poker vs Nash</h1>
<div class="metrics">
<div class="card">Hands<strong>{overall['hands']}</strong></div>
<div class="card">Exploitability<strong>{exploit:.4f} chips/hand</strong></div>
<div class="card">Mean Jev return<strong>{overall['mean_jev_return']:+.4f}</strong></div>
<div class="card">Latency<strong>p50 {lat['p50']:.0f} ms</strong></div>
<div class="card">Cost<strong>${cost['total_cost']:.5f}</strong></div>
</div>
<img src="kuhn_policy.png" alt="Policy bars">
<img src="kuhn_exploitability.png" alt="Exploitability">
<img src="kuhn_calibration.png" alt="Calibration">
<img src="kuhn_latency.png" alt="Latency">
<h2>Policy table (α=1/3)</h2>
<table>
<thead><tr><th>Infoset</th><th>Jev P(bet)</th><th>Nash P(bet)</th><th>Delta</th></tr></thead>
<tbody>{''.join(policy_rows)}</tbody>
</table>
<h2>Sample hands</h2>
<table>
<thead><tr><th>Episode</th><th>Alpha</th><th>Jev seat</th><th>Return</th></tr></thead>
<tbody>{''.join(rows)}</tbody>
</table>
</body>
</html>
"""


def report() -> Path:
    metrics = _load_json(METRICS_PATH)
    summary = _load_json(SUMMARY_PATH)
    episodes = []
    if EPISODES_PATH.exists():
        with EPISODES_PATH.open() as handle:
            episodes = [json.loads(line) for line in handle if line.strip()]

    RESULTS.mkdir(parents=True, exist_ok=True)
    write_policy_chart(metrics, RESULTS / "kuhn_policy.png")
    write_exploitability_chart(metrics, RESULTS / "kuhn_exploitability.png")
    write_calibration_chart(metrics, RESULTS / "kuhn_calibration.png")
    write_latency_chart(episodes, RESULTS / "kuhn_latency.png")
    page = RESULTS / "kuhn.html"
    page.write_text(_html(metrics, summary, episodes))
    print(f"wrote {page}")
    return page


if __name__ == "__main__":
    report()
