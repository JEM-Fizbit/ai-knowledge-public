# Data brokers and people-search sites

Phase 2. These sites sell or display contact data: personal email addresses, mobile numbers, home and past addresses, relatives. Removal is worth doing first because the data feeds spam, phishing and impersonation.

**Last verified: September 2026, UK-based person.** Routes change. Confirm each one live and update this file when it has moved.

## How to run a broker opt-out

1. **Find the listing first.** Search the broker for the person's name and each place they have lived. Most opt-outs need the listing URL, and several listings can belong to one person.
2. **Confirm with the person that the listing is theirs.** Leave relatives' and namesakes' listings alone, even when they share an address.
3. **Fill the form, then stop for approval.** The person does any human check, email verification or captcha.
4. **Record the request:** date, request ID if shown, which email was used, and what the site promised ("within 24 hours", "2 to 3 days").
5. **Re-check after the promised time**, logged out. Then add the broker to the next re-sweep: re-listing is common.

The email used for verification is disclosed to that broker. Prefer an address the broker already holds over a clean one.

## Contact-data brokers (B2B)

These list business and personal contact details scraped from professional profiles. They are relevant to anyone with a professional online presence.

| Broker | Route | What it needs | Known traps |
|---|---|---|---|
| RocketReach | `rocketreach.co/remove-profile` | Email, then a verification link | Often holds personal email and mobile numbers. Removal was verified the same day. |
| Apollo | `apollo.io/privacy-policy/remove` | Email | Shows "Opt-out Request – Successful"; removal within 24 hours |
| Lusha | `lusha.com/privacy-center/request-removal/` (the old `lusha.com/opt-out` returned 404 on 2026-09-29) | Email, then a verification link | Gives a request ID. Save it. |
| ContactOut | `contactout.com/optout` | LinkedIn profile URL and email, then a verification code by email | The person may have to fill it in themselves. Removal within 24 hours. |
| SignalHire | `signalhire.com/opt-out` (also `/do-not-sell`) | The URL of the SignalHire profile page | Finding that page is the hard part: search SignalHire for a current or past employer and open the person from its staff list. No confirmation is shown. Fallback: `support@signalhire.com`. |
| ZoomInfo | `privacyrequest.zoominfo.com` | Form | The form errored for both the assistant and the person (Sept 2026). Fallback that worked: an erasure email to `privacy@zoominfo.com` citing UK GDPR Articles 17 and 21 (template in `email-templates.md`). A reply is due within one month. |

## People-search sites

**UK**

| Site | Route | Notes |
|---|---|---|
| 192.com | `192.com/c01/new-request` | Name plus postcode suppression, one form per address, email confirmation and a human check. Many "director" records are derived from Companies House addresses. Suppress the residential ones, and fix the registry upstream (see `registries-uk.md`) or they return. Confirmed within 24 hours. |
| ukphonebook and similar | Site's own removal form | Usually electoral-roll derived. The open-register opt-out stops new data. |

**US** (also relevant to non-US residents with US history)

| Site | Route | Notes |
|---|---|---|
| Spokeo | `spokeo.com/optout` | One listing URL per request, plus email confirmation and a human check. A second request from the same email while the first was still pending was rejected as "Invalid email address". Wait for the first to complete, or write to `privacy@spokeo.com`. Listings often bundle old addresses, phones and aliases. |
| Radaris | Was `radaris.com/control/privacy` | Offline in September 2026, but cached pages remained. Check it on each sweep. |
| Whitepages, BeenVerified, TruePeopleSearch, FastPeopleSearch, Intelius, MyLife | Each has an opt-out page | Not yet exercised with this skill. Follow the general method and record what worked here. |

Paid removal services (DeleteMe, Incogni, Optery and others) re-file opt-outs on a schedule. They are worth suggesting when US people-search exposure is heavy, because manual removal from dozens of sites doesn't last.

## When a form fails

Send a written request instead. Under UK and EU GDPR, erasure (Article 17) and objection to processing (Article 21) must be answered within one month. US residents in states with privacy laws, such as California under the CCPA, have a deletion right. Templates are in `email-templates.md`. The person sends the request from their own mailbox. Record the due date.
