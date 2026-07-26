# Human Feedback Capture

> Capture the operator's quality verdicts on LLM output at click-cost, with enough
> frozen context that every verdict is attributable, replayable, and usable as training
> data. The human-in-the-loop companion to [AI_EVALS.md](AI_EVALS.md).

**Applies to:** Owner-operated or small-user-base AI apps producing subjective/generative
output (chat, narration, social posts, long-form drafts) where the operator is a better
judge than any rubric. Validated on a small-user-base AI chat/drafting app.
**Last Updated:** 2026-07-20
**Version:** 1.0

---

## Table of Contents

- [Overview](#overview)
- [When to Use](#when-to-use)
- [The pattern](#the-pattern)
- [Feeding downstream consumers](#feeding-downstream-consumers)
- [Anti-Patterns](#anti-patterns)
- [Adoption notes](#adoption-notes)
- [Resources](#resources)

---

## Overview

[AI_EVALS.md](AI_EVALS.md) covers *automated* regression evals and says of generative
output: "Generation/chat is harder — come to it later with an LLM-judge." For
owner-operated apps there is a better first move: **don't approximate the judge you
already have.** The operator sees every output during real use; a rating affordance at
the moment of judgment captures ground truth an LLM judge can only imitate — for the
cost of a click.

The catch is that a bare thumbs-up table is almost worthless. The value is in what the
click *carries*: the full model input frozen at generation time, the output, the
prompt/config version that produced it, provenance for any retrieval involved, and
(optionally) the operator's one-line reason. With those attached, one click
simultaneously feeds four consumers: **prompt iteration** (routable defect reports),
**regression dashboards** (down-rate per prompt version), **golden-set curation**
(up-votes ARE the curation), and a **fine-tuning corpus** (SFT from ups, KTO-style
preference data from the binary signal).

### Key Benefits

- Ground-truth quality signal from real use, no annotation sessions, no judge to build.
- Every verdict is self-describing: what the model saw, what it said, which prompt
  version, what retrieval fed it, and why the human objected.
- The golden set curates itself during normal use (`rating = 'up'` is the query).
- Training data accumulates from day one — **it cannot be backfilled later.**

---

## When to Use

| Scenario | Use this protocol? |
|----------|--------------------|
| Owner/small-team app with subjective generative output (chat DM, social drafts, long-form) | **Yes — this before an LLM judge** |
| High-volume bounded output (scores, labels, extraction) | No — [AI_EVALS.md](AI_EVALS.md) golden-set regression is the right tool |
| Output volume far beyond what the operator sees (thousands/day unreviewed) | LLM judge per AI_EVALS becomes necessary; keep this for the reviewed slice — human verdicts calibrate the judge |
| A future fine-tune is even a possibility | **Yes, start capturing now** — the corpus is the part you cannot recreate |
| Throwaway prototype | No |

The two protocols compose: automated evals catch drift on bounded outputs; human
capture owns the subjective ones; the human verdicts later become the calibration and
ground-truth subset the automated layer wants.

---

## The pattern

Seven primitives, in dependency order.

**1. Capture the full model input at generation time.** Persist the verbatim compiled
input (system-adjacent context + user message) on the turn/generation record the moment
it is sent. Mutable context (summaries, memories, workspace rules) makes it
unreconstructable later — capture-or-lose. Never let a capture failure kill a paid
generation (wrap it; log it).

**2. Stamp version identity on every generation.** A `prompt_sha` (hash of the
effective instruction text — including any DB-resident rule overrides folded in) plus
the deploy git sha. This is what makes ratings survive prompt evolution, powers
down-rate-per-version dashboards, and lets a later reader answer "which prompt wrote
this?" mechanically. If prompts live partly in code and partly in DB rules, hash the
*effective merged* text.

**3. Three-state rating affordance on the output surface.** Up = exemplar/golden
candidate; unrated = neutral (most outputs); down = defect. Click again to withdraw;
switching upserts. One verdict per generation per user (`UNIQUE(generation_id, user_id)`).
Persist server-side and **hydrate on load** — a rating that vanishes on refresh trains
the operator to stop rating. Server-side snapshot at verdict time: input, output, tool
calls, persona/task-kind, model, `prompt_sha`, provenance.

**4. Record provenance for attribution.** A down-vote is ambiguous between "generation
was bad" and "the pipeline fed it the wrong context" (retrieval, rules, source data).
Record what the pipeline actually supplied (e.g. file-search result attributes, the
rule-set version) on the generation record, and snapshot it into the verdict. Triage
then attributes post-hoc with zero click-time friction — and mis-attributed downs never
poison the training corpus (see anti-patterns).

**5. Optional why-comment, inline and non-blocking.** After a rating sticks, offer a
multiline comment box **inside the output's own container** — no modal, no backdrop —
so the content being judged stays visible, scrollable, and copy-pasteable into the
note. Offer it on BOTH verdicts: a down's "what went wrong" routes iteration; an up's
"why this was great" becomes the golden's curation note. Editable later via a small
affordance on rated items. Optional always; the common case is the bare click.

**6. Golden-set freeze from up-votes.** A curation tool that lists rated generations
and freezes chosen ones to committed JSON files (id, frozen input, live output,
rating, comment, capture provenance). A `freeze-ups` mode makes the 👍 stream the
default source. Balance rule: **a golden set of only triumphs under-tests** — add a few
ordinary and hard cases by hand.

**7. Human-judged side-by-side replay.** Before any prompt/model/pipeline change, replay
the goldens through the current config and render baseline-vs-candidate as a plain
report **for the operator's eyeball** — no LLM judge, no scores. Modes: rebaseline /
label-vs-baseline / two-live-sides compare. This is the measured gate for prompt edits
and model swaps.

---

## Feeding downstream consumers

- **Prompt iteration:** downs with comments are routable work items; fix, bump the
  prompt (git is the versioning), and the sha shift cleanly separates before/after.
- **Regression detection:** down-rate charted per `prompt_sha`/model is the
  boiling-frog defence — three subtle changes in one window are invisible to memory
  and obvious on the chart.
- **Fine-tuning corpus:** ups = SFT exemplars (full input → output). Ups+downs =
  binary unpaired preference data (KTO-style — no matched pairs needed). Where users
  pick one of N generated variants, **retain the losers**: selection events are natural
  pairwise (chosen, rejected) preference records, strictly stronger than unpaired.
  Volume expectation: hundreds of quality examples before a LoRA-class tune is
  meaningful; that is an argument for starting capture years early, not against it.
- **Implicit signals count too.** Any place the user's ordinary workflow expresses a
  verdict is free feedback: variant selection, the **edit distance between the
  generated draft and what actually got published/sent** (near-zero = implicit up;
  heavy rewrite = implicit down; both texts are usually already persisted), retries,
  abandonment. Capture them alongside explicit ratings with the same version stamps.

---

## Anti-Patterns

### A modal that blocks the content it judges

```
❌ Bad — a centered comment dialog with a backdrop: the operator cannot see, scroll,
   or copy the text they are criticising; comments become vague or skipped.
✅ Good — inline expandable box inside the output's container; chat/post stays live;
   the offending passage gets pasted into the note.
```

### Ratings without version identity

```
❌ Bad — a thumbs table with no prompt_sha: after three prompt edits, the corpus is
   an unattributable soup and the down-rate chart means nothing.
✅ Good — every generation stamped with effective-prompt hash + deploy sha at
   generation time (not at rating time).
```

### Deleting the losing variants

```
❌ Bad — user picks 1 of N drafts, the other N-1 are deleted. The strongest natural
   preference data the product produces is destroyed at the moment it is expressed.
✅ Good — persist the full option set with the selection event; losers are the
   'rejected' half of pairwise preference pairs.
```

### Training on mis-attributed downs

```
❌ Bad — feeding every down-vote into preference tuning. A down caused by bad
   retrieval/context punishes the generator for faithfully rendering what it was
   given — training on noise with authority.
✅ Good — provenance recorded per generation; downs attributed retrieval-caused are
   excluded from generator preference data and routed to the pipeline backlog.
```

### Building an LLM judge for output the operator already judges

```
❌ Bad — an LLM judge as the FIRST eval for an owner-operated chat/drafting app.
✅ Good — capture the operator's verdicts at click-cost; add a judge only when volume
   outgrows the operator's eyes, calibrated against the accumulated human verdicts.
```

### Assuming the corpus can be backfilled

```
❌ Bad — "we'll add feedback capture when we're ready to fine-tune."
✅ Good — mutable context makes past inputs unreconstructable; every unlogged good
   turn is a training example lost forever. Capture starts the day generation ships.
```

---

## Adoption notes

**Greenfield (all seven primitives from the start).** Capture at generation, prompt-sha
identity, three-state thumbs with hydration and inline comments, verdict snapshots, a
golden freeze-from-ups tool, and eyeball replay. The reference build wired these in one
pass; its first customers were prompt-version iteration and a model-swap comparison —
both of which need primitives 2 and 7 to mean anything.

**Retrofitting an app that already has strong automated evals but zero human capture.**
Highest-leverage order, and it is not the order teams expect:

1. **Version stamping first.** Hash the effective prompt (code modules plus any
   DB-resident rule overrides, merged) onto the generation record. Cheapest primitive,
   and a prerequisite for every other one. The common starting state is that *nothing*
   records which prompt produced a given output.
2. **Retain rejected variants.** Pipelines that let a user pick one of N drafts often
   delete the losers on selection. Keep them, persisted with the selection event, and
   every pick the user already makes mints a pairwise preference record — free, and
   strictly stronger than unpaired signal.
3. **Draft→published edit distance.** Where a generated draft and its
   eventually-published text are both stored and already linked, they are usually
   compared only for an exact-match badge. Compute and store a similarity score
   instead: it is a passive implicit-feedback signal that needs no new UI at all.
4. **Explicit thumbs and comments last.** The implicit signals above capture most of
   the value without asking the operator to change how they work.

---

## Resources

- [AI_EVALS.md](AI_EVALS.md) — the automated companion; this protocol supplies its
  ground-truth subset and owns subjective outputs
- [AI_OBSERVABILITY.md](AI_OBSERVABILITY.md) — runtime metrics the ratings join against
- [QA_PROTOCOL.md](QA_PROTOCOL.md) — replay-before-change is tier-Full verification for
  prompt/model edits

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2026-07-20 | Initial release. Extracted from a feedback/eval build on a small-user-base AI chat app (three-state ratings, turn-time context + provenance capture, prompt-sha identity, inline comments, golden freeze/replay), plus a retrofit assessment of a second app with mature automated evals. |

---

**Protocol Version:** 1.0
**Last Updated:** 2026-07-20
