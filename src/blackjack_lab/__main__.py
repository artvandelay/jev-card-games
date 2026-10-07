"""blackjack-lab play | blackjack-lab report"""

from __future__ import annotations

import argparse

from blackjack_lab.play import play
from blackjack_lab.report import report


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Run Gymnasium Blackjack-v1 and chart the logged policy."
    )
    commands = parser.add_subparsers(dest="command", required=True)

    play_parser = commands.add_parser("play", help="Play hands and write results/episodes.jsonl")
    play_parser.add_argument("--episodes", type=int, default=50)
    play_parser.add_argument("--policy", choices=("random", "jev"), default="jev")
    play_parser.add_argument("--seed", type=int, default=0)
    play_parser.add_argument(
        "--mode",
        choices=("random", "grid"),
        default="random",
        help="random deals or stratified grid coverage",
    )
    play_parser.add_argument(
        "--reps-per-box",
        type=int,
        default=3,
        help="repetitions per box when --mode grid is used",
    )

    commands.add_parser("report", help="Write the tutorial charts and results/index.html")

    args = parser.parse_args()
    if args.command == "play":
        play(
            episodes=args.episodes,
            policy=args.policy,
            seed=args.seed,
            mode=args.mode,
            reps_per_box=args.reps_per_box,
        )
    else:
        report()


if __name__ == "__main__":
    main()
