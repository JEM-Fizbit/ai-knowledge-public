# Development Lifecycle

> A map of how the workflow protocols fit together across a project's life — conceive → scaffold → track → execute → verify → resume. This is a **navigational overview**, not a rulebook: each phase links to the protocol that owns the detail. Read the phase you're in and follow the link.
>
> **Note:** this is a partial public mirror of a larger private protocol library. Cross-references shown as plain `code` (not links) point to protocols that aren't included in this mirror.

**Applies to:** Any project (code or research/writing). Useful to both people orienting to the protocol library and agents deciding which lifecycle protocol governs the work in front of them.
**Last Updated:** 2026-07-07
**Version:** 1.0

---

## Table of Contents

- [Overview](#overview)
- [The lifecycle at a glance](#the-lifecycle-at-a-glance)
- [The six-phase spine](#the-six-phase-spine)
- [AI-feature quality band (conditional)](#ai-feature-quality-band-conditional)
- [Cross-cutting protocols](#cross-cutting-protocols)
- [Entry router — "you are here → read this"](#entry-router--you-are-here--read-this)
- [Design throughline: proportional ceremony](#design-throughline-proportional-ceremony)
- [Anti-patterns](#anti-patterns)
- [Resources](#resources)

---

## Overview

The workflow protocols in this repo aren't a flat list — they form a lifecycle. A project moves from *deciding what it is* through *shipping and running it*, and a different protocol governs each step. This document is the map that shows where each one sits and how they hand off.

It exists because both people and agents routinely join a project **mid-lifecycle** — an agent lands in a repo that already has a backlog, or is asked to fix a bug, or to ship a change — and needs to know which protocol applies *right now* without reading the whole library. The [entry router](#entry-router--you-are-here--read-this) answers exactly that.

> **This is a map, not the territory.** Each phase below is one paragraph and a link. The linked protocol is **canonical** — it owns the tiers, templates, commands, and edge cases. If this map and a linked protocol ever disagree, the linked protocol wins; fix the map. Nothing here is duplicated from the spine docs by design (per the source repo's no-duplication rule).

---

## The lifecycle at a glance

```
  CONCEIVE          SCAFFOLD          TRACK / PLAN            EXECUTE              VERIFY             RESUME
 ──────────        ──────────        ──────────────         ─────────           ────────           ────────
 PROJECT_          PROJECT_          ROADMAP_AND_           design +            QA_                SESSION_
 INITIATION   →    INIT         →    BACKLOG          →     coding      →       PROTOCOL      →    HANDOFF_
 "what is it?"     "wire the         capture→spec→ship      discipline          Skip/Quick/        SAVE_POINTS
                    repo"            (living loop)                               Full + Hard gate   (multi-session)
                                          │                                          │
                                          └──────────── iterate loop ────────────────┘
                                          playtest → capture → sprint → implement → ship

 ── cross-cutting (every phase) ───────────────────────────────────────────────────────────────────────────
 Git · Dependency Hygiene · Model/Effort Selection · Instruction Layers · Agent-Swarm Research · Docs Audit

 ── AI-feature projects only ──────────────────────────────────────────────────────────────────────────────
 (Verify) AI_EVALS — pre-ship regression gate      →      (Operate, post-ship) AI_OBSERVABILITY — runtime
```

---

## The six-phase spine

### 1. Conceive — [`PROJECT_INITIATION.md`](PROJECT_INITIATION.md)
Translate a vision + rough requirements into an initial spec (and optionally a seed roadmap). Interview-led, tiered **None / Light / Full** — default lighter than you think. Answers *"what are we building?"* For a Cowork research/strategy/writing workspace rather than a code repo, use `COWORK_PROJECT_INIT.md` instead. **Hands off to:** Scaffold.

### 2. Scaffold — [`PROJECT_INIT.md`](PROJECT_INIT.md)
Wire up the repo: `.gitignore`, `.env.example`, `CLAUDE.md`, README, exact local protocol triggers, and registrations (assets register, docs-audit trigger). Answers *"now set up the repo."* **Hands off to:** Track/Plan, once the first spec lands.

### 3. Track & Plan — [`ROADMAP_AND_BACKLOG.md`](ROADMAP_AND_BACKLOG.md)
The ongoing work engine. Four stacked layers by signal density: `BACKLOG.md` (one-line capture) → `docs/specs/NNN-slug.md` (a work brief drafted **only on promotion, only when the work earns one** — most changes ship with no spec) → optional strategic roadmap → optional audit docs + sprint plans. Operating rhythm: `roadmap → playtest → capture → (audit) → sprint → implement → iterate`. **Feeds:** Execute; **loops with:** Verify.

### 4. Execute — [`SOLUTION_DESIGN_PRINCIPLES.md`](SOLUTION_DESIGN_PRINCIPLES.md) + [`BEST_PRACTICES_FIRST.md`](BEST_PRACTICES_FIRST.md)
How code actually gets written. `SOLUTION_DESIGN_PRINCIPLES` governs the design call — root-cause over symptom, parameterization, abstraction thresholds, anti-patterns, and the "just patch / MVP / spike" override triggers. `BEST_PRACTICES_FIRST` is the escalation rule: **the third commit on the same issue ⇒ STOP, find the pattern, propose architecture.** For a load-bearing architecture/methodology decision, run a research pass first via `AGENT_SWARM_RESEARCH.md`. **Hands off to:** Verify.

### 5. Verify — [`QA_PROTOCOL.md`](QA_PROTOCOL.md)
Verification is always required before shipping; the *depth* is matched to the change. Tiers **Skip / Quick / Full**, plus an orthogonal **Hard gate** for irreversible or externally-facing operations that fires regardless of change size. Ties back to the spec via the **`Verification:` citation line** — one sentence naming which tier ran. For AI-feature projects, evals extend this phase (see below). **Hands off to:** ship → back into the Track/Plan iterate loop, or Resume.

### 6. Resume — [`SESSION_HANDOFF_SAVE_POINTS.md`](SESSION_HANDOFF_SAVE_POINTS.md)
Not a phase so much as a continuity mechanism for multi-session work. A dated in-repo save-point doc (state, measured blockers, stepwise next task, invariants, how-to-run) so a fresh session resumes cold without re-deriving context. Invoke when ending a session mid-effort or recommending a fresh one.

---

## AI-feature quality band (conditional)

**Applies only to projects with LLM calls** — skip entirely otherwise. These two fill a gap the generic spine doesn't cover: quality assurance for non-deterministic output, and the post-ship *operate* dimension that lives beyond Verify and Resume.

- **[`AI_EVALS.md`](AI_EVALS.md) — extends Verify (pre-ship + scheduled).** A golden-set regression gate answering *"did my prompt/model/scoring change make the output worse?"* Golden set from prod + scored runner + exit-code gate. Sits alongside `QA_PROTOCOL` for the AI-output surface that a build/lint/test can't judge.
- **[`AI_OBSERVABILITY.md`](AI_OBSERVABILITY.md) — the Operate phase (post-ship, runtime).** Latency, cost, success/failure, `traceId` correlation, weekly digest. In-stack capture (no migration). This is where a shipped-and-running AI feature is watched — the spine's six phases stop at dev continuity, not production operation.

Together: evals catch regressions *before* the change ships; observability catches drift and cost/latency problems *after* it's live.

---

## Cross-cutting protocols

These apply at (nearly) every phase rather than owning one. Names not included in this mirror are shown as plain text:

| Protocol | Role across the lifecycle |
|---|---|
| `GIT_CONVENTIONS.md` | Commits, branches, PRs — the connective tissue of every phase. |
| `DEPENDENCY_HYGIENE.md` | Version / package-manager / runtime-pin decisions, mostly at Scaffold and Execute. |
| `MODEL_EFFORT_SELECTION.md` | Which Claude model + effort tier fits the work; surfaced at phase transitions. |
| `CLAUDE_INSTRUCTION_LAYERS.md` | Governs the `CLAUDE.md` / `AGENTS.md` / `NOW.md` / `BACKLOG.md` docs the spine relies on — consult before drafting or editing any of them. |
| `AGENT_SWARM_RESEARCH.md` | Research-first grounding before a load-bearing design/methodology decision (Execute). |
| `FILE_NAMING_AND_VERSIONING.md` | Naming/versioning any new file or rename — filenames are permanent identifiers. |
| `SCHEDULED_DOCS_AUDIT.md` + `AUDIT_ROUTINE_STANDARD.md` | Keep project docs (and these protocols) from drifting — monthly automated audit. |
| `MAINTENANCE.md` | The meta-lifecycle: how the protocols *themselves* are created, synced, and audited. |

---

## Entry router — "you are here → read this"

Match your situation to the row; open the protocol it points to.

| Situation | Read this |
|---|---|
| Empty / near-empty repo; the project isn't scoped yet | [`PROJECT_INITIATION.md`](PROJECT_INITIATION.md) |
| "I have an idea for X" / "let's plan a new project" | [`PROJECT_INITIATION.md`](PROJECT_INITIATION.md) |
| Setting up a Cowork research/strategy/writing workspace | `COWORK_PROJECT_INIT.md` |
| Scoped; now need the repo wired up | [`PROJECT_INIT.md`](PROJECT_INIT.md) |
| Capturing / retrieving / promoting / shipping open work (project has `BACKLOG.md`) | [`ROADMAP_AND_BACKLOG.md`](ROADMAP_AND_BACKLOG.md) |
| Writing or architecting code | [`SOLUTION_DESIGN_PRINCIPLES.md`](SOLUTION_DESIGN_PRINCIPLES.md) |
| Third commit on the same issue and still patching | [`BEST_PRACTICES_FIRST.md`](BEST_PRACTICES_FIRST.md) |
| Load-bearing architecture/methodology decision to make | `AGENT_SWARM_RESEARCH.md` |
| About to commit / push / PR / "this is ready" | [`QA_PROTOCOL.md`](QA_PROTOCOL.md) |
| Changed a prompt/model and need to know it didn't regress | [`AI_EVALS.md`](AI_EVALS.md) |
| AI feature is shipped and running — watching cost/latency/errors | [`AI_OBSERVABILITY.md`](AI_OBSERVABILITY.md) |
| Ending a session mid-effort / resuming cold | [`SESSION_HANDOFF_SAVE_POINTS.md`](SESSION_HANDOFF_SAVE_POINTS.md) |
| Editing a `CLAUDE.md` / `AGENTS.md` / instructions field | `CLAUDE_INSTRUCTION_LAYERS.md` |
| Authoring or editing a protocol in this repo | `MAINTENANCE.md` + `AGENTS.md` |

For anything outside the workflow lifecycle (API integrations, MCP servers, Slack ops, house style, document deliverables), this mirror doesn't include the full trigger index — see the six spine protocols and cross-cutting table above for what's here.

---

## Design throughline: proportional ceremony

Every spine protocol shares one principle: **ceremony scales with complexity and stakes, not with frequency.** The tiers are the same idea wearing different names —

- Conceive: **None / Light / Full** initiation intensity.
- Track/Plan: four opt-in layers; a spec exists **only when the work earns one**.
- Verify: **Skip / Quick / Full** depth, plus a non-bypassable **Hard gate** for irreversible/external ops.

The default everywhere is **lighter than you think**. A throwaway script gets a README, not a spec; a typo fix gets a Skip, not a full build. Under-ceremony on a change that turns out to matter is recoverable; over-ceremony on every change is the failure mode that makes the whole system get abandoned. When genuinely unsure, escalate exactly one tier.

---

## Anti-patterns

- **Manufacturing initiation ceremony for a throwaway.** A glue script does not need a spec or a roadmap. Default to None.
- **A full spec for a one-line change.** Most promotions ship with no spec file — the commit message + source row is the record. Reading process should never take longer than doing the work.
- **Treating this map as the source of truth.** It lags. The linked protocol is canonical for tiers, templates, and commands — this doc only tells you *which* protocol and *when*.
- **Running heavyweight QA on a typo, or shipping a migration on lint alone.** The tier rubric exists precisely to prevent both; match depth to blast radius.
- **Adding eval/observability scaffolding to a project with no LLM calls.** The AI-feature band is conditional — skip it entirely when there's no model in the loop.
- **Skipping the phase handoffs.** Jumping from an idea straight to code (no Conceive, no Scaffold) is how weeks-later-you loses the original framing and re-litigates every early decision.

---

## Resources

- The six spine protocols and the cross-cutting protocols named inline above (this mirror includes the spine + AI-quality band; several cross-cutting protocols are named for context but not included here)

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2026-07-07 | Initial release — six-phase spine (Conceive→Resume), AI-feature quality band (evals + observability), cross-cutting table, entry router, proportional-ceremony throughline. |

---

**Protocol Version**: 1.0
**Last Updated**: 2026-07-07
