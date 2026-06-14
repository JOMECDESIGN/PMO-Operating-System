# interface-sop.md — Seam S1: Client-Supplied Interface Clearance

> Governs the 14 client-supplied (甲供) part interface specs. The earliest and most urgent seam.

## The rule
Client must deliver interface specs **within 15 working days** of contract signing. Until specs land, software and hardware adaptation **cannot start** — this directly threatens the M2/M3 data path. Highest priority at project start.

## Top-3 highest priority (clear these first)
1. **P-HUD** — resolution / interface type / SDK / transmittance. Blocks software UI + windshield procurement.
2. **Magic screen** — control logic doc / dimensions / touch protocol. Blocks dashboard styling.
3. **Health-monitoring sensor set** — data interface (CAN FD/USB/ETH) / data format / whether algorithm is bundled. Blocks health-data visualization.

## Flow
1. Log every interface item in the Bitable tracker (`templates/interface-tracker.csv` seed).
2. Status per item: not-provided / provided-pending-confirm / confirmed-frozen / overdue.
3. When spec lands → engineer reviews → freeze via Feishu **Approval** (written confirmation, spec attached).
4. Automation chases overdue items **as a daily digest**, not per-record.

## Status meanings
- **not-provided** → still waiting on client.
- **provided-pending-confirm** → arrived, under technical review.
- **confirmed-frozen** → locked; downstream may start. Requires: spec attachment ✓ + approval no. ✓ + confirm date ✓.

## Escalation
L1 chase owner → L2 formally notify client + manager → L3 written delay-impact analysis + schedule-extension request → L4 milestone-level joint meeting.

## Maps to risk
This seam is **R02** in the risk register. Also feeds the change-control flow once an interface is frozen.
