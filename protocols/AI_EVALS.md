# AI Evals

> Measuring AI/LLM output so prompt, model and criteria changes are decided on evidence, not vibes. Two regimes: a **golden set + scored runner + exit-code gate** for bounded, high-volume output, and **blind, approval-gated comparisons** for subjective generation. Both rest on production-faithful harnesses, receipts that make re-scoring free, honest statistics and explicit spend control. Build thin scripts, not a framework.
>
> **Lifecycle:** extends the **Verify** phase for AI-powered projects — see [`DEVELOPMENT_LIFECYCLE.md`](DEVELOPMENT_LIFECYCLE.md) for how this fits with the other workflow protocols.

**Applies to:** Any AI-powered project whose non-deterministic LLM output matters (scoring, classification, extraction, ranking, generation). Tiered — minimum is one golden set + one `eval:*` command; comparative evals are added when a generation path's prompt, model or effort is deliberately changed.
**Last Updated:** 2026-09-27
**Version:** 2.0

---

## Table of Contents

- [Overview](#overview)
- [When to use](#when-to-use)
- [Regime 1 — Regression evals for bounded output](#regime-1--regression-evals-for-bounded-output)
- [Regime 2 — Comparative evals for subjective generation](#regime-2--comparative-evals-for-subjective-generation)
- [Shared foundations](#shared-foundations)
- [Operating model — how evals get triggered and surfaced](#operating-model--how-evals-get-triggered-and-surfaced)
- [Anti-patterns](#anti-patterns)
- [Resources](#resources)

---

## Overview

When you change a prompt, swap a model, or edit scoring criteria, how do you know you made it *better* and not *worse*? Without evals you don't — you eyeball a couple of cases and ship on vibes. That is exactly how a quality regression hides until a user finds it, and exactly how a team spins its wheels "fixing" an AI feature one symptom at a time.

> **Core principle:** Frontier-model robustness to phrasing makes evals *more* important, not less. The quality levers that remain — context, tools, retrieval, model choice — are precisely the ones you *cannot* eyeball. An eval is the only way to tell a real improvement from a plausible-looking regression.

The two regimes answer different questions:

- **Regime 1 — "did this change make it worse?"** Bounded output (a score, a label, a short structured object) gets a curated set of real cases, a runner that re-scores them and fails on regression, and a fast deterministic unit layer underneath. It runs itself: after every relevant change and weekly.
- **Regime 2 — "is the candidate better than what we ship?"** Subjective output (a post, an article, a reply) has no anchor to regress against, and an unvalidated LLM judge adds little signal. The unit is a controlled comparison — candidate vs incumbent, judged blind by the person whose judgment defines quality — run only when a change is proposed, with the spend approved up front.

**Don't build an eval framework.** Build thin scripts per target or experiment over a small shared kit (a review-page builder, a spend meter, a cost forecaster) and the project's existing test runner. Reach for Langfuse/Braintrust/Phoenix only when that is outgrown.

### Key benefits

- **Every prompt/model change is measured**, not guessed.
- **Model switches become recorded decisions** — evidence, known gaps and a one-line rollback, not a hunch.
- **The audit itself finds bugs.** Building the first golden set on a solo AI content app surfaced a pre-filter silently dropping 61% of inputs — invisible until the data was looked at.
- **It's a template, not a one-off** — the same shapes copy across every AI app.

---

## When to use

| Scenario | Use this protocol? |
|----------|--------------------|
| High-volume / cron-path AI output whose quality matters and can drift silently (scoring, extraction, classification, ranking, digest) | **Yes — Regime 1** |
| A task you may later move to a cheaper/local model (SLM migration candidate) | **Yes — Regime 1 is the side-by-side measuring stick that decision needs** |
| A deliberate change to a subjective generation path (prompt, role contract, model, effort) | **Yes — a Regime 2 comparison before it ships.** Not a standing golden set |
| Choosing between models or providers for a generation task (a bake-off) | **Yes — Regime 2**, with arms that differ only in the model id |
| AI-powered project heading to production | **Yes — design it in from the start**, don't bolt on later. Store generation receipts from day one (see [Shared foundations](#receipts-make-re-scoring-free)) |
| **Structure-only refactor** of an existing call (same prompt/model — e.g. swapping the output envelope to forced tool-use) | **No** — unit-test the pure parse helper + a spot-check; a golden set adds ~nothing (the change is behaviour-neutral by construction) |
| **Moving prompts from a hosted store into code** (same text, same settings — e.g. off OpenAI stored prompt objects before the 2026-11-30 `v1/prompts` shutdown) | **No** — the gate is a golden *payload* fixture: a unit test that snapshots the exact provider request per prompt, so the migration is byte-faithful and every later prompt edit surfaces as a reviewable diff (pattern proven in an owner-operated app: a shared prompt-request fixture test). A golden set measures output quality, which this change does not touch |
| Everyday generated output the operator already reads and judges | **No standing eval** — capture the operator's verdicts ([HUMAN_FEEDBACK_CAPTURE.md](HUMAN_FEEDBACK_CAPTURE.md)); receipts make later instruments free |
| Deterministic code path (no LLM) | No — ordinary unit/integration tests |
| Throwaway script / prototype | No |

**Build an eval for the task, not for every change.** A golden set earns its keep when the output is high-volume or drift-prone (a model shifting under you, a prompt regression degrading at scale) — reserve it for those. Don't reflexively add one to every call site or every refactor; that's the over-verification the [`QA_PROTOCOL.md`](QA_PROTOCOL.md) tiering warns against. The eval-worthy tasks tend to map onto the SLM-migration candidates, because "is this drift-prone enough to guard" and "is this safe to move to a local model" are the same question answered by the same measuring stick.

Start with the **most eval-able output first**: deterministic-ish (low temperature), bounded (a number, a label, a short structured object), and backed by abundant real data. On a solo AI content app that was signal scoring (`temperature: 0`, `relevance 0–1 + reason`). Inherently variable structured output (e.g. a digest's grouping + headlines) is eval-able too, but **validity-first** (absolute gates: schema-valid, length-bounded, grouping-respects-clusters) with a soft "agreement vs the prior anchor" signal — not an exact-match MAE. Generation is Regime 2: capture the owner's verdicts first, compare candidates blind when a change is proposed, and reach for an LLM judge only once it has been validated against those verdicts.

---

## Regime 1 — Regression evals for bounded output

Validated on a solo AI content app's regression evals: signal scoring, enrichment, digest and source search.

**1. Golden set from production, regenerable.** A committed `evals/<target>/golden.json` of real inputs, stratified across outcome buckets (off / low / mid / high) and every relevant config (theme, persona, channel). Build it with a committed extractor script (`build-golden.ts`) so it can be regenerated as data evolves. ~50–100 cases is plenty for v1. Add a few synthetic cases for failure shapes production rarely shows (navigation junk, paywalls, error pages).

**2. Anchor honestly.** The cheapest v1 anchors each case to the *current production score* — that makes it a **regression/drift anchor** (catches change), not human ground truth (a quality bar). State which it is. Upgrade by hand-curating a ground-truth subset, especially boundary cases, later. A deliberate prompt or model change is a **baseline reset**, not a regression to chase with a looser gate.

**3. Hit the real production path and configuration.** Extract a pure function (prompt-build → model call → parse) with no DB/side-effects, and have the production code and the eval both call it. Import the production model/provider constants rather than restating them, and fail loudly if the harness would run a different provider. A harness that defaults to a retired model or "the engine default" measures fiction as surely as a copied prompt — One app found three of its draft harnesses doing exactly that after a model switch.

**4. Runner with a gate and a noise floor.** `evals/<target>/run.ts` replays the golden set, computes metrics (mean abs error vs anchor, within-tolerance rate, boundary-classification agreement, output-format validity), writes a timestamped **scorecard**, diffs against the previous PASS, and **exits non-zero on regression**. Update `latest.json` (the baseline) *only on PASS* so a failing run is always compared to the last known-good. Gates use tolerances, not exact equality — even `temperature: 0` varies run-to-run — and thresholds are set from the observed baseline, never a priori. Run repeats (3 is a practical default), report the run-to-run spread, and label any delta inside it **WITHIN NOISE** rather than as a finding.

**5. Fast deterministic unit layer.** The fragile pure logic (JSON extraction, clamping, junk detection) and the eval's own instruments get ordinary unit tests (`pnpm test`) — no API, no cost, runs on every change. Pin live specimens of instrument behaviour here (a real output a detector must flag, one it must pass), so the instrument itself is regression-tested in CI. Keep this separate from the live eval (`pnpm eval:*`), which costs money and is mildly non-deterministic.

```
evals/<target>/
  build-golden.ts   # regenerate the golden set from prod
  golden.json       # stratified real cases + anchors
  run.ts            # live eval: metrics + scorecard + regression gate
  parse.test.ts     # fast deterministic unit tests (pnpm test)
  scorecards/       # per-run logs; latest.json = last PASS (the baseline)
  README.md         # method, gates, and the current baseline numbers
```

Scorecards can stay local (gitignored), but then **write the baseline numbers into the README** so the baseline survives a new machine — and never let a CI test read a local scorecard.

---

## Regime 2 — Comparative evals for subjective generation

Validated on a solo AI content app's post writer (Aug–Sep 2026): prompt, effort, reader-context and provider comparisons, a factorial design, and a three-arm model bake-off that moved production to a new writer model.

**1. Ask one question.** Change one factor and hold everything else fixed — including evidence: replay frozen source material so only the prompt or model varies. Add a control arm (incumbent vs itself, or a no-change arm) when the expected effect is small. Use a factorial design when two factors may interact, and state its limit (one draw per cell cannot establish broad superiority). Choose fresh inputs stratified across every role or mode the change touches (≥2 per mode), checked absent from earlier corpora.

**2. Freeze and preflight, for free.** Materialise the whole run as a manifest with a SHA. A free preflight proves the arms differ only in the intended factor — byte-compare the system prompt, user prompt, schema, output limit and effort — and that no case text or reference leaks into prompts. Forecast cost from calibrated historical token ratios (at least two matched prior calls per role) and report the likely spend separately from the worst-case cap.

**3. Approve, then run.** The owner approves the exact manifest and a dollar cap; the runner refuses without both (e.g. `--confirm-approved-cap-usd 12 <manifestSha>`). Inside the run:

- no SDK retries; write the spend ledger before dispatch and the raw response before parsing;
- a call of unknown cost reserves its full allowance and stops the batch;
- refuse to overwrite an existing ledger, output or review page; resume only the unfinished suffix;
- a refusal or failure is an **outcome**, not something to retry or repair away — and withhold that case's whole set from review, so the gap cannot reveal which arm failed.

**4. Review blind.** Neutral IDs, positions balanced with a Latin square, and the decoding key kept outside the artifact. One self-contained review page (no service, no account): an ordinal verdict per output (e.g. Publishable / Light edits / Substantial rewrite / Reject), inline comments anchored to exact text, and pairwise preference and set ranking as **separate** controls. Strip model, cost and timing from blind pages. Never regenerate a page while the owner is reviewing it. A single static HTML file built from a JSON corpus is enough.

**5. Freeze, then decode.** Hash the owner's export before opening the key; reconcile by body hash and quote offsets. Report ordinal counts, preferences and ranks — **never average ordinal verdicts**. State the limits every time: generations per arm, number of reviewers, roles or modes covered.

**6. Decide and record.** Mixed or close results **hold** the candidate. Promotion is the owner's call, recorded in the decisions log with the evidence, the known gaps (e.g. modes the comparison did not cover) and a one-line rollback kept in code. A round whose outputs share a defect across arms points at the prompt, not the model: fix it and re-run rather than spend the owner's review on it (one bake-off discarded two such rounds, about $1 each, before the reviewed third).

**7. An assistant first pass, if marking is the bottleneck.** An assistant may review first, but its verdicts are frozen before decoding and calibrated against a set of owner verdicts. Report agreement only from calls made before seeing the answers — explanations written afterwards are not calibration. Keep owner spot checks.

**8. Guard generalisation.** Keep sealed holdouts that are never used to tune wording. Before a candidate reaches production, audit it for topic leakage (no case keywords or exemplars in the prompt) and for numeric bands fitted to a single accepted example, then confirm it on at least two untuned topics with different needs. One or two wins are "limited transfer evidence", and should be reported as such.

Between comparisons, the standing signal is the owner's routine verdicts and reviewed edits ([HUMAN_FEEDBACK_CAPTURE.md](HUMAN_FEEDBACK_CAPTURE.md)); reviewed improvements promoted into an immutable eval corpus become the human-gold cases future comparisons draw on.

---

## Shared foundations

### Receipts make re-scoring free

Store an immutable receipt for every production generation: the exact model input, the output, a prompt hash, the contract or manifest version, the deploy SHA and the trace id ([HUMAN_FEEDBACK_CAPTURE.md](HUMAN_FEEDBACK_CAPTURE.md) primitives 1–2). Deterministic instruments — pure functions over input and output — can then re-score the entire history at **zero model spend**: an instrument change gets a free before/after, and a prompt change gets a free "before". For paid baselines, save the outputs and support `--rescore`, so a scorer defect found later never buys a second run. In practice: a read-only fidelity diagnostic that re-scores every stored option, required before and after any writer-prompt change.

### Instrument honesty

- **Calibrate before trusting.** Score a detector against labelled positives and negatives (e.g. AUC per parameter setting) and pin live specimens as unit tests.
- **Negative-test it.** Force the check to fail on a known-bad input before trusting its pass; regenerate derived artifacts after a mutation run.
- **Count independent units.** Nine points measured repeatedly are nine observations, not 555 trials.
- **Beware in-sample circularity.** A threshold fitted to the same cases guarantees a clean tally ("0 of 15 dropped"); report the distribution instead.
- **Whole-output judgment outranks a phrase detector.** When a surface metric and the owner's blind read disagree, the metric is measuring the wrong thing — in one app, hand-picked style metrics showed nothing where the owner's blind read split 7–1. A metric that improves while the prose does not is the same failure.

### Noise and sample size

- **Measure the noise floor before claiming an effect** — repeats, or a control arm. In one app, identical runs swung ±0.15 on the very metric being optimised, and a no-change arm exposed a 24.7% noise floor.
- **Budget replicates to the effect size** — about four per condition per seed for small effects — or don't run it.
- **Don't design from n=1.** Say "limited evidence" when that is what one or two wins are.
- **Separate content gains from length gains.** Length confounds most quality judgments; hold it fixed or measure it separately.

### LLM judges

- **Pairwise over pointwise** for subjective criteria; judge **both orders** and exclude pairs whose two verdicts disagree rather than coin-flipping them.
- **Validate before use.** The headline number is agreement with the owner's blind calls on the same pairs, not the judge's opinion of the outputs. A judge at chance per pair may still show aggregate direction, but it is not a per-pair proxy for the owner. (In one validation, a Sonnet judge was position-inconsistent on 8 of 9 pairs and was disqualified; an Opus judge's apparent 5/5 fell to 5/8 — chance — once given a channel-matched reference.)
- **Keep references leak-free** — nothing that is itself a candidate elsewhere.
- **Absolute rubric judges need forced discrimination** — see the ceiling-effect anti-pattern below.

### Independence

A judge or check that production uses to select or revise outputs is a **guardrail**, not independent evidence: the output was optimised against it, so a later score from the same rubric is correlated. Label guardrail metrics separately from eval metrics; base quality claims on a blinded human-gold holdout refreshed over time; and check factual claims against frozen source extracts rather than the summary the model consumed. Deterministic format and provenance checks stay valid as independent checks of the narrow property they test.

### Spend control

Regression evals on a Haiku-class path cost pennies; generation comparisons cost dollars per round. So:

- every paid command needs an explicit confirm flag (`--confirm-provider-spend`), and expensive variants (full set, repeats, holdouts) need their own;
- print the call ceiling before spending; meter at the fetch boundary with phase attribution (planner, writer, repair); exclude and flag unknown prices rather than counting them as zero; failed runs still write their usage;
- compare actual spend against the forecast afterwards, so the forecaster stays calibrated;
- checkpoint and resume, so an interrupted run never pays twice;
- update the savepoint or backlog when a lane closes — a stale "next step" line can re-buy a run already on disk.

---

## Operating model — how evals get triggered and surfaced

A wired-up eval nobody runs is shelfware. Triggering and surfacing are part of the protocol, not an afterthought.

**Triggered four ways:**

- **Change-triggered (convention).** A rule in the project's `CLAUDE.md` / [QA_PROTOCOL.md](QA_PROTOCOL.md): *when an AI prompt, model, or scoring path changes, run the relevant `eval:*` and any free instruments and report the scorecard + diff in-thread, unprompted.* This is tier-Full verification for AI-output changes. The user never has to ask. (It's convention — reliable because it's in the rules Claude follows; harden with CI if a guarantee is needed.)
- **Approval-gated (Regime 2).** Paid comparisons run only after the owner approves the manifest and cap. They report as a dated markdown report (status, verdict table, spend against forecast, limits) beside the permanent review page.
- **Time-triggered (drift).** A weekly scheduled run of the cheapest drift-prone regression eval, regardless of code changes — catches the *model* shifting under you and data-distribution drift that code-triggered checks miss. Delivered via the weekly digest below.
- **Enforced (optional).** A CI job that runs the eval only on PRs touching AI files. Real enforcement; set the gate with tolerance (live calls, mild non-determinism) and budget for the API cost.

**Surfaced two ways:**

- **In-thread, proactively, by Claude** — whenever an eval runs after an AI change, the PASS/FAIL + moved metrics are reported in the working thread. Need-to-know, Claude-initiated.
- **Weekly digest** — eval status, the observability summary (see [AI_OBSERVABILITY.md](AI_OBSERVABILITY.md)) and production quality signals such as refusal/fallback rate by model, pushed to the operator's DM. Open the message with "ran <date> · next <date>" so a missing message is itself the alert. A push that gets read beats a dashboard that doesn't. Built per `AUDIT_ROUTINE_STANDARD.md` (silent-green, push-delivered) over `SLACK_OPS_NOTIFICATION.md`.

---

## Anti-patterns

### Building an eval framework

```
❌ Bad — hand-rolling a bespoke eval platform: plugin registry, dashboard, DSL.
✅ Good — a golden JSON + a ~150-line runner per target; thin scripts per comparison
   over a small shared kit (review page, spend meter, forecaster). Reach for
   Langfuse/Braintrust/Phoenix only when that is outgrown.
```

### Calling the model's own past output "ground truth"

```
❌ Bad — anchoring to current production scores and implying the eval proves quality.
✅ Good — name it a regression/drift anchor. Curate a human ground-truth subset
   (boundary cases first) when you want an actual quality bar.
```

### A harness that drifted from production

```
❌ Bad — the eval hardcodes a model id, or omits it and tests the engine default,
   and nobody notices when production switches models.
✅ Good — import the production constants; refuse to run on a different provider;
   name any deliberate deviation (a frozen bake-off arm) in the harness itself.
```

### A lenient absolute LLM-judge (the ceiling effect)

When you move from a golden-set regression anchor to an **absolute LLM-judge** (a model scores each output against a rubric, no reference answer), the naive version is near-useless: the judge rates almost everything top-marks with near-zero variance, so it cannot separate a strong output from a weak one.

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

### An unvalidated judge standing in for the owner

```
❌ Bad — "the judge preferred B in 7 of 9 pairs", with no check that it agrees
   with the human it replaces.
✅ Good — judge both orders, drop self-inconsistent pairs, and report agreement
   with the owner's blind calls first. At chance per pair → aggregate direction only.
```

### Grading your own guardrail

```
❌ Bad — production revises drafts until a judge passes them, then the eval cites
   that judge's scores as evidence the drafts improved.
✅ Good — label it a guardrail metric; claim quality from a blinded human-gold
   holdout and from checks production never optimised against.
```

### Reporting an effect inside the noise

```
❌ Bad — one paid run per condition, a 0.1 delta, "the new prompt reduces copying".
✅ Good — measure run-to-run spread (repeats or a control arm) first; label deltas
   inside it WITHIN NOISE; replicate to the effect size or don't run it.
```

### Unblinding before the verdicts are frozen

```
❌ Bad — opening the key while the owner's review is still editable, or averaging
   "Publishable = 4, Light edits = 3" into a mean score.
✅ Good — hash the export, then decode; report ordinal counts, preferences and
   ranks separately.
```

### Tuning on the holdout

```
❌ Bad — rewording the prompt until the sealed cases pass, or shipping a length
   band fitted to the one rewrite the owner accepted.
✅ Good — holdouts are run, never tuned against; audit candidates for topic leakage
   and fitted bands; confirm on untuned topics before calling a change general.
```

### Paying twice for a scorer bug

```
❌ Bad — a paid baseline whose outputs were scored in-flight and not kept; the
   scorer turns out wrong and the run is bought again.
✅ Good — keep outputs and receipts; `--rescore` and receipt replays re-grade for free.
```

### Gating on exact equality

```
❌ Bad — failing the eval when a score differs by 0.001 from last run.
✅ Good — tolerances (MAE delta, within-N rate, large-mover count). Even temp 0 drifts.
```

### Evals on every commit

```
❌ Bad — running the live (paid, non-deterministic) eval in the pre-commit hook.
✅ Good — fast deterministic unit tests on every change; the live eval on AI-path
   changes + weekly; paid comparisons only when approved. Separate the surfaces.
```

### Wired but never surfaced

```
❌ Bad — the eval exists and passes, but results never reach the operator.
✅ Good — change-triggered in-thread reporting + the weekly digest. Monitored and used.
```

---

## Resources

- [AI_OBSERVABILITY.md](AI_OBSERVABILITY.md) — the runtime companion; share the weekly digest
- [HUMAN_FEEDBACK_CAPTURE.md](HUMAN_FEEDBACK_CAPTURE.md) — the human-in-the-loop companion: generation receipts, operator verdicts and reviewed improvements; supplies the human-gold cases both regimes lean on
- [QA_PROTOCOL.md](QA_PROTOCOL.md) — evals are tier-Full verification for AI-output changes
- `SIGNAL_SCORING_ARCHITECTURE.md` — an example scorer Regime 1 was first built against
- `ANTHROPIC_MODEL_REFERENCE.md` — choosing the model for the eval path and the arms of a bake-off
- `AUDIT_ROUTINE_STANDARD.md` / `SLACK_OPS_NOTIFICATION.md` — the weekly digest delivery
- [PROJECT_INITIATION.md](PROJECT_INITIATION.md) — where the "this project needs evals" decision is made

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 2.0 | 2026-09-27 | Restructured around two regimes. Regime 1 (bounded output) keeps the golden-set pattern and adds production-config imports, noise floors, baseline resets and README-recorded baselines. New Regime 2 (subjective generation): one-factor comparisons with frozen evidence, free preflight and cost forecast, owner-approved manifest + cap, safe run mechanics, blind review, freeze-then-decode, hold-or-promote with a recorded rollback, calibrated assistant first pass, generalisation guards. New shared foundations: generation receipts for zero-spend re-scoring, instrument honesty, noise and sample size, validated pairwise judges, guardrail independence, spend control. Operating model adds approval-gated runs and digest production signals. Seven new anti-patterns. Fixed the header, which still read 1.4. From a solo AI content app's Aug–Sep 2026 post-writer evaluations. |
| 1.5 | 2026-09-04 | Added the hosted-prompt-to-code migration row: the gate is a golden payload fixture test (request faithfulness), not a golden set (output quality). |
| 1.4 | 2026-07-20 | Cross-linked [HUMAN_FEEDBACK_CAPTURE.md](HUMAN_FEEDBACK_CAPTURE.md) as the first move for subjective/generative output on owner-operated apps; LLM-judge repositioned as the volume-outgrows-operator escalation. |
| 1.3 | 2026-07-05 | Updated the validation link to the archived shipped spec path and repaired stale footer metadata. |
| 1.2 | 2026-06-12 | Added the "build an eval for the task, not every change" heuristic: structure-only refactors get unit tests + spot-checks; golden sets are reserved for high-volume, drift-prone, or SLM-candidate tasks; inherently variable structured output uses validity-first gates. |
| 1.1 | 2026-06-08 | Added the "lenient absolute LLM-judge (ceiling effect)" anti-pattern + its four fixes (critic-first, strict anchoring, cross-model cite-forcing, distribution-tuned thresholds), from a rubric-judge pilot in the pharma domain. |
| 1.0 | 2026-06-06 | Initial release. Extracted from a solo AI content app's eval pilot: golden-set-from-prod, pure-path extraction, regression-anchor scorecard + gate, deterministic unit layer, convention + weekly operating model. |

---

**Protocol Version:** 2.0
**Last Updated:** 2026-09-27
