"""Frozen contract for the Kuhn Poker evaluation of Jev.

Every other module in `kuhn_lab` codes against this file. Nothing here calls
pyspiel or the network, so it is safe to import from anywhere.

OpenSpiel facts this contract encodes (from `kuhn_poker.cc`, do not re-derive):

- Two distinct actions: 0 = Pass (check or fold), 1 = Bet (bet or call).
- An information state string is the card digit followed by the betting
  history letters, where `p` = Pass and `b` = Bet. Card 0 = Jack, 1 = Queen,
  2 = King, ranked Jack lowest and King highest.
- Player 0 owns "0", "1", "2", "0pb", "1pb", "2pb". Player 1 owns "0p",
  "1p", "2p", "0b", "1b", "2b". Twelve information sets in total.
- Each player antes 1 chip; a bet or a call adds 1 more. The game is
  zero-sum and the equilibrium value to player 0 is -1/18.

Design rule, from `learning-lev/using-jev.md`: "The state is data. The
judgment is the question." `build_state` therefore returns pure game facts
only -- no rules text, no judgments, and nothing the model would have to
compute for itself. The pot size and the chips to call are precomputed here
deliberately. The rules live in `jev_instructions`, which feeds the question
`instructions`, never the state.

Frozen signatures every other stream codes against
--------------------------------------------------

    # kuhn.py (this file)
    def decode_infoset(key: str) -> dict
        # {"card": "Q", "history": "pb", "seat": 0, "facing_bet": True}
    def legal_action_names(history: str) -> dict[str, int]
    def build_state(key: str) -> dict
        # pure game facts, no rules, no judgments
    def jev_instructions(history: str) -> str
        # RULES_TEXT + "Choose the action." + option gloss

    # jev.py
    def decide(state: dict, action_names: dict[str, int], facing_bet: bool) -> dict
        # returns: model, action(int), action_name(str),
        #          probabilities(dict[name -> float]), p_bet(float),
        #          confidence(float|None), you_hold_higher_card(float),
        #          opponent_is_bluffing(float|None), usage(dict|None)

    # nash.py
    def nash_policy(game, alpha: float)
        # -> open_spiel.python.policy.TabularPolicy
    def nash_p_bet_table(alpha: float) -> dict[str, float]

    # policy_build.py
    def load_probe(path: Path) -> list[dict]
    def jev_p_bet_table(records: list[dict]) -> dict[str, float]
    def jev_policy(game, table: dict[str, float])
    def determinism(records: list[dict]) -> dict[str, dict]

Frozen record schemas
---------------------

`results/kuhn_probe.jsonl`, one JSON object per API call, sixteen keys:

    infoset, rep, seat, card, history, state, action, action_name,
    probabilities, p_bet, confidence, you_hold_higher_card,
    opponent_is_bluffing, elapsed_ms, usage, model

`results/kuhn_episodes.jsonl`, one JSON object per hand:

    episode, alpha, jev_seat, seed, cards, steps, returns, jev_return, model

Each entry of `steps` is:

    infoset, seat, actor, state, action, action_name, probabilities,
    confidence, you_hold_higher_card, opponent_is_bluffing, elapsed_ms, usage

`actor` is "jev" or "nash". Opponent steps carry `actor="nash"`,
`elapsed_ms=None`, and `usage=None`.
"""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
RESULTS = ROOT / "results"

PROBE_PATH = RESULTS / "kuhn_probe.jsonl"
EPISODES_PATH = RESULTS / "kuhn_episodes.jsonl"
METRICS_PATH = RESULTS / "kuhn_metrics.json"
SUMMARY_PATH = RESULTS / "kuhn_summary.json"
POLICY_CHART_PATH = RESULTS / "kuhn_policy.png"
EXPLOITABILITY_CHART_PATH = RESULTS / "kuhn_exploitability.png"
CALIBRATION_CHART_PATH = RESULTS / "kuhn_calibration.png"
LATENCY_CHART_PATH = RESULTS / "kuhn_latency.png"
HTML_PATH = RESULTS / "kuhn.html"

ACTION_PASS = 0
ACTION_BET = 1
CARD_NAMES = {0: "J", 1: "Q", 2: "K"}
INFOSETS_P0 = ("0", "1", "2", "0pb", "1pb", "2pb")
INFOSETS_P1 = ("0p", "1p", "2p", "0b", "1b", "2b")
ALL_INFOSETS = INFOSETS_P0 + INFOSETS_P1
ALPHAS = (0.0, 1.0 / 6.0, 1.0 / 3.0)
NASH_VALUE_P0 = -1.0 / 18.0
HIGHER_CARD_TRUTH = {"J": 0.0, "Q": 0.5, "K": 1.0}

RULES_TEXT = (
    "Kuhn Poker. The deck is three cards, J, Q, and K, ranked J lowest and K\n"
    "highest. Each player antes 1 chip and is dealt one private card. The third\n"
    "card is not used. The first player acts first. A player with no bet against\n"
    "them may check, adding no chips, or bet 1 chip. A player facing a bet may\n"
    "fold, giving up the pot, or call, matching the 1 chip. The hand ends after a\n"
    "fold, a call, or two checks. On a fold the other player takes the pot.\n"
    "Otherwise both cards are shown and the higher card takes the pot. Choose the\n"
    "action that wins the most chips on average."
)

# Context-correct action names, deliberately not a shared abstraction: Pass
# means check with no bet live and fold with one live. This is the direct fix
# for the Blackjack `usable_ace` finding, where an unexplained abstraction cost
# 16 points of agreement.
CHECK_BET_ACTIONS = {"check": ACTION_PASS, "bet": ACTION_BET}
FOLD_CALL_ACTIONS = {"fold": ACTION_PASS, "call": ACTION_BET}

ACTION_GLOSSES = {
    "check": "check, adding no chips to the pot",
    "bet": "bet 1 chip",
    "fold": "fold, giving up the pot",
    "call": "call, matching the 1 chip bet against you",
}

# The four history classes cover all 12 information sets.
HISTORY_FACTS = {
    "": {
        "seat": 0,
        "facing_bet": False,
        "you_are": "first player",
        "betting_so_far": [],
        "pot_chips": 2,
        "your_chips_in_pot": 1,
        "opponent_chips_in_pot": 1,
        "chips_to_call": 0,
        "actions": CHECK_BET_ACTIONS,
    },
    "p": {
        "seat": 1,
        "facing_bet": False,
        "you_are": "second player",
        "betting_so_far": ["opponent checked"],
        "pot_chips": 2,
        "your_chips_in_pot": 1,
        "opponent_chips_in_pot": 1,
        "chips_to_call": 0,
        "actions": CHECK_BET_ACTIONS,
    },
    "b": {
        "seat": 1,
        "facing_bet": True,
        "you_are": "second player",
        "betting_so_far": ["opponent bet 1"],
        "pot_chips": 3,
        "your_chips_in_pot": 1,
        "opponent_chips_in_pot": 2,
        "chips_to_call": 1,
        "actions": FOLD_CALL_ACTIONS,
    },
    "pb": {
        "seat": 0,
        "facing_bet": True,
        "you_are": "first player",
        "betting_so_far": ["you checked", "opponent bet 1"],
        "pot_chips": 3,
        "your_chips_in_pot": 1,
        "opponent_chips_in_pot": 2,
        "chips_to_call": 1,
        "actions": FOLD_CALL_ACTIONS,
    },
}


def decode_infoset(key: str) -> dict:
    """Split an OpenSpiel information state string into its parts."""
    if key not in ALL_INFOSETS:
        raise SystemExit(f"Unknown Kuhn infoset: {key!r}")
    card = CARD_NAMES[int(key[0])]
    history = key[1:]
    facts = HISTORY_FACTS[history]
    return {
        "card": card,
        "history": history,
        "seat": facts["seat"],
        "facing_bet": facts["facing_bet"],
    }


def legal_action_names(history: str) -> dict[str, int]:
    """Map the two context-correct option names to OpenSpiel action ids."""
    if history not in HISTORY_FACTS:
        raise SystemExit(f"Unknown Kuhn betting history: {history!r}")
    return dict(HISTORY_FACTS[history]["actions"])


def build_state(key: str) -> dict:
    """Pure game facts for one information set.

    No rules text, no judgments, and nothing the model would have to compute:
    `pot_chips` and `chips_to_call` are precomputed here on purpose.
    """
    decoded = decode_infoset(key)
    facts = HISTORY_FACTS[decoded["history"]]
    return {
        "your_card": decoded["card"],
        "history": decoded["history"],
        "seat": decoded["seat"],
        "facing_bet": decoded["facing_bet"],
        "you_are": facts["you_are"],
        "betting_so_far": list(facts["betting_so_far"]),
        "pot_chips": facts["pot_chips"],
        "your_chips_in_pot": facts["your_chips_in_pot"],
        "opponent_chips_in_pot": facts["opponent_chips_in_pot"],
        "chips_to_call": facts["chips_to_call"],
    }


def jev_instructions(history: str) -> str:
    """Question instructions: the full rules plus the two options in context."""
    names = legal_action_names(history)
    gloss = " ".join(f"{name}: {ACTION_GLOSSES[name]}." for name in names)
    return f"{RULES_TEXT}\n\nChoose the action.\n\n{gloss}"
