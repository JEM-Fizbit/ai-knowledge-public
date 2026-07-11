# Roadmap & Backlog System

> Layered system for capturing ideas/bugs/feature requests, promoting them into work briefs, and shipping with a clean audit trail. Designed for solo dev with an AI coding assistant as primary executor — minimum capture overhead, full spec drafting deferred until promotion.
>
> **Lifecycle:** the **Track & Plan** phase — see [`DEVELOPMENT_LIFECYCLE.md`](DEVELOPMENT_LIFECYCLE.md) for how this fits with the other workflow protocols.

**Applies to:** Any active development project. Tiered adoption — minimum is `BACKLOG.md` + `docs/specs/` + a decision log. Strategic roadmap, audit-doc, and sprint-plan layers are opt-in for projects with enough surface area to need them.
**Last Updated:** 2026-07-05
**Version:** 1.7

---

## Table of Contents

- [Overview](#overview)
- [Scope and triggers](#scope-and-triggers)
- [Reference dogfood loop](#reference-dogfood-loop)
- [When to Use](#when-to-use)
- [Triggers — when to invoke this protocol](#triggers--when-to-invoke-this-protocol)
- [Architecture](#architecture)
- [Quick Start](#quick-start)
- [Capture verbs](#capture-verbs)
- [Promotion contract](#promotion-contract)
- [Lifecycle (on ship)](#lifecycle-on-ship)
- [Spec templates](#spec-templates)
- [Roadmap layer (optional)](#roadmap-layer-optional)
- [Audit layer (optional)](#audit-layer-optional)
- [Sprint plans (optional)](#sprint-plans-optional)
- [Cross-source view (`show open work`)](#cross-source-view-show-open-work)
- [Decision log](#decision-log)
- [Anti-patterns](#anti-patterns)
- [Validation status](#validation-status)
- [Resources](#resources)

---

## Overview

Most informal issue tracking dies the same way: ideas land in scattered notes (Evernote, Notion, the brain), bugs get re-discovered after being filed, feature requests get re-scoped every time they come up, and shipped work leaves no trail to the original ask. The result is churn — the same conversation repeated, with no compounding context.

> **Core principle:** Ceremony scales with complexity, not with frequency. A spec exists when it earns its keep — when the work is genuinely complex, multi-file, or design-ambiguous. Trivial fixes and data tweaks should not spawn full spec files. Reading process should never take longer than doing the work.

This protocol fixes that with **four layers** stacked by signal density, plus an optional coordination layer:

1. **`BACKLOG.md`** — lightweight one-line capture for fresh ideas/bugs/requests.
2. **`docs/specs/NNN-slug.md`** — work briefs drafted on promotion **only when work earns one**. The durable record post-ship.
3. **Strategic roadmap** *(optional)* — phase-banded plan with hierarchical IDs.
4. **Audit docs** *(optional)* — dated tiered-finding snapshots that surface structured work (balance audits, security audits, etc.).
5. **Sprint plans** *(optional, coordination layer)* — `<sprint-dir>/SPRINT_<date>.md` documents that bundle a sprint's work across multiple sources. They can absorb small/trivial items so those items don't need their own spec file. Standalone-spec work and sprint-plan-absorbed work coexist within one sprint.

Plus a project-wide **decision log** that captures locked design decisions with rationale.

The two scripts (`scripts/backlog.sh`, `scripts/show-open-work.sh`) automate capture and cross-source visibility. The AI assistant runs them or invokes their semantic equivalents in conversation.

### Key benefits

- **Single point of capture** — everything funnels through `BACKLOG.md`, regardless of source (chat, terminal, mobile).
- **No duplication** — strict cardinal rule: one item lives in exactly one source. Cross-source view aggregates without copying.
- **Spec-on-promotion** — full spec drafting happens only when work is ready to start, not at capture time. Capture stays cheap.
- **Lifecycle is one PR** — archive spec / delete BACKLOG line / flip source row, all in the same commit. No coordination later.
- **Archive is the durable record** — the shipped spec carries source, criteria, work, and commit. BACKLOG and source-row noise is deleted.

---

## Scope and triggers

This protocol is referenced from a global instruction file loaded into every AI coding session. It is universally available across all projects; no registry or per-project flag is required.

**Structural trigger:** a project opts in by having `BACKLOG.md` at its root (optionally accompanied by `docs/specs/`, a sprint directory, or `ROADMAP.md`). When Claude enters such a project, this protocol governs work-capture and promotion by default.

**Semantic trigger:** even when no `BACKLOG.md` exists, Claude should invoke this protocol whenever the user gestures at open work — capturing a bug or idea, retrieving open items, promoting work, or shipping. If the project has no `BACKLOG.md` yet and the user wants to capture an item, offer to bootstrap one at the project root (a one-line capture is sufficient — no scaffolding ceremony). Then proceed under the protocol's None or Light intensity.

**Opt-in path:** create `BACKLOG.md` at the project root. That's the entire opt-in. Sprint dir, `docs/specs/`, and `ROADMAP.md` are optional and project-defined per the intensity tiers described below.

**Opt-out path:** projects that don't want this protocol simply don't create a `BACKLOG.md`. None-tier is the default state for new or small projects.

---

## Reference dogfood loop

The protocol describes layered artifacts; the expected operating rhythm — the loop that earns the layers their keep on a substantive project — is:

```
roadmap ── playtest/dogfood ── backlog capture ── (optional audit) ──
sprint plan ── implement ── iterate
```

1. **Roadmap** sets near-term direction (themes, current focus, explicit non-goals).
2. **Playtest / dogfood** generates findings: what feels off, what's broken, what's missing.
3. **Backlog capture** absorbs those findings one-liner-per-item, plus any out-of-band ideas/bugs that surface elsewhere.
4. **Audit doc** *(optional)* — when a single playtest produces enough findings to need triage before planning, write a dated audit doc (see [Audit layer](#audit-layer-optional)). For small batches, skip straight to sprint planning.
5. **Sprint plan** *(optional)* bundles 3-5 coherent items from roadmap / backlog / audit into a single brief.
6. **Implement** the sprint.
7. **Iterate** — close-out, playtest the result, capture findings, repeat.

This is a **reference pattern, not a mandate.** Lighter projects skip layers — a small utility might never need a roadmap, an audit cadence, or a sprint plan. Adopt the smallest stack that keeps the work coherent. The layers documented below are individually optional; the loop above is what the system looks like when all of them are in play.

---

## When to Use

| Scenario | Adopt? |
|---|---|
| Active dev project with ongoing feature/bug surface | Yes — full stack |
| Solo project with <1-month timeline | Optional — minimum stack (BACKLOG + specs) is fine |
| Tiny utility, single-file script | No — overkill |
| Multi-developer project | Adopt with care — protocol assumes one person promoting |
| Conceptual/exploratory project (not yet shipping code) | No — capture in design docs instead |
| Project with formal issue tracker (Linear, Jira) already in use | No — this is a replacement, not a layer |

---

## Triggers — when to invoke this protocol

**Critical: this protocol triggers on semantic intent, not literal verbs.** When a user is in a project that has `BACKLOG.md` + `docs/specs/` at the root, any conversational gesture about open work should invoke the protocol. Don't wait for the literal word "backlog."

### Capture triggers (→ add to `BACKLOG.md`)

- "add to backlog: X"
- "capture this", "track this", "let's not forget this", "remember this for later"
- User reports a bug while working on something else ("by the way, I noticed…")
- User describes a feature idea, even speculatively ("at some point we should…")
- User flags a concern that isn't being addressed in the current task

### Retrieval triggers (→ run `scripts/show-open-work.sh` or read `BACKLOG.md`)

- "show open work", "what's open?", "what's left?"
- "what should I work on next?", "any priorities?"
- "show me the backlog", "what bugs are tracked?"
- "what's the roadmap?" (if a roadmap layer exists)
- User asks about a feature they vaguely remember discussing — search BACKLOG and archived specs

### Promotion triggers (→ draft `docs/specs/NNN-slug.md`)

- "promote item N", "promote the X item", "let's work on [item]"
- "let's tackle the [X] bug", "let's build [Y]"
- User picks a specific item from the BACKLOG / roadmap / audit doc and signals intent to start work
- User says "draft a spec for [thing already discussed]"

### Ship triggers (→ run the on-ship lifecycle)

- "this is shipped", "done with X", "let's ship this", "this PR is ready"
- After a PR merges that maps to a spec
- User says "mark X done" / "close out the [Y] spec"

When in doubt, ask the user: *"Should I capture that in BACKLOG.md?"* — better to confirm than miss a capture.

---

## Architecture

```
                  ┌────────────────┐
                  │   BACKLOG.md   │  ◄── capture (1 line, no metadata)
                  └────────┬───────┘
                           │ promote — choose depth (see "Promotion contract")
                           ▼
                ┌──────────┴──────────┐
                ▼                     ▼
   ┌────────────────────────┐   ┌──────────────────────────┐
   │   docs/specs/NNN-…md   │   │  Sprint plan / commit    │  ◄── trivial fixes,
   │   (full spec)          │   │  message only            │      data tweaks,
   │   complex / multi-file │   │  (no spec file)          │      single-file
   └────────────┬───────────┘   └────────────┬─────────────┘      changes
                │                            │
                │ ship                       │ ship
                ▼                            ▼
   ┌────────────────────────┐   ┌──────────────────────────┐
   │ docs/specs/archive/…   │   │ Source row flip + delete │
   │ (durable record)       │   │ BACKLOG line. Archive    │
   │                        │   │ via commit history.      │
   └────────────────────────┘   └──────────────────────────┘

  Optional peer inboxes (also promote per the depth choice above):
  • <PROJECT_ROADMAP>.md  — strategic phase rows with ⬜/✅
  • <TOPIC>_AUDIT_<date>.md — dated tiered findings

  Optional coordination layer:
  • <sprint-dir>/SPRINT_<date>.md — multi-spec sprint plan that can absorb
    small items without spawning per-item specs

  Project-wide:
  • DECISIONS.md (or equivalent) — locked design decisions, append-only
```

### Cardinal rule: don't duplicate

One item lives in **exactly one source**. The cross-source view aggregates; it does not copy. When capturing, grep the four sources first to avoid duplication.

Specifically: **do not migrate audit findings into `BACKLOG.md`.** That destroys the structure (tier, evidence, recommended fix) the audit deliberately captures. Audits are peer inboxes, not staging areas for backlog migration.

---

## Quick Start

For a project adopting this protocol, scaffold from the templates:

```bash
# From the project root
cp ~/Projects/your-protocol-repo/templates/roadmap-system/BACKLOG.md.template BACKLOG.md
mkdir -p docs/specs/archive
cp ~/Projects/your-protocol-repo/templates/roadmap-system/docs-specs-README.md.template docs/specs/README.md

mkdir -p scripts
cp ~/Projects/your-protocol-repo/templates/roadmap-system/scripts/backlog.sh scripts/
cp ~/Projects/your-protocol-repo/templates/roadmap-system/scripts/show-open-work.sh scripts/
chmod +x scripts/backlog.sh scripts/show-open-work.sh

# Decision log (recommended for any project that will accumulate design decisions)
cp ~/Projects/your-protocol-repo/templates/roadmap-system/DECISIONS.md.template docs/DECISIONS.md
# (or place under Design-Docs/, design/, or wherever the project's design docs live)

# Optional: configure roadmap / audit / structured-doc layers
cp ~/Projects/your-protocol-repo/templates/roadmap-system/.backlogrc.example .backlogrc
# Edit .backlogrc to enable the layers this project uses

# Add a "Roadmap & Backlog System" section to project CLAUDE.md
# pointing at this protocol and listing project-specific glue (verification commands, etc.)
```

**Scripts are scaffolded once at adoption, not synced automatically.** They change rarely and per-project tweaks should be allowed. To pick up upstream changes, re-copy from the templates intentionally.

---

## Capture verbs

Three surfaces, one destination (`BACKLOG.md`):

1. **In-session (Claude):** the user says "add to backlog: X" or any [capture trigger](#capture-triggers--add-to-backlogmd). Claude prepends to `BACKLOG.md` and commits.
2. **Terminal:** `scripts/backlog.sh "<item text>"`. Set `BACKLOG_NO_COMMIT=1` to stage without auto-committing. (Users can alias this to `backlog` in `~/.zshrc` if they want — purely a personal-shell convenience; not part of the protocol.)
3. **Mobile / direct edit:** open `BACKLOG.md` in any editor (Working Copy on iPhone, GitHub web UI, etc.), add a line below the sentinel `<!-- backlog items below; newest first -->`, commit, push.

**Always pull before capturing on a different surface** to avoid merge conflicts on `BACKLOG.md`.

### Commit discipline (capture & promotion)

Backlog captures are committed **and pushed** immediately and automatically — do **not** ask the user for permission each time. A `BACKLOG.md` line (or a freshly-drafted `docs/specs/NNN-slug.md`) is append-only markdown with zero build/runtime impact; gating it behind a confirmation is pure friction, and leaving it uncommitted is how captures get lost. This is the one place the system auto-commits without a logical-unit QA gate — and it's safe precisely because the change surface is a single markdown file.

The hard rule that *keeps* it safe:

- **Stage only the capture file(s).** `git add BACKLOG.md` (plus the spec file, if one was drafted at promotion). **Never `git add -A` / `git add .` for a capture commit.** Working trees are frequently shared across parallel agent sessions and carry unrelated in-progress edits; `-A` sweeps that work into the capture commit — and on an auto-deploy branch, ships someone else's mid-flight code to production.
- **Push immediately.** If the push is rejected because a parallel session pushed first, `git pull --rebase` then re-push. **Never force-push.**

Code changes are different — they still follow the project's normal batch-and-QA commit discipline (iterate, QA the logical unit, then commit). The auto-commit-and-push default is specific to lightweight capture/promotion docs.

**Capture is an inbox dump, not an investigation.** Match the user's words; add at most a single file:line pointer if a 10-second grep confirms a reference the user already named. Scanning callers, proposing fixes, ranking options, or speculating on root cause happens at **promotion time**, not capture time. The inbox is lightweight by design — if a capture grows past ~3 lines, you've over-invested. See [Anti-patterns](#investigating-bugs-at-capture-time) for the full failure mode.

---

## Promotion contract

Trigger: any [promotion trigger](#promotion-triggers--draft-docsspecsnnn-slugmd).

On promotion, the AI assistant:

1. Reads the one-liner from `BACKLOG.md` (or the source row from a roadmap / audit doc).
2. Scans relevant code for current behaviour, constraints, dependencies — enough to write the spec accurately.
3. **Chooses spec depth** using the rubric below. Most promotions are not full specs.
4. If a spec is drafted: uses the [standard template](#standard-template) or [bug shortcut](#bug-shortcut-template). Sequential numbering across the project; no phase-scoped IDs. Asks **1-3 questions only if there's blocking ambiguity** — otherwise infers and notes assumptions in the "Assumptions" section. The default is to draft, not to interrogate.
5. Sets `Status: draft` and waits for "go" / "approved" before implementing.

### Spec-depth rubric (step 3)

| Work shape | Output |
|---|---|
| New system / new architectural component / multi-file architectural change / design ambiguity needing pre-resolution | **Standard spec** (`docs/specs/NNN-slug.md`) |
| Single-file bug fix with localized scope | **Bug shortcut** (`docs/specs/NNN-slug.md`, lighter template) |
| Trivial data tweak (numbers, weights, copy text) | **No spec.** Capture intent in commit message + source row. Cite the source line. |
| Single-file change with obvious intent | **No spec.** Commit message is the record. |
| Work already adequately described in an in-flight sprint plan | **No spec.** The sprint plan is the brief; ship under it. |
| Cluster-scoped or design-fuzzy exploration | **Audit doc**, not a spec. Specs promote *from* the audit later. |

**Default to "no spec" when uncertain.** Specs that don't earn their keep accumulate as overhead, not signal. Future-you reading the archive should learn something new from each spec; if the diff already says it, the spec adds nothing.

When no spec is drafted, the work still ships through the same lifecycle — the source row still flips, the BACKLOG line is still deleted. The commit message carries what would have been in the spec's `Source:` field.

If the source maps to a strategic roadmap row, the spec's `Source:` field (or commit message) links to it. If it maps to an audit doc section, cite that section (e.g. `BALANCE_AUDIT_2026-05-02.md §12`).

---

## Lifecycle (on ship)

When work lands, do **all of the following in the same PR** — this is the only multi-source coordination the system requires, and it's only paid once per shipped item.

1. **If a spec was drafted:** move it from `docs/specs/NNN-slug.md` to `docs/specs/archive/NNN-slug.md`. Set `Status: done` and append a `Shipped: YYYY-MM-DD, commit <short-hash>` line. The archived spec is the durable record.

   **If no spec was drafted** (per the spec-depth rubric): skip this step. The commit message is the record — it should cite the source (`Source: BACKLOG.md "<one-liner>"` or `Source: BALANCE_AUDIT_2026-05-02 §8`) so the work is traceable from `git log`.

2. **Flip the source's status:**
   - **`BACKLOG.md` item** → **delete the line entirely.** No "Shipped" section in `BACKLOG.md`; the archive (or commit history, for no-spec ships) carries the record.
   - **Strategic roadmap row** *(if used)* → flip ⬜ to ✅; add a brief shipped note to the row's Notes column.
   - **Audit doc item** *(if used)* → flip ⬜ to ✅; cite the spec or commit if useful.

3. **If an audit doc has all items ✅,** add `**Status:** Resolved YYYY-MM-DD` at the top of the doc and `git mv` it to the project's audit-archive directory. Prevents stale audit docs from accumulating as "open work" sources.

4. **If the shipped spec is cited from synced/shared protocol docs, update the canonical source before re-syncing.** Do not patch generated `docs/protocols/*` copies directly. Update the source protocol in your protocol repo, then run the project's sync command. This prevents canonical protocols from pointing at stale active-spec paths after `docs/specs/archive/...` moves.

This close-out sequence is what closes the orphan-risk loop and keeps `show open work` honest. It applies whether or not a spec was drafted.

> **Validation note.** Step 3 (audit-archival cycle) is **lightly validated** — it shipped with the protocol but had not yet fired in production at the time of writing. Treat as best-effort until the first real archival exercises it.

---

## Spec templates

Templates live in `~/Projects/your-protocol-repo/templates/roadmap-system/docs-specs-README.md.template` and are scaffolded into each project's `docs/specs/README.md` on adoption. Two templates:

### Standard template

Use for features, system additions, or any non-bug work. Fields: Status, Source, Roadmap link, Decisions impact, Related; Problem, Acceptance criteria, Out of scope, Technical constraints, Test plan, Data files touched, Verification commands, Assumptions.

### Bug shortcut template

Lighter form. Fields: Status, Type=bug, Source, Roadmap link; Repro, Expected, Actual, Root cause hypothesis, Fix approach, Regression test, Verification.

Use the shortcut when the standard template's "Out of scope / Technical constraints" overhead exceeds the bug's complexity.

See the project-level `docs/specs/README.md` for the copy-pasteable Markdown.

---

## Roadmap layer (optional)

Projects with enough surface area to need direction should maintain a roadmap document. The roadmap is the strategic peer inbox: it captures themes, current focus, near-term initiatives, and an explicit "not doing" list. It's the input that lets sprint plans cohere around themes rather than reading like batched chores.

**Content shape (suggested):**
- Active themes / pillars
- Current focus (the 1-2 themes the project is investing in now)
- Near-term initiatives (next 1-3 sprints' worth of work)
- Explicitly not doing (the negative space matters as much as the positive)

**Cadence:** living doc, updated when direction shifts — not on a calendar. Stale roadmaps are worse than no roadmap.

**Path:** project-defined. Common patterns: `docs/ROADMAP.md`, `Design-Docs/ROADMAP.md`. Set `ROADMAP_PATH` in `.backlogrc` so the cross-source view picks it up.

**Skip this layer if:** the project is a small utility, a short-lived script, or otherwise has no strategic direction worth writing down. "What do I want to do next?" answered by glancing at `BACKLOG.md` is fine for small surfaces.

---

## Audit layer (optional)

When a playtest / dogfood session or external review surfaces enough findings to warrant triage before sprint planning, write a dated audit doc. The audit captures findings with structure that a backlog one-liner can't: tier (severity), evidence, recommended fix.

**When to write one:**
- Findings cluster around a theme (e.g. balance, accessibility, security) and benefit from being read together.
- The set is large enough that promoting each finding individually into `BACKLOG.md` would drown the inbox and lose signal.
- The findings need triage (tier, prioritization) before any of them are ready for sprint planning.

**When to skip:** small batches (1-3 findings) — capture them directly in `BACKLOG.md` and skip the audit layer.

**Path and naming:** project-defined. Common patterns: `docs/audits/<topic>_AUDIT_<YYYY-MM-DD>.md` or `Design-Docs/<TOPIC>_AUDIT_<date>.md`. Set `AUDIT_GLOB` in `.backlogrc` so audit docs are picked up dynamically as they're added — no manual registration.

**Flow:** audit findings feed sprints via `[audit: …]` citations in sprint Blocks/items (see [Sprint plans](#sprint-plans-optional)). Findings are not migrated into `BACKLOG.md` — that destroys their structure (see Anti-patterns: "Migrating audit findings into BACKLOG.md").

A `BALANCE_AUDIT_*` cadence (playtest → audit → sprint), validated on a personal game project, is the reference implementation of this layer working end-to-end.

---

## Sprint plans (optional)

A sprint plan bundles a coherent set of work — pulled from roadmap, backlog, audit, or ad-hoc — into a single dated brief. Sprint plans are the coordination layer above specs: they let a small set of items ship together as a theme rather than as disconnected commits, and they can absorb small items that don't warrant their own spec file.

Sprint plans are **optional** and tiered. Projects opt in to the intensity that fits their work surface.

### Three intensities

**None.** Small or short-lived projects. No sprint files. Items ship individually via the standard lifecycle. This is the right default for utilities, scripts, and projects without a verification suite or audit cadence.

**Light (minimum viable).** Sprint files exist but stay flat.

- Path: `<sprint-dir>/SPRINT_<YYYY-MM-DD>[-suffix].md`. `<sprint-dir>` is project-defined (`Design-Docs/`, `docs/sprints/`, etc.).
- Content: a one-line goal at the top, then a flat checklist of items. Each item carries a brief description, an optional spec link, and a status marker — `[ ]` open, `[x]` shipped, `~strikethrough~` dropped.
- Close-out: optional section appended in place when the sprint ships.

Suited for projects that want some thematic bundling but don't have a verification suite or audit cadence to anchor a heavier plan.

**Full (reference pattern).** Sprint files carry the full sprint shape.

- Same path / naming convention as Light.
- Content structure:
  - `# Sprint — <slug>` heading.
  - **Why this sprint** — one paragraph framing the theme and what triggered it (playtest, audit, roadmap shift).
  - **Scope** — organized as **Blocks**, each with a **Mechanic** (what changes from the user's POV) and **Changes** (the concrete code/data moves).
  - **Out of scope (and why)** — the negative space. Surfaces deliberate staging (e.g. "v2 ships in Sprint N+1") so close-out logic doesn't trip on partial completion. See the anti-pattern "Recommending row close-out without checking sprint-plan staging."
  - **Verification** — project's commands (see [Verification in sprints](#verification-in-sprints) below).
  - **Lifecycle** — close-out appended in place on ship (see [Close-out appended in place](#close-out-appended-in-place) below).

Suited for projects with verification suites, audit-driven development, or larger work packages that need staged scope.

**Reference:** a personal game project's `Design-Docs/SPRINT_*.md` files are the Full pattern's reference implementation. Lift the structure from there rather than reinventing it.

### Composition gate

Before drafting any `SPRINT_*.md` file, the agent (or person) must read the project's ROADMAP + BACKLOG + recent audit findings (if any) and propose 3-5 items that **hang together as a coherent theme**. The gate is binary: if the proposed work doesn't satisfy this, you're writing a single commit, not a sprint plan.

The composition gate is what keeps sprint files honest. A sprint that's actually 5 unrelated commits with a date-stamped header glued on is overhead, not coordination — it gives the user a false signal of progress on a non-existent theme.

### One open sprint at a time

Per project, **only one sprint file is open at a time.** Close the current sprint (append close-out) before opening another.

Same-day suffix (`b`, `c`, `d`) is allowed when a sprint genuinely needs to close mid-day and a new theme starts — but the new sprint's top line must include a one-line justification (e.g. "playtest of SPRINT_2026-05-05 revealed urgent regression in X; this sprint addresses that before resuming the roadmap"). Repeated same-day spawning is a smell: it usually means sprints were undersized at composition or the theme wasn't clear. Surface this back to the user — don't normalize it.

### Source citation per block / item

Every Block (Full) or item (Light) in a sprint must cite its source. Use one of:

- `[backlog: <one-liner>]` — promoted from `BACKLOG.md`
- `[roadmap: <theme or row>]` — pulled from the strategic roadmap
- `[audit: <doc>:<finding>]` — pulled from an audit doc (e.g. `[audit: BALANCE_AUDIT_2026-05-02 §8]`)
- `[ad-hoc: <reason>]` — none of the above; surfaced in-sprint

Ad-hoc is a **valid but visible category.** It exists so genuine in-sprint discoveries (a bug spotted mid-implementation, a refactor surfaced by the work) can ship under the sprint without forcing a backwards capture. When ad-hoc items dominate a sprint, that's a signal the capture/composition discipline upstream is leaking — surface it back to the user rather than hiding it under a non-ad-hoc citation.

### Verification in sprints

Sprints **touching code** MUST include a Verification section citing the project's verification commands. Pull these from the project's `CLAUDE.md` (or equivalent — projects keep their canonical command list there). Examples from validated patterns:

- A solo web-app project: `pnpm qa:quick` for fast feedback, `pnpm qa:full` before close-out.
- A solo game project: `tsc`, `npm test`, plus a browser-side smoke checklist.

Sprints **not touching code** (docs sprints, planning sprints, comms sprints) MAY include success criteria but no formal verification commands. The decision rule is one question: **"Would I be embarrassed if this shipped broken?"** If yes, you need verification commands. If no, success criteria are enough.

### Close-out appended in place

When a sprint ships, the close-out — date, commit refs, test results, lessons learned — is **appended to the sprint file itself**, not moved or summarized elsewhere. Co-locating plan + outcome makes the sprint file the durable record: future-you reading `SPRINT_2026-05-02.md` sees both what was planned and what actually happened, in one read.

This mirrors the spec lifecycle's "archive carries the durable record" principle, scaled to the sprint coordination layer.

### Archive policy

**Version control is the canonical archive.** Shipped sprints can stay in place indefinitely (old `SPRINT_*.md` files sitting in `Design-Docs/` next to the active one), or projects may opt to move shipped sprints to `<sprint-dir>/Archive/` on full close-out. Either is fine.

Don't enforce one approach. Some projects want a visually-clean sprint dir; others want all sprint history at a glance. Pick what fits the project and stay consistent within it.

---

## Cross-source view (`show open work`)

The script `scripts/show-open-work.sh` produces a unified read-only view across all configured sources. Sections (in order):

1. **`BACKLOG.md` items** — numbered (matches `promote item N` semantics).
2. **Strategic roadmap** *(if `ROADMAP_PATH` set)* — open ⬜ rows grouped by phase.
3. **Audit docs** *(if `AUDIT_GLOB` set)* — open items per file, discovered dynamically by glob (so new audit docs appear without manual registration).
4. **In-flight specs** — every `docs/specs/*.md` (excluding `README.md`), with status from frontmatter.
5. **Structured design docs** *(if `STRUCTURED_DOCS` set)* — count-only summary (these are domain-design lists, not work-item lists, so they aren't expanded).

### Configuration

Project-specific paths live in `.backlogrc` at the repo root (sourced as bash). The default is the minimum stack — only `BACKLOG.md` + `docs/specs/`. Configure layers as needed:

```bash
# .backlogrc
ROADMAP_PATH="docs/ROADMAP.md"
AUDIT_GLOB="docs/audits/*_AUDIT_*.md"
STRUCTURED_DOCS=("docs/CATALOG.md")
```

Conventions the script assumes:
- Roadmap rows match `^| <phase>.<n> |...⬜` and live under `## Phase <N>` headings.
- Audit doc items use `### <N>. <title>` with `**Status:** ⬜` lines.
- Specs have `**Status:** <state>` near the top (the standard template emits this).

If a project diverges from these conventions, the script's awk patterns are the place to adjust — but staying on the convention is cheaper than diverging.

### Multi-project view (`what's open across my projects?`)

When the user gestures at the **fleet** rather than a single project — phrases like "what's open?", "show me everything in flight," "what's on the table across my projects" — assemble a unified view by walking the project tree. Triggered semantically, not by slash command. Phrases include: "what's open?", "what's open across my projects?", "show me everything in flight", "what's on the table", "what am I working on?".

**Recipe:**

1. **Walk `~/Projects/*`** for directories containing `BACKLOG.md` at the root. These are the projects on the protocol.
2. **Per project, summarize the backlog** — total item count plus the top 3 newest items (the cheap signal).
3. **Per project, scan the spec dir** (`docs/specs/` or project-equivalent) for in-flight specs — anything whose `Status:` is not `done` or `archived`. Count + titles.
4. **Per project, scan the sprint dir** (`Design-Docs/`, `docs/sprints/`, or project-equivalent) for open sprint files. For each open sprint: goal line + remaining (`[ ]`) items.
5. **Optional:** pull from external trackers (Linear, Asana, GitHub Issues) for projects that wire them in. Skip silently for projects that don't.
6. **Present grouped by project.** Per-project section: backlog count + top 3, in-flight spec count + titles, open sprint goal(s) + remaining items.

This is read-only and aggregating — the cardinal rule still applies: don't copy items between sources to produce the view, just walk and read.

---

## Decision log

Every project keeps a decision log — a separate document that captures **locked design decisions with rationale**. This is not part of the spec/backlog flow, but it pairs naturally and lives alongside.

**What goes in:** decisions where the *why* matters more than the *what*. "We chose X because Y constraint, rejected Z because W." Future-you needs Y and W to evaluate whether the decision still applies.

**What doesn't:** mechanical implementation choices, transient state, anything the code already documents.

**Format:** newest at top, append-only, with date and rationale. See `templates/roadmap-system/DECISIONS.md.template` for the entry shape.

**Location:** project's choice. Common spots:
- `docs/DECISIONS.md` (small projects)
- Inside an existing design-docs directory (e.g. `Design-Docs/WORKING_DECISIONS_LOG.md`)
- ADR style — `docs/decisions/NNN-slug.md` per decision (projects with many decisions and a need for individual review)

The project's `CLAUDE.md` should link to it so any AI session can find and consult it.

---

## Anti-patterns

### Drafting a spec for every promotion (most common failure mode)

```
❌ Bad — drafting a 12-section spec for a one-line bug fix or a JSON
   data-value tweak. Reading the spec takes longer than fixing the
   bug. Future-you wades through ceremonial scaffolding to find one
   line of intent. Specs that don't earn their keep accumulate as
   overhead, not signal.

✅ Good — apply the spec-depth rubric (see "Promotion contract" §
   step 3). Bug shortcuts for bugs. No-spec for trivial data tweaks
   and obvious single-file changes — the commit message + source
   row is the record. Standalone specs only for genuinely complex
   or multi-file work.

Heuristic: if you're about to write the spec's "Out of scope" and
"Technical constraints" sections and they'd be empty or restate
what the diff says, you don't need a spec.
```

### Migrating audit findings into BACKLOG.md

```
❌ Bad — promoting audit item by copying the one-liner into BACKLOG.md
   This destroys the audit's structure (tier, evidence, recommended fix).

✅ Good — promote audit item directly per the depth rubric, citing the
   audit section in the spec's Source field (or commit message if no
   spec). The audit ⬜ stays open until ship.
```

### Duplicating items across sources

```
❌ Bad — same idea captured in BACKLOG.md AND a roadmap row AND an audit doc
   ("just in case"). Now any update has to find and fix all three.

✅ Good — pick the highest-signal source, capture there once. The cross-source
   view will surface it from wherever it lives.
```

### Asking 5+ clarifying questions before drafting a spec

```
❌ Bad — interrogating the user about every adjacent design choice before
   writing a single line of the spec.

✅ Good — draft with reasonable assumptions, list them in the Assumptions
   section, ask 1-3 questions only on blocking ambiguity. The user reviews
   on "approved" before implementation, and corrects assumptions then.
```

### Investigating bugs at capture time

```
❌ Bad — at capture time, scanning code, identifying file:line refs,
   proposing multi-option fix paths, and ranking approaches by
   "surgicalness." The inbox is supposed to be lightweight; full
   investigation belongs at promotion time when the user has chosen
   to invest in the item. Symptoms: capture entries that grow past
   3 lines, capture commits that take longer than the user's typing.

✅ Good — prepend the user's observation verbatim. Add at most a
   one-line file pointer if a 10-second grep confirms a reference
   the user already named. Skip fix speculation, root-cause analysis,
   and option-ranking. The lightweight surface is the whole point —
   promotion is where investigation earns its keep.
```

### Recommending row close-out without checking sprint-plan staging

```
❌ Bad — reporting "implementation complete, time to flip the row ✅"
   immediately after the latest commit, without reading the current
   sprint plan's "Out of scope" / future-sprint sections. If the
   row's work is deliberately staged across multiple sprints (e.g.
   v1 + v2), close-out belongs to the final sprint — not the first.
   The user shouldn't have to remember the staging; the sprint plan
   already documented it.

✅ Good — before recommending lifecycle close-out, read the current
   sprint plan's full body, especially the "Out of scope (and why)"
   table and any "Sprint N+1" callouts. Cross-check: does the source
   row's text cover more than what just shipped? If yes, the row
   stays ⬜ until subsequent sprints land. Surface the next sprint
   *before* the user has to ask. Frame status as "Sprint N shipped X;
   Sprint N+1 owes Y to close the row" — not "ready to close out."
```

### Sweeping unrelated changes into a capture commit

```
❌ Bad — capturing a backlog item, then `git add -A && git commit && git push`
   to record it. In a working tree shared with parallel agent sessions (or
   just carrying your own unrelated WIP), this bundles in-progress code into
   a "docs: backlog" commit — and on an auto-deploy branch, ships it to prod
   mid-flight under a misleading message. (Real incident: a parallel
   session's half-finished feature went to production this way.)

✅ Good — stage only the capture file(s): `git add BACKLOG.md` (+ the spec
   file if one was drafted), commit, push. Auto-committing captures is the
   right default; tight staging is what makes it safe. See "Commit
   discipline (capture & promotion)" under Capture verbs.
```

### Skipping the on-ship triple flip

```
❌ Bad — merging the PR with the work but forgetting to delete the BACKLOG
   line. Item shows up forever as "open."

✅ Good — the same PR carries the code change, the spec → archive move,
   the BACKLOG line deletion, and any source-row status flip. One PR,
   one coordination point, then done.
```

### Trying to retrofit auto-sync-on-commit for the scripts

```
❌ Bad — wiring the scripts into an automated sync tool so they overwrite on
   every commit. Per-project tweaks (different audit-doc location, custom
   STRUCTURED_DOCS list) get clobbered.

✅ Good — scripts are copied once at adoption. To pick up upstream changes,
   re-copy from templates intentionally. Drift is acceptable; clobbering isn't.
```

---

## Validation status

- **End-to-end spec lifecycle (BACKLOG → spec → ship → archive):** ✅ validated. 12 specs shipped through a pilot project over 2 days.
- **Strategic roadmap row → spec promotion:** ✅ validated.
- **Audit doc → spec promotion:** ✅ validated (e.g. a balance-fix spec sourced from a dated `BALANCE_AUDIT` doc).
- **Audit doc archival cycle (all items resolved → mark Resolved → git mv):** ⚠️ lightly validated. The archive instruction shipped with the protocol but had not yet fired on a real audit at time of writing. Revisit the first time an audit reaches zero ⬜.
- **Cross-source `show open work` script:** ✅ validated on the pilot project's full stack.

If you hit an edge case the protocol doesn't cover, capture it in your protocol repo's own backlog (or open an issue) and surface back to the protocol.

---

## Resources

- `templates/roadmap-system/` (not included in this mirror) — `BACKLOG.md`, `docs/specs/README.md`, `DECISIONS.md`, scripts, `.backlogrc.example` templates referenced throughout this protocol
- [PROJECT_INIT.md](PROJECT_INIT.md) — Step 7a covers scaffolding this system into a new project
- Reference implementation: a personal game project was the pilot for this protocol — see its `CLAUDE.md` "Roadmap & Capture System" section for project-specific glue (verification commands, data-files convention, audit-doc naming)

---

## Version History

| Version | Date | Changes |
|---|---|---|
| 1.7 | 2026-07-05 | Added a protocol-hygiene close-out step: when shipped specs are cited by synced/shared protocols, update the canonical protocol source and re-sync generated project copies instead of patching `docs/protocols/*` directly. |
| 1.6 | 2026-06-06 | Added "Commit discipline (capture & promotion)" subsection under Capture verbs: backlog captures (and promotion-time specs) auto-commit-AND-push immediately without asking, but stage **only** the capture file(s) — never `git add -A` (shared/parallel-session working trees + auto-deploy branches make `-A` a prod-shipping hazard); `pull --rebase` on reject, never force-push. New anti-pattern "Sweeping unrelated changes into a capture commit" documenting a real incident. Codifies that auto-commit is the right default for lightweight capture docs while code keeps the batch-and-QA discipline. |
| 1.5 | 2026-05-17 | Added "Scope and triggers" section after Overview, documenting that the protocol is universally available via a global instruction file, that `BACKLOG.md` at a project root is the structural opt-in trigger, that semantic gestures at open work invoke the protocol even without a `BACKLOG.md` (with offer-to-bootstrap behavior), and that opt-out is just "don't create a BACKLOG.md". Makes the trigger logic and opt-in path explicit in the protocol itself rather than implicit from a global signpost. |
| 1.4 | 2026-05-17 | Consistency fix: unified path placeholder to `<sprint-dir>` everywhere (replaced the two remaining `<DESIGN_DIR>` references in the Overview and Architecture diagram with `<sprint-dir>`, matching the convention introduced in 1.3's new sections). No semantic change. |
| 1.3 | 2026-05-17 | Added "Reference dogfood loop" section framing the roadmap → playtest → backlog → audit → sprint → implement → iterate rhythm. Three new optional-layer sections: "Roadmap layer", "Audit layer", and a substantive "Sprint plans" section formalizing the None / Light / Full intensity tiers, composition gate (3-5 coherent items), one-open-sprint-at-a-time rule, source citation per block/item (`[backlog: …]` / `[roadmap: …]` / `[audit: …]` / `[ad-hoc: …]`), tiered verification rule, close-out-appended-in-place best practice, and archive policy. "Multi-project view" subsection added under Cross-source view with the `~/Projects/*` walking recipe for "what's open across my projects?" Refinements extracted from cross-project usage. |
| 1.2 | 2026-05-05 | "Capture is an inbox dump, not an investigation" clarification added under Capture verbs. Two anti-patterns added: "Investigating bugs at capture time" and "Recommending row close-out without checking sprint-plan staging." Both extracted from pilot-project incidents. |
| 1.1 | 2026-05-04 | Spec-depth rubric promoted into the Promotion Contract as a first-class step. "Ceremony scales with complexity, not with frequency" added as core principle. Sprint plans recognized as optional coordination layer. Architecture diagram redrawn to show the spec / no-spec branch. Lifecycle updated to support no-spec ships. "Drafting a spec for every promotion" elevated to first anti-pattern. |
| 1.0 | 2026-05-04 | Initial release — extracted from a pilot project. Audit-archival cycle marked lightly validated. |

---

**Protocol Version**: 1.7
**Last Updated**: 2026-07-05
