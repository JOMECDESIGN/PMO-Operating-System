# change-control.md — Freeze Lines F1 (CAS Data) + F2 (Interface Contract)

> Guards TWO freeze lines with one flow. After freeze, nothing changes without: request → impact → approval → update.

## One-line rule
**Before freeze, iterate fast. After freeze, no assessment + written approval = no change.** No verbal, no side-channel.

## The two freeze lines
| Line | Freezes | When | Risk shape |
|------|---------|------|-----------|
| **F1 — CAS / A-surface** | styling, CAS, A-surface (CATIA, 0.05mm) | ~M3/W11 | **Vertical** cascade: styling→frame→mechanism→software |
| **F2 — Interface contract** | WebSocket / scene API / IO table / CAN FD | ~W2–3 | **Horizontal** cross-site: one side changes → integration blows up |

## Five-step flow (both lines)
1. **Submit** — Feishu Approval "change request": content, reason, which freeze line, urgency. No verbal changes.
2. **Log & classify** — PMO logs to change tracker; classify **minor / major / cross-site** (decides the approval path).
3. **Assess + approve** — by type (see paths below).
4. **Execute & sync** — owner executes; PMO ensures all affected parties (esp. both sites) are notified and updated.
5. **Update baseline** — PMO updates the data version / interface-contract list; archives the approval. Closed.

## Path 3.1 — CAS change (vertical)
Approval **conditional branch** by "impact scope": auto-route to frame/mechanism/software leads for assessment; add client node if styling/CMF confirmation item. Then PM final approval. Sync to change tracker.

## Path 3.2 — Interface-contract change (horizontal)
Approval **parallel branch**: one request flows to Hangzhou lead AND Kunshan lead simultaneously — either dissents → returned. CC both sites' members. On approval, both sides update code/Mock; PMO updates the contract list and broadcasts "contract vX changed."

## Escalation
L1 assessment overdue → chase. L2 sites disagree → time-boxed alignment meeting. L3 affects M3/M4 → PM + client, schedule-extension. L4 unresolved → contract-level decision makers.

## Quality gate
Every frozen-content change has a full record (request/assessment/approval/execution/baseline-update). **An interface change closes only when "both sites synced" is confirmed** — the last guard against integration blowup. Maps to risks R02/R08.
