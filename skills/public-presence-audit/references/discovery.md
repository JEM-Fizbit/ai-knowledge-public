# Discovery: finding every surface

Phase 1 and every re-sweep. Aim for coverage first and judgement second. Record each find in the register with what it shows and its tier, even when nothing needs doing. A row that says "checked, correct" saves the next sweep from checking it again.

## 1. Start from what the person knows

Ask for a quick list: their main profiles, personal sites, blogs or newsletters, current and recent roles, boards and trustee posts, and any account they remember opening and abandoning. People forget a lot, so don't rely on this list. It seeds the searches.

## 2. Web searches

Run each name variant, in quotes, alone and combined with each context: employers past and present, boards, city, university, field. Useful patterns:

- `"First Last"` and `"First M. Last"`, plus any former names
- `"First Last" site:linkedin.com`, `site:x.com`, `site:crunchbase.com`, `site:theorg.com`, `site:muckrack.com`
- `"First Last" CEO`, `director`, `trustee`, `board`, `speaker`, `podcast`, `interview`
- The person's email addresses and phone numbers, in quotes. This is how exposure on broker and scraped pages turns up.
- Image search on their main headshot, to find pages that reuse it

Search engines block logged-out checks on some sites: Google Scholar, ResearchGate, Academia.edu, Reddit, 192.com, Bloomberg, Reuters, WSJ and MarketScreener, among others. Note each one as "not checked, blocked", then check it in the person's own browser if they have one connected.

## 3. Handle discovery

Try their usual handles directly on the platforms that matter to them. Only an account the person confirms, or that links to their known profiles, counts as theirs. Common platforms: X, Bluesky, Threads, Instagram, Facebook, TikTok, YouTube, LinkedIn, GitHub, Medium, Substack, Pinterest, Reddit, Quora, SlideShare, Gravatar, about.me, Calendly, Linktree, Wellfound (formerly AngelList), Meetup, Strava, TripAdvisor, Goodreads, Letterboxd.

Namesakes are the norm. When a handle belongs to someone else, record it once in P3 as "namesake, not the person" so the next sweep doesn't re-investigate it.

## 4. Mailbox sweep (the best source of forgotten accounts)

If a mail connector is available and the person agrees, search their mailbox **read-only** for account mail:

- Subjects or bodies with *welcome to*, *verify your email*, *confirm your account*, *your account*, *password reset*, *new sign-in*, *receipt*, *your subscription*
- Senders like `no-reply@`, `noreply@`, `accounts@`, `security@`
- Google Alerts or similar alerts on their name

Group the hits by service and note the most recent date: that is roughly when the account was last used. Blind spots to state in the register:

- Accounts opened with a different email, such as a work address, an old ISP address or a secondary Gmail
- Mail older than the mailbox's retention, since many mailboxes are only dense for the last few years

## 5. Structured sources

- **Company registries** such as Companies House for the UK (`references/registries-uk.md`). Search the officer name. People are often split across several unlinked officer records, and each shows different appointments and addresses.
- **Charity registers** for trustee roles.
- **Research indexes:** ORCID, OpenAlex, Semantic Scholar, PubMed, Google Scholar and Google Patents. These feed the knowledge graph.
- **Knowledge graph:** search the name on Google and look for a knowledge panel, and search Wikidata. See `references/knowledge-graph.md`.
- **Aggregators:** Crunchbase, The Org, Muck Rack, Equilar, CB Insights, PitchBook, Clay and similar.
- **Brokers and people-search sites:** see `references/brokers.md`. Search each one for the person's name plus the locations they have lived in.

## 6. Own code and content

- **GitHub and other code hosts:** public commits carry the author email. Check `https://api.github.com/users/HANDLE/events/public`, or clone and run `git log --format='%ae' | sort -u` on their public repos. Public forks of other people's repositories also show on their profile.
- **Personal sites and blogs:** what the contact page, the "about" page and the legal notice reveal. A company legal page often carries a registered office that is really a home address.

## 7. What to record for each surface

Surface name · URL or handle · what it shows (quote the stale or exposed part) · status (live, dormant, stale, private, historical, retired) · last visible activity · the account email for P1 rows (register only) · route to change it · Phase 1 notes, with ⚠ on major issues.

Close Phase 1 with the **Findings** list: the handful of issues that matter, most urgent first, each with a proposed next step.
