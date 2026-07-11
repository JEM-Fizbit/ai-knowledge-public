# AI Observability

> Runtime visibility for AI/LLM calls: latency, success/failure, and a traceId linking multi-step flows — not just cost. In-stack first, surfaced as a push. The companion to AI_EVALS (offline quality) for online behaviour.
>
> **Lifecycle:** the **Operate** dimension (post-ship, runtime) for AI-powered projects — see [`DEVELOPMENT_LIFECYCLE.md`](DEVELOPMENT_LIFECYCLE.md) for how this fits with the other workflow protocols.

**Applies to:** Any production AI app making LLM calls. Tiered — minimum is per-call latency + outcome + a traceId captured to your own datastore.
**Last Updated:** 2026-07-05
**Version:** 1.1

---

## Table of Contents

- [Overview](#overview)
- [When to use](#when-to-use)
- [The pattern](#the-pattern)
- [Operating model — how metrics get surfaced](#operating-model--how-metrics-get-surfaced)
- [Anti-patterns](#anti-patterns)
- [Resources](#resources)

---

## Overview

Evals tell you whether quality is good *offline*. Observability tells you what's happening *in production right now* — how slow calls are, what's failing, how much you're spending, and which calls belong to the same user action. Most AI apps log token cost and nothing else, which means: no latency, no failure visibility, and no way to trace a multi-step flow when it goes wrong.

> **Core principle:** Capture latency + outcome + a correlation id, not just cost — and keep it **in-stack** (your own datastore) before reaching for an external SaaS. A telemetry integration that's wired but never surfaced is *worse* than none: it reads as coverage while capturing nothing useful (one solo project had a `requestId` field defined and never populated, and a stale third-party analytics hookup that broke after a refactor).

The lean version reuses what you already have. On one solo AI app, the existing `TokenUsage` table gained latency/status/error capture and trace correlation with **zero schema change** — traceId reused an unused column, the rest folded into a metadata JSON. Promote to first-class indexed columns only when trace-queries or dashboards actually demand it.

### Key benefits

- **Debuggable** — a slow or failed AI interaction can be traced, not guessed at.
- **Failures are visible** — most cost trackers are success-only; you're blind to errors without this.
- **Multi-step flows correlate** — one traceId per chat turn / generation / scoring run links its child calls.
- **No data egress** — prompts and usage stay in your own database; no third-party SaaS by default.

---

## When to use

| Scenario | Use this protocol? |
|----------|--------------------|
| Production AI app making LLM calls | **Yes** |
| AI-powered project heading to production | **Yes — design the wrapper in early** |
| Local script / prototype with no users | Optional (console logging is fine) |

---

## The pattern

Validated on a solo AI content app's in-stack AI-call observability (a shipped, archived spec).

**1. A `traced()` wrapper around every AI call.** It times the call, assigns or propagates a traceId, logs token usage + `durationMs` on success, logs an **error row** (zero tokens) on failure, and **never throws** (tracking failures must not disrupt the pipeline). One wrapper, wired at each call site:

```ts
const response = await traced(
  { source: "scoring", model, workspaceId, traceId, metadata },
  () => anthropic.messages.create({ ... }),
);
```

**2. traceId correlates a flow.** Generate one id per logical flow (a chat turn, a generation request, a scoring run) and thread it through that flow's child calls. **Reuse an existing flow id** where one already exists (one app's draft-generation flow already had a `groupId` over its parallel calls — that became the traceId for free).

**3. In-stack storage, no migration.** Reuse the existing usage table. Put the traceId in an existing correlation column; fold `durationMs` / `status` / `errorMessage` into the metadata JSON. **Promote to indexed columns only when** you actually need fast trace-queries or dashboards — not before.

**4. Capture errors, not just successes.** A success-only cost log hides exactly the calls you most need to see. Error rows carry the outcome + message + duration with zero tokens / null cost.

**5. Defer prompt/response capture.** Logging full prompts/responses has PII and size cost — leave it out of v1 unless a concrete debugging need justifies it, and gate it behind a flag when added.

---

## Operating model — how metrics get surfaced

Capture is continuous and automatic; the question is how the operator *sees* it without babysitting a dashboard.

- **Weekly Slack digest (primary).** A scheduled job summarises the week — spend, latency p50/p95, error rate by source/feature, top cost drivers, and anything anomalous — and pushes it to the operator's DM. Built per `AUDIT_ROUTINE_STANDARD.md` (silent-green, push-delivered, no dashboards to check) over `SLACK_OPS_NOTIFICATION.md`. Shares the digest with [AI_EVALS.md](AI_EVALS.md)'s weekly eval status — one push covers offline quality + online behaviour.
- **In-thread, by Claude.** When working in an AI code path, Claude surfaces relevant anomalies it notices (error spikes, latency, runaway cost) rather than waiting to be asked.
- **On-demand.** An `obs:report` script or a saved SQL view over the usage table for when the operator wants to dig.
- **Dashboard — deferred.** Dashboards rot unwatched for a solo operator. Build one (Metabase / Supabase SQL / Grafana over the existing table) only if the weekly push proves insufficient.

---

## Anti-patterns

### Building a trace viewer before capturing anything

```
❌ Bad — designing an admin dashboard UI as step one.
✅ Good — capture latency/outcome/traceId into the existing table first.
   Surface via the weekly push; build a viewer only if that's not enough.
```

### Reaching for an external SaaS by default

```
❌ Bad — piping prompts + usage to a third-party observability SaaS reflexively.
✅ Good — in-stack first (your own DB, no egress). Adopt Langfuse/Phoenix later
   only if you specifically want its UI and accept the data leaving your stack.
```

### Success-only logging

```
❌ Bad — only writing a row when the call succeeds.
✅ Good — log error rows too (zero tokens, outcome + message). Failures are the
   point of observability.
```

### Wired but never surfaced (shelfware)

```
❌ Bad — rows accumulate in a table nobody queries; a telemetry field that's
   never populated; a stale integration that broke after a refactor.
✅ Good — the weekly digest + in-thread anomaly surfacing. If it isn't monitored
   and used, it isn't observability. Rip out dead/stale telemetry — it's worse
   than none because it reads as coverage.
```

### Premature column promotion

```
❌ Bad — a production schema migration to add indexed obs columns on day one.
✅ Good — metadata JSON + an existing column for v1 (no migration). Promote to
   indexed columns only when trace-queries/dashboards actually need them.
```

---

## Resources

- [AI_EVALS.md](AI_EVALS.md) — the offline-quality companion; shares the weekly digest
- `SLACK_OPS_NOTIFICATION.md` — routing the digest to Slack DM
- `AUDIT_ROUTINE_STANDARD.md` — the silent-green push-delivery contract the digest follows
- `SCHEDULED_JOBS_AND_POLLING.md` — scheduling the weekly digest
- `AI_TOOL_ORCHESTRATION.md` — where streaming-call usage is read (at stream end) for tracing

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.1 | 2026-07-05 | Updated the validation link to the archived shipped spec path. |
| 1.0 | 2026-06-06 | Initial release. Extracted from a solo AI content app's observability pilot: traced() wrapper, traceId correlation, in-stack metadata-first capture (no migration), error-row capture, weekly-digest operating model. |

---

**Protocol Version:** 1.1
**Last Updated:** 2026-07-05
