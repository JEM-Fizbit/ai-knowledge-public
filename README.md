# ai-knowledge-public

A public mirror of selected protocols from a larger private protocol library — reusable practices for AI-assisted software development, written to be read by both humans and coding agents (Claude Code, and similar).

Currently mirrors the **development-lifecycle cluster**: the protocols that cover a project's path from a rough idea through initiation, scaffolding, ongoing work tracking, execution discipline, verification, and multi-session continuity — plus an AI-feature quality band (evals + observability) for projects that make LLM calls.

## Start here

[`protocols/DEVELOPMENT_LIFECYCLE.md`](protocols/DEVELOPMENT_LIFECYCLE.md) is the map — it shows how the other files fit together and links out to each one.

## What's included

| Protocol | Covers |
|---|---|
| [`DEVELOPMENT_LIFECYCLE.md`](protocols/DEVELOPMENT_LIFECYCLE.md) | Navigational map across the whole lifecycle |
| [`PROJECT_INITIATION.md`](protocols/PROJECT_INITIATION.md) | Turning a vision into an initial spec (Conceive) |
| [`PROJECT_INIT.md`](protocols/PROJECT_INIT.md) | Technical repo setup (Scaffold) |
| [`ROADMAP_AND_BACKLOG.md`](protocols/ROADMAP_AND_BACKLOG.md) | Ongoing capture → spec → ship → archive (Track & Plan) |
| [`SOLUTION_DESIGN_PRINCIPLES.md`](protocols/SOLUTION_DESIGN_PRINCIPLES.md) | Design discipline (Execute) |
| [`BEST_PRACTICES_FIRST.md`](protocols/BEST_PRACTICES_FIRST.md) | Escalation rule for symptom-fix loops (Execute) |
| [`QA_PROTOCOL.md`](protocols/QA_PROTOCOL.md) | Tiered verification before shipping (Verify) |
| [`SESSION_HANDOFF_SAVE_POINTS.md`](protocols/SESSION_HANDOFF_SAVE_POINTS.md) | Multi-session continuity docs (Resume) |
| [`AI_EVALS.md`](protocols/AI_EVALS.md) | Regression evals for AI/LLM output quality |
| [`AI_OBSERVABILITY.md`](protocols/AI_OBSERVABILITY.md) | Runtime observability for AI/LLM calls |

## Scope note

This is a **partial mirror**, not the full private library. A few cross-references inside these files name protocols that aren't included here (shown as plain `code text`, not links) — that's expected. Illustrative examples throughout are drawn from real projects but described generically rather than by name.

## License

No license file yet — treat as "all rights reserved, provided for reading and adaptation" until one is added.
