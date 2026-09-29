---
name: catch-up
description: "Give a short, context-aware read of the current session: what was actually done, where things stand, what genuinely needs a decision from the user, and the next concrete step. Sections with nothing real in them are omitted rather than filled. Use when the user asks to recap, summarise where we are, catch me up, remind me what we did, give me the status, or where did we land — including when returning to a long session. Recognise equivalent intent without magic words. Do not trigger on requests to summarise a document, file, article, email, meeting or other external content; that is content summarisation, not a session recap. Do not trigger on wrap up, finish for now, save our progress or checkpoint requests, which belong to the wrap-up skill. Catch-up is read-only and writes nothing."
version: 1.1.0
metadata:
  version: "1.1.0"
---

# Catch-up

> **Skill version:** v1.1.0

A status read, not a transcript. The user is asking because the thread got long, not because they want it replayed. Read-only: write no files, create no artifacts, commit nothing, update no savepoint.

## The four sections

Use these labels, in this order, as bold inline labels — no headings, no nesting, no tables.

```
**Done** — …
**State** — …
**Needs you** — …
**Next** — …
```

- **Done** — what actually completed and where it landed. Only items with evidence behind them: a tool result, a file that exists, a commit that happened. An intention is not an outcome.
- **State** — what is in flight, partially done, or deliberately parked, plus delivery state: committed or not, pushed or not, deployed or not, still local. This is the line most often needed and least often given.
- **Needs you** — genuine decisions, and anything gone wrong that changes the user's plans. Order by consequence. Each item carries, in order: what the thing is (assume no familiarity with internal vocabulary), why it matters, your default and why, the honest cost if the default is wrong. Cap at three; if there are more, carry the top three and say how many remain.
- **Next** — the single next concrete action.

**Omit, do not fill.** A section with nothing real in it does not appear — no "N/A", no "nothing to report", no manufactured decision to populate *Needs you*. If only one section has content, the recap is one line, and that is correct.

## Budget

The brevity is the deliverable. A recap that sprawls has failed even if every line is true.

- 200 words maximum for the whole recap. Most are far shorter.
- One line per item. An item needing a second line is a decision — give it the four parts under *Needs you*, or put it in a document and link it.
- No preamble, no "here is a recap of our session", no closing offer to expand.
- Do not restate the previous message; the user just read it.
- Do not list evidence to show you checked. Outcomes only.
- Never a bare path. Anything the user should read arrives as a hyperlink.

## Honesty

A recap is where failures quietly become progress. Guard against it.

- Attempted but unverified is *State*, never *Done*.
- A step that failed or was skipped appears — under *State* or *Needs you*. Never dropped for tidiness.
- Claim no commit, push, deployment or upload without evidence it happened. "Committed locally, not pushed" is the useful sentence.
- If unsure whether something landed, check before writing the line, or mark it unverified. Do not infer completion from intent.
- Do not report a conclusion more confidently than it was held at the time.

## Scope

Default to the whole session. Honour a narrower request ("since lunch", "just the tracker work"), and name the window only when it is not the whole session.

If the session has no prior work to recap, say so in one line and stop. Do not reconstruct a session from files, memory or project state.

## Do not

- Do not write files, create artifacts, commit, deploy or update a savepoint. Session closeout with a savepoint and authorised delivery is `wrap-up`; catch-up has no side effects.
- Do not summarise external content — a document, email, meeting or article is a different request.
- Do not deliver as a file, artifact, dashboard or document, even where those are available and the content would render well. A recap is a chat reply, always.
- Do not offer a recap unprompted, or append one to an unrelated answer.
