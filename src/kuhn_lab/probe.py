"""Enumerate all Kuhn infosets and log Jev probe responses."""

from __future__ import annotations

import json
import time
from pathlib import Path

from kuhn_lab.jev import decide
from kuhn_lab.kuhn import ALL_INFOSETS, PROBE_PATH, build_state, decode_infoset, legal_action_names


def probe(reps: int = 10, output_path: Path | None = None) -> Path:
    out = output_path or PROBE_PATH
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text("")

    for rep in range(reps):
        for key in ALL_INFOSETS:
            meta = decode_infoset(key)
            history = meta["history"]
            action_names = legal_action_names(history)
            state = build_state(key)
            t0 = time.perf_counter()
            decision = decide(state, action_names, meta["facing_bet"])
            elapsed_ms = round((time.perf_counter() - t0) * 1000, 1)

            record = {
                "infoset": key,
                "rep": rep,
                "seat": meta["seat"],
                "card": meta["card"],
                "history": history,
                "state": state,
                "action": decision["action"],
                "action_name": decision["action_name"],
                "probabilities": decision["probabilities"],
                "p_bet": decision["p_bet"],
                "confidence": decision["confidence"],
                "you_hold_higher_card": decision["you_hold_higher_card"],
                "opponent_is_bluffing": decision["opponent_is_bluffing"],
                "elapsed_ms": elapsed_ms,
                "usage": decision["usage"],
                "model": decision["model"],
            }
            with out.open("a") as handle:
                handle.write(json.dumps(record) + "\n")
            print(
                f"rep {rep + 1}/{reps} infoset {key} "
                f"p_bet={decision['p_bet']:.3f} "
                f"latency {elapsed_ms} ms",
                flush=True,
            )

    print(f"wrote {out}", flush=True)
    return out


def main() -> None:
    probe()


if __name__ == "__main__":
    main()
