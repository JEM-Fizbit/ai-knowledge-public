# Best Practices First Protocol

**Last Updated:** 2026-02-04

> Stop symptom-fixing. Find the architectural solution first.
>
> **Lifecycle:** the **Execute** phase (escalation rule) — see [`DEVELOPMENT_LIFECYCLE.md`](DEVELOPMENT_LIFECYCLE.md) for how this fits with the other workflow protocols.

---

## When to Escalate

**STOP and research best practices if you observe:**

1. **Symptom-Fixing Pattern** - Multiple commits for the same issue
   - Example: "fix timeout" → "add retry" → "increase timeout" (all symptoms of missing async pattern)
   - **Action:** Step back, find root cause, propose comprehensive solution

2. **Framework Problems** - Issues with caching, state, routing, data fetching
   - **Action:** Check official docs for recommended patterns BEFORE implementing fixes

3. **3rd commit on same feature** - You missed the best practice

4. **User asks "better approach?"** - Current approach is wrong

---

## Research Protocol

Before implementing ANY complex fix:

1. `git log --oneline -10` - Check for related fixes
2. Check `docs/protocols/` - Known patterns for this?
3. Check framework docs - What's recommended?
4. **Propose architecture FIRST** - Then implement

---

## Anti-Pattern

**Bad:**
```
Commit 1: "fix race condition"
Commit 2: "prevent stale data"
Commit 3: "disable cache"
Commit 4: [User asks] "implement ISR" ← Should have been Commit 1!
```

**Good:**
```
Commit 1: "implement on-demand revalidation per Next.js ISR best practices"
[Done. No iteration needed.]
```

---

## Key Principle

**If you're on the 3rd commit for the same problem, you missed the best practice.**
