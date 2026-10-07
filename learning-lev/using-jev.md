# Using Jev: concepts, API, probability, and confidence

Read 22 September 2026 from the TypeSafe docs, starting at the [AI primer](https://docs.typesafe.ai/introduction/machine-learning-primer). This is the operating note. The launch claims are in `JEV.md`. The bibliography is in `prior-work.md`.

We call it through OpenRouter, not the TypeSafe console. The question shape is the same. The URL and the model id are not. See the API section below.

## What the primer is actually saying

TypeSafe’s bet is that most automation will be machine-to-machine, and a chat interface is the wrong shape for that. They call the thing they want **machine-native intelligence**: structure, reliability, observability, testability, speed, consistency, and low cost. The slogan on the same page is “build prod, not God.” The model is not supposed to do the whole job. Code needs one narrow decision it can inspect.

They place three post-training paths on the same pretrained language model:

| Path | What it rewards | What you get |
| --- | --- | --- |
| RLHF | Text a human rater prefers | Chat. Also sycophancy, confident-sounding wrong answers, and **mode dropping**: the model piles probability onto one style (instruction following) and starves the rest of the distribution. They treat that as a mild form of GAN mode collapse. |
| RLVR | An output a program can check | Reasoning models that are strong at math and similar tasks, and slow and expensive. |
| RLCD | A probability that matches how often the answer is right | No text. A decision plus a probability. |

RLCD’s contract, in their words: the model does not generate text; it returns decisions and probabilities; a higher probability should mean the answer is right more often. Calibration is a statement about a **group** of predictions. If you collect every case the model marked 0.2, about 20% of those cases should be the event. The same for 0.8 and for 1.0. One answer marked 0.8 is not an 80% promise about that one case.

That last sentence is the whole reason the rest of this note exists. The calibrated object is the probability. Confidence is something else.

## Words

| Word | Meaning |
| --- | --- |
| State | The material being judged. A string, a JSON object, or an array of text. Think of it as what you would put in front of a person before asking them to decide. Images, audio, and video are not accepted. English is the strong language. |
| Question | One snap judgment about that state. It has a `type`, `instructions`, and usually `criteria`. |
| Question id | The key you pick (`refund_requested`). It comes back on the answer. It is **not** sent to the model. The whole question has to be in `instructions`. |
| Choice | One option from a list you wrote. The options are not ordered. |
| Score | A position on a ladder of levels you wrote, from low to high. |
| Noul | The probability that a yes/no statement is yes. |
| Probability | Mass on an outcome. This is the number RLCD is trained to make honest. |
| Confidence | A single 0–1 summary of how peaked a Choice or Score distribution is. Derived from the probabilities. Not a second probability of “I am correct.” |
| Calibration | A group property of the probabilities. Stated 0.8s happen about 80% of the time. It is not a property TypeSafe claims for the confidence statistic. |

A good question is one a knowledgeable person could answer in a second if you handed them the state. “Does this message convey urgency?” is that. “Analyze this message and determine the best course of action” is several judgments hiding in one number. Split those, then combine them in code. When the weights change, you change a coefficient, not a prompt.

## API surface

TypeSafe’s own endpoint, from the [API reference](https://docs.typesafe.ai/api):

```
POST https://api.typesafe.ai/v1/systemone
Authorization: Bearer $TYPESAFE_API_KEY
```

```json
{
  "model": "jev-latest",
  "state": { "ticket": "Help! My payouts have been failing for 3 days." },
  "questions": {
    "is_urgent": {
      "type": "noul",
      "instructions": "Does `ticket` convey urgency?"
    },
    "team": {
      "type": "choice",
      "instructions": "Which team should handle `ticket`?",
      "criteria": {
        "billing": "Payments, invoices, refunds",
        "technical": "Bugs, outages, integrations"
      }
    },
    "anger": {
      "type": "score",
      "instructions": "How angry is the writer of `ticket`?",
      "criteria": ["Calm", "Frustrated but civil", "Very angry"]
    }
  }
}
```

The response is `model`, `answers` keyed by those same ids, and usage. `jev-latest` and `jev-preview` both currently resolve to `jev-1.13.0`. Log the `model` field that comes back. An alias can move, and a threshold tuned on one build can shift.

This project calls OpenRouter instead. Same `state` and `questions`. Different host, and the model id is theirs:

```
POST https://openrouter.ai/api/alpha/decisions
Authorization: Bearer $OPENROUTER_API_KEY
```

Model `typesafe/jev-1.13` to pin, or `~typesafe/jev-latest` if the tilde alias is what you want. Chat completions reject this model. Details and a recorded response are in `JEV.md`.

Limits that matter while you design the request, from the [models page](https://docs.typesafe.ai/models):

- 64k tokens for the state plus every question. 32k for the state plus the single longest question.
- Choice: up to 255 options. Above that, the launch post says they score candidates and then choose, and that second stage is slower.
- Score: 2 to 10 levels.
- Text only.
- On their API, 250,000 tokens per second and 1,200 requests per minute, and they say those move without notice. A 429 is the signal.

`instructions` and `criteria` can be a string or JSON. Put the question in one field and the bits it refers to in others, and name those fields in backticks. In the state, a path looks like `` `ticket.messages[0].text` ``.

## State, and what not to put in it

Use an object for almost everything, so each fact has a name. A string is enough when there is only one passage. Put related facts in the same state when the question has to compare them (the message and the policy). Leave out everything else. Unrelated text is a distractor, and they say accuracy falls as it grows. That is the context rot they document on the jaggedness page.

The state is data. The judgment is the question. Do not write “mark this urgent if…” into the state. Do not put the current time, a count, or a date comparison in and expect the model to do the arithmetic. Compute that in code, and if the model needs the result, pass the result or a named bucket (“overdue”, “due this week”).

## Which question, and when

| You need | Ask | Then in code |
| --- | --- | --- |
| One of a known set, no order (team, language, intent) | Choice. Add `other` if the list can miss. | `switch` on `choice`. Look at `confidence` before you act. |
| A place on a ladder you can describe (severity, frustration) | Score. Each level is a situation, not a word like “medium.” | Rank or threshold `score`. Read `probabilities` when two different spreads could land on the same score. |
| A yes/no, and the probability is the useful signal | Noul. | Threshold `noul`. There is no `confidence` field. |
| Several independent judgments about one state | All of them in **one** request. Mix types. | Ignore the answers you do not need. Adding questions barely changes latency. |
| The next options depend on the previous answer | A second request. | Only then. If you could have asked it against the original state, it belonged in the first call. |

Noul is not a dial. A value of 0.5 means yes and no got similar probability. It does not mean “medium skill” or “somewhat angry.” If you wanted a degree, that was a Score. “Is this candidate strong in Python?” is a bad Noul unless you define strong so tightly that there is no middle (“Does the resume say they have used Python at work?”).

Score levels are judged one at a time. The model does not see the level number or its neighbors, so “worse than the previous level” means nothing. Describe a situation. One dimension per Score. “Punctual and smart and experienced” is three questions. The `score` you get back is the probability-weighted level number:

`score = Σ (level_index × probability of that level)`

Levels are numbered from 0 in the order you wrote them. A three-level score of 1.43 is `0×0 + 1×0.57 + 2×0.43`. It can sit between levels. The same 1.0 can be “all the mass on level 1” or “half on 0 and half on 2.” Those are different situations. `probabilities` and `confidence` tell them apart. The score is not a measurement of a real quantity between the levels. The jaggedness page says the level probabilities are weak if you try to interpolate an exact magnitude. Use the score to rank, or to see which side of a threshold you are on, or round to the nearest level when you need one bucket.

Two requests are the exception. They are justified when the code cannot build the second question until it has the first answer: it has to fetch new evidence, the objects being classified did not exist yet, or the next option list is the children of the option just chosen. Otherwise ask everything at once. They call the extra questions you might not use **speculative fan-out**.

## Probability and confidence

These are the two numbers people mix up. They are not two opinions. One is the distribution. The other is a comment on the shape of that distribution.

### Probability is the calibrated object

For a Choice, `probabilities` is a map from your option names to weights that sum to 1. For a Score, the same map over level numbers `"0"`, `"1"`, `"2"`, also summing to 1. For a Noul, there is one number, `noul`, which is P(yes). P(no) is whatever is left, so a Noul does not need a second field to describe its distribution.

RLCD, as the primer defines it, trains those probabilities. The claim is group calibration:

- Among cases where an outcome was given probability 0.2, that outcome should happen about 20% of the time.
- Among cases given 0.8, about 80%.
- Among cases given 1.0, essentially all of them.

You use the probability when the number itself is the decision:

- Rank passages by a Noul (“does this passage answer the query?”) and sort. The [re-ranking cookbook](https://docs.typesafe.ai/cookbooks/rerank_typesafe) does this. A threshold would throw away the ordering.
- Take an expected score, as above, and compare it to a cutoff.
- Set a Noul threshold from the cost of the two mistakes. Use 0.5 when a false yes and a false no are about equally bad. Raise it when acting on a false yes is expensive (send a refund, page someone). Lower it when missing a true yes is expensive (a safety flag). The middle band can go to a person.

A peaked wrong answer is still possible. Calibration does not say the argmax is correct. It says that when the model puts 0.9 on an outcome, outcomes in that bucket come true about nine times in ten, across many cases, if the calibration holds on your data. It has to be checked on your data. The primer states the definition. It does not publish a calibration plot for your task.

### Confidence is how peaked that distribution is

Choice and Score also return `confidence`, from 0 to 1. The [confidence page](https://docs.typesafe.ai/confidence) is explicit: it is a statistic computed from `probabilities`, so you can threshold without doing the math. All of the mass on one option gives 1.0. The more evenly the mass spreads, the lower the number.

Their interactive demo, for exactly three options, uses this approximation:

`confidence ≈ (3 × largest probability − 1) / 2`

At 90% / 6% / 4% that is 0.85, which is the number the demo shows. An even three-way split gives 0. They have **not** published the general formula for other numbers of options. They say the demo is an approximation, that `confidence` is a default that fits most uses, and that you are not locked into it because the full `probabilities` are in the response. If you need a different summary (margin between the top two, entropy, probability of the chosen option), compute it yourself from `probabilities`.

Read confidence as: “is there a winner, or is the model split?”

- Low confidence on a Choice usually means no option beat the others cleanly.
- Low confidence on a Score usually means the levels overlap, the question is several questions at once, or the state does not contain the fact.
- Confidence 1.0 means the returned distribution sits on one option or one level. The Score page says that describes the shape of the answer, not that the answer is correct.

Noul has no `confidence` because a two-outcome distribution is already one number. Distance from 0.5 is the peakedness. `0.97` is a settled yes. `0.50` is a coin flip. `0.03` is a settled no. If you want a Noul “confidence” in the same 0–1 sense, `|2 × noul − 1|` is the two-outcome version of that idea. The API does not return it. Do not invent a field.

### They answer different questions

| | Probability | Confidence |
| --- | --- | --- |
| Question it answers | How much weight is on this outcome? | How settled is the distribution? |
| Where it lives | `probabilities`, and `noul` | `confidence` on Choice and Score only |
| What is trained to be calibrated | Yes, this. Group frequencies. | No. It is a summary of the shape. |
| Can it be high and wrong? | A single 0.95 can be the wrong case. The bucket of 0.95s should be right about 95% of the time if calibration holds. | Yes. A wrong option with all the mass has confidence 1.0. |
| What you threshold for acting | Noul: the probability itself, because it is both the answer and the certainty. | Choice and Score: confidence gates whether you trust the argmax or the score enough to act. The probability of the chosen option is a stricter alternative you can compute yourself. |

A concrete split:

- Choice picks `billing` with probabilities `{billing: 0.42, technical: 0.31, sales: 0.27}`. The answer is billing. Confidence is low, because nothing won. Do not auto-route.
- Choice picks `billing` with `{billing: 0.96, technical: 0.03, sales: 0.01}`. The answer is billing. Confidence is high. Auto-route if billing is a low-stakes path.
- Score returns `1.0` with all mass on level 1, confidence 1.0. The model is settled on the middle level.
- Score returns `1.0` with half the mass on level 0 and half on level 2, confidence low. Same score, opposite situation. Do not treat those two 1.0s as the same event.

### What is not calibrated, even when the probabilities are

The docs and the jaggedness page draw these lines themselves:

- One prediction is not a guarantee. Calibration is across a bucket.
- Confidence is not “P(this answer is correct).” A confident wrong answer is a peaked distribution on the wrong option.
- A Noul and a yes/no Choice on the same fact are different questions. The jaggedness page shows a case where `noul` is 0.22 and the Choice probability of yes is 0.01. Do not copy a threshold from one onto the other.
- A Noul and the Noul of its negation need not sum to 1. They showed 0.72 and 0.47. Ask the question you mean. Do not derive the other by arithmetic.
- A Score’s fractional part is a weak place to recover an exact number. “1.4 means 40% of the way from level 1 to level 2 in the real world” is the interpolation they tell you not to do.
- The model reads the words you wrote. A high probability of yes means yes to that sentence, including a negation you did not notice.

So: the part they claim is calibrated is the probability distribution (Choice and Score `probabilities`, and the Noul value). Confidence is a convenience reduction of that distribution’s shape. Check both on your own labels before a threshold ships. Their suggested way to start is conservative thresholds, then move them after you see your data.

## How to act on the numbers

The [confidence page](https://docs.typesafe.ai/confidence) and the [confidence-gated routing](https://docs.typesafe.ai/patterns/confidence-routing) pattern use the same three bands. The cutoffs are not universal. They move with the cost of being wrong.

| Band | Choice / Score | Noul |
| --- | --- | --- |
| Settled and low stakes | Act. Their banking example treats a balance check as fine around 0.6 confidence. | Threshold near 0.5 if both mistakes are cheap. |
| Settled but high stakes | Demand more. Their transfer example wants confidence above about 0.85 or 0.9, and otherwise asks the person to confirm. | Raise the threshold (0.8, 0.9) when a false yes is expensive. |
| Split | Do not act. Route to a person, ask again, or hand the case to a model that can write. Their floor examples are 0.5 and 0.6. | A band around 0.5 goes to a person. Do not flip a coin in code and call it a decision. |

The answer says what. Confidence, or a Noul’s distance from 0.5, says whether. A destructive action and a read-only action in the same request should not share one cutoff.

## When this is the wrong tool

Use ordinary code for anything with an exact answer: counts, arithmetic, date order, “which of these strings match,” legality of a move. Pass the result in if a later judgment needs it.

Use a language model when the output has to be new text, code, or a plan with several dependent steps. Jev can sit in front of that model (is this request in scope, which specialist, is the tool call safe) and behind it (does this answer match the source, how severe is this trace). It should not be the writer.

Use a second Jev call when the next question cannot be formed yet. Do not use a loop that asks Jev what to do next in the way an agent asks itself. The how-to-build page is blunt: this is for software with the control flow in code, not for an agent that chooses its own next action.

The failure modes worth designing around, from [jev-1.13 jaggedness](https://docs.typesafe.ai/model-jaggedness/jev-1.13): it is literal; it is bad at counting, math, and dates; extra hops of indirection hurt; junk in the state hurts; text inside the state can steer the answer; contradictory instructions and criteria confuse it; it will not generate a string worth having.
