---
name: feishu-pmo
description: Operate the PMO single source of truth (Feishu Bitable / Approval / Wiki / Messenger) from Claude Code via larksuite/cli. Use for the weekly flywheel — reading the three trackers, computing critical-path buffer, raising F1/F2 change-control approvals, and publishing the RAG weekly report. Command style follows the meegle-cli blueprint. Read docs/feishu-cli.md first.
---

# feishu-pmo — Feishu execution skill

Wraps [`larksuite/cli`](https://github.com/larksuite/cli) so Claude Code can **operate** the PMO single source of truth, not just describe it. Governance lives in `docs/feishu-cli.md`; this is the executable playbook. Command conventions are borrowed from the `meegle-cli` blueprint. **We do not use Meegle / 飞书项目.**

## Auth guard — run before ANY business command

Refuse to run Base/Approval/Wiki/Messenger commands until auth is confirmed:

```bash
lark-cli auth status        # must succeed; if not → lark-cli auth login (or --device-code on headless/remote)
```

If `docs/feishu-cli.md` §4 prerequisites (app scopes, quota, identity, host) are **not yet IT-confirmed**, operate in **read-only / `--dry-run` mode only**. Never make a real write under unconfirmed scopes.

## House command style (non-negotiable)

- **Output:** default `--format json`; `ndjson` to pipe; `table` for humans.
- **Projection:** pull only needed fields (buffer / owner / status), don't dump whole records.
- **Dry-run first:** every side-effectful call (record write, approval, message) runs `--dry-run`, output reviewed, *then* for-real.
- **Two-layer params:** simple `--flag`; complex payloads via `--params @file.json` (no shell-escaped JSON).
- **Confirm syntax:** exact flags vary by `lark-cli` version — check `lark-cli <domain> --help`; never invent flags.

## Command reference (domains → PMO)

| Need | Domain | Shape (confirm via `--help`) |
|------|--------|------------------------------|
| Read three trackers + Gantt | `base` | list/read records from the tracker tables |
| Write a tracker status | `base` | update record — **dry-run first**, never on a frozen-baseline row |
| Raise / query a change request | `approval` | create instance / query tasks |
| Publish weekly report | `wiki` / `drive` | create or update the report doc |
| Chase overdue / escalate | `messenger` | send message (bot identity, **daily digest** not per-row — quota) |
| Pull meeting action items | `meeting` / minutes | read minutes → create `task` |

## Playbooks

### P1 — Weekly state pull (before the meeting)
1. Auth guard.
2. `base` read the interface / risk / milestone trackers + Gantt → JSON.
3. Compute: critical-path buffer (days), overdue rows, milestone health (RAG).
4. Return a structured summary — data, not vibes. **Overall health = worst component.**

### P2 — Change control (F1 styling/CAS · F2 contract)
1. **Stop.** Route through `docs/change-control.md` first — the CLI does not bypass change control.
2. `approval` create the change request (**`--dry-run` → review → confirm**).
3. **F2 only:** assert **both Hangzhou AND Kunshan sign-offs present** before marking the contract changed. One-site sign-off → refuse (CLAUDE.md §5.2).
4. On approval, `base` update the affected tracker rows + interface-contract version; broadcast "contract changed vX" via `messenger`.

### P3 — Weekly RAG report (after the meeting)
1. Assemble the 6-section report per `docs/weekly-report.md` (overall = worst component; every red/amber carries a fix).
2. `wiki` publish; `messenger` CC the client.

### P4 — Overdue chase (daily)
1. `base` read rows past due.
2. `messenger` **single daily digest** (not per-record — Automation/API quota, §7), escalate per the ladder.

## Guardrails

- No write to a frozen-baseline row (F1/F2) without change control.
- F2 requires verified parallel two-site sign-off.
- Edit Bitable **in place** — never create a second copy that drifts.
- Read-only / dry-run until `docs/feishu-cli.md` §4 is confirmed.
