"""Play Gymnasium Blackjack-v1 and log every decision.

The environment is the Sutton and Barto version from the Gymnasium
Q-learning tutorial: gym.make("Blackjack-v1", sab=True).
"""

from __future__ import annotations

import json
from pathlib import Path
import time

import gymnasium as gym
import numpy as np

from blackjack_lab.jev import decide

ROOT = Path(__file__).resolve().parents[2]
RESULTS = ROOT / "results"
LOG_PATH = RESULTS / "episodes.jsonl"

ACTION_NAMES = {0: "stand", 1: "hit"}


def observation_state(obs: tuple) -> dict:
    player_sum, dealer_showing, usable_ace = obs
    dealer = int(dealer_showing)
    return {
        "player_sum": int(player_sum),
        "dealer_showing": "A" if dealer == 1 else str(dealer),
        "usable_ace": bool(usable_ace),
    }


def make_player_hand(player_sum: int, usable_ace: bool) -> list[int]:
    if usable_ace:
        remainder = player_sum - 11
        if remainder == 1:
            return [1, 1]
        return [1, remainder]
    else:
        if player_sum == 21:
            return [10, 6, 5]
        return [10, player_sum - 10]


def set_custom_state(
    env: gym.Env,
    player_sum: int,
    dealer_up: int,
    usable_ace: bool,
    rng: np.random.Generator,
) -> tuple:
    env.reset()
    env.unwrapped.player = make_player_hand(player_sum, usable_ace)
    hole_card = int(rng.choice([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10]))
    env.unwrapped.dealer = [dealer_up, hole_card]
    suits = ["C", "D", "H", "S"]
    env.unwrapped.dealer_top_card_suit = rng.choice(suits)
    if dealer_up == 1:
        env.unwrapped.dealer_top_card_value_str = "A"
    elif dealer_up == 10:
        env.unwrapped.dealer_top_card_value_str = rng.choice(["J", "Q", "K"])
    else:
        env.unwrapped.dealer_top_card_value_str = str(dealer_up)
    return env.unwrapped._get_obs()


def play(
    episodes: int = 50,
    policy: str = "jev",
    seed: int = 0,
    mode: str = "random",
    reps_per_box: int = 3,
    output_path: Path | None = None,
) -> Path:
    out = output_path or LOG_PATH
    out.parent.mkdir(parents=True, exist_ok=True)
    env = gym.make("Blackjack-v1", sab=True)
    rng = np.random.default_rng(seed)

    # Determine state sequence: either stratified grid or random deals
    if mode == "grid":
        # 10 player sums x 10 dealer showing x 2 usable ace conditions = 200 boxes
        states_to_run = []
        for rep in range(reps_per_box):
            for usable_ace in (False, True):
                for p_sum in range(12, 22):
                    for d_up in range(1, 11):
                        states_to_run.append((p_sum, d_up, usable_ace, rep))
        total_episodes = len(states_to_run)
    else:
        if episodes < 1:
            raise SystemExit("--episodes must be at least 1")
        total_episodes = episodes
        states_to_run = None

    # Clear/prepare log file
    out.write_text("")

    for episode in range(total_episodes):
        episode_seed = seed + episode
        if mode == "grid":
            p_sum, d_up, usable_ace, rep = states_to_run[episode]
            obs = set_custom_state(env, p_sum, d_up, usable_ace, rng)
        else:
            obs, _info = env.reset(seed=episode_seed)

        steps = []
        terminated = False
        truncated = False
        reward = 0.0
        model = None

        while not (terminated or truncated):
            state = observation_state(obs)
            if policy == "jev":
                t0 = time.perf_counter()
                decision = decide(state)
                elapsed_ms = round((time.perf_counter() - t0) * 1000, 1)
                model = decision["model"]
            elif policy == "random":
                t0 = time.perf_counter()
                action = int(rng.integers(0, 2))
                decision = {
                    "model": "random",
                    "action": action,
                    "action_name": ACTION_NAMES[action],
                    "probabilities": {"stand": 0.5, "hit": 0.5},
                    "confidence": None,
                    "usage": None,
                }
                elapsed_ms = round((time.perf_counter() - t0) * 1000, 1)
                model = "random"
            else:
                raise SystemExit(f"Unknown policy: {policy}")

            obs, reward, terminated, truncated, _info = env.step(decision["action"])
            steps.append(
                {
                    "observation": state,
                    "action": decision["action"],
                    "action_name": decision["action_name"],
                    "probabilities": decision["probabilities"],
                    "confidence": decision["confidence"],
                    "elapsed_ms": elapsed_ms,
                    "usage": decision["usage"],
                    "reward": float(reward),
                    "terminated": bool(terminated),
                }
            )

        record = {
            "episode": episode,
            "seed": episode_seed,
            "policy": policy,
            "model": model,
            "reward": float(reward),
            "steps": steps,
        }
        with out.open("a") as handle:
            handle.write(json.dumps(record) + "\n")

        first_obs = steps[0]["observation"] if steps else {}
        print(
            f"episode {episode + 1}/{total_episodes} "
            f"[sum {first_obs.get('player_sum')} vs {first_obs.get('dealer_showing')}, ace={first_obs.get('usable_ace')}] "
            f"reward {reward:+.0f} actions {[s['action_name'] for s in steps]}",
            flush=True,
        )

    env.close()
    print(f"wrote {out}", flush=True)
    return out
