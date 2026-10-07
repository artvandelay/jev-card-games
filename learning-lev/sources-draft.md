# Posts from the trusted list

Read 22 September 2026.

Fetch note: crawl4ai `batch` on `x.com` failed with `Access denied by robots.txt` for all 13 URLs. Twitter syndication (`cdn.syndication.twimg.com/tweet-result`) returned `{}`. Text below comes from one fallback: `https://api.fxtwitter.com/{handle}/status/{id}` (HTTP 200 JSON). No tweet text was invented.

Context (not re-summarized here): [Introducing System One Models & Jev](https://typesafe.ai/blog/introducing-system-one-models-and-jev). The YouTube song “Surprise Video - What A Time To Be Alive!” was not referenced by any of these posts.

## Per-post notes

### Alexis Gallagher — 16 Sep 2026

- **URL:** https://x.com/alexisgallagher/status/2100312082491322873
- **Handle:** @alexisgallagher
- Quotes Diogo’s launch thread. Says Jev looks interesting, but the reactions matter more: many people seem unaware that encoder-only classifiers already exist and are widely used. Gives ModernBERT (or maybe LFM2.5) fine-tunes as the familiar “fast cheap structured output” category; expects Jev is better and, as he understands it, does not need task-specific training, but says the category is not new.
- **Links in post:** none (no paper/model/repo URLs).

### Tamara J Tran — 17 Sep 2026

- **URL:** https://x.com/tamarajtran/status/2100694549362553153
- **Handle:** @tamarajtran
- Proposes agent-context compaction as a Jev use case: instead of a summarization prompt, score every tool call and drop irrelevant ones so compaction is instant. Demo video attached.
- **Links in post:** none beyond media.

### Mau Baron — 18 Sep 2026

- **URL:** https://x.com/maubaron/status/2100738237237002706
- **Handle:** @maubaron
- Demo video of Jev controlling all four Smash Bros characters against itself, choosing moves in a fraction of a second. Claims >22M tokens for the match at a couple of cents. Explicitly says Jev does not replace GPT-6 Astra; the value is instant response time.
- **Links in post:** none beyond media.

### Elvis Sun — 18 Sep 2026

- **URL:** https://x.com/elvissun/status/2100951347080421409
- **Handle:** @elvissun
- Claims Jev scored 384 morning news items for 15 brands in 24.9s for $0.19; Claude Opus 5 on the same feed got through 4/384 for $0.77 (~390× cheaper per headline). Positions Jev for PR / newsjacking workflows. Says the demo is open-sourced.
- **Links in post:** http://newsjack.sh (demo/ folder, plus “30+ skills”).

### Complete Skeptic 1 (Diogo Almeida) — 15 Sep 2026

- **URL:** https://x.com/completeskeptic/status/2099925684256899543
- **Handle:** @CompleteSkeptic (Diogo Almeida)
- Thread reply in the launch thread: gains are not free — Jev cannot generate text. Side-by-side vs LLMs makes the trade-off clear. Analogizes parallel (vs sequential) computation to how Transformers leapfrogged RNNs. Video attached.
- **Links in post:** none beyond media.

### Complete Skeptic 2 (Diogo Almeida) — 15 Sep 2026

- **URL:** https://x.com/completeskeptic/status/2099925685720760404
- **Handle:** @CompleteSkeptic (Diogo Almeida)
- Next reply: future is code + AI, hence workflow evals. States price $42 / billion input tokens ($0.042 / MTok), output free forever (too cheap to meter with the new architecture). Names Jev after Jevons paradox; chart images attached.
- **Links in post:** none beyond media/charts.

### Filipp Kowalski — 18 Sep 2026

- **URL:** https://x.com/filippkowalski/status/2100864984448147770
- **Handle:** @filippkowalski
- One-line endorsement of a quoted demo as “the best explanation on what Jev is that I've seen today.” Quote is @_MaxBlade showing Subway Surfers at high speed / 50 games at once for less than a cent, and saying Jev does not replace Astra/Fable.
- **Links in post:** none (quoted status https://x.com/_MaxBlade/status/2100634359099232678).

### Erik Gafni — 18 Sep 2026

- **URL:** https://x.com/egafni/status/2100770895325524242
- **Handle:** @EGafni (Erik Spock Gafni, TypeSafe CTO)
- Quotes a third-party self-driving demo and comments only: “the self driving stuff is nuts.” No technical claims of his own in the text.
- **Links in post:** none (quoted status https://x.com/Neel490/status/2100440723837313349).

### Mizore — 20 Sep 2026

- **URL:** https://x.com/mizorewww/status/2101473552956555427
- **Handle:** @mizorewww
- Introduces `laya-mlx`: open-source Jev-like classifier (text → output probabilities), ported to MLX with perf work. Claims ~50× faster than Jev on-device, ≤1GB RAM; Snake demo on M3 Max at ~60 decisions/sec.
- **Links in post:** https://github.com/mizorewww/laya-mlx

### Miu / vechen — 21 Sep 2026

- **URL:** https://x.com/miu21590/status/2101857866378362926
- **Handle:** @miu21590
- Uses Jev mid-task inside Codex to raise/lower GPT-6 reasoning effort (more when stuck, less on routine steps). Reports ~50% lower Astra cost in their tests, faster runs, prompt caching kept. Video attached.
- **Links in post:** none beyond media.

### Atomic Chat — 21 Sep 2026

- **URL:** https://x.com/atomic_chat_hq/status/2102160983409955244
- **Handle:** @atomic_chat_hq
- Quotes Mizore’s Laya post. Claims local open-weights Laya beat cloud Jev at Grok-4.7-built Tetris by deciding ~11× faster on a 16GB MacBook Air. Points to their local-model product.
- **Links in post:** https://atomic.chat (also quotes https://github.com/mizorewww/laya-mlx).

### Hugo Duprez — 18 Sep 2026

- **URL:** https://x.com/HugoDuprez/status/2100953089003921543
- **Handle:** @HugoDuprez
- Claims Jev can generate game levels in real time; argues faster/cheaper structured output matters for game dev. Video attached.
- **Links in post:** none beyond media.

### Viraj — 21 Sep 2026

- **URL:** https://x.com/heyxviraj/status/2102048070649405592
- **Handle:** @heyxviraj
- Demo: Jev (API) vs Laya (local Mac) controlling Chrome dinosaur runners on the same track; different latency; decisions for dodge/shield/survive. Notes TypeSafe’s Jev also controls obstacles. Open-sourced.
- **Links in post:** https://github.com/virajbhartiya/laya-vs-jev

## Table

| Handle | URL | What it adds |
| --- | --- | --- |
| @alexisgallagher | https://x.com/alexisgallagher/status/2100312082491322873 | Frames Jev against prior encoder-only / ModernBERT-style classifiers; category not new. |
| @tamarajtran | https://x.com/tamarajtran/status/2100694549362553153 | Compaction via per–tool-call scoring instead of summarization. |
| @maubaron | https://x.com/maubaron/status/2100738237237002706 | 4-player Smash Bros self-play demo; cost/latency anecdote; not a GPT-6 replacement. |
| @elvissun | https://x.com/elvissun/status/2100951347080421409 | News/PR batch scoring vs Opus 5; open demo at newsjack.sh. |
| @CompleteSkeptic | https://x.com/completeskeptic/status/2099925684256899543 | Official: no text generation; parallel vs sequential analogy. |
| @CompleteSkeptic | https://x.com/completeskeptic/status/2099925685720760404 | Official: workflow evals, $0.042/MTok in, free out, Jevons naming. |
| @filippkowalski | https://x.com/filippkowalski/status/2100864984448147770 | Endorses MaxBlade Subway Surfers multi-game demo as best “what Jev is” explainer that day. |
| @EGafni | https://x.com/egafni/status/2100770895325524242 | CTO reaction to a community self-driving demo (“nuts”). |
| @mizorewww | https://x.com/mizorewww/status/2101473552956555427 | Open local Laya MLX port; on-device Snake at 60 Hz; repo linked. |
| @miu21590 | https://x.com/miu21590/status/2101857866378362926 | Mid-task GPT-6 effort control in Codex; claimed Astra cost cut. |
| @atomic_chat_hq | https://x.com/atomic_chat_hq/status/2102160983409955244 | Local Laya vs cloud Jev Tetris latency claim; points to atomic.chat. |
| @HugoDuprez | https://x.com/HugoDuprez/status/2100953089003921543 | Real-time game-level generation demo angle. |
| @heyxviraj | https://x.com/heyxviraj/status/2102048070649405592 | Jev vs Laya Chrome dino duel; repo linked. |

## Unresolved

None. All 13 supplied URLs returned readable text via the fxtwitter fallback.

## Links these posts add

Paper / model / dataset / repo URLs actually present in the post text (or expanded from the post’s own link):

- http://newsjack.sh — @elvissun (demo + skills)
- https://github.com/mizorewww/laya-mlx — @mizorewww (also quoted by @atomic_chat_hq)
- https://atomic.chat — @atomic_chat_hq
- https://github.com/virajbhartiya/laya-vs-jev — @heyxviraj

Not found in these posts (so not completed here): huggingface.co/convaiinnovati…, DeepMostInnova…, datasets/DeepM…, proceedings.iclr.cc/paper_fil…, arxiv 2503.23303, arxiv 2510.01237, huggingface.co/blog/setfit. None of these thirteen posts linked those.

Quoted third-party posts (not primary sources on the list, but attached by quote):

- https://x.com/_MaxBlade/status/2100634359099232678 — quoted by @filippkowalski
- https://x.com/Neel490/status/2100440723837313349 — quoted by @EGafni
- https://x.com/CompleteSkeptic/status/2099925682726002904 — quoted by @alexisgallagher (parent launch tweet; not one of the two listed CompleteSkeptic URLs)
