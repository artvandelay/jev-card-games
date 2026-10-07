"""kuhn-lab probe | play | metrics | analyze | report"""

from __future__ import annotations

import argparse

from kuhn_lab.analyze import main as analyze_main
from kuhn_lab.metrics import main as metrics_main
from kuhn_lab.play import play, play_all_configs
from kuhn_lab.probe import probe
from kuhn_lab.report import report


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Evaluate TypeSafe Jev on OpenSpiel Kuhn Poker."
    )
    commands = parser.add_subparsers(dest="command", required=True)

    probe_parser = commands.add_parser("probe", help="Probe all 12 infosets via Jev")
    probe_parser.add_argument("--reps", type=int, default=10)

    play_parser = commands.add_parser("play", help="Sample hands vs Nash opponent")
    play_parser.add_argument("--hands", type=int, default=300)
    play_parser.add_argument("--alpha", type=float, default=1.0 / 3.0)
    play_parser.add_argument("--jev-seat", type=int, choices=(0, 1), default=0)
    play_parser.add_argument("--seed", type=int, default=0)
    play_parser.add_argument(
        "--all-configs",
        action="store_true",
        help="Run 3 alphas x 2 seats x --hands",
    )

    commands.add_parser("metrics", help="Exact exploitability from probe log")
    commands.add_parser("analyze", help="Summarize play log")
    commands.add_parser("report", help="Write charts and results/kuhn.html")

    args = parser.parse_args()
    if args.command == "probe":
        probe(reps=args.reps)
    elif args.command == "play":
        if args.all_configs:
            play_all_configs(hands=args.hands, seed=args.seed)
        else:
            play(
                hands=args.hands,
                alpha=args.alpha,
                jev_seat=args.jev_seat,
                seed=args.seed,
            )
    elif args.command == "metrics":
        metrics_main()
    elif args.command == "analyze":
        analyze_main()
    else:
        report()


if __name__ == "__main__":
    main()
