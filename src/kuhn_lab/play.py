"""Sampled Kuhn Poker hands: Jev vs Nash."""

from __future__ import annotations

import json
import time
from pathlib import Path

import numpy as np
import pyspiel

from kuhn_lab.jev import decide
from kuhn_lab.kuhn import (
    ALPHAS,
    CARD_NAMES,
    EPISODES_PATH,
    build_state,
    decode_infoset,
    legal_action_names,
)
from kuhn_lab.nash import nash_policy


def _sample_from_probs(
    rng: np.random.Generator,
    probabilities: dict[str, float],
    action_names: dict[str, int],
) -> tuple[int, str]:
    labels = list(action_names.keys())
    probs = np.array([float(probabilities.get(label, 0.0)) for label in labels])
    if probs.sum() <= 0:
        probs = np.ones(len(labels)) / len(labels)
    else:
        probs = probs / probs.sum()
    choice = labels[int(rng.choice(len(labels), p=probs))]
    return action_names[choice], choice


def play_hand(
    game,
    alpha: float,
    jev_seat: int,
    rng: np.random.Generator,
    nash,
) -> dict:
    state = game.new_initial_state()
    deal_order: list[tuple[int, int]] = []
    while state.is_chance_node():
        outcomes, probs = zip(*state.chance_outcomes())
        action = int(rng.choice(np.array(outcomes), p=np.array(probs)))
        deal_order.append((len(deal_order), action))
        state.apply_action(action)
    cards = {seat: CARD_NAMES[card] for seat, card in deal_order}

    steps = []
    model = None
    while not state.is_terminal():
        seat = state.current_player()
        key = state.information_state_string(seat)
        meta = decode_infoset(key)
        history = meta["history"]
        action_names = legal_action_names(history)
        state_dict = build_state(key)

        if seat == jev_seat:
            t0 = time.perf_counter()
            decision = decide(state_dict, action_names, meta["facing_bet"])
            elapsed_ms = round((time.perf_counter() - t0) * 1000, 1)
            model = decision["model"]
            action, action_name = _sample_from_probs(
                rng, decision["probabilities"], action_names
            )
            step = {
                "infoset": key,
                "seat": seat,
                "actor": "jev",
                "state": state_dict,
                "action": action,
                "action_name": action_name,
                "probabilities": decision["probabilities"],
                "confidence": decision["confidence"],
                "you_hold_higher_card": decision["you_hold_higher_card"],
                "opponent_is_bluffing": decision["opponent_is_bluffing"],
                "elapsed_ms": elapsed_ms,
                "usage": decision["usage"],
            }
        else:
            probs = nash.action_probabilities(state, seat)
            named = {
                name: float(probs.get(aid, 0.0)) for name, aid in action_names.items()
            }
            action, action_name = _sample_from_probs(rng, named, action_names)
            step = {
                "infoset": key,
                "seat": seat,
                "actor": "nash",
                "state": state_dict,
                "action": action,
                "action_name": action_name,
                "probabilities": named,
                "confidence": None,
                "you_hold_higher_card": None,
                "opponent_is_bluffing": None,
                "elapsed_ms": None,
                "usage": None,
            }
        steps.append(step)
        state.apply_action(action)

    returns = [float(x) for x in state.returns()]
    return {
        "cards": cards,
        "steps": steps,
        "returns": returns,
        "jev_return": returns[jev_seat],
        "model": model,
    }


def play(
    hands: int = 300,
    alpha: float = 1.0 / 3.0,
    jev_seat: int = 0,
    seed: int = 0,
    output_path: Path | None = None,
    append: bool = False,
) -> Path:
    out = output_path or EPISODES_PATH
    out.parent.mkdir(parents=True, exist_ok=True)
    if not append:
        out.write_text("")

    game = pyspiel.load_game("kuhn_poker")
    nash = nash_policy(game, alpha)
    rng = np.random.default_rng(seed)
    start_episode = 0
    if append and out.exists() and out.stat().st_size:
        with out.open() as handle:
            start_episode = sum(1 for _ in handle)

    for i in range(hands):
        episode = start_episode + i
        hand_rng = np.random.default_rng(seed + episode)
        result = play_hand(game, alpha, jev_seat, hand_rng, nash)
        record = {
            "episode": episode,
            "alpha": alpha,
            "jev_seat": jev_seat,
            "seed": seed + episode,
            **result,
        }
        with out.open("a") as handle:
            handle.write(json.dumps(record) + "\n")
        print(
            f"episode {episode + 1} alpha={alpha:.4f} jev_seat={jev_seat} "
            f"return {result['jev_return']:+.0f}",
            flush=True,
        )

    print(f"wrote {out}", flush=True)
    return out


def play_all_configs(hands: int = 300, seed: int = 0, output_path: Path | None = None) -> Path:
    out = output_path or EPISODES_PATH
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text("")
    for alpha in ALPHAS:
        for jev_seat in (0, 1):
            play(
                hands=hands,
                alpha=alpha,
                jev_seat=jev_seat,
                seed=seed,
                output_path=out,
                append=True,
            )
    return out
