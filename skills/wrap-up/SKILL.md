---
name: wrap-up
description: "Close out the current work session with a durable savepoint, verified Git commit/push and authorised deployment where applicable, plus a next-session model/effort recommendation and short kickoff prompt. Use when the user asks to wrap up, finish for now, save our progress, checkpoint the session, prepare a handoff, or move this work to a fresh session. Recognise equivalent intent without magic words. Do not trigger on status questions, hypothetical discussion about handoffs, an isolated Git operation, or wrapping up a paragraph/document. Respect narrower requests such as savepoint only or do not push/deploy."
version: 1.1.0
metadata:
  version: "1.1.0"
---

# Wrap up

> **Skill version:** v1.1.0

Leave the work resumable and its delivery state explicit. This is a session closeout, not an instruction to finish every item in the product backlog. A request to stop or pause takes precedence over continuing implementation. Use existing session authority and project rules; the skill grants no additional permissions.

## Establish the actual state

Read the current project's governing instructions and applicable savepoint, Git, verification and deployment guidance. Prefer its established savepoint and tracker rather than creating a competing home. A fuller savepoint method is [`SESSION_HANDOFF_SAVE_POINTS.md`](https://github.com/JEM-Fizbit/ai-knowledge-public/blob/main/protocols/SESSION_HANDOFF_SAVE_POINTS.md); use a project-local equivalent when available. Do not copy the protocol into the savepoint.

Inspect live branch, HEAD, remotes, status (including staged and untracked files), relevant diff and recent commits. Identify this session's work separately from existing or concurrent changes. Reconcile any ongoing commands, agents or deployments affecting the checkpoint; wait for a bounded result or record what is still running. Do not silently abandon a deployment you initiated.

## Save a useful continuation record

Update the existing savepoint in place; if none exists, create one in the project's normal documentation home using its naming rules. Capture only what the next session needs:

- What was completed, where it lives, and the verified baseline; distinguish source state, deployment state and historical evidence.
- Settled decisions, rejected approaches worth remembering, important invariants and scope/approval constraints, including spending already consumed.
- Remaining work, concrete next actions, blockers and the smallest unresolved decision. Link to the owning tracker; do not create a second backlog.
- Tests and checks actually run, their results and limits; relevant commands and access prerequisites without credentials.
- Where private/ignored artifacts remain, whether they are available in a fresh checkout, and any deliberate transfer needed to resume elsewhere.

Preserve previous outcomes and original evaluation evidence. Add an inbound pointer from the initiative/anchor document where useful. A savepoint should not depend on this conversation or promise a commit SHA that does not yet exist: name the verified baseline and identify the checkpoint as the commit containing the savepoint. Do not edit personal memory or the Brain unless separately authorised. Do not create a new task, cross-agent packet or remote repository merely to wrap up.

## Verify and deliver the in-scope work

Complete proportionate checks for the actual changes. Reuse checks already passed against unchanged content; do not run a full build for prose-only closeout or spend on AI evals without authority. If a check fails, fix an in-scope defect when practical; otherwise preserve the partial state and report the failed check. Never label an unfinished milestone complete because the session is ending.

Inspect what will be committed and stage only understood in-scope changes. Include overlooked source, tests and documentation needed to resume. Leave credentials, private records and intentionally ignored runtime artifacts out of Git; explicitly disclose any meaningful work that stays local. Never delete, reset, stash, force-add ignored files, or commit unrelated work just to obtain a clean status. Account for commit hooks that may introduce extra changes.

Commit and push under the user's existing authority and the repository's normal completion workflow. Follow an authorised base-branch merge workflow; do not invent a PR, push only a feature branch and call it deployed, or merge across a real review gate. An explicit local-only, audit-only, no-push or no-deploy limit persists. Respect repositories intentionally lacking a remote; do not invent one. For non-Git workspaces, save through their existing versioned/document home and report Git as not applicable.

After commits/hooks, re-read status. After push, verify the intended remote branch contains the checkpoint and report whether it matches local HEAD or has advanced. If concurrent work remains, identify it without altering it and report that the overall tree is not clean. Use normal access mechanisms and bounded recovery for failures; do not retry indefinitely or force-push to bypass divergence.

## Follow authorised deployment through to verification

Determine the actual delivery mechanism from project instructions/configuration, not the presence of a generic hosting file or an old URL. If the normal authorised push auto-deploys, inspect that deployment. If deployment is separate and already authorised, perform the normal release step. Do not duplicate an automatic deployment or redeploy deliberately skipped documentation changes just to make a box green. An explicit no-deploy instruction also rules out pushing to a known auto-deploy branch unless deployment is disabled or the user resolves the conflict.

Verify the intended application/environment, the deployed source revision or equivalent build identifier, completion status, and proportionate live behaviour for the changed surface. A successful push, queued build or HTTP 200 alone does not establish a successful release. Distinguish this checkpoint's documentation commit from the application revision actually running. Preserve working releases and avoid unrelated applications. Deployment authority does not authorise email, social publishing or other communications.

If required approval/access is genuinely missing, finish independent closeout work first, state the exact action and reason, and ask only for that missing decision. Report deployment as pending, failed, unchanged or unverified as appropriate. Record material deployment outcomes in the savepoint; if that requires a final documentation commit, keep the application release SHA distinct from it and reconcile any resulting build. Do not enter an endless deploy/document/commit cycle.

## Recommend the next session's setup

Recommend the model and reasoning effort for the agreed next work unit, not for the closeout itself. Use the applicable model-selection skill when available (`choose-model-and-effort` in Codex; `model-effort-selection` in Claude Code), current environment-exposed choices and relevant official guidance. Respect the intended destination and any explicit model choice. Do not infer that a model or effort exists in another tool from its availability here, or hard-code a model roster into this skill. If destination availability cannot be verified, label that limit and give a conditional recommendation rather than inventing an exact setting.

Put a concise **Next session: model / effort** recommendation with one short reason in the final response, **before** the kickoff prompt, so the user can set the controls before launching the new session. Recommend the least costly setup that preserves the needed quality; do not turn this into a model survey, paid benchmark or extra approval cycle. The recommendation is advisory, not a claim that settings were changed.

Ordinarily keep model settings out of the pasteable kickoff prompt because the user sets them manually first. Exception: when the continuation needs a materially useful, more complex execution arrangement, also capture that arrangement in the prompt and savepoint—for example, a frontier-model coordinator assigning bounded implementation tasks to a faster model, or a justified phase-specific model/effort change. State the roles, model/effort choices and review boundaries needed to execute it; do not add agents or role switches by default. Such an arrangement remains a recommendation unless already authorised, and must not be phrased as user-approved delegation when it is not. Preserve the separate pre-launch recommendation even in this exceptional case.

## Final response

Keep it short:

1. Link the savepoint and state commit/remote/cleanliness status, with any intentionally local or unresolved work.
2. State deployment outcome only when relevant, naming any failed or unverified step plainly.
3. Give the next-session model/effort recommendation and a short reason before the kickoff prompt.
4. Give a short pasteable kickoff prompt naming the project and savepoint, the agreed next task, and material restrictions. It should tell the fresh session to read the governing instructions and verify current state before proceeding.

Do not claim fresh-session skill discovery, successful deployment, remote backup of ignored files or full completion without evidence. End after delivering the checkpoint and kickoff; no new workstream is implied.
