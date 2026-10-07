# Trusted-researcher papers and models

These came from a researcher the user trusts. Resolved and read 22 Sep 2026. Only the URLs listed below were opened; no neighbor links were invented.

Also noted in the same video description (not prior work): [Lambda GPU cloud / papers](https://lambda.ai/papers) and the song [YouTube](https://www.youtube.com/watch?v=4RtUJkjrKMI).

---

## Laya (model)

- **URL:** https://huggingface.co/convaiinnovations/laya
- **Name / org / year:** Laya — Convai Innovations (model card current as of read date; family of three checkpoints). Apache-2.0.
- **Main insight:** Multilingual, non-autoregressive “System 1” decision model: state + typed questions → typed answers with calibrated probabilities in one forward pass (~33–40 ms). Trained with what the card calls **RLCD** (Reinforcement Learning for Calibrated Decisions): strictly proper scoring rules so honest probabilities maximize reward. Does not generate text.
- **Environments / datasets:** MASSIVE intent, XNLI (English + other languages), typed-decisions (2,000 decisions / four workflows), AG News, DAIR Emotion, Banking77; ECE / Brier / soft accuracy; latency on Tesla T4. Compares to published TypeSafe Jev 1.13.0 numbers (third-party; card says no TypeSafe API access).
- **Relative to Jev:** Open competitor / open implementation of the same product category. Card explicitly benchmarks against Jev, reuses the RLCD acronym with TypeSafe’s expansion, and positions Laya as faster, open-weight, and stronger on some typed-decision and calibration metrics while weaker on high-cardinality labels (e.g. Banking77) and soft distribution matching.

---

## SalesRLAgent (paper)

- **URL:** https://arxiv.org/abs/2503.23303
- **Title / authors / year:** “SalesRLAgent: A Reinforcement Learning Approach for Real-Time Sales Conversion Prediction and Optimization” — Nandakishor M, 2025 (arXiv 30 Mar 2025).
- **Main insight:** Treats sales conversion prediction as a sequential decision problem with specialized RL, not off-the-shelf LLM+RAG Q&A. Claims moment-by-moment conversion probability with real-time guidance for reps.
- **Environments / datasets:** Synthetic conversations generated with GPT-4O; Azure OpenAI embeddings (3072-dim); reports 96.7% conversion-prediction accuracy vs LLM-only, 85 ms vs 3450 ms GPT-4 inference, and a 43.2% conversion-rate lift when reps use guidance. Named public NLP benchmarks not stated on the abstract page.
- **Relative to Jev:** Different task. Same broader idea (fast probability over outcomes, not chat generation). Does not mention Jev.

---

## Sales conversion RL model (implementation)

- **URL:** https://huggingface.co/DeepMostInnovations/sales-conversion-model-reinf-learning
- **Name / org / year:** `sales-conversion-model-reinf-learning` — DeepMostInnovations; Stable-Baselines3 PPO; cites arXiv:2503.23303; MIT.
- **Main insight:** Open PPO agent that tracks conversion probability turn-by-turn over sales dialogues, using embeddings plus optional LLM-derived engagement metrics.
- **Environments / datasets:** Card repeats paper numbers (96.7% accuracy, etc.); training described as 100,000+ synthetic sales conversations. Framework: Stable Baselines3; embeddings BAAI/bge-m3 (1024-dim) with optional Azure OpenAI.
- **Relative to Jev:** Open implementation of SalesRLAgent’s sales-conversion task, not a Jev clone. Different domain (sales conversion trajectory vs typed System 1 decisions).

---

## SaaS sales conversations (dataset)

- **URL:** https://huggingface.co/datasets/DeepMostInnovations/saas-sales-conversations
- **Name / org / year:** `saas-sales-conversations` — DeepMostInnovations; linked to SalesRLAgent (2025); Apache-2.0; ~100k rows.
- **Main insight:** Synthetic B2B SaaS sales dialogues with outcomes, engagement/effectiveness scores, probability trajectories, and 3072-dim embeddings for training conversion predictors / RL agents.
- **Environments / datasets:** This artifact *is* the dataset (English, synthetic via Azure GPT-4). Single train split; users make their own val/test.
- **Relative to Jev:** Training resource for a different task (sales conversion). Does not mention Jev.

---

## Confidence-aware routing (paper)

- **URL:** https://arxiv.org/abs/2510.01237
- **Title / authors / year:** “Confidence-Aware Routing for Large Language Model Reliability Enhancement: A Multi-Signal Approach to Pre-Generation Hallucination Mitigation” — Nandakishor M, 2025 (arXiv 23 Sep 2025).
- **Main insight:** Estimate reliability *before* generation from semantic alignment, layer-convergence, and learned confidence; route to local gen / RAG / larger model / human review instead of fixing hallucinations after the fact.
- **Environments / datasets:** Abstract says “knowledge-intensive QA benchmarks”; specific dataset names not stated on the abs page. Reports hallucination-detection improvement (0.74 vs 0.42), F1 0.61→0.82, ~40% compute cut vs post-hoc methods.
- **Relative to Jev:** Different task (LLM routing / hallucination mitigation). Shares the theme of using confidence to decide what to do next; does not mention Jev. Related in spirit to Laya’s `Router`, which is language/script routing across decision checkpoints, not LLM quality routing.

---

## SetFit (blog)

- **URL:** https://huggingface.co/blog/setfit
- **Title / authors / year:** “SetFit: Efficient Few-Shot Learning Without Prompts” — Hugging Face blog with Intel Labs / UKP Lab (26 Sep 2022). Points to paper arXiv:2209.11055 and code.
- **Main insight:** Few-shot text classification by contrastive fine-tuning of a Sentence Transformer then a classification head—no prompts; small models, fast train/infer.
- **Environments / datasets:** RAFT few-shot leaderboard; Customer Reviews / SentEval-CR (8 examples/class demo); multilingual classification experiments (German, Japanese, Mandarin, French, Spanish). Compared to PET, GPT-3, T-Few, ADAPET, PERFECT, vanilla fine-tuning.
- **Relative to Jev:** Distant ancestor of the “encoder + head, no generation” pattern. Not a decision/calibration/RLCD paper; does not mention Jev.

---

## RouteLLM (ICLR paper)

- **URL:** https://proceedings.iclr.cc/paper_files/paper/2025/hash/5503a7c69d48a2f86fc00b3dc09de686-Abstract-Conference.html
- **Title / authors / year:** “RouteLLM: Learning to Route LLMs from Preference Data” — Isaac Ong, Amjad Almahairi, Vincent Wu, Wei-Lin Chiang, Tianhao Wu, Joseph E. Gonzalez, M. Kadous, Ion Stoica; ICLR 2025.
- **Main insight:** Train a router from preference data (plus augmentation) to pick a stronger vs weaker LLM at inference, cutting cost while preserving quality and generalizing to unseen model pairs.
- **Environments / datasets:** Abstract says “public benchmarks”; specific names not stated on the abstract page. Claims >2× cost reduction without quality loss.
- **Relative to Jev:** Different task (LLM cost/quality routing). Does not mention Jev. Useful context for “routing” as an idea; not TypeSafe’s calibrated System 1 product.

---

## Summary table

| Paper or artifact | Year | Main insight | Environments / datasets |
| --- | --- | --- | --- |
| SetFit (HF blog) | 2022 | Prompt-free few-shot classification via Sentence Transformer + head | RAFT; SentEval-CR / Customer Reviews; multilingual classification (DE/JA/ZH/FR/ES) |
| RouteLLM (ICLR) | 2025 | Learn a preference-trained router between strong/weak LLMs for cost vs quality | “Public benchmarks” (names not stated on abstract page) |
| SalesRLAgent (arXiv:2503.23303) | 2025 | RL for turn-by-turn sales conversion probability, not LLM chat | Synthetic GPT-4O sales dialogues; Azure OpenAI embeddings; named public NLP suites not stated |
| DeepMost sales-conversion PPO model | 2025 | Open SB3/PPO implementation of SalesRLAgent | 100k+ synthetic sales conversations (card); paper metrics repeated |
| DeepMost saas-sales-conversations | 2025 | Synthetic SaaS B2B sales corpus with outcomes and embeddings | This dataset (~100k English synthetic rows) |
| Confidence-aware routing (arXiv:2510.01237) | 2025 | Pre-generation multi-signal confidence → route query path | Knowledge-intensive QA (specific names not stated on abs page) |
| Laya (`convaiinnovations/laya`) | 2026* | Open non-AR System 1 decisions with RLCD-calibrated probs; routes checkpoints | MASSIVE, XNLI, typed-decisions, AG News, DAIR Emotion, Banking77; vs published Jev 1.13.0 |

\*Card does not give a release year in the scraped text; treated as contemporaneous with the Jev comparison (Jev announced Sep 2026).

---

## Chronological idea lineage (strict)

Only from items above plus already-known `prior-work.md` entries these clearly extend:

Guo et al. 2017 (calibration / ECE) and Kadavath et al. 2022 (models stating when they know) set the measurement language for “honest probabilities.” SetFit 2022 shows that small encoder classifiers can beat prompt-heavy few-shot LLM setups—an architecture neighbor to later non-generative decision heads. Yang et al. 2023 RLCD is the **name collision** already recorded: preference alignment via contrastive distillation, not calibrated decisions. Damani et al. 2025 RLCR is the published RL objective that rewards calibration; Laya’s card uses the same proper-scoring-rule idea under the TypeSafe-style **RLCD** name. RouteLLM (ICLR 2025) and Nandakishor’s confidence-aware routing paper (2025) develop **routing from confidence/preference**, which Laya later applies as language/script checkpoint routing (different mechanism, same family of idea). SalesRLAgent + DeepMost model/dataset (2025) apply RL to **conversion probabilities in sales dialogue**—same author’s stack, different product surface than typed System 1 decisions. Laya (HF card) is the open artifact that **explicitly competes with TypeSafe Jev** on typed decisions, calibration, and latency.
