# Orchestrated Sessions — one parent, bounded children

> How one parent session runs a complex task through child sessions and subagents: what the
> brief must contain, who writes what, how shared resources are held, how results are judged,
> and how decisions reach the human. Invoke with "orchestrate this".

**Applies to:** Claude Code (desktop sessions, subagents), Codex, or any agent surface that can
start and message other sessions; any task too big or too parallel for one session
**Last Updated:** 2026-11-11
**Version:** 1.4

---

## Table of Contents

- [Overview](#overview)
- [When to Use](#when-to-use)
- [Quick Start — the twelve rules](#quick-start--the-twelve-rules)
- [The Brief](#the-brief)
- [Implementation](#implementation)
- [Kick-off Prompt](#kick-off-prompt)
- [Keeping the Parent Going — /loop and /goal](#keeping-the-parent-going--loop-and-goal)
- [Anti-Patterns](#anti-patterns)
- [Troubleshooting](#troubleshooting)
- [Resources](#resources)
- [Version History](#version-history)

---

## Overview

A human starting sessions by hand gets collisions: two sessions editing one checkout, two test
runs sharing one temp folder, a deploy refused because another session's files were dirty, and
the human as the only router between them. The fix is not fewer sessions but one owner of the
traffic. A single **parent** session holds the plan, briefs each **child**, verifies each result,
sequences what lands, and is the only channel to the human.

This is the bounded, single-task counterpart of
`AGENTIC_TEAM_DESIGN.md`, which governs standing teams that persist for
months. Its rules 1 (single human interface), 4 (generator ≠ judge), 5 (single writer) and
8 (watch the watcher) apply here unchanged; this protocol adds the operating detail for a
parent that starts, briefs, checks and retires children within one piece of work.

**Scope: how the coding agents working with the human organise the development work, not how
the product they build runs.** A product that is itself agent-operated keeps its runtime in its own
architecture — workers, schedulers and their control surface — and a product step owned by "a
session" is a defect there, never a use of this protocol.

Distilled from a real project (Oct–Nov 2026): the 4 October "one stream only" rule that answered
manual-spawning collisions, and the 4 November replacement by a parent-orchestrated model.

---

## When to Use

| Scenario | Use this protocol? |
|---|---|
| A staged plan whose stages each need a fresh session | **Yes** |
| Two or more independent pieces of work that could run at once | **Yes** |
| The human says "orchestrate this", or asks you to run work in parallel or in the background | **Yes** |
| A wide read or search whose conclusion you need this turn | No — one subagent, no ceremony |
| A handful of tool calls, one edit, one question | No — do it in the session |
| A standing team of agents over weeks | No — `AGENTIC_TEAM_DESIGN.md` |
| A child that runs on the other vendor's model (Codex driving Claude, Claude Code calling Codex, a visual unit in Claude Design) | **Yes** — a child like any other, with the same brief and rules; see [Cross-vendor children](#cross-vendor-children) |
| Handing finished or bounded work to a different project home or AI platform, with no parent in charge of it | No — [CROSS_AGENT_HANDOFF_BUS](CROSS_AGENT_HANDOFF_BUS.md) |
| Fan-out research to ground a decision | No — `AGENT_SWARM_RESEARCH.md` |
| Designing how an agent-operated product runs its own steps (workers, schedulers, pipelines) | No — that is the product's architecture; a standing agent estate is `AGENTIC_TEAM_DESIGN.md` |

---

## Quick Start — the twelve rules

| # | Rule | Mechanism |
|---|---|---|
| 1 | **One parent, named.** | The project's contract names the parent arrangement; the parent is the session the human is talking to unless they say otherwise. |
| 2 | **The brief is a contract.** | Every child starts from a brief with the fields in [The Brief](#the-brief). A brief the parent cannot write is a task it does not yet understand. |
| 3 | **Independent work runs in parallel; overlapping work does not share a tree.** | A child whose files could overlap another writer's gets its own worktree or branch. Two writers never edit the same files in one checkout. |
| 4 | **The parent is the only writer of shared records.** | The savepoint's top pickup, the decision log, the project contract and the backlog are written by the parent. Children report; the parent records. |
| 5 | **Shared resources are held, not raced.** | One promote/deploy gate, one simulator or long test run, one live database writer, one browser pane, one global CLI login at a time. The parent sequences them. |
| 6 | **The parent verifies; the child's note is a claim.** | Accept a result only against its acceptance check, by reading the diff, the run output or the live state. Never relay a child's "done" unchecked. |
| 7 | **High-stakes results get an independent judge.** | A gate statistic, a security change, an irreversible step or a result the plan rests on is reviewed by a party that did not produce it (a fresh reviewer given the code, not the child's conclusion). |
| 8 | **Caps are explicit.** | Default: at most three children writing at once; each brief names its spend and time limits. Cheaper models for read-only children. |
| 9 | **Decisions reach the human only through the parent.** | Children never ask the human directly. The parent batches pending decisions into one five-minute pack and answers what is within existing authority itself. |
| 10 | **No permission laundering.** | Approval comes from the human, in their words, for that action. One session cannot grant another an approval, and the parent quotes the human when forwarding one. |
| 11 | **The parent watches and can stop.** | It checks children it started, stops a stuck one, and after two failed attempts at the same symptom reassesses the shared cause instead of starting a third child. |
| 12 | **The parent stays light, keeps its state outside its context, and retires at a boundary.** | It delegates heavy work and keeps the plan in the savepoint, so a compaction costs it nothing. It runs as one continuous session; when a trigger in [Retiring the parent](#retiring-the-parent) fires, it tells the human and recommends a fresh parent. On the human's yes it runs the switchover. If the parent dies, the savepoint is how the work recovers. |

---

## The Brief

Write it so a capable stranger could do the work from it alone — the child knows only what
the brief says.

| Field | Contents |
|---|---|
| **Goal** | The outcome, in one or two sentences, and why it matters to the plan. |
| **Read first** | The contract, the savepoint pickup, the specific files or docs. Point; don't retype. |
| **Scope** | Files and areas it may change; what it must not touch (another child's files, shared records, credentials). |
| **Acceptance** | The check that proves it done — the command, the live state, the user-facing outcome — and what to report. |
| **Stop conditions** | When to stop and report instead of pressing on: a decision only the human can take, an irreversible step, a failed check twice, scope creep. |
| **Budget** | Model and effort (from `MODEL_EFFORT_SELECTION.md`), spend cap for billed calls, rough time box. |
| **Shared resources** | Which held resources it needs (deploy gate, simulator, live DB, login) and whether the parent has granted them or it must ask. |
| **Report** | What its final note must contain: what moved, the evidence, what is unverified, anything it left. |

Already ruled out and what was tried belongs in the brief too: a child handed only a hypothesis
tends to return it confirmed.

---

## Implementation

### Starting

1. Split the plan into units. A unit qualifies for its own child when it ends in something of its
   own (a commit, a branch, a finding) and does not need another unit's result.
2. For each unit decide: subagent (result needed this turn, read-heavy) or session (outlives the
   turn, the human may want to open it). Pick model and effort per unit.
3. Decide isolation: shared checkout only for read-only work or files no other writer touches;
   otherwise a worktree.
4. Write the brief. Name the child after its unit so the human can find it.

### Running

- Do your own unit while children run; don't poll. Queue long waits detached and take the next item.
- When a child reports, check its result against its acceptance before anything else uses it.
- Merge or land children's branches in an order the parent chooses, one through the shared gate
  at a time. Merging branches into the parent's checkout needs the human's say-so where the project
  requires it.
- Record each landing in the savepoint yourself; update the plan.

### Closing

- Reconcile every child: landed, stopped, or recorded as left with where its work lives.
- Archive finished children only on the human's yes.
- The savepoint names what is still running, not just what finished.

### Retiring the parent

A parent's state lives outside its context: the savepoint, git, the task list and the gate queue's own records.
That makes a long-running parent safe, and it makes a switch cheap. Whether to keep one parent or start fresh
depends on the model and harness in use, so this section is re-checked when either changes.

**Default, checked 2026-11-11 (frontier models with automatic compaction): one continuous parent.** Current vendor
guidance for these models is one session with compaction handling context growth, state kept outside the session,
and a fresh session at a task boundary. A compaction is not a trigger: a harness may compact a large idle session
on its own (Claude Code does, shortly before its prompt cache expires), so it says nothing about drift.

**Triggers.** When one fires, say so at the next pause in one line: which trigger fired, and a recommendation
for a fresh parent.
- A dropped thread: something it forgot and the human or a child caught. Examples: a commit never landed, a
  child's model not set as asked, a report never relayed. This is the evidence of drift; count it.
- A natural boundary: the approved batch is finished, or the next work is unrelated to what the parent holds.
  A fresh parent costs least here, and a long session pays to re-read its history on every turn.
- A change of model or harness under the parent, or a parent on a smaller or older model than the default was
  checked on. Until it is re-tested there, the older rule applies: recommend a fresh parent at the first compaction.

**After every compaction, a check, not a trigger:** re-read the savepoint and the live state (the gate queue, each
child's last report) before acting. If the savepoint could not have rebuilt what the parent needed, that is a
dropped thread. Children are rotated the same way: at a boundary, after a handover file, never mid-slice.

**Which model.** The answer has moved with model generations. Vendor write-ups record that an earlier mid-tier
model wound its work down as its context filled, and compaction did not cure it, so fresh-context resets with a
structured handoff were needed; from Claude Opus 4.5 the same author dropped the resets and ran one continuous
session, and a Claude Fable 5.2 lead ran a 1,000-agent team for over a day with coordination held in shared tables.
Treat the default as shown for the frontier Claude tiers (Opus from 4.5, Fable 5.x); for a later Opus it is an
inference from the tier, not a published check. No equivalent published check was found for Codex or for a
smaller model as parent: use the older rule there and let the dropped-thread count decide. Every rule in a
harness encodes an assumption about what the model cannot do; re-test this one when a new model lands.

The human decides. The parent never switches on its own.

**Switchover, on the human's yes:**
1. Finish or park its own unit. Leave nothing half-edited in a shared checkout.
2. Write the savepoint's top pickup. Include every child (id, state, branch, next step, acceptance check), the
   gate queue, what waits on the human, the pre-approvals in the human's words, and the session's standing lessons.
   Commit it.
3. Stop its loop or goal, so two parents never act at once. Running children and queued gates keep going; stop
   none of them for the switch.
4. Give the human a short kickoff prompt naming the savepoint, with a recommended model and effort for the new
   parent.
5. The new parent reads the savepoint, verifies live state, and messages each child: "I am your parent now;
   report to me". A child's finished turn wakes only the session that started it, so until then the old
   parent relays.
6. Archive the old parent once the new one confirms it has every child, and only on the human's yes.

### Cross-vendor children

The parent and a child need not run on the same vendor's model. Briefing a child on the other
vendor's model where it is stronger for that unit has worked well in practice: a Codex parent on
GPT-6 Astra driving Claude (Fable 5.1, Opus) for design exploration and the parts where Claude is
stronger; a Claude Code parent handing a first-principles review to Codex; a visual unit going to
Claude Design. A cross-vendor child is a child like any other — a brief, a worktree, an acceptance
check, and no authority beyond the parent's — which is what separates it from a handoff packet,
which moves work to another project or platform with no parent in charge of it. Mechanics:
`codex exec` from Claude Code, `claude -p` from Codex (unset `ANTHROPIC_API_KEY` so the call draws
on the subscription, and run it `--restricted` in the narrowest permission mode the unit allows);
the commands, the permissions that contain the driven agent, and what each vendor's terms say about doing it on a subscription are on the hub page *Running Claude Code and Codex side by side*. Pick the model per brief with
`MODEL_EFFORT_SELECTION.md`.

### Claude Code mapping

| Need | Mechanism |
|---|---|
| Child that outlives the turn | `start_session` (desktop) with `user_asked` when the human asked for it |
| Result needed this turn | `Agent` subagent; `fork` when it needs the conversation |
| Message a child | `SendMessage` to its `local_…` id |
| Isolation | `use_worktree: true`; `false` only for read-only or non-overlapping work |
| Model ceiling | A child cannot run a model above the parent's; start the parent on the strongest model the plan needs |
| Child on the other vendor's model | `codex exec` from Bash: read-only sandbox unless told otherwise, and only once the human approves it or a permission rule allows it; same brief, same rules |
| Parent kept working between reports | `/loop <prompt>` with no interval, typed by the human: Claude picks each wait (1 min–1 h) and stops when done or on Esc. The desktop app also wakes the parent when a child session finishes a turn; `/loop` covers what nothing else will wake it for |
| Child working to a finish line | `/goal <condition>` with a checkable condition and a turn or time clause ("or stop after 20 turns") |
| Many subagents from one script | The `Workflow` tool (dynamic workflows), opted into only by the human writing `ultracode`; a run can use meaningfully more tokens than the same task in conversation |

### Codex mapping

The rules are the same; the mechanisms differ in ways that change how the parent works
([Codex subagents](https://developers.openai.com/codex/subagents), checked 2026-11-04 against CLI 0.155; goals and cross-vendor calls checked 2026-11-08).

| Need | Mechanism | What changes for the parent |
|---|---|---|
| Child within the turn | A subagent, spawned when asked or when `AGENTS.md` / a skill tells it to; `/subagents` to inspect | The main thread waits for all requested results and consolidates them, so the parent's own unit runs before or after, not alongside. |
| Child that outlives the turn | A detached `codex exec` run with its output written to a file, or a Codex Cloud task (`codex cloud`, `codex apply`) | No completion notice reaches the parent: it checks each child's output at its own checkpoints, with a bounded wait. Message a saved session with `codex queue --thread`. |
| Parent kept working between checkpoints | A goal: `/goal <objective>`, or one Codex starts itself when the conversation has become an objective; cap it with `goals.max_goal_token_budget` (no limit if unset) | Continuation is event-driven (only while idle, active and within budget; a continuation with no tool call suppresses the next), so the parent can hold a goal for hours without spinning. Write the checkpoints and the evidence that closes the goal into the objective, and say in `AGENTS.md` whether Codex may start goals itself. |
| Child on the other vendor's model | `claude -p "<brief>" --restricted --permission-mode plan` (or a write mode in its own worktree) with `ANTHROPIC_API_KEY` unset; the sandbox asks to leave for the network call | Auto-review may refuse a call that would send project files out. Keep credentials and the landing with the parent. |
| Isolation | Subagents share the parent's checkout and sandbox; the `worktrees` feature is experimental and off | Give each writing child its own `git worktree add` folder (or a cloud task). A read-only child is read-only only by instruction: use the built-in `explorer` or a custom agent with `features.shell_tool = false`. |
| Model and effort | Per child: an explicit spawn value, a custom agent in `.codex/agents/*.toml` (`model`, `model_reasoning_effort`), or `[agents]` defaults; otherwise inherited | No parent ceiling, so a child may run a stronger or cheaper model than the parent. Pick it per brief. |
| Concurrency cap (rule 8) | `agents.max_concurrent_threads_per_session` (legacy `agents.max_threads`); unset = 6 spawned threads in code ([#13964](https://github.com/openai/codex/issues/13964)), though the docs say only "Codex chooses" | It counts readers as well as writers, so it cannot express rule 8's writer limit: keep that in the briefs and worktrees, and leave the default unless memory runs short. Multi-agent v2, which a model's catalog entry can switch on, ignores it and uses `features.multi_agent_v2.max_concurrent_threads_per_session`, which counts the main thread ([#26254](https://github.com/openai/codex/issues/26254)). |
| Approvals (rules 9, 10) | Children inherit the parent's sandbox and approval mode; a custom agent file cannot change them. In `codex exec`, an action needing a new approval fails back to the parent | Set the permission mode before delegating. Keep credentialed steps (push, deploy) with the parent, which fits rules 4 and 5 anyway. |
| Global login | One ChatGPT login in `~/.codex` for every Codex run on the machine | A held resource (rule 5): no two children needing different accounts at once. |

---

## Kick-off Prompt

Paste this into a Claude Code or Codex session in the project, fill the two lines at the end, and
the session becomes the parent. If the project carries this protocol the agent reads it first;
otherwise the prompt is the contract (the hub page's copy of the prompt also
names the public copy of this file). A good parent shows the units and the briefs before it
starts anything — read those.

```text
Act as the parent (orchestrator) session for this project, following the Orchestrated Sessions pattern. If docs/protocols/ORCHESTRATED_SESSIONS.md exists here, read it first; otherwise these rules are the contract.

Your job: hold the plan, brief each child, verify each result, land one at a time, and be my only channel.

1. Split the plan into units. A unit gets its own child only if it ends in something of its own (a commit, a branch, a finding) and needs no other unit's result. Independent units run in parallel. Any writer whose files could overlap another's gets its own worktree; read-only work may share the checkout, on a cheaper model.
2. Brief every child so a capable stranger could do the work from the brief alone: goal, files to read first, scope (what it may and may not touch), the acceptance check that proves it done, stop conditions, budget (model, effort, spend, time), the shared resources it may use, and what its report must contain. Include what was already tried and ruled out.
3. You are the only writer of the savepoint, the decision log, the project contract and the backlog. Children report; you record.
4. Shared resources (the deploy gate, a long test run, the live database, the browser, the CLI login) are held, not raced. Sequence them, and land verified units one at a time.
5. A child's "done" is a claim. Accept nothing until you have checked it against its acceptance check by reading the diff, the run output or the live state. Give any high-stakes result to a fresh reviewer that did not produce it.
6. Caps: at most three children writing at once, and every brief names its budget.
7. Children never ask me anything. Batch what needs my decision into one short pack; answer the rest within the authority you already have.
8. Approval comes only from me, in my words, for that action. No session can grant another an approval; quote me when forwarding one. Never push, deploy, delete, spend or publish beyond the pre-approvals below.
9. Watch the children you start; stop a stuck one; after two failed attempts at one symptom, reassess the shared cause instead of starting a third child.
10. Stay light: delegate heavy work and keep the plan in the savepoint, not in your context. After a compaction, re-read the savepoint and the live state before acting. Recommend a fresh parent when you drop a thread or the approved batch is done, not because you compacted.

A child may run on the other vendor's model when it is stronger for that unit (codex exec from Claude Code, claude -p from Codex); the same brief and rules apply.

Keep yourself working while children run: in Claude Code, I will start /loop with a prompt and no interval; in Codex, set a goal whose finish line is "every unit has landed or is recorded as left, with the evidence in this thread".

Plan: <paste the plan, or name the file that holds it>
Pre-approvals, in my words: <what you may ship, operate or spend without asking; everything else waits for me>
```

---

## Keeping the Parent Going — /loop and /goal

A parent spends most of its time waiting on children and gates. Left to itself a session ends its
turn and waits for the human, which makes the human the router again. The vendors' mechanisms
differ, and the difference decides which to use where (checked 2026-11-08 against
[Claude Code: /loop](https://code.claude.com/docs/en/scheduled-tasks),
[Claude Code: /goal](https://code.claude.com/docs/en/goal),
[Codex: goals](https://learn.chatgpt.com/use-cases/follow-goals) and the
[OpenAI cookbook on goals](https://developers.openai.com/cookbook/examples/codex/using_goals_in_codex)).

| | Claude Code `/loop` | Claude Code `/goal` | Codex `/goal` |
|---|---|---|---|
| **Set by** | The human types it; never inferred from a sentence | The human types it | The human, or Codex itself: "the model can start a Goal and can mark an existing Goal complete only when the evidence supports completion"; pause, resume and clear stay with the human or the system |
| **Next turn starts when** | A time interval elapses: fixed (`/loop 10m …`) or chosen by Claude each pass between 1 min and 1 h, with the reason printed | The previous turn finishes, until a small fast model judges the condition met or impossible; waits while a subagent or background command runs, checking in after 30 min then at doubling intervals | The thread is idle, the goal is active and the token budget is not spent; a continuation with no tool call suppresses the next, plan-only work does not continue, an interruption pauses |
| **Scope and limits** | Session-scoped: fires only while the session is open and idle; closing the terminal stops it; the self-paced form is not restored on resume; a recurring loop expires after 7 days; Esc stops a self-paced loop | One goal per session, up to 4,000 characters; restored on resume; needs hooks enabled; `/goal clear` | Thread-scoped, persisted; Codex 0.128.0+, `features.goals` on by default (`codex features enable goals` if `/goal` is missing); `goals.max_goal_token_budget` caps it, no limit if unset |
| **Use it for** | **The parent**, which has nothing to do until a child reports or a gate finishes: wait on a timer, do not spin on a condition | **A child** with a checkable finish line ("every test in `test/auth` passes and the linter is clean") | **The Codex parent**: in-turn subagents are waited for and detached `codex exec` children send no notice, so a goal is what brings the parent back to its checkpoints |

Rules that follow:

- **A condition that can be checked.** The tests pass, every unit has landed, the gate is green. "Finish the UI" is not a condition; a goal with no evidence in it gets marked done on the model's say-so.
- **A cap.** Turns or time for Claude Code (`or stop after 20 turns`), tokens for Codex. Set the permission mode before leaving: auto mode in Claude Code, Codex's approval mode, knowing what unattended means.
- **Pre-approvals in the human's words, written where the parent reads them.** A child's request is never one (rule 10), and neither is a loop prompt that says "do whatever is needed".
- **In the Claude Code desktop app, a child session's finished turn wakes the parent on its own.** `/loop` is for what nothing else will wake it for: a gate running on another machine, a CI run, an overnight simulation.

Starters, to adapt. Claude Code parent, typed by the human once the first children are running:

```text
/loop Act as the parent session for the plan in the savepoint. On each wake-up: read every child's latest report; verify any finished unit against its acceptance check before anything uses it; land verified units one at a time through the gate; re-brief or stop a stuck child; record each landing in the savepoint. Never push, deploy or delete anything the pre-approvals do not name. Stop when every unit has landed or been recorded as left, and write the morning report.
```

Codex parent:

```text
/goal Every unit in the savepoint's plan has landed on main through the project's land script with its acceptance check shown green in this thread, or is recorded as left with a reason. Children build in their own worktrees; this thread verifies each diff before it lands, lands one at a time, and never pushes, deploys or deletes anything the pre-approvals do not name. If the budget runs out, summarize progress and blockers and stop.
```

---

## Anti-Patterns

| Anti-pattern | What happened | Rule |
|---|---|---|
| Human as router | The human spawned sessions by hand; they edited one checkout and collided. | 1, 3 |
| Child writes the savepoint | Two sessions each rewrote the top pickup; the next session read a half-merged plan. | 4 |
| Racing the gate | A deploy refused because another session's files were dirty; two test runs shared a fixed temp folder. | 5 |
| Relaying "done" | A child's note said green; the deploy it named had failed its gate. | 6 |
| Self-certified result | The session that built a check also judged it passed. | 7 |
| A child asks the human | Questions arrived from several places, each without the others' context. | 9 |
| Laundered approval | A peer session's message was treated as permission to escalate. | 10 |
| Third patch on one symptom | Each child fixed the symptom it was shown; the shared cause stayed. | 11 |
| Parent does the heavy work | Its context filled with file dumps and it lost the plan. | 12 |
| Parent outlived its context | After a compaction it left a commit unlanded and started a child on the wrong model; the human caught both. | 12 |
| Parent retired on a compaction | An idle-hour compaction fired the trigger on a model that did not need it; the switchover cost a morning and every child had to be re-attached. | 12 |
| Parent stopped when the human did | No loop or goal was set; the children finished into silence and the landings waited for the morning. | — |
| Parent spun on a condition | A `/goal` was set on a session that had nothing to do but wait; every turn re-read the same reports. | — |
| Goal with no evidence in it | "Finish the feature" was marked done on the model's say-so; nothing in the thread proved it. | 6 |

---

## Troubleshooting

| Symptom | Likely cause | Fix |
|---|---|---|
| Child's work missing from main | It committed to its own worktree branch | Land the branch through the parent; name it by full ref |
| Deploy refused "dirty tree" | A child left uncommitted files in the shared checkout | Have the child commit by path, or give it a worktree next time |
| Two children report conflicting facts | Each read a different snapshot | The parent re-reads the live state and records which is current |
| A child is silent | Stuck on a prompt, a permission or a long run | Check its state; answer, stop, or re-brief |
| Parent lost track after compaction | The plan lived only in its context | Keep the plan in the savepoint and the task list, not in prose |
| The loop stopped overnight | `/loop` is session-scoped: the terminal closed, the machine slept, or the loop expired | Keep the session open and the machine awake, or run the parent as a background session; work that must survive the laptop belongs in a routine or scheduled task |
| The loop was gone after a resume | A self-paced `/loop` is not restored | Run `/loop` again with the same prompt |
| Codex marked the goal complete too early | The objective named no evidence | Put the proving command or artefact in the objective, and the acceptance check in each brief |

---

## Resources

- Sources for rule 12, checked 2026-11-11: [Effective harnesses for long-running agents](https://www.anthropic.com/research/effective-harnesses-for-long-running-agents) (Nov 2025); [Harness design for long-running apps](https://www.anthropic.com/research/harness-design-long-running-apps) (Mar 2026); [Claude Code best practices](https://code.claude.com/docs/en/best-practices); [Safely scaling multi-agent teams with Claude Fable 5.2](https://claude.dev/blog/safely-scaling-multi-agent-teams-with-fable-5-2/) (Nov 2026)
- `AGENTIC_TEAM_DESIGN.md` — standing teams; rules 1, 4, 5, 8 are shared
- [SESSION_HANDOFF_SAVE_POINTS](SESSION_HANDOFF_SAVE_POINTS.md) — the savepoint the parent owns
- `MODEL_EFFORT_SELECTION.md` — per-child model and effort
- [CROSS_AGENT_HANDOFF_BUS](CROSS_AGENT_HANDOFF_BUS.md) — work leaving this platform or project
- `AGENT_SWARM_RESEARCH.md` — fan-out research
- [QA_PROTOCOL](QA_PROTOCOL.md) — the checks a child's acceptance names
- [Claude Code: /loop](https://code.claude.com/docs/en/scheduled-tasks) · [Claude Code: /goal](https://code.claude.com/docs/en/goal) · [Claude Code: subagents](https://code.claude.com/docs/en/sub-agents) · [Claude Code: dynamic workflows](https://code.claude.com/docs/en/workflows) — vendor pages, checked 2026-11-08
- [Codex: goals](https://learn.chatgpt.com/use-cases/follow-goals) · [OpenAI cookbook: using goals in Codex](https://developers.openai.com/cookbook/examples/codex/using_goals_in_codex) · [Codex: subagents](https://learn.chatgpt.com/docs/agent-configuration/subagents) · [Codex: Git worktrees](https://learn.chatgpt.com/docs/environments/git-worktrees) — vendor pages, checked 2026-11-08

---

## Version History

| Version | Date | Changes |
|---|---|---|
| 1.4 | 2026-11-11 | Rule 12 re-based on current vendor guidance: one continuous parent by default on frontier models; a compaction is a check (re-read the savepoint), not a trigger; triggers are a dropped thread, a natural boundary, or a change of model or harness; the default is tied to the model it was checked on; sources listed; one anti-pattern row. |
| 1.3 | 2026-11-11 | Rule 12 made concrete: the parent counts context-rot triggers (first compaction, a dropped thread, more than eight children or a working day), recommends a fresh parent, and on the human's yes runs a six-step switchover; one anti-pattern row. |
| 1.2.1 | 2026-11-08 | Published to the public mirror on the owner's decision, so the hub's kick-off prompt can link it; provenance genericised. No rule changes. |
| 1.2 | 2026-11-08 | Keeping the parent going: `/loop` (Claude Code, typed, timer-based) for the parent, `/goal` (both vendors; Codex can start one itself) for a child or a Codex parent, with vendor facts checked that day; cross-vendor children are in scope (a handoff is not); kick-off prompt; mapping rows for loop, goal, workflows and cross-vendor calls; three anti-patterns and three troubleshooting rows. |
| 1.1 | 2026-11-04 | Codex mapping: in-turn subagents wait and consolidate; detached children send no notice; manual worktrees; per-child models with no ceiling; concurrency cap (default 6, counts readers, not a writer limit); inherited approvals. |
| 1.0 | 2026-11-04 | Initial — from a project's move from a one-stream rule to a parent-orchestrated model. |
