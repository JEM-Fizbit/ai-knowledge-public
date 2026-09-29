# Platform notes

Settings and traps on specific platforms. **Last verified: September 2026.** Every path here is a starting point: platforms move settings, so confirm them live, and update this file when something has moved.

## Keep, park or delete

Apply the dormant-account rule from `SKILL.md`. When deleting:

- **Deactivate vs delete.** Deactivation usually hides the profile but keeps the data, and a single login reactivates it. It leaves the person an account they still have to secure. Prefer delete unless they might return soon.
- **Grace periods.** Many platforms delete after a delay, often 14 or 30 days, and logging in cancels it. During the delay the public page may still show the name and old details under a "deactivated" banner. Record a re-check date.
- **The person deletes.** Give them the exact path, then verify the public page afterwards.

## Code hosts (GitHub)

Public commits expose the author email, and forks of other people's repositories show on the profile.

- In GitHub settings, under **Emails**, turn on *Keep my email addresses private* and *Block command line pushes that expose my email*. Do the same for every account the person uses.
- Set `git config user.email` to the GitHub noreply address, `ID+USERNAME@users.noreply.github.com`, for future commits.
- Cleaning history means rewriting it: `git filter-repo --mailmap` for author emails, and `--replace-text` for emails inside files. **That needs a force-push, which the person runs themselves.** It is destructive: collaborators must re-clone, existing forks keep the old history, and old commit SHAs stay reachable until GitHub garbage-collects them. Decide repo by repo, and delete unwanted public forks rather than rewriting them.

## LinkedIn

- **Settings → Visibility → Edit your contact info** controls who sees email and phone. Visibility to first-degree connections is a real trade-off: contact-scraping browser extensions used by connections are a known broker source. Let the person choose, and record the choice.
- Also under Visibility: who can find the person by email or phone.
- **Settings → Data privacy → Data for Generative AI Improvement** can be switched off.
- The public location is set on the profile's intro card.

## Facebook, Instagram, Threads, TikTok and Pinterest

- **Facebook:** Settings & privacy → Privacy → *allow search engines outside Facebook to link to your profile*: off. Also set who can look the person up by email and by phone.
- **Instagram and TikTok:** switch to a private account if the person doesn't use them publicly.
- **Threads:** the bio is edited in the Threads app or on the web, and follows the Instagram account's privacy.
- **Pinterest:** boards often show home, garden and family events. Make the profile private or make those boards secret.

## X (Twitter)

- **Login email dependency:** if the account logs in with an email on a domain the person might let lapse, whoever re-registers that domain can take the account over. Either treat the domain as critical (auto-renew, recorded in the person's asset list) or move the login email.
- An email address already held by another X account (often a suspended or deactivated one) can't be reused through normal flows, and password-reset pages ask for a username. The route that exists is X's privacy form: `help.x.com/forms/privacy` → *I want to ask a question regarding privacy on X* → *Modifying the information X has about me*. Use it as a GDPR request to identify or release the address. A reply is due within one month.
- Bio and location are under Edit profile.

## YouTube

- **One Google account can own several channels**: a personal one plus brand channels. In YouTube Studio, check the channel name and handle in the top-left corner before editing. Switch with the avatar menu → *Switch account*.
- **Handle change:** Studio → Customisation → Profile. The previous handle is held for 14 days, then released, and links using it will break. Update the links elsewhere, including the person's own records. The channel name can change only twice in 14 days.
- Third-party footage such as TV clips can attract copyright claims. It's the person's call to keep it public or make it unlisted, which keeps links working but hides it from the channel and search.

## Medium, Calendly, Meetup and Quora

- **Medium:** Settings → *Profile information* holds the name and a 160-character bio, where a link in plain text becomes clickable. Reading lists can be private.
- **Calendly (park):** turn off every event type from each type's ⋮ menu (the On/Off switch). The public page then says "No openings at the moment". Ignore any new-terms banner. Don't accept it on the person's behalf.
- **Meetup:** profile visibility lives under **Edit profile**, not the Privacy page. It has switches for groups, interests, relationship status and work industry. The Privacy page only controls who can contact the person. The profile city drives event suggestions, so changing it has a cost.
- **Quora:** delete rather than deactivate. Deletion runs a 14-day grace period.

## Others seen

- **SlideShare (now Scribd):** older accounts may sign in through LinkedIn. Delete it under Account settings.
- **about.me, Gravatar and Linktree:** forgotten bio pages. Update or delete them.
- **Wellfound (formerly AngelList):** profiles live at `/u/handle`. Check it logged out. Old accounts often have no public page.
- **TripAdvisor and review sites:** usually pseudonymous. Check the display name and home city shown.
