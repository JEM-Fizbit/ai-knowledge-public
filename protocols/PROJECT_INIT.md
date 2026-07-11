# Project Initialization

> Step-by-step checklist for setting up a new project repo with Claude Code and (optionally) a personal AI-context repo integration.
>
> **Lifecycle:** the **Scaffold** phase — see [`DEVELOPMENT_LIFECYCLE.md`](DEVELOPMENT_LIFECYCLE.md) for how this fits with the other workflow protocols.

**Applies to:** All new project repositories
**Last Updated:** 2026-06-27
**Version:** 1.9

---

## Table of Contents

- [Overview](#overview)
- [When to Use](#when-to-use)
- [Quick Start](#quick-start)
- [Implementation](#implementation)
- [Common Patterns](#common-patterns)
- [Anti-Patterns](#anti-patterns)
- [Troubleshooting](#troubleshooting)
- [Resources](#resources)

---

## Overview

Every new project needs a consistent foundation: secrets management, Claude Code context, documentation, and registration in the knowledge ecosystem. This protocol ensures nothing gets missed.

### Key Benefits

- Consistent project structure across all repos
- Claude Code has full project context from the first session
- Project-specific protocols are surfaced by exact trigger, not left to generic discovery
- Secrets never land in git history
- Projects are discoverable in your protocol repo (and a personal AI-context repo, if you keep one)

---

## When to Use

| Scenario | Use This Protocol? |
|----------|-------------------|
| New personal project | Yes — full checklist including personal AI-context repo registration |
| New work project (a different org) | Yes — skip the personal AI-context repo registration |
| Forking or cloning an existing repo | Yes — adapt steps (skip repo creation, focus on CLAUDE.md + env) |
| Throwaway prototype or experiment | Optional — at minimum do env + .gitignore |

---

## Quick Start

Condensed checklist — see [Implementation](#implementation) for details on each step.

```
 1. Create GitHub repo + clone with correct SSH alias
 2. .gitignore — ensure .env, .env.local, .env*.local, and project runtime state are excluded
 3. .env.example — template with all required vars (no real values)
 4. .env — actual keys (copied from .env.example, never committed)
 5. dotenv — install and import so .env is loaded at runtime
 6. Dependency/tooling baseline — package manager, runtime pins, system/local dependencies, script safety categories, current stable core packages, peer compatibility, migration notes
 7. CLAUDE.md — from `PROJECT_CLAUDE_TEMPLATE.md` for code projects (only file needed — code-native equivalents handle mutable state; see Step 3). Non-code GitHub repos: `PROJECT_CLAUDE_TEMPLATE_RESEARCH.md` + `NOW.md` + `JOURNAL.md`. Cowork-based research / strategy / writing projects: use `COWORK_PROJECT_INIT.md` instead. Consult `CLAUDE_INSTRUCTION_LAYERS.md` (slim-pointer section) before drafting.
 7a. (Optional) Roadmap & backlog system — scaffold from `templates/roadmap-system/` if the project will accumulate ideas/bugs over time
 7b. Protocol surfacing — identify relevant protocol triggers, sync local copies into `docs/protocols/`, and add exact trigger -> local protocol lines to `CLAUDE.md` / `AGENTS.md`
 8. README.md — project overview, quick start, tech stack
 9. Register in your protocol repo's README projects table
 9a. Update your private assets register — add a row for the project (+ rows for any new services)
10. Register in your personal AI-context repo (personal projects only)
11. Add repo to a scheduled documentation-audit routine, if you run one
12. Verify git credentials (multi-account switching)
13. Commit and push
```

---

## Implementation

### Step 1: Create Repo & Clone

Create the repo on the correct GitHub account and clone using the appropriate SSH alias.

```bash
# Personal account
gh auth switch --user your-personal-username
gh repo create your-username/project-name --private
git clone git@github-personal:your-username/project-name.git

# Work or other org — use the appropriate SSH alias and org
git clone git@github.com:OrgName/project-name.git
```

See `GITHUB_MULTI_ACCOUNT.md` for SSH alias setup.

### Step 2: Secrets & Environment

#### .gitignore
Ensure these entries exist:
```
.env
.env.local
.env*.local
*.pem
```

Add project-specific runtime paths before starting agents, LaunchAgents, sync loops, OAuth smoke flows, or local desktop launchers. Runtime paths include token caches, daemon logs, lock/health files, generated latency snapshots, sync cursors, and smoke/canary artifacts. If a runtime file was accidentally committed, remove it from the index while preserving the local file:

```bash
git rm --cached path/to/runtime-state.json
```

See `GIT_CONVENTIONS.md` -> Runtime State and Daemons.

#### .env.example
Create a committed template with empty values:
```bash
# Project Name — Environment Variables
# Copy this file to .env and fill in your keys

REQUIRED_API_KEY=
ANOTHER_KEY=

# Server configuration
PORT=3000
NODE_ENV=development
```

#### .env
Copy `.env.example` to `.env` and fill in real values. **Never commit this file.**

#### Load .env at runtime
Install dotenv (or equivalent) and import it as the first line of your server entry point:

```bash
npm install dotenv
```

```typescript
// First import in server entry point
import "dotenv/config";
```

### Step 3: CLAUDE.md (slim-pointer architecture)

**Pick the right path:**
- **Code projects** (web app, CLI, library, service) — most common case → `PROJECT_CLAUDE_TEMPLATE.md` only. No NOW.md / JOURNAL.md (see "Why no NOW.md / JOURNAL.md for code projects" below).
- **Non-code GitHub repos** (rare — docs-only, writing-only, evaluation workspaces that need versioned history in git) → `PROJECT_CLAUDE_TEMPLATE_RESEARCH.md` + `NOW.md` + `JOURNAL.md` (four-surface model).
- **Cowork-based research / strategy / writing projects** (no GitHub repo, lives in a Cowork workspace folder) → use `COWORK_PROJECT_INIT.md` instead. PROJECT_INIT does not cover this path.

```bash
# Code project (most common):
cp ~/Projects/your-protocol-repo/templates/PROJECT_CLAUDE_TEMPLATE.md ./CLAUDE.md

# Non-code GitHub repo:
cp ~/Projects/your-protocol-repo/templates/PROJECT_CLAUDE_TEMPLATE_RESEARCH.md ./CLAUDE.md
cp ~/Projects/your-protocol-repo/templates/_TEMPLATE_NOW.md ./NOW.md
cp ~/Projects/your-protocol-repo/templates/_TEMPLATE_JOURNAL.md ./JOURNAL.md
```

**Why no NOW.md / JOURNAL.md for code projects.** Mutable state and running history are already handled by code-native equivalents:
- `BACKLOG.md` (per [ROADMAP_AND_BACKLOG.md](ROADMAP_AND_BACKLOG.md)) — open ideas, bugs, feature requests, in-progress threads
- `docs/DECISIONS.md` (ADR pattern) — architecture decisions and rationale
- `git log` / commit history — running history of what changed and why

NOW.md and JOURNAL.md are the **four-surface model**, which works because non-code projects have no git equivalent — the markdown IS the deliverable. For code, adding NOW.md / JOURNAL.md duplicates state already tracked by git, BACKLOG.md, and ADRs, and creates drift between parallel histories.

**Before filling CLAUDE.md:** consult `CLAUDE_INSTRUCTION_LAYERS.md` — specifically the "slim-pointer, not dual-copy mirror" section. Target ≤ 50 lines for non-code projects, ≤ 80 for code projects. Most bloat enters at draft time, not edit time.

**Minimum sections to fill in:**
- Project Context (name, description, status)
- Tech Stack
- Development Commands
- Architecture Overview (data flow + directory structure)
- Environment Variables (required + optional tables)
- Protocol Triggers (exact local protocol filenames for project-specific domains)
- Key Files
- Common Gotchas (add as they're discovered)

**Remove template sections that don't apply** (e.g., Database Operations if no DB, Design System if not user-facing).

### Step 3a: Dependency / Tooling Baseline

Before committing the initial scaffold, apply `DEPENDENCY_HYGIENE.md`:

- Prefer current stable major versions for the core stack.
- Check latest package versions, peer compatibility, and official framework docs before pinning.
- Avoid deprecated examples and old scaffold defaults.
- Pick the package manager from the lockfile/workflow, then pin or document it (`packageManager`, Corepack note, or explicit install command).
- Record runtime expectations (`.nvmrc`, `.python-version`, `engines`, Docker/serverless runtime) when version drift can change behavior.
- Document system/local dependencies that are outside the language package manager, such as cloud CLIs, Playwright browser binaries, native libraries, macOS tools, hardware constraints, and model/data caches.
- Categorize scripts that touch generated files, external APIs, databases, cloud resources, deployments, or irreversible state.
- If a current major version is deferred, document the reason and next review trigger in `CLAUDE.md` or maintenance notes.
- Run the initial install, build, lint, and smoke checks before treating the scaffold as production-ready.

### Step 3b: Roadmap & Backlog System (Optional)

For any project that will accumulate ideas, bugs, or feature requests over time, scaffold the layered roadmap/backlog/spec system. Skip for tiny utilities or projects already on a formal tracker (Linear, Jira).

```bash
# Minimum stack — works for any active dev project
cp ~/Projects/your-protocol-repo/templates/roadmap-system/BACKLOG.md.template BACKLOG.md
mkdir -p docs/specs/archive
cp ~/Projects/your-protocol-repo/templates/roadmap-system/docs-specs-README.md.template docs/specs/README.md
mkdir -p scripts
cp ~/Projects/your-protocol-repo/templates/roadmap-system/scripts/*.sh scripts/
chmod +x scripts/backlog.sh scripts/show-open-work.sh

# Decision log — recommended for any project with non-trivial design surface
cp ~/Projects/your-protocol-repo/templates/roadmap-system/DECISIONS.md.template docs/DECISIONS.md
# (or place it under the project's design-docs directory)

# Optional layers (configure in .backlogrc if used)
cp ~/Projects/your-protocol-repo/templates/roadmap-system/.backlogrc.example .backlogrc
# Edit .backlogrc to enable strategic roadmap / audit-doc / structured-docs layers
```

Add a "Roadmap & Backlog System" section to `CLAUDE.md` listing project-specific glue (verification commands, data-files convention, audit-doc naming if used) — see `templates/PROJECT_CLAUDE_TEMPLATE.md` for the section template. The protocol itself is canonical at [ROADMAP_AND_BACKLOG.md](ROADMAP_AND_BACKLOG.md).

**Important:** the protocol's promotion contract uses a spec-depth rubric — most promotions are *not* full specs. The CLAUDE.md section should reflect this rather than unconditionally instruct "draft a spec on promotion." Pattern-matching every promotion to the standard template is the most common failure mode of this system; the project CLAUDE.md is where that mistake gets locked in if not worded carefully. See ROADMAP_AND_BACKLOG.md → "Promotion contract" → "Spec-depth rubric".

### Step 3c: AI Evals & Observability Scaffold (Optional — AI-powered projects)

For any project that makes LLM/AI calls and is heading to production, scaffold evals and observability **from the start** rather than bolting them on later (the gap that lets AI features regress silently). Minimum:

- An `evals/<target>/` directory with a golden set pulled from real data + a runner with a regression gate (`pnpm eval:<target>`). See [AI_EVALS.md](AI_EVALS.md).
- A `traced()` wrapper around AI calls capturing latency / outcome / a traceId, written to your own datastore (no migration needed to start). See [AI_OBSERVABILITY.md](AI_OBSERVABILITY.md).

Add the change-triggered eval rule to the project's `CLAUDE.md` QA section (run + report the eval when an AI prompt/model/criteria changes) and wire the weekly eval+obs digest per the operating model in those protocols. Skip for projects with no AI calls.

### Step 3d: Protocol Surfacing (Required for durable repos)

Generic "use the protocol repo" pointers are not enough. During project init, make the relevant protocol triggers local and exact so future agents can discover them without re-deriving the project domain.

**Process:**

1. Scan your protocol repo's trigger index and the planned stack/domain for protocols likely to fire repeatedly or carry high risk if missed.
2. Select the smallest useful set, usually 3-10 protocols. Include domain protocols, runtime/infrastructure protocols, and AI-quality protocols (`AI_EVALS.md`, `AI_OBSERVABILITY.md`) when they are central to the repo.
3. Sync those protocols into `docs/protocols/` via a sync tool when the project will keep them current, or copy them manually for a small/static repo.
4. Add a terse `## Protocol Triggers` section to the project `CLAUDE.md` / `AGENTS.md` with exact trigger -> exact local file references.
5. Keep the section as a routing table. Do not paste protocol content into the project instructions.

Template:

```markdown
## Protocol Triggers

Before work in these areas, read the local synced protocol:

- **[domain / workflow trigger]** -> `docs/protocols/[PROTOCOL_NAME].md`
- **[domain / workflow trigger]** -> `docs/protocols/[PROTOCOL_NAME].md`
```

If no project-specific protocol applies beyond global rules, write `No project-specific synced protocols yet.` and revisit when the repo graduates from prototype to durable project.

### Step 4: README.md

Create a project README covering:
- What the project does (1-2 sentences)
- Features (bullet list)
- Tech stack (table)
- Quick start (install, env setup, run)
- Scripts reference
- Architecture overview (brief)
- License

### Step 5a: Update Assets Register

Add a row to your private assets register before closing the session, if you keep one — a running inventory of which services, cloud accounts, and repos each project depends on. See your register's own conventions for the full maintenance contract.

If the project uses any cloud service not yet in your register, add that entry too (service name, provider, category, account email, auth method).

### Step 5b: Register in your protocol repo

Add a row to the projects table in your protocol repo's `README.md`:

```markdown
| project-name | Brief description | Relevant protocols |
```

Protocols should list which protocols the project uses (e.g., Git, GitHub Multi-Account, Supabase, OpenAI, etc.).
This list should match the repo's `Protocol Triggers` section at the category level; if the project syncs a local copy, name that protocol explicitly.

### Step 6: Register in a personal AI-context repo (optional, personal projects only)

**Only if you maintain a personal AI-context repo alongside your protocol repo, and only for personal projects — not work/client projects.**

Add an entry under the appropriate category section:

```markdown
### ProjectName
- **What:** Brief description.
- **Stack:** Key technologies.
- **Repo:** `git@github-personal:your-username/project-name.git`
```

If no existing category fits, create a new `##` section.

### Step 7: Verify Git Credentials

Confirm the correct GitHub account is active for this directory:

```bash
# Check SSH remote is using correct alias
git remote -v

# Check gh CLI account
gh auth status

# If wrong account (common in Claude Code shells):
unset GH_TOKEN GITHUB_TOKEN
gh auth status
```

See `GITHUB_MULTI_ACCOUNT.md` for common multi-account gotchas.

### Step 8: Add to a scheduled documentation-audit routine (optional)

If you run a scheduled agent that checks project documentation for staleness, broken cross-references, terminology drift, version coherence, and TODO accumulation, register new projects with it as part of init.

**Pattern worth adopting:** segregate the audit trigger by which account/environment owns the work (e.g., a personal-account trigger vs. a separate one per client/org), so work-product visibility stays on the right account and there's no cross-account credential handoff when registering a new repo.

For a multi-repo auditor, the lowest-friction design is to make the prompt repo-agnostic and let each repo self-describe its own audit needs via an optional config file (declaring things like staleness-check paths, version sources, retired terminology, and protected paths) — omitted fields just fall back to safe generic checks. Adding a repo is then: drop the config file, then register the repo's URL with the trigger.

### Step 9: Commit & Push

```bash
git add .gitignore .env.example CLAUDE.md README.md
git commit -m "Project init: CLAUDE.md, README, env config"
git push origin main
```

Commit any protocol-repo or personal-context-repo registrations separately in their respective repos.

---

## Common Patterns

### Pattern A: Full-Stack TypeScript (React + Express/Node)

```
Quick Start fully applied.
dotenv for env loading.
Zod for shared schemas.
A protocol-sync tool for keeping synced protocol copies current (if using multiple protocols).
```

### Pattern B: Work Project (different org from your personal account)

```
Steps 1-5b, 8, 11-12.
Skip Step 6 (personal AI-context repo).
Use work SSH alias and org in Step 1.
Ensure `gh` keyring has the work account active (`gh auth switch --user <work-user>`). See GITHUB_MULTI_ACCOUNT.md.
```

### Pattern C: Quick Prototype

```
Minimum: Steps 2-3 (.gitignore, .env.example, .env, CLAUDE.md).
Skip registration steps — add later if the project graduates to active.
```

---

## Anti-Patterns

### Hardcoding API keys with fallback values

```typescript
// ❌ Bad — keys leak into git history even as "defaults"
const API_KEY = process.env.API_KEY || "sk-actual-key-here";

// ✅ Good — empty fallback, app fails fast if .env is missing
const API_KEY = process.env.API_KEY || "";
```

### Creating .env but forgetting dotenv

```typescript
// ❌ Bad — .env file exists but nothing loads it
const key = process.env.MY_KEY; // undefined

// ✅ Good — import dotenv/config as first import
import "dotenv/config";
const key = process.env.MY_KEY; // loaded from .env
```

### Skipping CLAUDE.md because "the code is self-explanatory"

Claude Code reads CLAUDE.md at the start of every session. Without it, every conversation starts cold — no awareness of the tech stack, conventions, gotchas, or architecture. Always create one.

### Registering work projects in a personal AI-context repo

A personal AI-context repo is your own personal context system. Work projects (client work, employer projects) should only be registered in your protocol repo, not in personal context storage.

---

## Troubleshooting

### Problem: `.env` values not loading

**Cause:** `dotenv` not installed or not imported as the first server import.

**Solution:**
```bash
npm install dotenv
```
Then add `import "dotenv/config";` as the **first line** of your server entry point.

### Problem: Port conflict on macOS

**Cause:** macOS AirPlay Receiver uses port 5000. Other services may use common ports.

**Solution:** Use a non-conflicting port in `.env` (e.g., 3001, 5001, 8080). Avoid binding to `0.0.0.0` with `reusePort` on macOS/Node 25+.

### Problem: Pushed with wrong GitHub account

**Cause:** `GH_TOKEN` env var overriding `gh` keyring auth. See `GITHUB_MULTI_ACCOUNT.md`.

**Solution:**
```bash
unset GH_TOKEN GITHUB_TOKEN
gh auth status  # verify correct account
```

---

## Resources

- `PROJECT_CLAUDE_TEMPLATE.md` — CLAUDE.md template (code projects)
- `PROJECT_CLAUDE_TEMPLATE_RESEARCH.md` — CLAUDE.md template (research / operator / non-code projects)
- `_TEMPLATE_NOW.md` — NOW.md (mutable state layer)
- `_TEMPLATE_JOURNAL.md` — JOURNAL.md (append-only history layer)
- `GLOBAL_CLAUDE_TEMPLATE.md` — Global Claude config template
- `CLAUDE_INSTRUCTION_LAYERS.md` — Four-layer architecture + slim-pointer pattern
- `GITHUB_MULTI_ACCOUNT.md` — Multi-account git credentials
- `GIT_CONVENTIONS.md` — Commit and branch conventions
- [AI_EVALS.md](AI_EVALS.md) — Eval scaffold for AI-powered projects (Step 3c)
- [AI_OBSERVABILITY.md](AI_OBSERVABILITY.md) — Observability scaffold for AI-powered projects (Step 3c)

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2026-03-27 | Initial release — extracted from an early project's setup session |
| 1.2 | 2026-05-15 | Step 8 (docs-audit registration) restructured as a routing rule by account/org — personal repos to a personal-account trigger, client/org repos to a separate trigger on that account. Matches the existing account-segregation pattern used elsewhere. Replaces a dead stale trigger reference. |
| 1.3 | 2026-05-23 | Added Step 5a (Update Assets Register) — mandatory private register update before closing a new-project session. |
| 1.4 | 2026-05-24 | Step 3 (CLAUDE.md) restructured around slim-pointer architecture. Two template variants: PROJECT_CLAUDE_TEMPLATE.md (code projects) + PROJECT_CLAUDE_TEMPLATE_RESEARCH.md (research / operator / non-code). New companion templates: _TEMPLATE_NOW.md and _TEMPLATE_JOURNAL.md as required siblings. Cross-link to CLAUDE_INSTRUCTION_LAYERS.md for the architecture itself. Drove this change: original PROJECT_CLAUDE_TEMPLATE.md embodied anti-patterns (Project Status / In Progress / Planned mutable-state sections) it should have prevented. |
| 1.5 | 2026-05-26 | Step 3 narrowed: NOW.md and JOURNAL.md removed as mandatory siblings for code projects. They belong to the four-surface model for non-code work, where markdown IS the deliverable and there's no git equivalent. For code projects, mutable state and history are already covered by BACKLOG.md (per ROADMAP_AND_BACKLOG.md), docs/DECISIONS.md (ADR pattern), and git — adding NOW.md / JOURNAL.md duplicates state and creates parallel-history drift. Three paths now distinguished: (a) code projects → PROJECT_CLAUDE_TEMPLATE.md only; (b) non-code GitHub repos (rare) → research template + four-surface model; (c) Cowork-based research/strategy/writing → use COWORK_PROJECT_INIT.md instead, not this protocol. Fixes drift introduced in v1.4 where the slim-pointer refactor overshot into mandating four surfaces for SWE repos. Triggered by a misfire observed in an AI-pilot project's `/init` session. |
| 1.6 | 2026-06-04 | Step 8 (multi-repo audit path) rewritten for a **generalized multi-repo auditor**. The trigger prompt is now repo-agnostic; each repo self-describes via an optional audit-config file (generic checks always run; config-driven checks — version coherence, retired terminology, roadmap chronology, spec-index, env coherence — activate per field). Adding a repo = drop the config file + register its URL with the trigger. Previously the trigger was hardcoded to a single repo, so "add a repo" was a silent no-op for others. |
| 1.7 | 2026-06-22 | Step 2 expanded to cover project-specific runtime state before agents, LaunchAgents, sync loops, OAuth smoke flows, or desktop launchers start writing: token caches, daemon logs, lock/health files, generated latency snapshots, sync cursors, and smoke/canary artifacts. Cross-linked to GIT_CONVENTIONS.md runtime-state rule. |
| 1.8 | 2026-06-25 | Step 3a expanded from dependency baseline to dependency/tooling baseline: package-manager policy, runtime pins, system/local dependencies, and script safety categories now ride with initial project setup. Cross-linked to DEPENDENCY_HYGIENE.md v1.1. |
| 1.9 | 2026-06-27 | Added required Step 3d protocol surfacing so new durable repos sync relevant protocols locally and expose exact trigger -> local protocol lines in project instructions. Driven by protocol-invocation drift eval showing generic pointers are weaker than exact local protocol names. |

---

**Protocol Version**: 1.9
**Last Updated**: 2026-06-27
