# Jev card games

Two evaluations of TypeSafe Jev (`typesafe/jev-1.13`, via the OpenRouter Decisions API) on card games.

- **Blackjack.** Gymnasium `Blackjack-v1`, no rules in the prompt. Jev matched basic strategy on 83.7% of decisions. Write-up: [docs/blog/jev-blackjack-evaluation.md](docs/blog/jev-blackjack-evaluation.md). Charts: [results/index.html](results/index.html).
- **Kuhn Poker.** OpenSpiel `kuhn_poker` against a Nash opponent, with the rules in the question. Jev is about halfway between perfect and random play (exploitability 0.22 chips per hand). Write-up: [docs/kuhn-poker-report.md](docs/kuhn-poker-report.md). Charts: [results/kuhn.html](results/kuhn.html).

Notes on the model are in `learning-lev/`. Code is in `src/blackjack_lab/` and `src/kuhn_lab/`.

```bash
uv pip install -e .
blackjack-lab --help
kuhn-lab --help
```

The API key belongs in `.env` as `OPENROUTER_API_KEY`. That file is not in this repo.
