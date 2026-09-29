# ai-knowledge-public

A public mirror of selected protocols and skills from a larger private library — reusable practices for AI-assisted software development, written to be read by both humans and coding agents (Claude Code, and similar). Grows over time as more protocols get mirrored out; not limited to one topic.

## Start here

[`protocols/DEVELOPMENT_LIFECYCLE.md`](protocols/DEVELOPMENT_LIFECYCLE.md) is the map for the development-lifecycle cluster below — it shows how those files fit together and links out to each one.

## What's included

### Development-lifecycle cluster

A project's path from a rough idea through initiation, scaffolding, ongoing work tracking, execution discipline, verification, and multi-session continuity — plus an AI-feature quality band (evals + observability) for projects that make LLM calls.

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
| [`HUMAN_FEEDBACK_CAPTURE.md`](protocols/HUMAN_FEEDBACK_CAPTURE.md) | Capturing operator quality verdicts on generative output (the human half of the eval band) |

### Reference protocols

Standalone technical guides, not tied to the lifecycle spine above.

| Protocol | Covers |
|---|---|
| [`LOCAL_LLM_OLLAMA.md`](protocols/LOCAL_LLM_OLLAMA.md) | Installing, running, and configuring local AI models on Apple Silicon with Ollama |

### Skills

Installable [Agent Skills](https://agentskills.io) — a folder with a `SKILL.md` that an agent loads when a request matches.

| Skill | Covers |
|---|---|
| [`public-presence-audit`](skills/public-presence-audit/) | Audit, clean up and maintain your own public footprint: data-broker opt-outs, home addresses on company registries, stale bios, the Google knowledge panel, dormant accounts. Keeps a private register sorted by how much control you have. UK and US playbooks. |
| [`audit-codebase-architecture`](skills/audit-codebase-architecture/) | A decision-grade audit of a whole existing codebase: reconstructs what was actually built, tests it against the product's intent, and reports findings with evidence and severity. Read-only apart from its report; stops for your correction before the full audit. |
| [`wrap-up`](skills/wrap-up/) | Closes a working session: writes a dated save point, verifies commits and authorised delivery, recommends the next session's model and effort, and hands you a short kickoff prompt. |
| [`catch-up`](skills/catch-up/) | The read-only partner to `wrap-up`: a short "where are we" on the current session (done, state, needs you, next) that writes nothing. |

**Install in Claude (web, desktop, mobile, Cowork):** download the skill's `.skill` file from [`skills/`](skills/) (for example [`public-presence-audit.skill`](skills/public-presence-audit.skill)), then upload it at [claude.ai/settings/skills](https://claude.ai/settings/skills). **Claude Code:** copy the skill's folder into `~/.claude/skills/`. **Codex:** `wrap-up` and `catch-up` include `agents/openai.yaml`; copy the folder into `~/.codex/skills/`. **Other agents:** point them at the skill's `SKILL.md`; it links to the reference files it needs.

## Scope note

This is a **partial mirror**, not the full private library. A few cross-references inside these files name protocols that aren't included here (shown as plain `code text`, not links) — that's expected. Illustrative examples throughout are drawn from real projects but described generically rather than by name.

## License

[MIT](LICENSE).
