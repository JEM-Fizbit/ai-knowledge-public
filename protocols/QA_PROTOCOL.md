# QA Protocol

> Tiered verification system for shipping work. Matches QA depth to task surface — small/isolated changes ship with light checks; risky/wide-blast-radius changes ship with full verification; irreversible or externally-facing operations pass a hard gate. Avoids the two failure modes of project QA: heavyweight ceremony that blocks small edits, and lax practice that lets risky changes through.
>
> **Lifecycle:** the **Verify** phase — see [`DEVELOPMENT_LIFECYCLE.md`](DEVELOPMENT_LIFECYCLE.md) for how this fits with the other workflow protocols.

**Applies to:** Any active development project. Tiered adoption — minimum is a one-line `qa:quick` style command and the tier rubric. Manual checklists, hard gates, and design-QA audit docs are opt-in per project surface area.
**Last Updated:** 2026-06-06
**Version:** 1.0

---

## Table of Contents

- [Overview](#overview)
- [Scope and triggers](#scope-and-triggers)
- [Core principle: proportional verification](#core-principle-proportional-verification)
- [Tier rubric](#tier-rubric)
- [Hard gates](#hard-gates)
- [Verification surfaces](#verification-surfaces)
- [Project glue (what to put in `CLAUDE.md`)](#project-glue-what-to-put-in-claudemd)
- [Spec citation pattern](#spec-citation-pattern)
- [Manual verification checklist (template)](#manual-verification-checklist-template)
- [Design-QA audit doc (optional)](#design-qa-audit-doc-optional)
- [Anti-patterns](#anti-patterns)
- [Validation status](#validation-status)
- [Resources](#resources)

---

## Overview

Most informal QA dies in one of two ways. Either every commit demands the same heavyweight ritual (so the ritual gets skipped, then atrophies, then disappears), or there's no ritual at all and a risky change lands with the same scrutiny as a typo fix. Both failure modes produce the same outcome: production breakage that "should have been caught."

This protocol fixes that by **separating the question of *whether* to verify from the question of *how much***. Verification is always required before shipping; the depth is matched to the change.

> **Core principle:** QA depth scales with task surface, not with frequency. A typo fix doesn't need a full build; a schema migration doesn't ship on lint alone; an irreversible data operation doesn't ship without a hard-gate check regardless of code size.

The protocol stacks four verification tiers plus a separate hard-gate lane:

1. **Skip** — no QA check required. Reserved for non-code or trivially isolated edits.
2. **Quick** — fast static checks (lint, typecheck). The most common tier for everyday code edits.
3. **Full** — Quick + production build + relevant automated tests + manual verification where applicable. Required for changes with cross-cutting blast radius.
4. **Hard gate** — non-negotiable verification for irreversible, externally-facing, or data-shape operations. Runs *in addition to* the tier check, never instead of.

Hard gates are orthogonal: a change can be tier-Quick *and* hit a hard gate (e.g., a one-line RSS feed add). The tier governs how much general verification you run; the hard gate governs whether a specific risky operation is allowed at all.

### Key benefits

- **Small edits ship fast.** No heavyweight ritual for copy/docs/style changes.
- **Risky changes get scrutiny.** Build, tests, and manual checks fire on cross-cutting work.
- **Irreversible ops can't sneak through.** Hard gates are non-bypassable even on small commits.
- **One sentence per spec.** Specs cite which tier ran — no QA prose, no after-the-fact justification.
- **Project-tuned, protocol-shared.** Each project defines its own tier commands; the rubric is universal.

---

## Scope and triggers

This protocol is referenced from a global instruction file loaded into every AI coding session. It is universally available across all projects; no registry or per-project flag is required.

**Semantic triggers — invoke when the user gestures at:**

- Shipping work ("this is ready", "let's commit/push/merge", "PR this")
- Verifying a change ("does this work", "test this", "make sure this didn't break X")
- Cross-cutting edits (dependency bumps, schema changes, shared component edits, AI prompt changes)
- Operations with irreversibility or external surface (adding feeds, schema migrations, prod deploys, third-party API integrations, data deletions)
- Picking a verification command to cite in a spec (per [Spec citation pattern](#spec-citation-pattern))

Don't wait for the literal word "QA." Triggers are semantic.

**Structural trigger:** projects with a `qa:quick` / `qa:full` (or equivalent) script in `package.json` / `Makefile` / `justfile` are using this protocol's command surface; honor the tier rubric.

**Opt-in path:** add `qa:quick` and `qa:full` scripts to the project's task runner, cite them in `CLAUDE.md` under a "Verification commands" section, and follow the tier rubric. That's the entire opt-in.

**Opt-out:** projects can use any tier names they prefer (e.g., `check:fast` / `check:full`) — the rubric is what matters, not the literal command names.

---

## Core principle: proportional verification

The rubric below answers two questions for any change:

1. **Which tier?** Skip / Quick / Full. Determined by *task surface* — what code paths the change touches and whose blast radius reaches them.
2. **Hard gate fired?** Yes / No. Determined by *operation class* — does this change touch an irreversible or externally-facing surface?

The two questions are independent. A one-line RSS feed addition is tier-Skip *and* hits the RSS hard gate. A wide-scope refactor with no irreversible operations is tier-Full *and* no hard gate.

When unsure, escalate one tier. Cost of running a slightly heavier check is low; cost of missing a regression is high.

---

## Tier rubric

| Tier | What runs | When to use | Typical examples |
|------|-----------|-------------|------------------|
| **Skip** | Nothing | Pure prose/docs/non-code edits, isolated styling that can't break logic | README fixes, copy tweaks in static text, color-token swaps in a single component |
| **Quick** | Lint + typecheck (and any sub-second checks) | Code edits with localized blast radius, no shared-data-flow involvement | Single-component changes, isolated utility tweaks, internal refactors that don't cross module boundaries |
| **Full** | Quick + production build + automated tests (unit / E2E as relevant) + manual verification where applicable | Cross-cutting changes, anything that touches shared data flow, API surface, or framework wiring | Component changes used across pages, API route edits, schema changes, signal/ingestion pipeline edits, dependency bumps, AI prompt restructuring, auth/permissions, publishing flow |

### How to choose a tier

Walk this checklist top-to-bottom and stop at the first match:

1. **Hard gate fires?** → Run the hard-gate check unconditionally, *and* continue to tier selection.
2. **Touches shared data flow, API surface, schema, dependencies, or framework wiring?** → **Full**.
3. **Touches code (TS/TSX/JS/Python/etc.) but blast radius is localized?** → **Quick**.
4. **Pure prose / non-code / trivially isolated visual edit?** → **Skip**.

When two cases apply, the higher tier wins. When uncertain, escalate one tier.

### Examples (from validated patterns)

- **Solo web app, single-component button color change** → Quick (`pnpm qa:quick`)
- **Solo web app, dependency bump on Next.js** → Full (`pnpm qa:full`)
- **Solo web app, edit to signal-scoring algorithm or any AI prompt/model/criteria** → Full + `pnpm eval:scoring` (per [AI_EVALS.md](AI_EVALS.md)) + relevant manual checklist sections
- **Solo web app, adding an RSS feed** → Skip (one-line data add) + RSS hard gate (mandatory probe)
- **Solo game project, balance number tweak in `src/data/*.json`** → Skip + unit tests if any cover the formula
- **Solo game project, new enemy AI behavior** → Full (`npm test` + `npm run test:e2e`)
- **Solo game project, refactor that changes a core component shape** → Full + audit doc if blast radius is unclear

---

## Hard gates

Hard gates are operation-class checks that fire *independent of tier*. They exist because some operations have failure modes that no amount of lint/build/test can catch — they need a domain-specific check at the point of execution.

A hard gate has three required parts:

1. **Trigger condition** — exactly when it fires (e.g., "adding or modifying an RSS feed URL").
2. **Verification command** — the specific check that must pass (e.g., `curl` probe returning HTTP 200 + XML content type + non-empty item list).
3. **Failure handling** — what to do when the check fails (typically: do not proceed, report status, propose alternatives).

### When to define a hard gate

A change qualifies for a hard gate when:

- The operation is **irreversible or expensive to reverse** (data deletion, schema migration on prod data, public publish/post)
- The operation **commits the project to an external dependency** (adding a feed, integrating an API, pinning a critical dep version)
- A **historical incident** showed that automated checks alone weren't sufficient
- The **failure mode is silent** (broken feed that returns 200 with wrong content type, schema drift that doesn't fail builds)

### Examples (validated)

- **RSS feed hard gate** — mandatory `curl` probe + HTTP 200 + XML/RSS/Atom content type + verified item presence before any feed is added. Source: `RSS_FEED_INGESTION.md`.
- **Universal: never delete data as a fix** — Hard-gate framing makes it explicit: any change that deletes user data requires explicit user approval citing the data class and recovery path.

### Project pattern

Each project's `CLAUDE.md` should list its hard gates under a dedicated section. Don't bury them in prose. The reader should be able to scan and answer "what can't I do without an extra check?" in five seconds.

---

## Verification surfaces

The tiers above are surface-agnostic. A given project's tier-Full check might include any subset of:

| Surface | What it is | Best for | Examples |
|---------|------------|----------|----------|
| **Static checks** | Lint, typecheck, formatter | Catching syntax, type errors, style violations | `pnpm lint`, `tsc --noEmit`, `ruff check` |
| **Build** | Production build | Catching dead imports, bundler errors, build-time validation | `pnpm build`, `npm run build`, `cargo build --release` |
| **Automated tests** | Unit + integration + E2E | Verifying logic correctness, catching regressions in covered paths | Vitest, Playwright, Jest, Pytest |
| **AI evals** | Golden-set regression eval of LLM output | Verifying AI-output quality didn't regress on a prompt / model / criteria change | `pnpm eval:*` per [AI_EVALS.md](AI_EVALS.md) |
| **Manual checklist** | Human walkthrough of golden-path flows | UX correctness, visual regressions, state combinations no test covers | A project's `VERIFICATION_CHECKLIST.md` |
| **Visual review** | Actually VIEWING the rendered UI — a legible screenshot or the live result | Any change to visual output: layout, spacing, sizing, color, sprites/figures, overlays | Capture + look at a screenshot; for design work, show the sponsor for sign-off **before** committing |
| **Audit doc** | Tiered findings document with evidence and fixes | Design-QA, fuzzy-scope balance/security/UX work that doesn't map to a single spec | A dated `BALANCE_AUDIT_<date>.md` |
| **Hard-gate check** | Operation-specific verification | Irreversible / externally-facing / domain-critical operations | RSS feed probe, schema migration dry-run, prod deploy preview |

Projects pick the subset that applies. A library with no UI doesn't need a manual checklist; a game without external APIs doesn't need a hard gate; a content tool without dense test coverage relies more on manual checks and audits.

> **Visual work is not verified by green tests.** Static checks + tests + DOM-geometry measurements (`scrollWidth == clientWidth`, element rects) prove a UI change *runs and is mechanically correct* — they say nothing about whether it *looks right*. For any change to visual output, the gate is **viewing the rendered result**: capture a legible screenshot (size the preview to the component, or zoom a region), look at it, self-review against the design direction, and for design work show the sponsor and get sign-off **before** committing. Do not substitute measurements for looking, and do not auto-ship visual changes on passing tests alone. (Origin: a UI sprint on a solo game project where green gates repeatedly shipped clipped/cramped/opaque layouts and a pointer-events regression that were obvious on sight.)

---

## Project glue (what to put in `CLAUDE.md`)

Each project's `CLAUDE.md` should declare its QA surface explicitly. Recommended section structure:

```markdown
## QA Cadence

Use checks proportional to change surface. Universal rubric: [QA_PROTOCOL.md](docs/protocols/QA_PROTOCOL.md).

### Tier commands
- `<command for Quick>` — what it runs
- `<command for Full>` — what it runs

### Tier selection
- Skip: <project-specific skip cases>
- Quick: <project-specific quick cases>
- Full: <project-specific full cases>

### Manual verification
- Checklist: <path/to/checklist.md> (or "n/a" if none)
- Run after: <triggers, e.g., "dependency updates, UI changes, AI tool changes">

### Hard gates
- **<Gate name>** — <trigger condition>. Check: <command or skill>. Failure: <handling>.
- (repeat per gate)

### Design-QA audits (optional)
- Pattern: <path>/AUDIT_<date>.md when <trigger>
- (or "n/a")
```

Keep it under 30 lines. If the section grows past that, the rubric is being violated — push detail into a linked file (checklist, audit template), don't inline it.

---

## Spec citation pattern

Every spec promoted under [ROADMAP_AND_BACKLOG.md](ROADMAP_AND_BACKLOG.md) cites verification commands. With this protocol, that citation becomes:

> **Verification:** <tier> — `<command>`. <hard-gate name if fired>.

Examples:

- `**Verification:** Quick — pnpm qa:quick.`
- `**Verification:** Full — pnpm qa:full + signals section of VERIFICATION_CHECKLIST.md.`
- `**Verification:** Skip + RSS hard gate (probe per RSS_FEED_INGESTION.md).`

This is one line. No prose, no after-the-fact justification. The line answers two questions: which tier ran, and did a hard gate fire.

---

## Manual verification checklist (template)

For projects with UI or user-visible flows, a `VERIFICATION_CHECKLIST.md` at the project root (or under `docs/`) lists the golden-path walks for tier-Full work.

Structure:

```markdown
# Manual Verification Checklist

Use after dependency updates, UI changes, <project-specific surface area>, or other tier-Full work.

## Prerequisites
- Dev server running on port <N>
- <Required state, e.g., authenticated user, seed data>

## <Surface 1, e.g., Workspace Flow>
- [ ] **<Action>** — <expected behavior, including edge cases>
- [ ] **<Action>** — <expected behavior>

## <Surface 2>
- [ ] ...

## Cross-Cutting
- [ ] **Build passes** — `<full build command>`
- [ ] **Lint passes** — `<lint command>`
- [ ] **No browser console errors** — <pages to check>
- [ ] **<Project-specific universal>**, e.g., dark theme consistency, date format
```

Rules:

- One concrete action per line, in active voice.
- Group by user surface (Workspace, Admin, etc.), not by code module.
- End with a "Cross-Cutting" section for non-feature-specific universals.
- Keep the whole document scannable in under 5 minutes; if it grows past that, split per surface.

---

## Design-QA audit doc (optional)

For projects where design-fuzzy or cluster-scoped work surfaces faster than specs can absorb it (game balance, security audit findings, UX redesigns), use the audit-doc pattern — a dated `BALANCE_AUDIT_<date>.md` (or equivalent) file.

An audit doc is:

- **Dated** — `<DOMAIN>_AUDIT_<YYYY-MM-DD>.md`. Captures a point-in-time snapshot.
- **Tiered** — findings grouped by severity (Tier 1: must-fix, Tier 2: should-fix, Tier 3: nice-to-have).
- **Evidenced** — each finding cites file refs, line numbers, reproduction steps.
- **Actionable** — each finding has a recommended fix, even if the fix is "discuss in next sprint."
- **Open-state-tracked** — open items marked ⬜, shipped items marked ✅, linked to the spec or commit that resolved them.

Audit docs act as **peer inboxes to `BACKLOG.md`**. Items promote out of them into specs the same way backlog items do (per [ROADMAP_AND_BACKLOG.md](ROADMAP_AND_BACKLOG.md)).

Trigger for creating one: a request is large-scope or design-fuzzy enough that a single spec would either be too broad (>10 items) or too narrow (misses the system view). Propose the audit doc *before* drafting specs.

Don't migrate audit findings into `BACKLOG.md` — that destroys the structure (tier, evidence, recommended fix) the audit deliberately captures. Both inboxes feed the same spec pipeline.

---

## Anti-patterns

### One-size-fits-all QA

**Bad:** Every commit runs the full build + every test + the manual checklist.

**Why it fails:** Ritual becomes burden, gets skipped on small edits, then atrophies and disappears entirely. The team ends up with worse QA than if they'd started lighter.

**Good:** Match tier to task. Skip is a legitimate tier for prose and isolated styling.

### Tier inflation to "be safe"

**Bad:** Default to Full for every change "just in case."

**Why it fails:** Same as one-size-fits-all. Quick exists because most code edits don't need a production build. If you're always running Full, you've lost the proportionality the rubric is designed to give you.

**Good:** Trust the rubric. Escalate one tier only when uncertain — not by default.

### Hard gate as suggestion

**Bad:** "I'll run the RSS probe later" / "the schema migration is small, I'll skip the dry-run."

**Why it fails:** Hard gates exist precisely because the failure mode is silent or expensive. Deferring them defeats the point.

**Good:** Hard gate is unconditional. If it can't run, the change doesn't ship.

### Manual checklist rot

**Bad:** Checklist references features that no longer exist or omits surfaces added in the last six months.

**Why it fails:** Stale checklist gives false confidence — items pass because the feature is gone, not because the new feature works.

**Good:** Update the checklist in the same PR as the feature change. Treat it as code, not as docs.

### Skipping QA on "obvious" changes

**Bad:** "It's just renaming a variable, I don't need to lint."

**Why it fails:** Rename-across-files frequently misses one call site. Lint/typecheck catches it in two seconds.

**Good:** Quick is two seconds. Run it.

### Confusing tier and gate

**Bad:** "I ran Full, so the hard gate is covered."

**Why it fails:** Tier and gate are orthogonal. Full doesn't include the RSS probe; the RSS probe doesn't include lint.

**Good:** Run both. Cite both in the spec.

---

## Validation status

This protocol is generalized from two validated project patterns:

- **A solo web app** — original source for the tier model. Defined `pnpm qa:quick` (lint) and `pnpm qa:full` (lint + build), the proportional cadence ("personal-production app, not safety-critical"), the manual `VERIFICATION_CHECKLIST.md`, and the RSS Feed Hard Gate. In production use since 2026-Q1.
- **A solo game project** — original source for the automated-test surface and design-QA audit pattern. 88 unit tests (Vitest) + E2E tests (Playwright), specs cite `npm test` / `npm run test:e2e` per [ROADMAP_AND_BACKLOG.md](ROADMAP_AND_BACKLOG.md). Balance audit docs act as peer inboxes to the backlog.

Both patterns share the underlying structure formalized here: proportional tier selection, irreversible-op hard gates, project-defined surfaces, single-line spec citation.

Untested in production: the unified rubric framing itself. Expected to need one or two minor refinements over the first quarter of use. Track refinements in this file's version history.

---

## Resources

- [ROADMAP_AND_BACKLOG.md](ROADMAP_AND_BACKLOG.md) — Spec citation contract, audit-doc pattern (peer inbox)
- [BEST_PRACTICES_FIRST.md](BEST_PRACTICES_FIRST.md) — Pattern recognition when the same fix recurs
- [SOLUTION_DESIGN_PRINCIPLES.md](SOLUTION_DESIGN_PRINCIPLES.md) — Root cause vs symptom, blast-radius assessment
- `DEPENDENCY_HYGIENE.md` — Tier-Full triggers for dependency changes
- `RSS_FEED_INGESTION.md` — Canonical RSS hard-gate example
- [PROJECT_INITIATION.md](PROJECT_INITIATION.md) — Companion protocol for new-project scoping
- [AI_EVALS.md](AI_EVALS.md) — Golden-set regression eval; tier-Full verification for AI-output changes
- [AI_OBSERVABILITY.md](AI_OBSERVABILITY.md) — Runtime AI-call tracing; the online companion to evals

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2026-05-17 | Initial release. Generalized from two validated project patterns. |

---

**Protocol Version:** 1.0
**Last Updated:** 2026-06-06
