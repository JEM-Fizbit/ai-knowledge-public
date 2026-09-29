# UK public registries

Phase 2. Statutory records are public by law, so the aim is not to hide them. It is to make sure they carry a **service address**, not a home address, and consistent facts. Mirrors and people-search sites (OpenCorporates, Endole, CompanyCheck, 192.com) copy these records and lag by months, so fix the source first.

**Last verified: September 2026.** Companies House rules changed under the Economic Crime and Corporate Transparency Act 2023, and more changes are phasing in. Check GOV.UK for the current form names and fees before advising.

## Companies House

**Find every officer record.** Search the person's name on `find-and-update.company-information.service.gov.uk`. One person is often split across several **unlinked officer IDs**, one per spelling or date of birth format that different filers used, each listing different appointments. Record each ID in the register with its appointments, addresses and nationality as shown.

**Where a home address shows up:**
- A company's **registered office**. This is common for a personal consultancy run from home.
- A director's **correspondence (service) address**.
- A person with significant control (PSC) **service address**.

**Remedies**, filed by whoever controls that company's filings:

| Problem | Form | Who files |
|---|---|---|
| Registered office is a home address | **AD01**, to change it to a registered-office service or business address | The company |
| Director's service address or nationality is wrong | **CH01** | The company. For a board seat at someone else's company, ask their **company secretary** to file it. |
| PSC details | **PSC04** | The company |
| Home address in **past** filings | **SR01**, an application to make a residential address unavailable on the public register. It carries a fee. | The individual |

A registered-office service costs a modest annual fee and gives an address to use for the registered office and the director and PSC service addresses. File AD01 first, then CH01 and PSC04 pointing at the new address, then SR01 for the history.

**Split officer records.** There is no self-service merge, and identity verification did not merge them in 2026. Write to Companies House enquiries asking them to link the records, listing each officer ID and its appointments (template in `email-templates.md`). Inconsistent details such as nationality recorded three ways need a CH01 from each company concerned. Agree the correct form with the person first; "British, American" style dual nationality is recorded as they choose.

**Dates.** A registry appointment date is the date a role was *filed*, not necessarily the date it began. Never copy registry dates into profiles without asking the person.

## Charity Commission

Trustee names and appointment dates appear on the charity's register entry. Changes go through the charity's own filings. Ask its governance or company secretary contact if something is wrong.

## The open electoral register

Local councils can sell the **open** register to anyone. The full register is only used for elections and a few lawful purposes. Opting out of the open register stops new copies reaching people-search sites.

- Route: the person's council electoral services team, by email or its online form. `gov.uk/electoral-register/opt-out-of-the-open-register` finds the council.
- They can opt out at any time. It takes effect at the next monthly update, and copies already sold aren't recalled.
- Draft the email; the person sends it from their own mailbox with their full name and address.

## Outside the UK

Most countries have a company registry with a similar split between registered office and service address. In the US, state business filings show a **registered agent**, and using a commercial registered agent keeps a home address off them. Record what worked in a new `registries-XX.md` file rather than stretching this one.
