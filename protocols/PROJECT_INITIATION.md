# Project Initiation

> Tiered protocol for translating a project's vision and requirements into an initial spec and (optionally) a roadmap. Runs BEFORE ongoing work flows through `ROADMAP_AND_BACKLOG.md`. Distinct from `PROJECT_INIT.md`, which covers technical repo setup.
>
> **Lifecycle:** the **Conceive** phase — see [`DEVELOPMENT_LIFECYCLE.md`](DEVELOPMENT_LIFECYCLE.md) for how this fits with the other workflow protocols.

**Applies to:** Any new project being scoped — game, app, platform, tool, or service. The default execution mode is a Claude-led interview, not a template fill-in. Tiered intensity (None / Light / Full) keeps the ceremony matched to the work.
**Last Updated:** 2026-06-06
**Version:** 1.2

---

## Table of Contents

- [Overview](#overview)
- [Scope and triggers](#scope-and-triggers)
- [Decision rule — do we need initiation docs at all?](#decision-rule--do-we-need-initiation-docs-at-all)
- [Three intensity tiers](#three-intensity-tiers)
- [Interview as default creation mode](#interview-as-default-creation-mode)
- [Spec → Roadmap bridge](#spec--roadmap-bridge)
- [Handoff to PROJECT_INIT.md](#handoff-to-project_initmd)
- [Useful section vocabulary](#useful-section-vocabulary)
- [Anti-patterns](#anti-patterns)
- [Resources](#resources)

---

## Overview

This protocol governs the **conceptual initiation** of a new project — the act of translating a vision and a rough requirement set into an initial spec, and (optionally) into a phased roadmap that seeds the project's ongoing work.

It runs **before** the ongoing work flows through `ROADMAP_AND_BACKLOG.md`. The roadmap/backlog system assumes a project that already knows what it is; this protocol covers the upstream step of deciding what the project is in the first place.

It is **distinct from** `PROJECT_INIT.md`, which covers the technical side of repo setup — `.gitignore`, `.env.example`, `CLAUDE.md` scaffolding, README, repo registrations. Initiation answers "what are we building?"; PROJECT_INIT answers "now wire up the repo." The two chain: initiation → repo init → ongoing work via roadmap/backlog/sprint.

> **Core principle:** Initiation ceremony should match the project's shape and stakes. A throwaway script gets a README; a small app gets a one-page spec; a platform with multiple integrated systems gets a multi-doc chain. Default to lighter than you think — overspecifying at initiation produces shelfware, and the gap is easy to fill later.

---

## Scope and triggers

This protocol is referenced from a global instruction file loaded into every AI coding session. It is universally available across all projects; no registry or per-project flag is required.

**Structural trigger:** Claude enters an empty or near-empty new repo where no `BACKLOG.md`, design docs, or other initiation artifacts exist yet — i.e. the project hasn't been scoped. Initiation is the protocol that applies until the first spec lands.

**Semantic trigger:** the user says any of "I'm starting a new project," "I want to build X," "scoping a new thing," "let's plan a new project," "I have an idea for a project," or any equivalent gesture that signals the work isn't yet shaped. Trigger on intent, not literal phrasing.

**Opt-out:** small utilities, glue scripts, throwaway prototypes, and projects whose scope is self-evident skip this entirely. The None tier (README only) is the default for those. When in doubt, default to Light — cheap to create, easy to discard.

---

## Decision rule — do we need initiation docs at all?

Three signals trigger **Yes, write something**:

1. **Non-obvious scope.** The project isn't a one-liner — there are choices to make about what's in and what's out, and those choices benefit from being written down before code lands.
2. **Multi-week scope.** The project is going to outlive a single sitting. Without an artifact, weeks-later-you (or a fresh Claude session) loses the original framing.
3. **Multi-session / multi-collaborator work.** The project will be touched across more than one Claude session, or by more than one person. The artifact is the shared context handoff.

Hit any one and Light tier is at least worth a pass. Hit two or more and you're probably in Full territory.

**Default to None when:** trivial utility, glue script, throwaway prototype, or a project whose scope is self-evident ("scrape this URL into a CSV"). A README is sufficient.

**When in doubt, default to Light.** A one-page spec costs ~15 minutes; throwing it away later costs nothing. Skipping it on a project that turns out to need it costs a re-litigation of every early decision.

---

## Three intensity tiers

### None — README only

For utilities, scripts, throwaways, and projects whose scope is self-evident. No spec, no roadmap, no design docs. The README covers what the thing does, how to run it, and any non-obvious gotchas. The project's `CLAUDE.md` (per `PROJECT_INIT.md`) carries the rest.

This is the right default for most one-off work. Don't manufacture initiation ceremony for projects that don't need it.

### Light — single initiation artifact (default for most new projects)

One free-form Markdown artifact, 1-3 pages, output of a Claude-led interview. Captures the vision, the in/out scope, the key decisions made during scoping, and what success looks like. There is **no required section list** — the project shape dictates the content, and the interview's natural arc produces the structure.

Filename is project-defined. Common patterns: `docs/INITIAL_SPEC.md`, `docs/VISION.md`, `docs/BRIEF.md`. Pick one that signals the doc's role; consistency across projects matters less than the artifact itself existing.

The Light artifact is the **input** to whichever roadmap/backlog pattern the project adopts. It is not maintained as a living spec post-init — it captures the moment of decision, and subsequent change flows through the project's ongoing systems.

### Full — multi-artifact chain or pair

For projects with enough scope, ambiguity, or staging to need more than a single doc. The shape is project-dependent. Three reference shapes from actual practice:

**Shape 1 — Game / creative project: master design doc.** A single substantive design doc covering vision, inspirations, world/setting, mechanics, art direction, target experience, and phased milestones. Long-form, narrative-heavy where appropriate. Reference: a creative project's `Design-docs/01_MASTER_DESIGN_DOC.md`.

**Shape 2 — Product / app with evolving scope: phased requirements chain.** Multiple artifacts produced in sequence as the project's scope tightens. Typical chain: a Phase 1 requirements brief → a unified target spec that absorbs the brief and extends it → a customer-facing app brief. Each artifact builds on the prior and captures a moment of scope-evolution rather than overwriting. Reference: a solo AI content app's `docs/01_phase1_requirements_spec.md` chain.

**Shape 3 — Platform / system project: conceptual primer + target-state spec pair.** Two artifacts working together — a conceptual primer that explains the system's purpose, principles, and architectural posture; and a target-state spec that says concretely what the built system looks like at the end of initiation. The primer is read-once-then-internalize; the spec is the implementation guide. Reference: a personal AI-context system's `docs/PRIMER_*.md` + `docs/SPEC_*.md` pair.

A standard section vocabulary (Brief, Key Features, Scope, User Journeys, Milestones) can be drawn on during interviews regardless of shape — see [Useful section vocabulary](#useful-section-vocabulary) below. Don't treat it as a checklist — let Claude surface those sections from the interview when they're earning their keep.

---

## Interview as default creation mode

The Light or Full artifact is produced by a **Claude-led conversational interview**, not by the user filling out a template. The interview is the protocol's primary execution mode; the artifact is its output.

### Universal opening questions

Always ask these, regardless of project shape. They are the smallest set that ensures the doc has a spine:

- What are we building?
- Why does this exist — what problem does it solve, what gap does it fill?
- Who's it for — primary users, audience, or the user being you?
- What does success look like — observable signals that the project is doing its job?
- What's explicitly out of scope — the negative space that bounds the work?

The opening turn typically takes the first 5-10 minutes of the interview. The answers seed the rest of the conversation.

### Interview technique

The cardinal rule: **one question at a time.** Never send a single message asking the user to answer multiple distinct questions. Walls of questions are unprocessable and explicitly disliked.

Acceptable patterns:

- Ask one question, wait for the answer, then ask the next.
- Preview a list of upcoming questions upfront for context ("To scope this I'll want to know about audience, success criteria, and what's out of scope") — but then pick them off one at a time across turns.

Not acceptable: a single message containing three or more distinct questions expecting answers.

Other technique guidance:

- Prefer open questions ("what does success look like?") over closed ("is X your goal?") in early turns. Closed questions are appropriate later, for confirming understanding.
- Let the user's answer guide the next question rather than following a fixed sequence. If an answer surfaces something interesting, drill into it before moving on.
- Mirror back understanding before moving to a new topic ("So success means X and Y — confirming before I move on") — but keep mirrors brief, not a wall of text.
- If three or more questions feel necessary in the same area, that's a signal to slow down: pick the one whose answer most shapes what comes next, ask that, iterate.

### Project-shape follow-up modules

Claude infers the project's shape from the opening turn and asks adaptive follow-ups. Three common modules:

**Game / creative.** Vision narrative (the experience you want the player/reader to have), inspirations and reference works, world/setting depth, core mechanics or beats, target experience texture.

**Product / data.** User personas and primary journeys, core entities and how they relate, integrations and external surfaces, data model invariants, deployment shape.

**Tool / utility.** Key features and surface, input/output contracts, technical constraints, dependencies.

**AI-powered overlay (applies on top of any module).** If the project makes LLM/AI calls and is heading to production, treat **evals and observability as first-class scope from the start**, not a later bolt-on — the most common way AI projects spin their wheels is shipping quality changes blind. Surface during the interview: which AI output's quality actually matters, how it will be measured offline (a golden-set regression eval), and how runtime behaviour (latency, errors, cost) will be monitored. See [AI_EVALS.md](AI_EVALS.md) and [AI_OBSERVABILITY.md](AI_OBSERVABILITY.md).

Module selection is by inference, not by checklist. If the project resists a single module — e.g. a creative project with a strong product layer — pull from multiple.

### Iteration loop

Draft → user reviews → Claude updates → loop until approved. The first draft is rarely the final draft; the interview is structured as a converging conversation, not a one-shot. Expect 2-4 iteration rounds for a Light artifact and 3-6 for a Full chain.

### Time budgets

- **Light tier:** ~10-20 minutes of interview, plus iteration.
- **Full tier:** may span multiple sessions, particularly when the artifact chain is long or the design space is genuinely open.

If a Light interview is running past 30 minutes, the project probably wants Full intensity — surface that observation back to the user rather than continuing to compress.

---

## Spec → Roadmap bridge

The initial spec doesn't replace the project's ongoing roadmap — it seeds it. There are two valid bridge patterns:

**Pattern A — Embedded.** The initial spec ends with a "Phase plan" or "Milestones" section that lays out the project's near-term work in order. After approval, that section is extracted into a standalone `ROADMAP.md` (or equivalent) and the project picks up the ongoing `ROADMAP_AND_BACKLOG.md` protocol from there.

Use Pattern A when the scope is well-bounded and the phase plan falls out naturally from the spec's structure.

**Pattern B — Sequential.** The initial spec is approved first, then a dedicated `ROADMAP.md` is drafted in a follow-up interview. The roadmap is its own artifact, not extracted from the spec.

Use Pattern B when roadmap shaping benefits from a separate working session — typically when the scope is broad enough that the roadmap needs its own design pass, or when stakeholders for the spec and the roadmap differ.

In both cases, the roadmap output feeds the project's ongoing `ROADMAP_AND_BACKLOG.md` flow once the project is live. Initiation produces the seed; the ongoing protocol carries the lifecycle.

---

## Handoff to PROJECT_INIT.md

Once the initiation spec is approved, the technical side of repo setup is governed by `PROJECT_INIT.md`. That protocol covers `.gitignore`, `.env.example`, dotenv loading, dependency baseline, `CLAUDE.md` scaffolding, README, and repo registrations.

The two protocols chain in order:

```
PROJECT_INITIATION.md  →  PROJECT_INIT.md  →  ROADMAP_AND_BACKLOG.md
   (what are we           (wire up the         (ongoing capture,
    building?)             repo)                spec, ship, archive)
```

The initiation artifact is the input to `PROJECT_INIT.md`'s Step 3 (CLAUDE.md scaffolding) — the project's context, tech stack, and architecture overview pull directly from the approved spec. Don't redraft them; lift them.

---

## Useful section vocabulary

A handful of section framings tend to earn their keep across project shapes. Reach for them during interviews regardless of tier — as vocabulary, not a checklist:

- **Brief** (what / who / why / success) — universally applicable; close to the universal opening questions of this protocol.
- **Scope in/out** — bounds the work explicitly. Always worth capturing.
- **User journeys** — happy-path flows. Useful for any project with a user surface.
- **Milestones / phase plan** — the seed for the roadmap bridge.

Pull the ones that fit the project; skip the ones that don't. The interview's natural arc decides which sections earn space in the artifact.

---

## Anti-patterns

### Filling out a fixed template manually

```
❌ Bad — the user types answers into a pre-fab section list. Defeats the
   interview. The artifact ends up structured around the template
   rather than around the project.

✅ Good — Claude leads the interview. The artifact is structured by
   the conversation's natural arc. The standard section vocabulary
   can be drawn on, but no rigid template is the form factor.
```

### Insisting on Full tier for a small project

```
❌ Bad — drafting a primer + spec pair for a one-page utility because
   "we should do this properly." Produces shelfware. The artifact
   carries less signal than the README it replaced.

✅ Good — apply the decision rule honestly. Most projects need Light
   or None. Full is for genuine multi-system or multi-week scope.
   Defaulting lighter is recoverable; defaulting heavier creates
   sunk-cost pressure to keep the artifact alive.
```

### Skipping the spec entirely on multi-week projects

```
❌ Bad — "we'll figure it out as we go" on a project that's going
   to take three weeks and span six Claude sessions. Each session
   re-litigates scope. Decisions get lost. Scope creeps without
   notice.

✅ Good — pay the 15-minute Light-tier cost. The artifact pays itself
   back the first time a session lands cold and reads it to catch up.
```

### Treating the initial spec as immutable

```
❌ Bad — refusing to update the initiation artifact when scope
   evolves, on the grounds that "that was the original plan." The
   doc rots. Future sessions read stale framing.

✅ Good — capture revisions explicitly (a sequential chain, each
   artifact capturing a moment of scope evolution rather than
   overwriting). Or, for Light tier, amend in place with a changelog
   at the bottom. The spec evolves; the system tolerates that.
```

### Pattern-matching every new project to a fixed section list

```
❌ Bad — assuming every project needs a Definition of Done, Core
   Entities, Tech Constraints, Non-Functional Requirements, and
   Execution Contract section, regardless of whether the project
   has anything substantive to say in those slots.

✅ Good — let the project shape the artifact. A creative project
   may have no "Core entities" worth writing down but a long
   "World / setting" section. A platform may have rich entities
   but no UX section. Match the artifact to the project, not
   the project to the artifact.
```

---

## Resources

- [PROJECT_INIT.md](PROJECT_INIT.md) — Technical repo setup; runs after this protocol completes.
- [ROADMAP_AND_BACKLOG.md](ROADMAP_AND_BACKLOG.md) — Ongoing capture / spec / ship / archive system; runs after the project is initialized.
- A creative project's `Design-docs/01_MASTER_DESIGN_DOC.md` — Reference for the game/creative Full-tier shape.
- A solo AI content app's `docs/01_phase1_requirements_spec.md` chain — Reference for the product/app Full-tier shape (sequential, scope-evolving chain).
- A personal AI-context system's `docs/PRIMER_*.md` + `docs/SPEC_*.md` pair — Reference for the platform/system Full-tier shape.

---

## Version History

| Version | Date | Changes |
|---|---|---|
| 1.2 | 2026-05-17 | add Interview technique subsection (one question at a time cardinal rule) |
| 1.1 | 2026-05-17 | Retire legacy template reference; rename salvage section to standalone vocabulary description. |
| 1.0 | 2026-05-17 | Initial release. Tiered intensity (None / Light / Full), interview as default creation mode, universal opening questions plus project-shape follow-up modules, spec → roadmap bridge with embedded vs sequential patterns, explicit handoff to `PROJECT_INIT.md`. Extracted from a working conversation about the lean approach wanted for project initiation across a personal project portfolio. |

---

**Protocol Version**: 1.2
**Last Updated**: 2026-05-17
