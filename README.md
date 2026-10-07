# Jev already knows blackjack. It does not know Kuhn poker.

Jev returns a decision and a probability, not a paragraph. We asked it to play two card games.

**Blackjack, no rules in the prompt.** It matched the textbook on 84% of decisions. It already knows the famous game. It stood on a soft 17, because we handed it the number 17 and a flag called *usable ace*, and never said an ace can drop from 11 to 1.

**Kuhn poker, rules written out.** A perfect opponent wins 0.22 chips a hand from it. Coin-flip play loses 0.46. Perfect play loses nothing. Jev calls with a jack, which cannot win, and folds a king, which cannot lose.

**Takeaway.** Jev can replay a decision it has seen in words. Give it the fact in plain language. Leave a sure thing, like “never call with a jack,” to code. It will not work out how often to bluff.

The reading page is [github.jigarkdoshi.com/jev-card-games](https://github.jigarkdoshi.com/jev-card-games). The full notes are [Blackjack](docs/blog/jev-blackjack-evaluation.md) and [Kuhn poker](docs/kuhn-poker-report.md).
