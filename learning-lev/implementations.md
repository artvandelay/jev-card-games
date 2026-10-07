# Jev implementations beyond classify-and-route

Read 22 September 2026. These are public GitHub projects that use Jev for a loop, a game, or a control split, rather than one inbox tag. Descriptions come from the repositories’ own READMEs. Several are days old. Treat measured numbers as the author’s, on their own task.

The pattern that repeats: code owns anything with an exact answer (legal moves, physics, pixels-to-JSON, the list of buttons). Jev is asked a narrow typed question about what that state means. A wrong type is impossible because the options were enumerated. A wrong judgment still happens, and the interesting projects log it instead of hiding it.

## Games and real-time control

**Clash Royale on a real phone.** [bytelabs-oss/clash-jev](https://github.com/bytelabs-oss/clash-jev). Screen video comes over adb. OpenCV and a small hand-trained network turn the frame into JSON (hand, elixir, towers, troops). Jev never sees pixels. Once a second it picks a strategy from a fixed list of 12, then a card, then a legal square. Three requests per play, about 135 ms each, about $0.004 for a match of 150–200 requests. The author refused to pre-filter “sensible” options or to put counters in the state, because that measured their list rather than Jev. Illegal or unaffordable picks are logged and not tapped. Replays: https://clash-jev.vercel.app. Automating the game is against Supercell’s terms. The repo says it is a study, not a product.

**Chess, two ways.** [TholeG/typesafe-chess](https://github.com/TholeG/typesafe-chess) plays Jev against Jev. chess.js lists legal moves. One request carries a Choice per legal move, a Score of the position, and a Noul for “is this tactically sharp?” Fast mode is about 350 ms a move. An optional Monte Carlo tree search uses those distributions as policy and value, AlphaZero-style. [wondertwins/jev-benchmark](https://github.com/wondertwins/jev-benchmark) measured the other side of that. On a raw board Jev was no better than random. With code-supplied facts it beat random by about 65%, and with one-ply tactical facts by about 78%. Mate-in-one was found 24% of the time. On a Stockfish-anchored ladder the tactical version played at roughly 950 Elo: it beat bots up to about 650 and lost to depth-1 Stockfish (about 1166). Eleven games, so the rating is soft. The same repo’s second task, “which NPC is being spoken to?”, is inside the lane: F1 0.96 on clean text, precision 1.0, including on messy speech-to-text.

**Snake.** [sorrycc/typesafe-snake](https://github.com/sorrycc/typesafe-snake). Flood fill and food distance are computed in code. Jev picks one legal direction. If the call misses the tick, the snake keeps going straight.

**Minesweeper.** [comoc/jev-minesweeper](https://github.com/comoc/jev-minesweeper). Every unopened cell touching a number becomes its own Noul (“is this a mine?”) in one request. Code opens cells under 5% and flags cells over 95%. An exact solver sits beside Jev as the fallback when confidence is low and as the check on Jev’s probabilities.

**Stealth guards.** [AbdelStark/heist-one](https://github.com/AbdelStark/heist-one). Guards make split-second judgments from incomplete evidence (a door, a light, a badge). Deterministic code still runs the world. The point of the game is that you can click a guard and see the judgment.

**Civilization II harness.** [phyous/tsai-civ2](https://github.com/phyous/tsai-civ2). The original game runs in DOSBox. Named Choice vectors cover policy, cities, research, diplomacy, units, exploration, and war. The displayed numbers are action probabilities, not a chance of victory. The README says no complete-game win has been verified yet.

**Quadrotor.** [RomanSlack/jev-drone](https://github.com/RomanSlack/jev-drone). A Skydio X2 in MuJoCo. The geometric controller runs at 500 Hz and always owns safety. A camera becomes a symbolic scene at 15 Hz. Jev is advisory at about 2.5 Hz: what the situation means, not the motor command.

**Pixel art by classification.** [Wizhill05/typesafe-image-diffusion](https://github.com/Wizhill05/typesafe-image-diffusion). A 16×16 image is 256 Choice questions, one per pixel, over a 16-color palette. Later passes show each pixel only its previous color and its 3×3 neighborhood. Sending the whole grid blew the token limit (pass 0 was about 57k tokens).

**Minecraft.** [Hardel-DW/jev.mods](https://github.com/Hardel-DW/jev.mods) is a design note, not a finished bot. The author wants an unscripted agent whose only given goal is the dragon, with a stack of Jevs where finer decisions sit under coarser ones.

## Agents that still use a language model for words

**Browser, one request per step.** [browser-use/jev-ultrafast](https://github.com/browser-use/jev-ultrafast). The page becomes a numbered element table. One Jev call picks the operation (click, type, select, scroll, wait, done, blocked) and, in the same call, the best target for each operation that needs one. Code uses only the target that matches the chosen operation. A small language model writes text only for `TYPE_TEXT`. Their published demo is Zürich to London on Google Flights in 7.1 seconds.

**Voice, acting on a partial sentence.** [moritzkremb/jev-voice-browser](https://github.com/moritzkremb/jev-voice-browser). Chrome’s speech API streams words. Every partial transcript, debounced 200 ms, is one Jev request with about a dozen questions: intent, target, site, “is the command finished?”, “is this addressed to me?”, “is it destructive?”. Answers come back in about 250–350 ms. Search text is extracted by code. Jev only picks a span, which is copied verbatim. About $0.0002 a call.

**Per-turn model routing.** [0xNatoshi/jev-codex-router](https://github.com/0xNatoshi/jev-codex-router). Jev picks the model and the thinking effort for each Codex turn, including continuations after tools. A historical simulation claimed about 60% less spend than always using Astra, on 237 turns, under an older policy. The README says that figure is not measured quota saved.

**Reflexes.** [evoke-build/evoke](https://github.com/evoke-build/evoke). A sentence is matched to a small program someone wrote and installed from git. Jev chooses the program and its arguments. A confidence gate runs it, asks, or refuses.

**Search inside an agent.** [lhemerly/mcts-agent](https://github.com/lhemerly/mcts-agent). Gemini proposes actions. Jev Choice supplies the prior over those actions and Jev Score scores hypothetical states. Only the winning next step is executed. Git diffs and terminal output come back as the next state. A D3 page replays the tree.

## Open recreations

These are independent. They are not TypeSafe weights and not a published RLCD recipe.

- [kshetrajna12/reflex](https://github.com/kshetrajna12/reflex). One forward pass over frozen Qwen, same request shape as `POST /v1/systemone`. The author reports that LoRA and distillation helped on data like the training set and hurt general judgment. What helped was the readout: lettered yes/no, an evidence/criterion frame, and averaging two option orders. On their own hard tier, frozen Qwen3.5-4B was 0.685 accuracy and 0.081 ECE, against their run of official Jev at 0.730 and 0.031.
- [vinnylarouge/jevlike](https://github.com/vinnylarouge/jevlike). A small option-attention head: each option is a query over the context, one score, one softmax. Includes a Doom button controller and a chess controller. The Doom film is a selected window, not a competence claim.
- [yzfly/edgejev](https://github.com/yzfly/edgejev). ONNX INT8 wrappers around other people’s open weights (laya, kev, NanoJev, PlayJev). They report 15.6 ms per question on a 4-core CPU for the laya INT8 build, against a 314 ms hosted call. Accuracy is on AG News and an emotion set, not on TypeSafe’s workflows.

## What is worth copying

From the projects that measured themselves:

- Enumerate the legal actions in code. Ask Jev to pick among them.
- Put measurements in the state. Keep judgments out of the option text, or the probability measures the hint.
- Ask every independent question in one call. Sequence only when the next option list depends on the previous answer (Clash’s strategy, then card, then square).
- Keep a fast deterministic layer for safety and timing. Jev is the slow advisor (drone at 2.5 Hz, snake that goes straight if the call is late).
- Log the model’s pick even when you refuse to act on it.
- A probability is useful next to an exact solver (minesweeper) or a search (chess MCTS). It is a weak chess engine by itself.
