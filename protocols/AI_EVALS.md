# AI Evals

> Automated regression evaluation for AI/LLM outputs. A golden set + a scored runner + an exit-code gate, so prompt/model/criteria changes can't silently degrade quality. Adopt, don't build.
>
> **Lifecycle:** extends the **Verify** phase for AI-powered projects — see [`DEVELOPMENT_LIFECYCLE.md`](DEVELOPMENT_LIFECYCLE.md) for how this fits with the other workflow protocols.

**Applies to:** Any AI-powered project that produces non-deterministic LLM output where quality matters (scoring, classification, extraction, ranking, generation). Tiered — minimum is one golden set + one `eval:*` command.
**Last Updated:** 2026-07-20
**Version:** 1.4

---

## Table of Contents

- [Overview](#overview)
- [When to use](#when-to-use)
- [The pattern](#the-pattern)
- [Operating model — how evals get triggered and surfaced](#operating-model--how-evals-get-triggered-and-surfaced)
- [Anti-patterns](#anti-patterns)
- [Resources](#resources)

---

## Overview

When you change a prompt, swap a model, or edit scoring criteria, how do you know you made it *better* and not *worse*? Without evals you don't — you eyeball a couple of cases and ship on vibes. That is exactly how a quality regression hides until a user finds it, and exactly how a team spins its wheels "fixing" an AI feature one symptom at a time.

> **Core principle:** Frontier-model robustness to phrasing makes evals *more* important, not less. The quality levers that remain — context, tools, retrieval, model choice — are precisely the ones you *cannot* eyeball. An eval is the only way to tell a real improvement from a plausible-looking regression.

This protocol is the lean version: a curated set of real examples, a runner that re-scores them and fails on regression, and a fast deterministic unit layer underneath. **Adopt existing tooling; do not build an eval framework.** The whole MVP is one golden set + one command.

### Key benefits

- **Every prompt/model change is measured**, not guessed.
- **Model migrations have a safety net** — re-run the eval before/after a version bump.
- **The audit itself finds bugs.** Building a golden set on a solo AI content app surfaced a pre-filter silently dropping 61% of inputs — invisible until the data was looked at.
- **It's a template, not a one-off** — the same shape copies across every AI app.

---

## When to use

| Scenario | Use this protocol? |
|----------|--------------------|
| High-volume / cron-path AI output whose quality matters and can drift silently (scoring, extraction, classification, ranking, digest) | **Yes** |
| A task you may later move to a cheaper/local model (SLM migration candidate) | **Yes — the eval is the side-by-side measuring stick that decision needs** |
| AI-powered project heading to production | **Yes — design it in from the start**, don't bolt on later |
| **Structure-only refactor** of an existing call (same prompt/model — e.g. swapping the output envelope to forced tool-use) | **No** — unit-test the pure parse helper + a spot-check; a golden set adds ~nothing (the change is behaviour-neutral by construction) |
| Low-volume, user-facing one-shot output (a single generation the user sees and judges immediately) | **No / lower priority** — failures are immediately visible; unit tests + manual check suffice |
| Deterministic code path (no LLM) | No — ordinary unit/integration tests |
| Throwaway script / prototype | No |

**Build an eval for the *task*, not for every change.** A golden set earns its keep when the output is high-volume or drift-prone (a model shifting under you, a prompt regression degrading at scale) — reserve it for those. Don't reflexively add one to every call site or every refactor; that's the over-verification the [`QA_PROTOCOL.md`](QA_PROTOCOL.md) tiering warns against. The eval-worthy tasks tend to map onto the SLM-migration candidates, because "is this drift-prone enough to guard" and "is this safe to move to a local model" are the same question answered by the same measuring stick.

Start with the **most eval-able output first**: deterministic-ish (low temperature), bounded (a number, a label, a short structured object), and backed by abundant real data. On a solo AI content app that was signal scoring (`temperature: 0`, `relevance 0–1 + reason`). Generation/chat is harder (subjective, multi-turn) — for owner-operated apps, capture the real human evaluator's verdicts first ([HUMAN_FEEDBACK_CAPTURE.md](HUMAN_FEEDBACK_CAPTURE.md)); reach for an LLM-judge only when volume outgrows the operator's eyes, calibrated against those verdicts. Inherently variable structured output (e.g. a digest's grouping + headlines) is eval-able too, but **validity-first** (absolute gates: schema-valid, length-bounded, grouping-respects-clusters) with a soft "agreement vs the prior anchor" signal — not an exact-match MAE.

---

## The pattern

Validated on a solo AI content app's signal-scoring eval harness (a shipped, archived spec).

**1. Golden set from production, regenerable.** A committed `evals/<target>/golden.json` of real inputs, stratified across outcome buckets (off / low / mid / high) and every relevant config (theme, persona, channel). Build it with a committed extractor script (`build-golden.ts`) so it can be regenerated as data evolves. ~50–100 cases is plenty for v1.

**2. Anchor honestly.** The cheapest v1 anchors each case to the *current production score* — that makes it a **regression/drift anchor** (catches change), not human ground truth (a quality bar). State which it is. Upgrade by hand-curating a ground-truth subset, especially boundary cases, later.

**3. Hit the real production path.** Extract a pure scoring function (prompt-build → model call → parse) with no DB/side-effects, and have the production code and the eval both call it. The eval must exercise the *exact* prompt/model/parse the app uses, or it measures fiction.

**4. Runner with a gate.** `evals/<target>/run.ts` replays the golden set, computes metrics (mean abs error vs anchor, within-tolerance rate, boundary-classification agreement, output-format validity), writes a timestamped **scorecard**, diffs against the previous PASS, and **exits non-zero on regression**. Update `latest.json` (the baseline) *only on PASS* so a failing run is always compared to the last known-good. Gates use tolerances, not exact equality — even `temperature: 0` varies slightly run-to-run.

**5. Fast deterministic unit layer.** The fragile pure logic (JSON extraction, clamping, junk detection) gets ordinary unit tests (`pnpm test`) — no API, no cost, runs on every change. Keep this separate from the live eval (`pnpm eval:*`), which costs money and is mildly non-deterministic.

```
evals/<target>/
  build-golden.ts   # regenerate the golden set from prod
  golden.json       # stratified real cases + anchors
  run.ts            # live eval: metrics + scorecard + regression gate
  parse.test.ts     # fast deterministic unit tests (pnpm test)
  scorecards/       # per-run logs; latest.json = last PASS (the baseline)
```

---

## Operating model — how evals get triggered and surfaced

A wired-up eval nobody runs is shelfware. Triggering and surfacing are part of the protocol, not an afterthought.

**Triggered three ways:**

- **Change-triggered (convention).** A rule in the project's `CLAUDE.md` / [QA_PROTOCOL.md](QA_PROTOCOL.md): *when an AI prompt, model, or scoring path changes, run the relevant `eval:*` and report the scorecard + diff in-thread, unprompted.* This is tier-Full verification for AI-output changes. The user never has to ask. (It's convention — reliable because it's in the rules Claude follows; harden with CI if a guarantee is needed.)
- **Time-triggered (drift).** A weekly scheduled run, regardless of code changes — catches the *model* shifting under you and data-distribution drift that code-triggered checks miss. Delivered via the weekly digest below.
- **Enforced (optional).** A CI job that runs the eval only on PRs touching AI files. Real enforcement; set the gate with tolerance (live calls, mild non-determinism) and budget for the API cost.

**Surfaced two ways:**

- **In-thread, proactively, by Claude** — whenever the eval runs after an AI change, the PASS/FAIL + moved metrics are reported in the working thread. Need-to-know, Claude-initiated.
- **Weekly Slack digest** — eval status + the observability summary (see [AI_OBSERVABILITY.md](AI_OBSERVABILITY.md)) pushed to the operator's DM. A push that gets read beats a dashboard that doesn't. Built per `AUDIT_ROUTINE_STANDARD.md` (silent-green, push-delivered) over `SLACK_OPS_NOTIFICATION.md`.

Cost is negligible — pick the cheapest capable model's path (Haiku-class) and a weekly run plus change-triggered runs is pennies.

---

## Anti-patterns

### Building an eval framework

```
❌ Bad — hand-rolling a bespoke eval/scoring harness and runner from scratch.
✅ Good — a golden JSON + a ~150-line runner + the project's existing test runner.
   Reach for Langfuse/Braintrust/Phoenix only when the lean version is outgrown.
```

### Calling the model's own past output "ground truth"

```
❌ Bad — anchoring to current production scores and implying the eval proves quality.
✅ Good — name it a regression/drift anchor. Curate a human ground-truth subset
   (boundary cases first) when you want an actual quality bar.
```

### A lenient absolute LLM-judge (the ceiling effect)

When you move from a golden-set regression anchor to an **absolute LLM-judge** (a model scores each output against a rubric, no reference answer — needed for generative/unbounded outputs), the naive version is near-useless: the judge rates almost everything top-marks with near-zero variance, so it cannot separate a strong output from a weak one.

```
❌ Bad — "score each dimension 0–5 against this rubric." A frontier judge returns
   4.9/5 for everything; the eval carries no signal.
✅ Good — force discrimination:
   • Critic-first: make the judge state the single biggest FLAW before it scores.
   • Strict anchoring: 3 = competent default; reserve the top score for "no flaw
     nameable"; tell it most outputs should land mid-scale.
   • Cross-model + cite-forcing: a DIFFERENT model judges, and must quote the text
     justifying each score (blunts circularity + ungrounded scores).
   • Tune CONCERN thresholds to the OBSERVED score distribution — an a-priori
     cutoff (e.g. "< 3.0") often never fires; run a baseline first, then set the
     cutoff at the real bottom tail.
```
Source: an AI signal-scoring pilot's (pharma domain) rubric-judge work — the naive rubric scored several hundred generated items at a ~4.9/5 mean (~zero spread); the four fixes above restored a usable 3.6–4.4 spread with sensible ordering.

### Gating on exact equality

```
❌ Bad — failing the eval when a score differs by 0.001 from last run.
✅ Good — tolerances (MAE delta, within-N rate, large-mover count). Even temp 0 drifts.
```

### Evals on every commit

```
❌ Bad — running the live (paid, non-deterministic) eval in the pre-commit hook.
✅ Good — fast deterministic unit tests on every change; the live eval on AI-path
   changes + weekly. Separate the two surfaces.
```

### Wired but never surfaced

```
❌ Bad — the eval exists and passes, but results never reach the operator.
✅ Good — change-triggered in-thread reporting + the weekly digest. Monitored and used.
```

---

## Resources

- [AI_OBSERVABILITY.md](AI_OBSERVABILITY.md) — the runtime companion; share the weekly digest
- [QA_PROTOCOL.md](QA_PROTOCOL.md) — evals are tier-Full verification for AI-output changes
- [HUMAN_FEEDBACK_CAPTURE.md](HUMAN_FEEDBACK_CAPTURE.md) — the human-in-the-loop companion: operator ratings with frozen context for subjective/generative output; supplies this protocol's ground-truth subset
- `SIGNAL_SCORING_ARCHITECTURE.md` — an example scorer this pattern was first built against
- `ANTHROPIC_MODEL_REFERENCE.md` — choosing the model for the eval path
- `AUDIT_ROUTINE_STANDARD.md` / `SLACK_OPS_NOTIFICATION.md` — the weekly digest delivery
- [PROJECT_INITIATION.md](PROJECT_INITIATION.md) — where the "this project needs evals" decision is made

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.4 | 2026-07-20 | Cross-linked [HUMAN_FEEDBACK_CAPTURE.md](HUMAN_FEEDBACK_CAPTURE.md) as the first move for subjective/generative output on owner-operated apps; LLM-judge repositioned as the volume-outgrows-operator escalation. |
| 1.3 | 2026-07-05 | Updated the validation link to the archived shipped spec path and repaired stale footer metadata. |
| 1.2 | 2026-06-12 | Added the "build an eval for the task, not every change" heuristic: structure-only refactors get unit tests + spot-checks; golden sets are reserved for high-volume, drift-prone, or SLM-candidate tasks; inherently variable structured output uses validity-first gates. |
| 1.1 | 2026-06-08 | Added the "lenient absolute LLM-judge (ceiling effect)" anti-pattern + its four fixes (critic-first, strict anchoring, cross-model cite-forcing, distribution-tuned thresholds), from a rubric-judge pilot in the pharma domain. |
| 1.0 | 2026-06-06 | Initial release. Extracted from a solo AI content app's eval pilot: golden-set-from-prod, pure-path extraction, regression-anchor scorecard + gate, deterministic unit layer, convention + weekly operating model. |

---

**Protocol Version:** 1.4
**Last Updated:** 2026-07-20
