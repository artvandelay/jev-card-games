# Jev

Read 22 September 2026. How to call it, and what probability and confidence mean, is in `using-jev.md`.

The source of record is Diogo Almeida’s launch post, [Introducing System One Models & Jev](https://typesafe.ai/blog/introducing-system-one-models-and-jev) (TypeSafe AI, 15 September 2026). We call the model through OpenRouter, not the TypeSafe console.

## What the announcement says

TypeSafe AI spent about two years in stealth. Almeida (OpenAI, RLHF / InstructGPT / the work behind ChatGPT) says chat models got superhuman at talking to people and still did not produce automation. Jev is their first public **System One model**: a frontier model for fast, structured decisions that software can use directly.

The name comes from Kahneman’s System 1 (fast, intuitive) versus System 2 (slow, deliberate). They say “System 1” has implied error-prone, and they expect this class to be made more reliable than that. “Jev” is William Stanley Jevons: cheaper intelligence should raise demand, the way more efficient steam engines raised coal use.

The stack they describe:

- A new architecture (weights, paper, and exact architecture are not in the post).
- A **parallel sampler**. All outputs come from one query. No token-by-token generation.
- Training they call **Reinforcement Learning for Calibrated Decisions (RLCD)**. The target is epistemically honest probabilities on System One tasks, as opposed to human preference (RLHF) or programmatically verifiable rewards (RLVR).

Their one-line interface: unstructured state in, typed probabilistic decisions out. “A frontier-intelligence function call.” Giving up string generation is the point. Possible outputs are defined in advance, so they say the model cannot make a type error and, in that sense, cannot hallucinate. Schema match is guaranteed, not measured. They put 0% type-error on their plot for that reason.

### Against existing LLMs, in their words

| | Existing LLMs | Jev |
| --- | --- | --- |
| Trained with | RLHF / RLVR | RLCD |
| Input emphasis | Sequential messages | Structured program state |
| Output | Strings, then parse and validate | Type-safe values, plus probabilities and confidence |
| Sampling | One token at a time | All outputs in one query |
| Price | Input about $0.20–$10 / million tokens; output about 5× input | Input **$0.042 / million tokens** ($42 / billion). Output **free** |
| Latency | They cite 3–329 seconds for frontier chat models | **70–500 ms**, which they read as about 40×–200× on System One queries |
| Confidence | Often overconfident if you ask for it | Every output carries confidence; higher confidence should mean higher accuracy |
| Fit | Chat, copilots, coding agents, verifiable loops (math, kernels), demos | Workflows and “smart if-statements”, map-reduce over data, real-time apps, judging or guardrailing LLM outputs |

Use they name: classify, route, score, extract, or branch where hand-written logic is brittle. The surrounding code holds the freedom. Questions in one call are independent. Adding questions barely changes latency. Choice cardinality goes to **255**. Above that they score candidates, then choose, and that second stage is slower.

### Evidence they published, and the caveats they printed next to it

Easy to check, by their account:

- Speed. Published evals were run from laptops on the US West Coast, where the service is hosted.
- Price. Public. They say they cannot prove it is unsubsidized, and they expect the price to fall.
- Type errors. One counter-example would falsify it. They say it is mathematically impossible.

Bolder claims, with their own nuance:

- **Side-by-side demo.** Jev emits all probabilities in parallel. The recorded run mostly agreed with GPT-5.6 Terra at default reasoning, which they treat as the closest intelligence match. The one disagreement (“churn likelihood”) they call genuinely ambiguous. The state was short and dense, which favors Jev. Playground share: `shr_13a74b495fb786c4bd7964f11597301e7c9`.
- **Workflow evals** at [evals.typesafe.ai](https://evals.typesafe.ai/). Same workflow for every model. Reference labels are the average of GPT-6 Astra and Claude Fable 5.1 at high thinking. Four workflows: security incidents, agent-trace review, invoice processing, customer service. Homepage figures **193.6× faster** and **444.6× cheaper** come from here, and they say those sit at the high end of real gains. The workflows were written by their model-capabilities team, so bias is possible, and they are not in the training distribution. Using Astra and Fable as the reference biases the score toward OpenAI and Anthropic. LLMs were forced through their [System One adapter](https://github.com/typesafe-ai/system-one-adapter-python), which is slower and costlier than asking an LLM for a decision without probabilities. On the published average, Jev’s workflow is about **67.8%** agreement with that reference, **$0.0004** per case, **0.4 s**. Opus 5’s workflow is higher agreement (about 73%) and far slower and costlier. Invoice processing is a weak spot for Jev (about 61.8% versus Opus 5 at 78.4%).
- **Hallucination chart.** LLM numbers are from OpenRouter traffic, so harder queries may have been routed to stronger models. Jev’s 0% is the schema guarantee, not an empirical error rate. A wrong *decision* is still possible. The type cannot be wrong.

### Demos in the post

- **Doom.** Text state, not pixels. About 10 queries a second, which they cost at about **$7/hour**. A scripted bot could play better. The point was reacting to different state representations and following instructions. They plan a walkthrough and hack events.
- **Wikiracing.** Pick the next link among hundreds or thousands. Speedup versus LLMs was smaller because the LLMs were on non-reasoning settings (Astra at its lowest). Jev finished in fewer steps. Cardinality above 255 uses the two-stage chooser.

Early access opened with the post. The FAQ on the page answers the names. The other FAQ headings (why a new training algorithm, good use cases, “is it a small LLM”, public benchmarks, training data, how the results are possible) did not expand in the page text.

Company frame around the post, from [the manifesto](https://typesafe.ai/manifesto): composable “smart if-statements”, intelligence as a primitive next to ordinary code, “build prod, not God.” Founders on [the team page](https://typesafe.ai/team): Diogo Almeida (CEO), Sasha Sheng (COO), Erik Gafni (CTO). San Francisco, in person.

Official limits for the shipped model, [Jev 1.13 jaggedness](https://docs.typesafe.ai/model-jaggedness/jev-1.13) (reviewed 17 September 2026):

- It reads the words written, including negations, at face value.
- Counting, arithmetic, dates, and numeric calibration of Score levels belong in code.
- Extra hops of indirection and irrelevant state hurt accuracy. It has context rot.
- State is not treated as hostile. Injected instructions in the state can move the answer.
- A Noul and a yes/no Choice on the same fact are different questions. Probabilities need not sum to 1 across a question and its negation.
- It does not generate text. For extraction, find candidates in code or with another model, then let Jev pick.

Three question types, from the [docs introduction](https://docs.typesafe.ai/introduction): **Choice** (one option, probabilities, confidence), **Score** (a level, probabilities, confidence), **Noul** (probability from 0 to 1 that a statement is true; no confidence field).

## Calling it on OpenRouter

Listed 18 September 2026. One provider: TypeSafe. OpenRouter forwards every request there.

| | |
| --- | --- |
| Pinned model | `typesafe/jev-1.13` |
| Moving alias | `~typesafe/jev-latest` (the tilde is required) |
| Provider page | https://openrouter.ai/typesafe |
| Model page | https://openrouter.ai/typesafe/jev-1.13 |
| Recipes | https://openrouter.ai/labs/jev |
| Price | $0.042 / million input tokens, $0 output |
| Context | OpenRouter lists 32,000 tokens. TypeSafe’s model page is finer: 64k tokens for the whole request, and 32k for `state` plus the longest single question |
| Latency on OpenRouter | about 0.26 s p50, 0.40 s p95, 0.55 s p99 (their 1-week chart) |
| Uptime | 100% reachable over 3 days; 99.88% returned inference |

Chat completions do not work. OpenRouter’s own quick start says this model runs on the **Decisions API**.

```
POST https://openrouter.ai/api/alpha/decisions
Authorization: Bearer $OPENROUTER_API_KEY
Content-Type: application/json
```

The path is `/api/alpha/decisions`, not under `/api/v1`. The endpoint is marked alpha.

Body: `model`, `state` (string, object, or array), and `questions`. Each question has `type` (`noul`, `choice`, or `score`), `instructions`, and `criteria` where the type needs them. Question keys are for the caller. The model sees `instructions` and `criteria`.

OpenRouter’s TypeScript SDK is `openrouter.alpha.decisions.create({ decisionsRequest: { model, state, questions } })`. A third-party cookbook that hit the live API on 18 September 2026 recorded this answer shape ([nexibeo/jev-cookbook GUIDE](https://github.com/nexibeo/jev-cookbook/blob/main/docs/GUIDE.md)):

```json
{
  "model": "typesafe/jev-1.13-20260917",
  "answers": {
    "category": {
      "type": "choice",
      "choice": "recruiting",
      "probabilities": { "recruiting": 1, "sales": 0 },
      "confidence": 1
    },
    "is_writing_task": { "type": "noul", "noul": 0.99 },
    "specificity": {
      "type": "score",
      "score": 1.03,
      "probabilities": { "0": 0, "1": 0.97, "2": 0.03 },
      "confidence": 0.96
    }
  },
  "usage": { "input_tokens": 476, "output_tokens": 87, "cost": 0.000019992 },
  "provider": "TypeSafe"
}
```

Log `model`. The alias can move, and a threshold tuned on one dated build can shift. Pin `typesafe/jev-1.13` while thresholds are being set.

TypeSafe’s own [models page](https://docs.typesafe.ai/models) (direct API, same weights): current id `jev-1.13.0`. Aliases `jev-latest` and `jev-preview` both point at it. Rate limits on their API are 250,000 tokens per second and 1,200 requests per minute, and they say those move without notice while demand is high. Text only. English is the strongest language. No per-customer fine-tune or LoRA. Customer requests are not used for training. Domain knowledge goes in `state`, `instructions`, and `criteria`.

Key lives in the project root `.env` as `OPENROUTER_API_KEY` when we start calling it.

## Other writing

Primary:

- Announcement: https://typesafe.ai/blog/introducing-system-one-models-and-jev
- Home, manifesto, team: https://typesafe.ai/ https://typesafe.ai/manifesto https://typesafe.ai/team
- Docs: https://docs.typesafe.ai/introduction
- Jaggedness: https://docs.typesafe.ai/model-jaggedness/jev-1.13
- Evals: https://evals.typesafe.ai/
- Earlier essay, 10 Sep 2026, [The Bitterest Lesson](https://typesafe.ai/blog/bitterest-lesson): Almeida’s order is right task, then data, then compute, then algorithms. InstructGPT on a small model beat a much larger GPT-3 because the task was instruction-following, not next-token prediction. The June 2026 post [AI: too good to be true, too bad to be useful](https://typesafe.ai/blog/ai-too-good-to-be-true-too-bad-to-be-useful-typesafe-ai) is a video embed with no article text.

OpenRouter:

- https://openrouter.ai/typesafe/jev-1.13
- https://openrouter.ai/~typesafe/jev-latest
- https://openrouter.ai/labs/jev
- Decisions API reference linked from the cookbook: https://openrouter.ai/docs/api/api-reference/alphadecisions/submit-a-decisions-questions-and-answers-request

Press. Wikipedia’s article (edited 22 September 2026) is the index. I have now read TechCrunch (18 Sep) and SiliconANGLE (16 Sep). Forbes blocked the fetch with a captcha. The Register blocks scrapers.

From those two pieces, matching Wikipedia: $40 million seed led by DCVC (James Hardiman). SiliconANGLE cites Forbes for a $200 million valuation, “a person familiar with the transaction.” TechCrunch: Jev is transformer-based, trained only on synthetic data, architecture undisclosed. Almeida called the synthetic-data bet better than the launch and better than RLHF, and said about half the company is a lab for that data. Outside observers suspect an open-weight LLM underneath. He said later versions will add modalities. Armin Ronacher (Earendil, Pi) : the user still has to decide what a 50% versus a 95% answer means. SiliconANGLE’s speed line (“under 100 ms”, “up to 100×”) is looser than the announcement’s 70–500 ms and 40–200×.

- https://en.wikipedia.org/wiki/Jev_(AI_model)
- Forbes, 15 Sep 2026: https://www.forbes.com/sites/the-prompt/2026/09/15/this-200-million-startup-wants-to-fix-ais-overconfidence-problem/
- The Register, 16 Sep 2026: https://www.theregister.com/ai-and-ml/2026/09/16/typesafe-ai-debuts-model-for-machines-that-plays-doom/5296711
- SiliconANGLE, 16 Sep 2026: https://siliconangle.com/2026/09/16/typesafe-ai-exits-stealth-with-40m-to-build-ai-for-use-by-software/
- The Rundown, 16 Sep 2026: https://www.therundown.ai/articles/chatgpt-co-creator-launches-a-new-kind-of-ai
- TechCrunch, 18 Sep 2026: https://techcrunch.com/2026/09/18/a-new-kind-of-ai-model-from-a-chatgpt-inventor-is-thrilling-developers/

Secondary explainers (same week, mostly restating the post): LangChain harness guide, MarkTechPost, Turing Post, DataCamp, MindStudio, eesel, TrueFoundry, Eigent, explainx, DEV Community practical guide.
