"""Macro charts, taken from Gymnasium's blackjack Q-learning tutorial.

Source: docs/tutorials/training_agents/blackjack_q_learning.py
The reward and length panels match that notebook. The third panel there is
training error; here it is mean decision confidence, because this run does
not train a Q table. The policy figure is their create_plots: a state-value
surface and a stand/hit heatmap, once with a usable ace and once without.
State value is the mean terminal reward of hands that visited the cell,
which is the Monte Carlo return for this one-step-reward game.
"""

from __future__ import annotations

import json
from collections import defaultdict
from pathlib import Path

import gymnasium as gym
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from matplotlib.patches import Patch

from blackjack_lab.play import LOG_PATH, RESULTS


def load_episodes() -> list[dict]:
    if not LOG_PATH.exists():
        raise SystemExit(f"No log at {LOG_PATH}. Run: blackjack-lab play")
    with LOG_PATH.open() as handle:
        return [json.loads(line) for line in handle if line.strip()]


def write_training_figure(episodes: list[dict], path: Path) -> None:
    rewards = np.array([episode["reward"] for episode in episodes], dtype=float)
    lengths = np.array([len(episode["steps"]) for episode in episodes], dtype=float)
    confidences = []
    for episode in episodes:
        values = [
            step["confidence"]
            for step in episode["steps"]
            if step["confidence"] is not None
        ]
        confidences.append(float(np.mean(values)) if values else np.nan)
    confidences = np.array(confidences, dtype=float)

    window = min(500, max(1, len(episodes) // 10))
    kernel = np.ones(window)

    def rolling(series: np.ndarray) -> np.ndarray:
        filled = np.where(np.isnan(series), 0.0, series)
        return np.convolve(filled, kernel, mode="valid") / window

    fig, axs = plt.subplots(ncols=3, figsize=(12, 5))
    reward_line = rolling(rewards)
    axs[0].set_title("Episode rewards")
    axs[0].plot(range(len(reward_line)), reward_line)
    length_line = rolling(lengths)
    axs[1].set_title("Episode lengths")
    axs[1].plot(range(len(length_line)), length_line)
    axs[2].set_title("Decision confidence")
    if np.isnan(confidences).all():
        axs[2].set_xlabel("No confidence on this policy")
    else:
        confidence_line = rolling(confidences)
        axs[2].plot(range(len(confidence_line)), confidence_line)
    fig.suptitle(f"Rolling window {window}, from the Gymnasium tutorial layout")
    plt.tight_layout()
    fig.savefig(path, dpi=120)
    plt.close(fig)


def _grids(episodes: list[dict], usable_ace: bool):
    returns = defaultdict(list)
    actions = defaultdict(list)
    for episode in episodes:
        for step in episode["steps"]:
            obs = step["observation"]
            if obs["usable_ace"] != usable_ace:
                continue
            dealer = 1 if obs["dealer_showing"] == "A" else int(obs["dealer_showing"])
            key = (obs["player_sum"], dealer, usable_ace)
            returns[key].append(episode["reward"])
            actions[key].append(step["action"])

    player_count, dealer_count = np.meshgrid(np.arange(12, 22), np.arange(1, 11))
    value = np.full(player_count.shape, np.nan)
    policy = np.full(player_count.shape, np.nan)
    for row in range(player_count.shape[0]):
        for col in range(player_count.shape[1]):
            key = (int(player_count[row, col]), int(dealer_count[row, col]), usable_ace)
            if key not in actions:
                continue
            value[row, col] = float(np.mean(returns[key]))
            counts = np.bincount(actions[key], minlength=2)
            policy[row, col] = int(np.argmax(counts))
    return (player_count, dealer_count, value), policy


def create_plots(value_grid, policy_grid, title: str):
    """Same figure as Gymnasium's create_plots in the blackjack tutorial."""
    player_count, dealer_count, value = value_grid
    fig = plt.figure(figsize=plt.figaspect(0.4))
    fig.suptitle(title, fontsize=16)

    ax1 = fig.add_subplot(1, 2, 1, projection="3d")
    if np.isnan(value).all():
        ax1.set_title(f"State values: {title}")
        ax1.text2D(0.1, 0.5, "No hands in this chart")
    else:
        masked = np.ma.array(value, mask=np.isnan(value))
        ax1.plot_surface(
            player_count,
            dealer_count,
            masked,
            rstride=1,
            cstride=1,
            cmap="viridis",
            edgecolor="none",
        )
    plt.xticks(range(12, 22), range(12, 22))
    plt.yticks(range(1, 11), ["A"] + list(range(2, 11)))
    ax1.set_title(f"State values: {title}")
    ax1.set_xlabel("Player sum")
    ax1.set_ylabel("Dealer showing")
    ax1.zaxis.set_rotate_label(False)
    ax1.set_zlabel("Value", fontsize=14, rotation=90)
    ax1.view_init(20, 220)

    fig.add_subplot(1, 2, 2)
    ax2 = sns.heatmap(
        policy_grid,
        linewidth=0,
        annot=True,
        cmap="Accent_r",
        cbar=False,
        mask=np.isnan(policy_grid),
    )
    ax2.set_title(f"Policy: {title}")
    ax2.set_xlabel("Player sum")
    ax2.set_ylabel("Dealer showing")
    ax2.set_xticklabels(range(12, 22))
    ax2.set_yticklabels(["A"] + list(range(2, 11)), fontsize=12)
    legend_elements = [
        Patch(facecolor="lightgreen", edgecolor="black", label="Hit"),
        Patch(facecolor="grey", edgecolor="black", label="Stick"),
    ]
    ax2.legend(handles=legend_elements, bbox_to_anchor=(1.3, 1))
    return fig


def render_episode(episode: dict, directory: Path) -> list[Path]:
    """Save Gymnasium's rgb_array frames for one logged hand."""
    directory.mkdir(parents=True, exist_ok=True)
    env = gym.make("Blackjack-v1", sab=True, render_mode="rgb_array")
    env.reset(seed=episode["seed"])
    frames = []
    frame = env.render()
    path = directory / "step-0.png"
    plt.imsave(path, frame)
    frames.append(path)
    for index, step in enumerate(episode["steps"], start=1):
        env.step(step["action"])
        frame = env.render()
        path = directory / f"step-{index}.png"
        plt.imsave(path, frame)
        frames.append(path)
    env.close()
    return frames


def _html(episodes: list[dict], frame_paths: dict[int, list[Path]]) -> str:
    rewards = [episode["reward"] for episode in episodes]
    wins = sum(reward > 0 for reward in rewards)
    losses = sum(reward < 0 for reward in rewards)
    draws = sum(reward == 0 for reward in rewards)
    mean_reward = float(np.mean(rewards)) if rewards else 0.0
    win_rate = 100.0 * wins / len(episodes) if episodes else 0.0
    loss_rate = 100.0 * losses / len(episodes) if episodes else 0.0

    latencies = [
        step["elapsed_ms"]
        for episode in episodes
        for step in episode["steps"]
        if step.get("elapsed_ms") is not None
    ]
    costs = [
        step["usage"]["cost"]
        for episode in episodes
        for step in episode["steps"]
        if step.get("usage") and step["usage"].get("cost") is not None
    ]
    p50_lat = float(np.percentile(latencies, 50)) if latencies else 0.0
    mean_lat = float(np.mean(latencies)) if latencies else 0.0
    total_cost = float(np.sum(costs)) if costs else 0.0
    cost_per_turn = float(np.mean(costs)) if costs else 0.0
    rows = []
    for episode in episodes:
        actions = " ".join(step["action_name"] for step in episode["steps"])
        rows.append(
            "<tr>"
            f"<td><a href='#episode-{episode['episode']}'>{episode['episode']}</a></td>"
            f"<td>{episode['reward']:+.0f}</td>"
            f"<td>{actions}</td>"
            f"<td>{episode['seed']}</td>"
            "</tr>"
        )
    sections = []
    for episode in episodes:
        images = []
        for path in frame_paths.get(episode["episode"], []):
            relative = path.relative_to(RESULTS).as_posix()
            images.append(f"<img src='{relative}' alt='{relative}'>")
        steps = []
        for index, step in enumerate(episode["steps"]):
            obs = step["observation"]
            steps.append(
                "<li>"
                f"sum {obs['player_sum']}, dealer {obs['dealer_showing']}, "
                f"usable ace {obs['usable_ace']}: "
                f"<strong>{step['action_name']}</strong> "
                f"probabilities {json.dumps(step['probabilities'])} "
                f"confidence {step['confidence']} "
                f"latency {step.get('elapsed_ms')} ms "
                f"reward {step['reward']:+.0f}"
                "</li>"
            )
        sections.append(
            f"<section id='episode-{episode['episode']}'>"
            f"<h2>Episode {episode['episode']}</h2>"
            f"<p>Seed {episode['seed']}. Reward {episode['reward']:+.0f}. "
            f"Model {episode.get('model')}.</p>"
            f"<div class='frames'>{''.join(images)}</div>"
            f"<ol>{''.join(steps)}</ol>"
            "</section>"
        )
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>Blackjack lab</title>
<style>
body {{ font: 15px/1.4 sans-serif; margin: 2rem; max-width: 1100px; }}
img {{ max-width: 100%; height: auto; }}
.frames img {{ width: 280px; margin: 0 0.5rem 0.5rem 0; vertical-align: top; }}
table {{ border-collapse: collapse; }}
td, th {{ border: 1px solid #ccc; padding: 0.3rem 0.6rem; text-align: left; }}
.metrics {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 0.75rem; margin: 1rem 0; }}
.card {{ border: 1px solid #ccc; padding: 0.75rem; border-radius: 6px; }}
.card strong {{ display: block; font-size: 1.1rem; }}
</style>
</head>
<body>
<h1>Blackjack-v1</h1>
<div class="metrics">
<div class="card">Total Episodes<strong>{len(episodes)}</strong></div>
<div class="card">Win Rate %<strong>{win_rate:.1f}%</strong></div>
<div class="card">Loss Rate %<strong>{loss_rate:.1f}%</strong></div>
<div class="card">Mean Return<strong>{mean_reward:+.3f}</strong></div>
<div class="card">Turn Latency<strong>mean {mean_lat:.0f} ms, p50 {p50_lat:.0f} ms</strong></div>
<div class="card">Cost<strong>${total_cost:.5f} total, ${cost_per_turn:.8f} / turn</strong></div>
</div>
<p>Wins {wins}, losses {losses}, draws {draws}.</p>
<h2>Aggregate</h2>
<p>Charts follow the Gymnasium blackjack Q-learning tutorial.
Card frames are Gymnasium's rgb_array render of the logged actions.</p>
<img src="rewards.png" alt="Episode rewards, lengths, and confidence">
<img src="policy_usable_ace.png" alt="Policy with a usable ace">
<img src="policy_no_usable_ace.png" alt="Policy without a usable ace">
<h2>Hands</h2>
<table>
<thead><tr><th>Episode</th><th>Reward</th><th>Actions</th><th>Seed</th></tr></thead>
<tbody>
{''.join(rows)}
</tbody>
</table>
{''.join(sections)}
</body>
</html>
"""


def report() -> Path:
    episodes = load_episodes()
    RESULTS.mkdir(parents=True, exist_ok=True)
    write_training_figure(episodes, RESULTS / "rewards.png")
    for usable_ace, name in (
        (True, "policy_usable_ace.png"),
        (False, "policy_no_usable_ace.png"),
    ):
        title = "With usable ace" if usable_ace else "Without usable ace"
        value_grid, policy_grid = _grids(episodes, usable_ace)
        fig = create_plots(value_grid, policy_grid, title)
        fig.savefig(RESULTS / name, dpi=120, bbox_inches="tight")
        plt.close(fig)

    frame_paths = {}
    render_limit = 100 if len(episodes) <= 100 else 50
    for episode in episodes[:render_limit]:
        directory = RESULTS / "episodes" / str(episode["episode"])
        frame_paths[episode["episode"]] = render_episode(episode, directory)

    page = RESULTS / "index.html"
    page.write_text(_html(episodes, frame_paths))
    print(f"wrote {page}")
    return page
