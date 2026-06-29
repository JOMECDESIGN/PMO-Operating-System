# feishu-cli-it-checklist.md — IT Sign-off Before First Real Write

> One-pager for IT. Until every box is ✅, the `feishu-pmo` skill runs **read-only / dry-run** only (see `docs/feishu-cli.md` §4).
> Gate: PMO does not enable real writes to the single source of truth until this is signed.

**Tenant / host:** ______________________  **App name:** ______________________
**Requested by (PMO):** ______________  **Confirmed by (IT):** ______________  **Date:** __________

---

## 1. App + Open API scopes

A Feishu **custom app** (企业自建应用) with these permissions. 企业版 does **not** grant them by default.

| # | Domain | Scope needed | Why | Status |
|---|--------|--------------|-----|--------|
| 1 | **Base / Bitable** | Read **and** write records on the tracker tables | Pull + update interface/risk/milestone trackers + Gantt | ☐ |
| 2 | **Approval** | Create + query approval instances | Raise/track F1/F2 change requests; verify two-site sign-off | ☐ |
| 3 | **Wiki / Drive** | Read + write docs | Publish weekly RAG report | ☐ |
| 4 | **Messenger (im)** | Send messages (bot) | Overdue chasing + escalation ladder | ☐ |
| 5 | **Tasks** | Create + read tasks | Convert meeting action items | ☐ |
| 6 | **Contacts** | Read directory | Resolve owner/team for a tracker row | ☐ |

> Minimum to start the weekly flywheel = rows **1 + 2**. Rows 3–6 can follow.

## 2. Identity

| Item | Decision | Status |
|------|----------|--------|
| **Bot identity** for chasing / automation / report broadcast | app/bot: ____________ | ☐ |
| **PMO user identity** for authored reports (CLI identity switch) | user: ____________ | ☐ |

## 3. Rate / quota (the trap)

CLI calls hit **Open API rate limits** — **separate from** the Automation run quota (CLAUDE.md §7). Confirm so we design for **daily-digest batch calls**, not per-record loops.

| Question | IT answer |
|----------|-----------|
| Open API per-app rate limit (QPS / daily)? | ____________ |
| Any tenant-level cap we'd share with other apps? | ____________ |
| OK to run a daily batch read of ~all tracker rows? | ☐ yes / ☐ no |

## 4. Access scope (least privilege)

| Item | Decision | Status |
|------|----------|--------|
| App restricted to **the demo project's** Base/Wiki only (not whole tenant)? | ☐ |
| Bitable token/app-token of the tracker base shared with PMO? | base: ____________ | ☐ |
| Credential delivery: OS keychain / env-var (`${VAR}`), **never** in a config file in git | ☐ |

## 5. Sign-off

- [ ] Rows 1–6 scopes granted (or 1+2 minimum, rest scheduled: __________)
- [ ] Identities provisioned
- [ ] Rate/quota answered; daily-digest design confirmed safe
- [ ] Least-privilege scope confirmed
- [ ] Credentials delivered securely

**On full sign-off:** flip the `feishu-pmo` skill out of read-only mode and run P1 (weekly state pull) as the first live test against the trackers.
