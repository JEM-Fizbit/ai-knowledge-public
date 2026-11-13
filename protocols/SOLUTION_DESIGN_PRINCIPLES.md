# Solution Design Principles

> Principles for designing code that matches stated intent — lean, scalable, readable — without drifting into band-aids or over-engineering.
>
> **Lifecycle:** the **Execute** phase (design discipline) — see [`DEVELOPMENT_LIFECYCLE.md`](DEVELOPMENT_LIFECYCLE.md) for how this fits with the other workflow protocols.

**Applies to:** All new code and non-trivial refactors
**Last Updated:** 2026-11-13
**Version:** 1.2.0

---

## Table of Contents

- [Overview](#overview)
- [When to Consult](#when-to-consult)
- [Core Principles](#core-principles)
- [Anti-Patterns](#anti-patterns)
- [Override Triggers](#override-triggers)
- [Self-Check Before Committing](#self-check-before-committing)
- [Relationship to BEST_PRACTICES_FIRST](#relationship-to-best_practices_first)
- [Resources](#resources)

---

## Overview

Two failure modes dominate AI-assisted coding. **Band-aid patching** accretes fixes around a symptom without addressing its cause. **Over-engineering** layers abstraction, flexibility, and configuration that the problem doesn't call for. Both produce code that is harder to maintain than what it replaces.

The principles below are the content-level rules for avoiding both. They are deliberately few and deliberately opinionated. When in doubt, match the spec — not more, not less.

### Key Benefits

- Prevents silent growth of complexity that no ticket asked for
- Catches the "three-commit patch cycle" that [`BEST_PRACTICES_FIRST.md`](BEST_PRACTICES_FIRST.md) diagnoses, by preventing the first symptom-fix commit from landing
- Gives a shared vocabulary (band-aid, magic value, premature abstraction) so code review can name the problem quickly

---

## When to Consult

- Writing any new function, module, or component
- Refactoring existing code where "simplify" is part of the goal
- Reviewing AI-generated code before accepting it
- On the second commit addressing the same issue — step back and self-check before the third

Skip for: one-line fixes, renames, typo corrections, obviously correct mechanical changes.

---

## Core Principles

### 1. Root cause over symptom

Before writing a fix, identify the mechanism that produces the bug. A symptom-fix that doesn't name the mechanism is a guess that will need follow-up fixes for related symptoms.

- If the bug is a race, the fix is synchronization or ordering — not a retry or a timeout bump.
- If the bug is stale cache, the fix is invalidation or revalidation — not disabling the cache.
- If the bug is a boundary violation, the fix is moving the boundary — not catching the error.

When you cannot identify the mechanism, say so explicitly and propose diagnostics, not a patch. See [`BEST_PRACTICES_FIRST.md`](BEST_PRACTICES_FIRST.md) for the escalation protocol when the symptom-fix cycle is already underway.

### 2. Parameterize, don't hardcode

Values that vary by environment, user, or deploy target belong in configuration — not in source. Values that are true facts about the domain can be constants, but they should be named.

- Env-varying values (URLs, credentials, feature flags) → env vars or config files.
- Domain constants (tax rate, page size limit, retry count) → named constants at module top.
- Magic numbers mid-function are almost always the wrong answer.

The cost of a named constant is one line. The cost of tracking down a hardcoded `86400` across a codebase in six months is an afternoon.

### 3. Extract, don't duplicate

Two copies of the same logic is a sign. Three is a rule. By the third copy, extract a function — not a class, not an abstraction, just a function.

The inverse is equally important: **don't extract until you have two copies.** A function that's called from one place, parameterized against a second hypothetical caller that doesn't exist yet, is premature abstraction (see below). Wait for the duplicate to appear.

### 4. Match the spec, don't exceed it

Code the feature that was asked for. Not the feature that might be asked for next quarter. Not the admin panel the feature might need someday. Not the retry logic for an API call that has never failed.

Scope creep during design feels like helpfulness. In review it reads as noise — reviewers cannot tell which lines implement the requested feature and which implement a speculative one. When the speculative requirement does arrive, the speculative code is usually wrong for it anyway.

### 5. Readability over cleverness

Code is read more times than it is written. A three-line loop that obviously does what it says beats a one-line reduce-filter-map chain that requires ten seconds of staring to parse. A named intermediate variable beats a deeply nested expression.

Cleverness earns its place only when (a) performance measurably demands it, or (b) the clever form is idiomatic in the language's ecosystem and the plain form would be the surprising choice. Neither is the default.

### 6. Structural invariant over statistical detector

When a class of bug must never occur, prefer making the bad state **unrepresentable** over **detecting** it after the fact. A structural contract holds by construction and is testable directly ("the invariant holds"); a detector chases a symptom that may be small, noisy, or regime-dependent, and silently fails when the symptom is below threshold.

- Leakage in a backtest: give the predictor an input type that *has no outcome field*, so it cannot read the answer — don't run a statistical test for "did the prediction correlate suspiciously with the future."
- Cross-series time ordering: order by an absolute timestamp (and *raise* if one is missing), so a future row cannot enter a training prefix — don't flag-after-the-fact when one does.
- Invalid state in a model: make it unconstructable (required field, enum, newtype), not validated-on-read in twelve call sites.

The tell that you're on the wrong side of this: you're writing code that *watches for* the bad thing. Ask whether the bad thing can be made impossible instead. (Worked examples — leakage surfaces and why the detector is fragile — in `LEAKAGE_SAFE_BACKTESTING.md`.)

---

### 7. Durable progress and paid-result custody

Apply this required contract when work advances an ingestion cursor, replaces authoritative data, or performs paid or externally consequential steps. The design-speed overrides below do not waive these durability, access or allowance boundaries. Use the existing datastore and the smallest mechanism that satisfies it; a new workflow service is not a requirement.

- **Progress follows durability.** Advance a cursor, validator, content hash or successful-processing marker only when all accepted items are durable in their destination or recoverable staging. Replay pending staged work independently of unchanged-input shortcuts. Track attempted refresh separately from the last successful snapshot.
- **Publish only validated replacements.** A failed or incomplete refresh must not replace last-good data with empty data. Validate and durably commit the replacement before making it current, using a transaction or equivalent atomic publication pointer with concurrency checks. Preserve the previous usable version until replacement succeeds. Retractions, permission changes and authorised deletion have separate semantics; retained data must not bypass current access or source-use restrictions.
- **Save paid progress before dependent work.** Durably reserve a logical step before dispatch; persist its received response before parsing, validation, another paid step or publication. Save independent completed results individually. Identity includes the relevant inputs, source snapshot, model/settings and contract version; a changed input invalidates only dependent results. Do not buy again a compatible result already held.
- **Separate receipt from validation.** A saved raw response is evidence, not proof of a valid result. Persist validation status and any authorised correction ordinal/count. Resume deterministic parsing/validation from that receipt; an invalid result neither vanishes nor gains a fresh allowance. A previously classified invalid response follows the existing bounded correction/hold path rather than cycling through validation forever.
- **Reconcile uncertainty.** A timeout, process death or lost acknowledgement does not prove non-execution. Keep a durable unresolved intent until an original result or authoritative evidence of non-acceptance resolves it. Disable automatic SDK/transport retries for consequential submissions unless the provider's verified idempotency contract makes them safe under the same logical key and allowance. Proven rejection can return to a bounded, authorised retry policy; an unconfirmed outcome cannot.
- **Keep admission authoritative.** Atomic ownership, fencing and persistent attempt/allowance state cover every scheduler, manual and CLI entrypoint. Persist the reservation before dispatch; stop new paid work if custody or admission cannot be established. Lease expiry alone never turns a possibly accepted dispatch into permission to resend. Existing production authority remains sufficient for ordinary in-scope calls; this contract grants no new allowance and adds no per-call human approval ceremony.
- **Keep recovery possible.** Store receipts where they survive the deployed worker/runner replacement boundary. Preserve output fidelity and provenance; no shortened response, reduced model/voice quality or fresh research substituted as a recovery shortcut. Rollback keeps a recovery-aware reader and admission controls. Do not erase journals or disable their checks to clear a hold.
- **Bound custody explicitly.** Keep recovery data private under the applicable source, privacy and retention policies. Do not persist credentials, authentication headers or secret-bearing signed URLs inside request snapshots or receipts; resolve transport credentials separately at dispatch and use a non-secret account namespace/digest where identity needs it. A completed journal may be removed atomically with verified publication if the project's audit/receipt obligations are satisfied; unresolved paid results and intents must not be swept away as temporary files. This is not permission to retain everything indefinitely.

The following adapter-based example specifies the boundary; it is not a datastore implementation. `reserve(step)` atomically checks identity, current access, ownership and the approved policy, then returns a saved receipt, a hold/busy result, or a newly persisted dispatch reservation. A replacement process reads the same durable store. `saveResponse` verifies and durably seals the complete response (or private object reference plus length/hash) before returning; admission and publication reject stale fences. A verifiably matched late response is still attached immutably to its original dispatch identity (or durably quarantined for reconciliation), even after ownership changes; it cannot overwrite another response or publish under a stale owner. If a write acknowledgement is lost, the next read reconciles its committed state.

```javascript
async function resumePaidStep(journal, step, invokeOnce) {
  const claim = await journal.reserve(step);
  if (claim.kind === "saved") return claim.receipt;
  if (claim.kind !== "dispatch") {
    throw new Error(`Step held: ${claim.kind}`);
  }

  let receipt;
  try {
    // One submission. The adapter disables automatic paid-request retries.
    receipt = await invokeOnce(step.request);
  } catch (error) {
    // The original reservation remains unresolved even if this write fails.
    await journal.recordUnknown(claim.id, claim.fence);
    throw error;
  }
  // Outside the dispatch catch: a save failure must not trigger generation.
  await journal.saveResponse(claim.id, claim.fence, receipt);
  return receipt;
}
```

This conservative example holds every dispatch exception. A project may reconcile a proven rejection and schedule another eligible attempt; it must not infer rejection from a timeout or generic exception. Backend atomicity and crash survival need the affected-workflow checks in [QA Protocol](QA_PROTOCOL.md#recovery-and-publication-gate). [AI Evals](AI_EVALS.md#shared-foundations) already requires production-generation receipts; its evaluation-specific approval/blinding rules do not become production runtime policy.

---

## Anti-Patterns

### ❌ Band-aid fix

```typescript
// ❌ Bug: occasional duplicate rows in a list view.
//    Fix: filter duplicates client-side before render.
function renderList(items) {
  const seen = new Set();
  const unique = items.filter(i => !seen.has(i.id) && seen.add(i.id));
  return unique.map(renderItem);
}
```

The duplicates are coming from somewhere. The fix is in the query (JOIN producing a Cartesian, missing DISTINCT, stale cache, duplicate subscription) — not in the render layer. Patching at the render layer means the next view of the same data will have the same bug and need its own patch.

```typescript
// ✅ Trace to the source. If it's a query bug, fix the query.
//    If it's a subscription bug, fix the subscription.
//    The render layer renders what it's given.
function renderList(items) {
  return items.map(renderItem);
}
```

### ❌ Hardcoded magic values

```typescript
// ❌ What is 86400? Why that value? Can it change?
if (Date.now() - session.createdAt > 86400 * 1000) {
  logout();
}
```

```typescript
// ✅ One line of cost, permanent clarity.
const SESSION_LIFETIME_SECONDS = 86400; // 24h
if (Date.now() - session.createdAt > SESSION_LIFETIME_SECONDS * 1000) {
  logout();
}
```

If `SESSION_LIFETIME_SECONDS` is set by product policy and varies by deploy, it moves to config. If it's a fixed spec decision, it stays as a named constant. Either way, it is not `86400`.

### ❌ Premature abstraction

```typescript
// ❌ Called from one place. "Flexibility" for a second caller that doesn't exist.
interface FetchStrategy {
  fetch(url: string): Promise<Response>;
}
class DefaultFetchStrategy implements FetchStrategy { /* ... */ }
class RetryingFetchStrategy implements FetchStrategy { /* ... */ }
function createClient(strategy: FetchStrategy = new DefaultFetchStrategy()) { /* ... */ }
```

```typescript
// ✅ One caller, one concrete implementation. When a second caller arrives with
//    genuinely different needs, extract then.
async function fetchFromApi(url: string): Promise<Response> {
  return fetch(url);
}
```

The abstraction's cost is paid immediately (more files, more types, more indirection). Its benefit is paid only when a second concrete implementation appears. Premature abstraction is a loan with no guarantee the payoff ever lands.

### ❌ Copy-paste-modify

```typescript
// ❌ Three handlers, 90% identical.
function handleCreate(req) {
  const user = await getUser(req);
  validatePermissions(user, 'create');
  const data = parseBody(req);
  return db.insert('items', data);
}
function handleUpdate(req) {
  const user = await getUser(req);
  validatePermissions(user, 'update');
  const data = parseBody(req);
  return db.update('items', req.params.id, data);
}
function handleDelete(req) {
  const user = await getUser(req);
  validatePermissions(user, 'delete');
  return db.delete('items', req.params.id);
}
```

```typescript
// ✅ Extract the duplicated prefix. The three handlers become readable.
async function authorizeAndParse(req, action) {
  const user = await getUser(req);
  validatePermissions(user, action);
  return { user, data: action === 'delete' ? null : parseBody(req) };
}

async function handleCreate(req) {
  const { data } = await authorizeAndParse(req, 'create');
  return db.insert('items', data);
}
// ... handleUpdate, handleDelete similarly
```

Three copies is the threshold. Two copies is a judgment call — if the bodies are trivially short and the duplication is obvious, leaving them separate is often clearer than an abstraction.

### ❌ God component / god function

A 400-line React component that owns fetching, state, derived values, mutation handlers, rendering, and three different dialogs is a god component. A 200-line function that does validation, parsing, transformation, persistence, and notification is a god function. They're hard to test, hard to read, and impossible to reuse.

The fix is not to split arbitrarily. The fix is to name the responsibilities and extract each one. If you can't name the responsibilities, the code has no design — design it first, then split.

---

## Override Triggers

These principles are defaults, not laws. Override them deliberately, and **say so in the PR description or commit message** so reviewers and future readers know the decision was intentional.

### Explicit user directive

When the user explicitly asks for a "quick fix," "just patch it," "spike," "MVP," or "throwaway" — defer to speed. Note the trade-off in your response (e.g., "This is a band-aid on the render layer; the root cause is likely in the query. Flagging for follow-up.").

### Production urgency

Live incident, money-losing bug, customer-facing outage. Stop the bleeding first, root-cause second. File a follow-up to unpatch the band-aid once the fire is out.

### Throwaway code

Research spikes, data migrations that run once, demos for a stakeholder meeting tomorrow. The code will not live long enough for design debt to matter. Skip the abstraction work entirely.

### Known refactor incoming

If you already know the module is scheduled to be rewritten in two weeks, a band-aid is correct — investing in a proper fix is investing in code that will be deleted.

In all four cases, the override should be **explicit**, not assumed. Silent overrides become the new norm.

---

## Self-Check Before Committing

Before `git commit`, ask five questions. If any answer is "no" or "not sure" — consider another pass.

1. **Does this fix the cause, or a symptom?** If a symptom, is this an explicit override (urgency, throwaway, directive)?
2. **Is every non-obvious literal named?** (`86400`, `"admin"`, `0.15`, `"https://api..."` — any of these anonymous in the diff?)
3. **Is every duplicate intentional?** (Are there 2+ copies of a block I just wrote? Is that the right choice here?)
4. **Does this match the ticket/spec, or does it exceed it?** If exceeds, is the extra work justified and flagged in the description?
5. **Can a reader with no context read this in under a minute and understand what it does?** If not, what would make it faster to read — better names, fewer nesting levels, a comment explaining *why*?

These aren't gates. They're a last look.

---

## Relationship to BEST_PRACTICES_FIRST

[`BEST_PRACTICES_FIRST.md`](BEST_PRACTICES_FIRST.md) is the **process** cousin of this protocol. It answers "when should I stop patching?" (answer: by the third commit on the same issue, at the latest).

This protocol answers "what makes a fix a patch vs. a solution?" — the content-level rules that prevent the first patch commit from landing in the first place.

Consult both:

- **SOLUTION_DESIGN_PRINCIPLES.md** — before writing new code, to pick the right design from the start.
- **BEST_PRACTICES_FIRST.md** — when you notice yourself in a symptom-fix loop, to escalate to a proper redesign.

An agent that reads one should see a pointer to the other.

---

## Resources

- Related protocols: [`BEST_PRACTICES_FIRST.md`](BEST_PRACTICES_FIRST.md) (when to escalate out of a symptom-fix loop), `GIT_CONVENTIONS.md` (commit message discipline for flagging overrides).
- [Rule of three](https://en.wikipedia.org/wiki/Rule_of_three_(computer_programming)) — the "three copies → extract" heuristic under Principle #3, popularised by Martin Fowler's *Refactoring*.
- [YAGNI](https://martinfowler.com/bliki/Yagni.html) — backs Principle #4 (match spec, don't exceed).

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.2.0 | 2026-11-13 | Durable progress, validated publication and production paid-result custody with explicit uncertainty, privacy and rollback boundaries. |
| 1.0 | 2026-04-24 | Initial release. Five principles (root cause, parameterize, extract, match spec, readability), five anti-patterns, four override triggers, self-check. Cross-links with BEST_PRACTICES_FIRST. |
| 1.1 | 2026-06-14 | Added Principle #6 (structural invariant over statistical detector — make the bad state unrepresentable, don't watch for it). From a research project's backtesting-leakage work; cross-links LEAKAGE_SAFE_BACKTESTING. |
| 1.1.1 | 2026-10-03 | Resources: replaced the dead Martin Fowler "Rule of Three" bliki link (404) with the Wikipedia article. No rule change. |

---

**Protocol Version**: 1.2.0
**Last Updated**: 2026-11-13
