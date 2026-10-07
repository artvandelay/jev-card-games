# Prior work people cite around Jev

Read 22 September 2026.

TypeSafe has not published a Jev architecture paper or an RLCD training paper. The [AI primer](https://docs.typesafe.ai/introduction/machine-learning-primer) names the objective and does not give a loss, a reward model, or a backbone. Coachix, checking on 19 September 2026, found the same gap and wrote that none of the papers below should be labeled “the Jev paper.” [Coachix’s guide](https://coachix.dev/llm/jev/) is the clearest public bibliography. [Ginger Labs](https://gingerlabs.ai/blog/rlcd-vs-rlhf-how-does-typesafe-ai-jev-work) and [explainx](https://www.explainx.ai/blog/how-does-jev-work-rlcd-system-one-model-explained-2026) cite a smaller subset and say the same thing about the missing paper.

Hacker News commenters guessed an encoder-only transformer, a text-diffusion model, or a purpose-built head. explainx records those as reader hypotheses. A LLaDA fork in TypeSafe’s GitHub organization is not evidence that Jev is that model.

## What TypeSafe itself names

These are sources the company points at in the launch post, the primer, or [The Bitterest Lesson](https://typesafe.ai/blog/bitterest-lesson) (10 September 2026; the essay also lives at [completeskeptic.com](https://www.completeskeptic.com/p/the-bitterest-lesson)).

**InstructGPT.** Long Ouyang, Jeff Wu, Xu Jiang, Diogo Almeida, and others, “Training language models to follow instructions with human feedback,” 2022. https://arxiv.org/abs/2203.02155

Almeida is a coauthor. The bitterest-lesson essay uses figure 31 from this paper: a GPT-2-sized model trained on instruction following beat a much larger model trained to predict the next token. The primer uses the same lineage to say what Jev is leaving. RLHF trains a model to produce text people prefer. TypeSafe’s claim is that this also rewards a confident style and drops other modes of the distribution. RLCD is their name for a third post-training path, after RLHF and RLVR, whose target is a probability that matches how often the answer is right.

**The bitter lesson.** Richard Sutton, “The Bitter Lesson,” 2019. http://www.incompleteideas.net/IncIdeas/BitterLesson.html

Sutton’s claim is that general methods plus compute beat hand-built knowledge. Almeida’s essay puts a stricter order in front of that: the right task, then data, then compute, then algorithms. Jev is the product version of “chat was the wrong task for automation.”

**Thinking, Fast and Slow.** Daniel Kahneman, 2011. Named in the launch FAQ. System 1 is fast intuitive judgment. System 2 is slow deliberate reasoning. TypeSafe took the fast half as the product category and said they expect it can be made more reliable than the “error-prone System 1” reading.

**Jevons.** William Stanley Jevons, *The Coal Question* (1865), via the paradox named after him. Named in the launch FAQ. More efficient use of a resource can raise total consumption. The model is named for the bet that cheaper decisions create more decisions, not a smaller bill for the same ones.

The primer also describes GAN mode collapse as the extreme form of RLHF “mode dropping,” without citing a paper.

## Papers other people attach, and what they actually are

Coachix lists these as related ideas. Ginger Labs adds the RLAIF paper.

**Calibration, the measurement Jev’s marketing depends on.** Chuan Guo, Geoff Pleiss, Yu Sun, Kilian Weinberger, “On Calibration of Modern Neural Networks,” ICML 2017. https://arxiv.org/abs/1706.04599

A model can be accurate and still be a bad probability. Expected calibration error and temperature scaling come from this line of work. When TypeSafe says “70% should be right about 70% of the time,” this is the standard they are invoking. The paper is about classifiers, not about RLCD.

**Whether a language model can say when it knows.** Saurav Kadavath and others, “Language Models (Mostly) Know What They Know,” 2022. https://arxiv.org/abs/2207.05221

Models can be asked for P(the answer is true) and sometimes those numbers are useful. Transfer across tasks is hard. Coachix cites it to say uncertainty estimates are older than Jev.

**A published reinforcement-learning objective that rewards calibration.** Mehul Damani and others, “Beyond Binary Rewards: Training LMs to Reason About Their Uncertainty,” 2025, revised 2026. https://arxiv.org/abs/2507.16806

They call their method RLCR: a correctness reward plus a Brier penalty, so the model is trained both to be right and to state a probability that matches its hit rate. Project page: https://rl-calibration.github.io/. This is the closest public training paper to the *goal* TypeSafe describes. It trains reasoning language models. It is not TypeSafe’s recipe, and the acronym is different on purpose.

**The other RLCD.** Kevin Yang and others, “RLCD: Reinforcement Learning from Contrastive Distillation for Language Model Alignment,” 2023, ICLR 2024. https://arxiv.org/abs/2307.12950

Code: https://github.com/facebookresearch/RLCD. This paper generates preference pairs from contrastive prompts so you can do RLHF-style alignment without human labels. Ginger Labs and Coachix both warn that the shared initials are a collision. TypeSafe’s expansion is “Reinforcement Learning for Calibrated Decisions.” Reading the 2023 paper as the Jev paper is a mistake.

**RLAIF, the neighbor Ginger Labs adds.** Harrison Lee and others, “RLAIF vs. RLHF: Scaling Reinforcement Learning from Human Feedback with AI Feedback,” 2023. https://arxiv.org/abs/2309.00267

AI raters replace human raters inside the preference loop. Still a preference method. Cited as context for the RLHF family, not as Jev’s trainer.

**Diffusion, only because people guessed it.** Shen Nie and others, “Large Language Diffusion Models” (LLaDA), 2025. https://arxiv.org/abs/2502.09992

Coachix includes it as background for the Hacker News guess that parallel sampling means diffusion. The authors of that guide say a fork in TypeSafe’s org is not lineage.

## How to read this stack

The company’s own citations explain the motive: InstructGPT showed that the training task dominates scale, Kahneman named the fast kind of judgment, Jevons named the demand response to cheaper intelligence. The outside citations explain the claim they have not documented: honest probabilities (Guo), models that know when they know (Kadavath), and one published way to reinforce calibration (Damani). The Yang RLCD paper is the one to keep out of that stack.

## From a researcher the user trusts

These are the research links in that video description, read 22 September 2026. The song and the Lambda page in the same description are not prior work. The posts are below. X blocked a direct fetch; the wording comes from the fxtwitter text of each status.

**SetFit.** Lewis Tunstall, Nils Reimers, and others, “Efficient Few-Shot Learning Without Prompts,” Hugging Face blog, 26 September 2022, with Intel Labs and UKP Lab. https://huggingface.co/blog/setfit — paper https://arxiv.org/abs/2209.11055

Few-shot classification by contrastive fine-tuning of a sentence transformer, then a classification head. No prompts. Shown on the RAFT leaderboard, Customer Reviews (SentEval-CR, 8 examples per class), and multilingual sets in German, Japanese, Mandarin, French, and Spanish, against PET, GPT-3, T-Few, and others. A distant ancestor of “encoder plus a head, no generation.” It does not mention Jev.

**RouteLLM.** Isaac Ong, Amjad Almahairi, Vincent Wu, Wei-Lin Chiang, Tianhao Wu, Joseph E. Gonzalez, M. Waleed Kadous, Ion Stoica, “RouteLLM: Learning to Route LLMs from Preference Data,” ICLR 2025. https://proceedings.iclr.cc/paper_files/paper/2025/hash/5503a7c69d48a2f86fc00b3dc09de686-Abstract-Conference.html

A router trained on preference data picks a stronger or a weaker language model per query. The abstract claims more than a 2× cost cut without a quality drop, and generalization to model pairs it was not trained on. The abstract page says “public benchmarks” and does not name them. This is cost routing between chat models, not a System One decision model.

**SalesRLAgent.** Nandakishor M, “SalesRLAgent: A Reinforcement Learning Approach for Real-Time Sales Conversion Prediction and Optimization,” arXiv, 30 March 2025. https://arxiv.org/abs/2503.23303

Conversion prediction as a sequential decision, with a probability at each turn of a sales conversation, rather than an LLM answering questions about the transcript. Evaluated on synthetic dialogues generated with GPT-4o and 3072-dimensional Azure OpenAI embeddings. The abstract reports 96.7% conversion-prediction accuracy against an LLM-only baseline, 85 ms versus 3450 ms inference, and a 43.2% conversion-rate lift when reps follow the guidance. No named public NLP benchmark.

**Open sales model and data.** DeepMost Innovations, Stable-Baselines3 PPO weights, MIT. https://huggingface.co/DeepMostInnovations/sales-conversion-model-reinf-learning — dataset https://huggingface.co/datasets/DeepMostInnovations/saas-sales-conversations

The model card is an open PPO agent for that paper, trained on 100,000+ synthetic sales conversations, with BAAI/bge-m3 embeddings (1024-d) and an optional Azure embedding path. The dataset is about 100,000 synthetic English B2B SaaS dialogues with outcomes, engagement scores, probability trajectories, and 3072-d embeddings. One train split. Same task as the paper, not a Jev interface.

**Confidence-aware routing.** Nandakishor M, “Confidence-Aware Routing for Large Language Model Reliability Enhancement: A Multi-Signal Approach to Pre-Generation Hallucination Mitigation,” arXiv, 23 September 2025. https://arxiv.org/abs/2510.01237

Estimate whether a query is safe to answer before generating, from semantic alignment, layer convergence, and a learned confidence score, then send it to a local model, retrieval, a larger model, or a person. The paper HTML names Natural Questions, TriviaQA, and HotpotQA, plus synthetic sets with injected factual errors. The abstract reports hallucination detection of 0.74 against 0.42, F1 from 0.61 to 0.82, and about a 40% compute cut versus post-hoc checks. Same author as SalesRLAgent. Routing by confidence, not typed decisions.

**Laya.** Convai Innovations, Hugging Face model card, Apache-2.0. https://huggingface.co/convaiinnovations/laya

An open, multilingual, non-autoregressive System 1 model: state and typed questions in, calibrated probabilities out, one forward pass, about 33–40 ms on a T4. The card uses RLCD in TypeSafe’s sense, strictly proper scoring rules. It reports MASSIVE intent, XNLI, a typed-decisions set (2,000 decisions, four workflows), AG News, DAIR Emotion, and Banking77, and it compares those numbers to published Jev 1.13.0 figures without calling the TypeSafe API. The card’s own reading: faster and open, stronger on some calibration and typed-decision scores, weaker on high-cardinality labels such as Banking77. This is the artifact in the list that is actually trying to be Jev.

### Key papers

Academic papers only. Model cards, datasets, blogs, tweets, and the song stay in the sections above or in “What the posts add.” Yang et al. 2023 remains a **name collision** with TypeSafe’s “Reinforcement Learning for Calibrated Decisions”; TypeSafe has not published an RLCD paper.

| Paper (title, year, link) | Main insight | Environments / datasets |
| --- | --- | --- |
| InstructGPT — Ouyang, Wu, Jiang, Almeida, et al., “Training language models to follow instructions with human feedback,” 2022. https://arxiv.org/abs/2203.02155 | Preference feedback can make a smaller instruction-tuned model beat a much larger next-token model on the same prompt distribution. | Labeler-written and OpenAI API prompts for SFT + rankings; human preference evals on that distribution; abstract also notes public NLP dataset checks (unnamed on the abs page). |
| Guo et al., “On Calibration of Modern Neural Networks,” 2017. https://arxiv.org/abs/1706.04599 | Accuracy and honest probability are different; temperature scaling often fixes overconfident classifiers. | Image and document classification datasets (abstract). |
| Kadavath et al., “Language Models (Mostly) Know What They Know,” 2022. https://arxiv.org/abs/2207.05221 | Models can often report useful P(True) / P(I know) self-evaluations, with uneven transfer to new tasks. | Diverse multiple-choice and true/false formats; open-ended P(True); math word problems with hints (abstract). |
| Damani et al., “Beyond Binary Rewards…” (RLCR), 2025. https://arxiv.org/abs/2507.16806 | RL that adds a Brier term to correctness keeps accuracy and improves calibration on reasoning LMs. | Train: HotPotQA-Modified; Big-Math subset. Eval: HotpotQA, TriviaQA, SimpleQA, GPQA, Math500, GSM8K, Big-Math, CommonsenseQA (paper HTML). |
| Yang et al., “RLCD: Reinforcement Learning from Contrastive Distillation…,” 2023 (ICLR 2024). https://arxiv.org/abs/2307.12950 | **Name collision.** Contrastive prompts invent preference pairs for RLHF-style alignment without human labels. | Harmlessness / helpfulness prompts from Anthropic HH sets; story-outline premises; LLaMA-7B/30B preference simulation. |
| Lee et al., “RLAIF vs. RLHF…,” 2023. https://arxiv.org/abs/2309.00267 | AI-labeled preferences can match human RLHF on several alignment tasks. | Summarization (Reddit TL;DR / OpenAI human preferences); Anthropic Helpful and Harmless. |
| Nie et al., “Large Language Diffusion Models” (LLaDA), 2025. https://arxiv.org/abs/2502.09992 | A masked diffusion LM trained from scratch can match strong AR baselines and helps on reversal tasks. | Among reported tables: MMLU, BBH, ARC-C, HellaSwag, TruthfulQA, WinoGrande, PIQA, GSM8K, Math, GPQA, HumanEval, MBPP, CMMLU, C-Eval; poem reversal set. |
| Sutton, “The Bitter Lesson,” 2019. http://www.incompleteideas.net/IncIdeas/BitterLesson.html | General methods plus compute tend to beat hand-built knowledge over time. | Essay; no experimental datasets. |
| Tunstall, Reimers, et al., “Efficient Few-Shot Learning Without Prompts” (SetFit), 2022. https://arxiv.org/abs/2209.11055 | Contrastive Sentence-Transformer fine-tuning plus a head beats prompt-heavy few-shot recipes at small size. | RAFT; Customer Reviews (CR); SST2, IMDB, AG News, Amazon Polarity, Emotion, and other Hub SetFit sets (paper appendix); multilingual CR-style evals in the blog. |
| Ong et al., “RouteLLM…,” ICLR 2025. https://proceedings.iclr.cc/paper_files/paper/2025/hash/5503a7c69d48a2f86fc00b3dc09de686-Abstract-Conference.html | Preference-trained router chooses a stronger or weaker LLM per query to cut cost. | Abstract says “public benchmarks” and does not name them. |
| Nandakishor M, “SalesRLAgent…,” 2025. https://arxiv.org/abs/2503.23303 | RL over conversation state emits turn-by-turn conversion probabilities instead of chat about the call. | Synthetic GPT-4o sales dialogues (~1.2M in the HTML; model/dataset cards cite ~100k releases); Azure / BGE embeddings; CRM integration targets. |
| Nandakishor M, “Confidence-Aware Routing…,” 2025. https://arxiv.org/abs/2510.01237 | Estimate reliability before generation and route to local gen / RAG / larger model / human. | Natural Questions, TriviaQA, HotpotQA; synthetic error-injection sets (paper HTML). |

**Not papers (kept out of the table):** DeepMost sales model + `saas-sales-conversations` dataset; `convaiinnovations/laya` model card; SetFit / TypeSafe blogs; launch-window tweets; Two Minute Papers song https://www.youtube.com/watch?v=4RtUJkjrKMI.

### Idea lineage

**What TypeSafe claims.** The launch post and primer put Jev in a System 1 slot: fast structured decisions whose probabilities should match hit rate. They point at InstructGPT / RLHF, Kahneman’s fast judgment, Jevons’s demand paradox, and Sutton (tightened in Almeida’s “bitterest lesson”). They name their post-training idea RLCD — Reinforcement Learning for Calibrated Decisions — and have not released a loss, reward model, or backbone. Parallel-sampling / LLaDA guesses stay outside what the company documents.

**What this researcher’s list adds as intellectual ancestors.** SetFit as the prompt-free encoder-plus-head pattern; RouteLLM and Nandakishor’s confidence-aware paper as “act on uncertainty before you spend a big model”; SalesRLAgent plus DeepMost weights/data as open probability-over-dialogue work; Laya as an open System 1 API shape that scores itself against published Jev numbers. Launch tweets are reception and demos.

**Ordered chain:**

1. Sutton / bitter(est) lesson — right task, then general methods and compute.
2. InstructGPT / RLHF — preference-tuned text wins the chat era; Almeida later argues chat was the wrong automation task.
3. Guo calibration + Kadavath self-knowledge — “70% should be right ~70% of the time,” and models can sometimes say when they know.
4. Damani RLCR — published RL that rewards correctness and calibrated confidence (closest public *goal* match; different acronym; still a reasoning LM).
5. Lee RLAIF + Yang contrastive RLCD — preference-family neighbors; quarantine the Yang acronym collision.
6. SetFit — small encoder + head, typed labels, no generation.
7. RouteLLM + SalesRLAgent + confidence routing + DeepMost/Laya artifacts — open routing and “decide, don’t chat” systems the researcher treats as precursors.
8. TypeSafe Jev — hosted System One product with that *shape*; training recipe unpublished.

Do not invent a Jev training recipe from this stack.

### What the posts add

None of the thirteen posts link the papers or model cards above. They are demos and arguments. Treat the numbers as the author’s claim.

| Who | What they add |
| --- | --- |
| [Diogo Almeida](https://x.com/completeskeptic/status/2099925684256899543), 15 Sep | The speed comes from giving up text. Parallel decisions versus token-by-token generation is the same kind of jump as transformers over recurrent nets. |
| [Diogo Almeida](https://x.com/completeskeptic/status/2099925685720760404), 15 Sep | Workflow evals, $0.042 per million input tokens, output free, and the Jevons name. |
| [Alexis Gallagher](https://x.com/alexisgallagher/status/2100312082491322873), 16 Sep | The skeptical frame: encoder-only classifiers (he names ModernBERT, and maybe LFM2.5 fine-tunes) already do fast cheap structured output. He thinks Jev is better and does not need a fine-tune per task, and that the category is old. |
| [Tamara Tran](https://x.com/tamarajtran/status/2100694549362553153), 17 Sep | Compact an agent trace by scoring each tool call and dropping the irrelevant ones, instead of asking a model to summarize. |
| [Erik Gafni](https://x.com/egafni/status/2100770895325524242), 18 Sep | Points at a community self-driving demo and calls it nuts. No technical claim of his own. |
| [Mau Baron](https://x.com/maubaron/status/2100738237237002706), 18 Sep | Jev plays all four Smash Bros characters against itself. He says the match used more than 22 million tokens for a couple of cents, and that this is not a replacement for GPT-6 Astra. |
| [Elvis Sun](https://x.com/elvissun/status/2100951347080421409), 18 Sep | 384 news items for 15 brands in 24.9 seconds for $0.19, against Claude Opus 5 getting through 4 of 384 for $0.77. Demo at [newsjack.sh](http://newsjack.sh). |
| [Filipp Kowalski](https://x.com/filippkowalski/status/2100864984448147770), 18 Sep | Points at MaxBlade’s Subway Surfers clip (50 games at once, under a cent) as the clearest “what Jev is” demo that day. |
| [Hugo Duprez](https://x.com/HugoDuprez/status/2100953089003921543), 18 Sep | Real-time game-level generation. |
| [Mizore](https://x.com/mizorewww/status/2101473552956555427), 20 Sep | [laya-mlx](https://github.com/mizorewww/laya-mlx): Laya on Apple MLX, claimed about 50× faster than hosted Jev on device, under 1 GB, Snake at about 60 decisions a second on an M3 Max. |
| [Miu](https://x.com/miu21590/status/2101857866378362926), 21 Sep | Inside Codex, Jev raises or lowers GPT-6 reasoning effort mid-task. Claims about 50% lower Astra cost in their tests. |
| [Viraj](https://x.com/heyxviraj/status/2102048070649405592), 21 Sep | [laya-vs-jev](https://github.com/virajbhartiya/laya-vs-jev): hosted Jev and local Laya race the Chrome dinosaur. |
| [Atomic Chat](https://x.com/atomic_chat_hq/status/2102160983409955244), 21 Sep | Local Laya beat cloud Jev at Tetris by about 11× on a 16 GB MacBook Air. Product page [atomic.chat](https://atomic.chat). |

Gallagher is the one who changes the lineage. He puts Jev in the existing encoder-classifier line (ModernBERT-style fine-tunes), and says the new part, if any, is that one model answers new tasks without a training run for each task. The game posts and the two Laya ports are evidence of use, not of a new paper. Laya on a laptop, at game tick rate, is the practical version of the open model in the table above.
