# Public Presence Register

> **Scope:** every public surface personally identifiable to {FULL_NAME}: their own accounts and sites, pages others host that they can influence, and pages they have little or no control over. **Out of scope:** {OUT_OF_SCOPE, e.g. products and company accounts}.
> **Last updated:** {YYYY-MM-DD}
> **Phase status:** Phase 1 (survey and inventory) not started — see Plan.

**Tiers:** **P1** they control it (their login). **P2** someone else hosts it, but they can edit, claim, file or ask for a correction. **P3** little or no control (brokers, mirrors, press, namesakes).

**Public descriptor:** "{DESCRIPTOR}" (durable, not tied to a job title). Profiles converge on it.

**Public location:** "{PUBLIC_LOCATION}". Statutory and legal filings keep the real address.

**Jurisdictions:** {e.g. UK, US} (which broker and registry playbooks apply).

**Correction principle:** dated content that was accurate when published (bylines, event speaker pages, press, testimonials) is a historical record and is **not** corrected. Only pages presenting stale information **as current** are.

**Dormant-account rule:** hold a dormant account only if its handle is unique and matches the person's name or brand, **and** their audience would plausibly look for them there. Held accounts are **parked** (descriptor, public location, link to the main profile, strong password and 2FA) and not flagged as stale. Everything else is deleted, by the person.

**Conventions:** ⚠ = major issue. † = account mail arrives at that address, but the login address is not independently confirmed. "confirm" = ownership inferred, not yet confirmed by the person. Cite rows by surface name, never by number. Status words: *requested* (we asked), *confirmed* (the site said yes), *verified* (we saw it ourselves).

---

## Private settings

Not shown on the dashboard. Never copy these into anything public.

- **Names and handles to search:** {LEGAL_NAME}; {PUBLIC_NAME}; {FORMER_NAMES}; {HANDLES}
- **Email addresses to look for:** {EMAILS}
- **Phone numbers to look for:** {PHONES}
- **Places lived (for broker searches):** {TOWNS_AND_PERIODS}
- **Current roles:** {ROLES_WITH_START_DATES, as the person describes them}

---

## Table P1 — Surfaces they control

### P1a — Professional, publishing and own sites

| Surface | URL / handle | Type | Status | Last visible activity | Account email | Phase 1 notes |
|---|---|---|---|---|---|---|

### P1b — Personal social, reviews and community

| Surface | URL / handle | Type | Status | Last visible activity | Account email | Phase 1 notes |
|---|---|---|---|---|---|---|

### P1c — Dormant or low-exposure accounts

| Surface | URL / handle | Last seen | Account email | Phase 1 notes |
|---|---|---|---|---|

---

## Table P2 — Surfaces they can influence or ask to correct

### P2a — Current roles and statutory records

| Surface | Owner | URL | What it shows | Route to change | Status | Phase 1 notes |
|---|---|---|---|---|---|---|

### P2b — Past roles, events and speaker pages

| Surface | Owner | URL | What it shows | Status | Phase 1 notes |
|---|---|---|---|---|---|

### P2c — Claimable aggregators and knowledge graph

| Surface | URL | What it shows | Route | Phase 1 notes |
|---|---|---|---|---|

---

## Table P3 — Limited or no control

| Class | Examples | What it exposes | Remedy | Phase 1 notes |
|---|---|---|---|---|
| Contact-data brokers | | | Opt-out requests | |
| People-search sites | | | Opt-out per listing | |
| Registry mirrors | | | Fix the registry upstream | |
| Executive and people aggregators | | | Claim or correct where offered | |
| Scraped bios | | | None practical | |
| Research and patent indexes | | | Fix ORCID upstream | |
| Namesakes and unverified accounts | | | — | |

---

## Findings

Major issues, tracked to closure. **Status:** Open · In progress · Resolved.

| Finding | Status | Next step / outcome |
|---|---|---|

---

## Plan

### Phase 1 — Survey and inventory · Now
- Inventory every public surface by control tier; list the major issues as Findings.

### Phase 2 — Urgent exposure fixes · Next
- Data-broker and people-search removals; home address on public registries; leaked personal email in public code; account-security dependencies; privacy settings on active social accounts.

### Phase 3 — Accuracy and consistency · Later
- Bring live profiles into line with the descriptor (upstream first: ORCID, then Wikidata, then the Google panel); keep, park or delete dormant accounts; correction requests for pages that fail the correction principle.

### Phase 4 — Publications and media record · Later
- Optional: reconcile indexed works, press and podcasts with the person's own bibliography.

---

## Maintenance

- **Add a row** when opening an account that creates a public profile, or on learning of a new page that describes the person. **Mark `retired`** rather than deleting rows.
- **Re-sweep** every 6 to 12 months and after every role change, the moment most third-party bios go stale.
- **Rebuild the dashboard** after edits, if one is kept: `python3 build_dashboard.py path/to/this-register.md`.
