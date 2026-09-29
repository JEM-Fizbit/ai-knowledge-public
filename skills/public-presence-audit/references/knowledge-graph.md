# Knowledge graph and claimable aggregators

Phase 3. These pages summarise the person for everyone who searches their name, and they copy each other. **Fix upstream first**, or the downstream page reverts.

The usual chain: **ORCID → Wikidata → Google knowledge panel**, with research indexes (OpenAlex, Semantic Scholar) also fed by ORCID. A Wikidata item is often created automatically from an ORCID record with the description "researcher", and Google then shows "Researcher" as the person's title.

**Last verified: September 2026.**

## ORCID

For anyone with papers, patents or an academic past. The person logs in; you can then edit section by section with their approval.

- Update the name and other names, a short biography in the descriptor's spirit, employment with dates the person gives you, education, distinctions, service and memberships (board and trustee roles), websites, and works (add by DOI).
- Set each item's visibility to public, or it won't propagate.
- The forms are built with Angular Material. Type into fields rather than setting values by script, or the form won't register them. Clicking outside a dialog closes it and loses the edits. Watch for text doubled by autofill ("CEOCEO").
- Changes reach Wikidata and OpenAlex over weeks, not days.

## Wikidata

Openly editable. **The person must be logged in.** An anonymous edit publishes the editor's IP address in the page history. Never edit anonymously.

- **Label and aliases:** the public name, plus full and former names as aliases.
- **Description:** short, lowercase, no full stop. It usually takes the form *nationality + descriptor*, such as "British-American product leader and investor". **Check the other languages too.** Descriptions in other languages drift independently and often still say "researcher". Correct them or remove any that are wrong.
- **Statements:** occupation (set the right one to preferred rank rather than deleting the others), educated at, awards, employers. **Every statement needs a reference**: ORCID, an official bio, an award page.
- In a logged-in browser session, the edit API (`wbeditentity` with the session's CSRF token) is quicker than the UI for bulk statement edits. Show the person the diff before sending it.

## Google knowledge panel

Search the person's name. A panel with a "Claim this knowledge panel" link, or a verified "Name on Google" card, is the target.

- **Claim or verify** through the person's Google account. Google checks it against their linked official profiles. After verification the menu may *still* show "Claim this knowledge panel". That doesn't mean a different account holds it.
- **Suggest edits** as the verified owner: choose the field (usually the subtitle), give the new value, and **add a citation URL**. Google requires a public page that supports the change. An independent page (an employer bio, a board bio, an award profile) is stronger than the person's own site. Offer a primary citation and one or two backups.
- A confirmation email arrives, and changes take one to several weeks. Put a re-check date in the register.
- Images, videos and other captions are chosen by Google. Fix them at their source if possible. A dated video caption that was accurate when published passes the correction principle.

## Crunchbase

Usually shows stale "current" roles because it rarely gets updated.

- The person creates a free account (they do this, not you). Connecting LinkedIn and verifying email lets them claim and edit their person profile.
- The edit page has sections for Overview (website, bio, location), Primary Job, Jobs, Founded Organizations and Education. **Each job edit is queued with "Continue"; nothing is live until "Save All Edits".** Show the review page to the person before saving.
- When adding a job, check that the organisation is the right entity. The org name may differ from the everyday name. Crunchbase's own autocomplete and org data (location, description) help confirm it.
- **Founded Organizations can't be removed by the person.** Removal needs an email to Crunchbase support. Ask whether the person minds the attribution first: some people accept "co-founder" from a third party (as an early investor or founding board member) even though they wouldn't claim it themselves.
- Edits appear within minutes. Verify them logged out.

## Muck Rack

Auto-generates a "journalist" profile from anything published under the person's byline, including pieces where they were only quoted.

- The "Issue with article?" menu on each item is a **mailto link to `hello@muckrack.com`**. Draft the email yourself instead, naming the article and saying the person was quoted, not the author.
- **Don't claim the profile** unless the person is a journalist. Claiming makes them a pitchable contact in a PR database.
- Note the pieces they genuinely wrote. They belong in the person's bibliography (Phase 4).

## The Org

Org charts per company. A person's profile can be claimed, but the company page is the employer's to claim and correct. Pass company-page errors to the employer rather than editing them yourself.

## Other bio pages

Gravatar, about.me, Linktree and similar are often forgotten and badly stale. Update them to the descriptor and public location, or delete them under the dormant-account rule.

Executive and people aggregators (Equilar, Clay, Mesh, Village, CB Insights) are rarely worth the effort. Correct them only when they are high-visibility and offer a claim or correction route.
