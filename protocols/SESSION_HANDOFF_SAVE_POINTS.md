# Session Handoff Save Points

> Dated, in-repo "save point" docs that let any fresh session (or human) resume
> mid-flight technical work cold — no important state lives only in conversation.
>
> **Lifecycle:** the **Resume** phase — see [`DEVELOPMENT_LIFECYCLE.md`](DEVELOPMENT_LIFECYCLE.md) for how this fits with the other workflow protocols.

**Applies to:** Multi-session technical work in any project (code or research), any AI surface
**Last Updated:** 2026-09-09
**Version:** 1.1

---

## Overview

A **save point** is a dated markdown doc, committed to the project repo, that
captures the full working state of an in-flight technical effort at the moment a
session pauses: what's built, what's blocking, the agreed next task as concrete
steps, the invariants a successor must not break, and how to run everything.

It exists because conversation context is the *least* durable place state can
live. Harness features (CLAUDE.md auto-load, auto-memory, transcript resume,
compaction) preserve the **map** — pointers and summaries that degrade with
length. The save point is the **territory**: curated, tool-agnostic, in git,
readable by any assistant or human, immune to context loss.

**Proven:** a personal ML-simulation project's `SIM_AGENT_HANDOFF_2026-06-10.md`
cold-started a fresh session into a multi-week ML training effort (the session
shipped the planned feature in one day) and then absorbed the close-out as an
OUTCOME section — both directions of the lifecycle within 24 hours.

### Distinct from the adjacent patterns

| Pattern | Carries | Cadence |
|---|---|---|
| `NOW.md` (Cowork four-surface model) | standing project state | continuously current |
| `BACKLOG.md` / roadmap (`ROADMAP_AND_BACKLOG.md`) | work items + status | per capture/ship |
| **Save point (this protocol)** | **mid-flight working state of ONE effort** | written at pause, updated at milestone |
| `JOURNAL.md` | history of what happened | append-only |

---

## When to Use

Write a save point when **all three** hold:

1. The effort is **multi-session** (won't finish before the session ends).
2. The working state is **richer than a backlog line** — diagnosed blockers,
   measured findings, invariants, a stepwise plan.
3. A fresh session resuming from scratch would otherwise **re-derive or lose**
   something expensive (an investigation, a design decision, a failed approach).

Skip it for: work finishable now; state fully captured by a spec/backlog item;
purely conversational context (preferences → memory instead).

---

## The Artifact

**Location & name:** `Design-Docs/<TOPIC>_HANDOFF_<YYYY-MM-DD>.md` (or the
project's design-doc home). Dated like audit docs; the date is the save moment,
not an expiry.

**Section skeleton** (adapt, don't worship):

```markdown
# <Topic> — Handoff / Save Point (<date>)

**Read this first if you're a fresh session picking up <topic>.**
[1-line banner: what this doc is + pointer to strategic anchor doc]

## TL;DR — where we are          ← 2-3 paragraphs, state + the agreed pivot
## 1. What's built (verified)    ← table: piece · file · notes; cite tests
## 2. History / what each step taught us   ← prevents re-walking dead ends
## 3. The diagnosed blocker      ← MEASURED, not guessed; cite the evidence
## 4. Findings that belong elsewhere       ← pointers out (audits, backlog)
## 5. THE NEXT TASK              ← concrete numbered steps, file-level detail
## 6+. Context / deferred follow-ons       ← the "why", future options
## N. Gotchas for the next session         ← invariants, env vars, footguns
### How to run                   ← exact commands, speed realities
```

**Quality bar — the parts that make it actually work:**

- **Measured claims only.** Label guesses as guesses. (One reference doc explicitly
  corrected a wrong prior claim and said *"don't trust unmeasured claims — use
  the onDamage hook"* — that sentence saved the successor session from a dead end.)
- **Invariants get named.** Anything a successor could silently break (e.g.
  "any new mutable engine state must be added to snapshot/restore or test X
  fails") goes in Gotchas with the enforcing test cited.
- **The next task is steps, not vibes.** File paths, function names, budget
  estimates, "run this in the background because it takes 80 min".
- **Honest context survives.** If the plan changed or expectations were missed,
  say so and why — the successor needs the real history, not the tidy one.

---

## Lifecycle

1. **Write at the pause.** Before the session ends (or when pivoting away),
   while the state is cheap to capture and expensive to reconstruct.
2. **Update, don't replace, at milestones.** When the named next task ships,
   append an **OUTCOME section** under it (what happened, what was learned,
   the new next rungs) and add a dated banner at the top pointing to it. The
   doc accretes the effort's true history.
3. **Record decisions as they land.** If the sponsor agrees a sequencing or
   scope call mid-effort, write it into the doc *then* ("agreed order (owner,
   <date>): …"), not at the next pause.
4. **Retire when the effort fully lands.** The doc becomes historical record —
   archive per project convention (e.g. `Design-Docs/Archive/`); durable
   outcomes live in specs/roadmap/audits by then.

---

## Pointer Discipline (how a fresh session finds it)

The save point is only as good as its inbound pointers. On every save:

1. **Strategic anchor doc** (initiative/roadmap doc) gets a banner at the top:
   *"▶ Active handoff (<date>): work is mid-flight, read <handoff doc> first."*
2. **Assistant auto-memory** gets one entry: status + "resume via <doc> §X".
   Update it at every milestone — a stale memory pointer is worse than none.
3. **Kickoff prompt.** When the user starts the fresh session, the opening
   message should name the handoff doc explicitly ("Read X FIRST"). Offer this
   prompt to the user when recommending a session break.
4. `CLAUDE.md` / `AGENTS.md` only if the effort is the project's primary active
   workstream — and remove the pointer when it isn't (slim-pointer rule).

---

## Anti-Patterns

- **Transcript-as-handoff.** Relying on `--resume`/compaction for multi-session
  technical state. Summaries lose invariants and measured numbers first.
- **Save point as second backlog.** Work items belong in BACKLOG/audits; the
  save point *points* at them (its §4) rather than tracking them.
- **Replace-on-update.** Overwriting the doc at each milestone destroys the
  history of what was tried. Append OUTCOME sections; keep the lineage.
- **Unmeasured blocker claims.** A guessed diagnosis sends the successor down
  the wrong path with the full confidence of the written word.
- **Orphan save points.** No banner on the anchor doc, no memory entry — the
  doc exists but no fresh session will ever read it.
- **Eternal save points.** If the doc outlives the effort by months, it has
  become a stale second source of truth — archive it.

---

## Resources

- Reference pattern: a personal ML-simulation project's
  `Design-Docs/SIM_AGENT_HANDOFF_2026-06-10.md` (full skeleton, OUTCOME-section
  milestone update, pointer discipline in action)
- Related: `ROADMAP_AND_BACKLOG.md` (work tracking the save point points into),
  `CLAUDE_INSTRUCTION_LAYERS.md` (slim-pointer rule), `COWORK_PROJECT_INIT.md`
  (NOW.md/JOURNAL.md standing-state model for research workspaces),
  `LLM_CONTEXT_MEMORY_ARCHITECTURE.md` (why conversation context degrades), and
  `CROSS_AGENT_HANDOFF_BUS.md` when unfinished work must cross an agent,
  platform, or project boundary rather than only resume inside one project.

---

| Version | Date | Changes |
|---|---|---|
| 1.1 | 2026-09-09 | Distinguished in-project save points from the cross-agent handoff bus and linked the new governing protocol. |
| 1.0 | 2026-06-11 | Initial release. Generalized from a personal ML-simulation project's session handoff doc after it proved both lifecycle directions (cold-start resume + milestone close-out) within 24 hours. |
