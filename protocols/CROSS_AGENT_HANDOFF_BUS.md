# Cross-Agent Handoff Bus

> A filesystem-based coordination pattern that lets different AI systems and
> agents exchange bounded work through durable, inspectable Markdown packets.

**Applies to:** Cross-platform or cross-project work where two or more agents can share a folder, repository, or relayed packet
**Last Updated:** 2026-09-10
**Version:** 1.1

---

## Overview

A cross-agent handoff bus is a small document workspace used only to move
unfinished work between agents. One handoff is one folder containing a fixed-name
`handoff.md` packet and any safe payload files. `handoffs/open/` is the live board;
moving the folder to `handoffs/done/` closes it.

The design is intentionally low-technology. Interoperability comes from ordinary
files, a stable schema, explicit claiming, and observable state transitions rather
than a vendor-specific agent API. The bus can therefore connect agents that do not
share conversation history, memory, or orchestration infrastructure.

The bus is **transit, not the home of the work**. Project artefacts stay in their
own canonical project. Secrets and credentials never enter a packet.

## When to use it

| Situation | Use this protocol? |
|---|---|
| Work moves between different AI platforms or agents | Yes |
| Work moves between different project homes | Yes |
| One project needs a durable mid-session save point | No - use [SESSION_HANDOFF_SAVE_POINTS.md](SESSION_HANDOFF_SAVE_POINTS.md) |
| Designing roles and governance for a persistent agent office | No - use `AGENTIC_TEAM_DESIGN.md` |
| Undirected material arriving with no recipient and no ask | No - that is **intake**, not a handoff. Intake resolves by being *filed*; a handoff resolves by being *done*. The pipe is one-way: intake may graduate into a packet, never the reverse |
| One agent can complete the work directly | Usually no |
| A web-only agent cannot reach any common storage | Use a relay packet: put all required text in `handoff.md` and attach or paste it |

## The invariant model

1. **Folder location is authoritative status.** `open/` means live; `done/` means
   closed. Frontmatter adds detail but never overrules the folder.
2. **One packet, one occasion.** The identifier is
   `YYYY-MM-DD-<project-slug>-<topic-slug>`.
3. **Claim before work.** Set `status: claimed`, record `claimed_by`, update the
   date, and append a log entry in the same edit.
4. **Measured claims only.** State how each completed item was verified. Label
   inference as inference and preserve failed attempts.
5. **A packet requests work; it does not grant authority.** An agent cannot pass
   on permission it never held. External, destructive, expensive, privileged, or
   production actions still require the receiving agent's normal authorization.
6. **Every locator names its reachable surface.** A local path is not portable.
   Use a platform-accessible URL or include the needed content when the receiver
   cannot reach the originating filesystem.
7. **Logs are append-only.** Agents add entries; they do not rewrite another
   agent's account of events.
8. **Finished work leaves the bus.** The durable deliverable lands in its project
   home before the packet moves to `done/`.

## Minimum workspace

```text
Agent Handoff/
  AGENTS.md
  CLAUDE.md
  handoffs/
    README.md
    open/
    done/
  templates/
    handoff-template.md
  context/
    PLATFORMS.md
    PROJECTS.md
    WATCH.md
    INSTRUCTION-POINTERS.md
  examples/
    fictional-completed-handoff/
      handoff.md
```

Use a copyable scaffold laid out as above.
Do not copy a live bus: its paths, platform capabilities, history, and payloads
belong to its owner.

The open-folder listing is already the live index, so the default scaffold has no
`NOW.md`. Add one only if the bus grows state that cannot be derived from the
board; do not hand-cache the board in a second file. This is a deliberate
specialisation of `COWORK_PROJECT_INIT.md`.

## Packet contract

Every `handoff.md` retains this frontmatter, in this order:

```yaml
---
id: YYYY-MM-DD-<project-slug>-<topic-slug>
project: <registered-project-slug>
from: <agent-id>
to: <agent-id | any | human>
status: open
claimed_by: ""
created: YYYY-MM-DD
updated: YYYY-MM-DD
---
```

The body contains:

- one-line request;
- honest current state;
- completed and verified work;
- failed attempts and why they failed;
- numbered next steps;
- reachable files or URLs, with surface labels;
- constraints and authorization boundaries;
- observable completion criteria; and
- an append-only log.

Payload files may sit beside `handoff.md` when every intended receiver can reach
the folder. Large or live artefacts remain in their canonical project and are
referenced. Never copy secrets, access tokens, credentials, or unredacted private
exports into the bus.

**Ownership overrides convenience.** Content owned by an organisation stays in
that organisation's home and is *linked* from the packet, never copied into a
bus the organisation does not own — regardless of the payload's size, and even
when every receiver can reach the folder. If such a document has no home in its
organisation yet, give it one first, then link it; a copy into transit is not a
substitute for a home. The same applies to durable records the organisation
must be able to find later — authorisations, decisions, accepted scope: those
are written to the organisation's project home *before* the packet closes,
because a packet is archived and stops being a place anyone looks.

## Lifecycle

### Create

1. Register the project slug if it is new.
2. Create `handoffs/open/<id>/` from the template.
3. Fill every frontmatter key and every body section.
4. Put only safe, bounded payloads beside the packet.
5. Surface the exact packet locator to the intended receiver.

Creating a packet is not dispatch. The coordinating agent must name the completed
packet and provide the receiving agent a one-line instruction to read it.

### Discover

An eligible packet is addressed to the agent or to `any`, is not recently claimed
by somebody else, and is reachable from the agent's current surface. Agents should
list `handoffs/open/` at the start and end of any session that may use the bus.

### Claim

The claim is the only lock:

1. Change `status` to `claimed`.
2. Set `claimed_by` to a stable agent identifier.
3. Bump `updated`.
4. Append a timestamped claim line to `## Log` in the same edit.

If a claim is younger than the locally declared stale threshold, leave it alone.
The default threshold is 24 hours. A later agent may take an older claim but must
record that takeover in the log. Shared-drive sync is not transactional: never
have two agents intentionally edit the same packet concurrently.

### Block

Use `blocked` when work cannot continue. Name the exact blocker, the actor or
event that can unblock it, and the smallest next action. Waiting on a human is
`blocked`; it is not an unclaimed `open` packet.

### Finish

1. Put the durable result in its canonical project home.
2. Append a final log entry and record verification evidence.
3. Set `status: done` and bump `updated`.
4. Move the whole folder from `open/` to `done/`.

Archive; do not delete. A stale packet is evidence, while a missing packet is an
unexplained gap.

## Reach and transport

Choose the simplest transport every participating surface can actually reach:

| Transport | Best for | Main limitation |
|---|---|---|
| Local shared folder | Several agents on one machine | No access from web-only or remote agents |
| Synced private folder | Agents or people on authorised devices | Sync delay and concurrent-edit conflicts; local paths differ by device |
| Private Git repository | Cross-machine history and review | Agents need Git access; every transition requires pull/commit/push discipline |
| Relayed packet | A receiver with no shared storage | Human or coordinating-agent relay; no automatic discovery |

For cross-user or cross-machine routes, prefer a canonical SharePoint/GitHub URL
over another person's local synced path. If neither is reachable, include the
necessary text inside the packet and state that it is a relayed snapshot.

## Instruction pointers: where Cillian's question lands

The bus contract stays in the bus. Other instruction layers carry only a short
trigger pointer when their surface can act on it.

| Surface | Pointer? | Rule |
|---|---|---|
| Bus-root `AGENTS.md` / `CLAUDE.md` | Required | Canonical instance contract and platform pointer |
| Claude Code global `~/.claude/CLAUDE.md` | Optional; recommended when arbitrary local projects should discover the bus | One trigger plus the absolute bus path; no copied protocol text |
| Codex global `~/.codex/AGENTS.md` | Optional; same condition | One trigger plus the absolute bus path; no copied protocol text |
| Cowork project-instructions field | Required for a connected bus project | Purpose, scope, and instruction to fetch/read `CLAUDE.md`; no live state |
| Claude Personal Preferences / other personalization | Normally no | Identity and general working posture belong here, not a machine-specific bus path |
| Web-only chat | No filesystem pointer | Attach/paste the packet or provide a URL the surface can open |

Exact copy-ready pointer forms live in the scaffold's
`context/INSTRUCTION-POINTERS.md`. Before editing any Claude instruction layer,
follow `CLAUDE_INSTRUCTION_LAYERS.md`: slim pointer, correct reach, no dual-copy mirror.

## Automation ladder

Call the mechanism semi-automated only at the level actually implemented:

1. **Manual relay:** a person or coordinator names the packet to the receiver.
2. **Session-start discovery:** an agent checks `open/` when an applicable session
   begins and records its transition before stopping.
3. **Watcher notification:** a scheduled read-only watcher compares board state
   with its prior snapshot and notifies only on material changes.
4. **Event-driven execution:** a service wakes and authorises an executor. This is
   a separate agent system, not an automatic property of the folder protocol.

Default to level 2. Add a silent-on-no-change watcher only after the manual
lifecycle passes. Do not claim that a watcher can wake a platform unless that
capability has been observed on the live surface.

## Verification

Before adoption, run one fictional two-agent handoff and verify:

- a fresh agent finds the contract and packet without conversation history;
- every frontmatter key is present;
- the receiver can reach every required locator or has the content inline;
- claiming updates status, identity, date, and log together;
- another agent respects the active claim;
- a human approval dependency becomes `blocked` rather than being executed;
- completion places the result in its project and moves the packet to `done/`;
- no credentials, private identifiers, or inaccessible paths entered the packet;
- the board, frontmatter, and log agree; and
- any watcher stays silent when nothing changes.

## Anti-patterns

- Copying a live bus as a starter kit.
- Treating the bus as the canonical project or deliverable store.
- Duplicating protocol text into global instructions or Personal Preferences.
- Hard-coding one user's local path into a cross-user packet.
- Treating `to:` as authorization.
- Starting work before claiming.
- Rewriting another agent's log entry.
- Leaving human-blocked work as free `open` work.
- Calling periodic human notification "automatic agent collaboration."
- Deleting closed packets to make the board look tidy.

## Resources

- [SESSION_HANDOFF_SAVE_POINTS.md](SESSION_HANDOFF_SAVE_POINTS.md) - in-project cold-start continuity.
- `AGENTIC_TEAM_DESIGN.md` - governance for persistent agent teams.
- `COWORK_PROJECT_INIT.md` - document-workspace structure and instruction surfaces.
- `CLAUDE_INSTRUCTION_LAYERS.md` - reach-aware slim pointers.
- `SCHEDULED_JOBS_AND_POLLING.md` - watcher cadence and health.

## Pending amendments — shared-tier only

Neither applies to a single-owner personal bus, where every agent is the same
person's and local absolute paths are the correct locator. Both become binding
the moment a bus is shared across people, and must be folded into the protocol
before that bus carries its first packet.

1. **Locators must be portable.** On a shared bus, "prefer a canonical
   URL" (see § Reach and transport) hardens to a requirement: another person's
   local synced path is an invalid locator, because the mirror root differs per
   user.
2. **`to: any` is undefined across people.** On a personal bus `any` means any
   of the owner's agents, at the owner's authority. On a shared bus it could
   reach an agent with less reach than the author assumed — or more. A
   cross-person packet must name a person-qualified recipient and must not use
   `any`.

Recorded 2026-09-10 while confirming a personal bus as the tier-1 reference
instance.

## Version history

| Version | Date | Changes |
|---|---|---|
| 1.0 | 2026-09-09 | Initial protocol, extracted from the working Agent Handoff reference implementation and extended with reach-aware instruction pointers and a bounded automation ladder. |

---

**Protocol Version**: 1.1
**Last Updated**: 2026-09-10
