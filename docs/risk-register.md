# risk-register.md — 17-Risk Register + Weekly Review

> Turns the static risk list (8 high + 9 mid) into a live, alerting tracker. Risk ≠ issue: see it BEFORE it becomes a problem.

## One-line principle
A risk list isn't a write-once archive — it's a live table reviewed every week.

## High risks (8) — lock mitigations in design phase
- **R01** Front-seat 180° rotation mechanism safety — dual mechanical+electrical limits · ≥100-cycle reliability test · on-site engineer.
- **R02** Client interface-spec delay — 15-working-day obligation · interface tracker · parallel dev (see interface-sop).
- **R03** Multi-screen/device real-time sync stability — DC headroom ≥8 (rec 16) cores · async queue · per-scene load test · degrade strategy.
- **R04** Multi-team parallel — cascade dependency — dependency graph · critical-path buffer · dedicated coordination.
- **R05** Health-data authenticity vs effect — set A/B boundary in design; if unstable, written approval for simulated data.
- **R06** Show-grade exterior quality after transport — custom protective packaging · adjustable mounts · spare exterior parts · on-site gap manual.
- **R07** Whole-vehicle power — show power-loss recovery — UPS redundancy · auto-recovery (state persistence) · recover A-class first · drill.
- **R08** Styling-confirm delay → all downstream — pre-align before review · ≤2 review rounds · M1 delay → impact analysis + extension request.

## Mid risks (9) — track regularly, set early warning
R09 Console mechanism noise · R10 Voice recognition in show noise · R11 Heating-film temp-control safety · R12 IMSE film effect · R13 Client-supplied late arrival · R14 Zero-gravity seat × rotation compatibility · R15 8-hour on-site install · R16 CMF color batch consistency · R17 Starry-headliner fiber routing concealment.

## Status lifecycle
not-started → monitoring → **triggered** (= now an issue, handle + escalate) → mitigated → closed. Every risk has a clear status and owner — no orphans.

## Weekly review (10 min)
1. Check **triggered** column — any risk became an issue? Handle + escalate.
2. Check **monitoring** — mitigations on track? Owner reports.
3. Risks near their trigger milestone → move not-started → monitoring proactively.
4. Any new risks? Log now. Update each reviewed risk's last-review date.

## Stage focus
M1: R08. Pre-freeze (W8–11): R02, R08. Integration (W22–26): R03, R07, R10. Pre-show: R06, R15, R01.

## Escalation & dashboard
L1 mid in window → owner mitigates. L2 high in window / mid triggered → owner+PMO. L3 high triggered → PM + plan. L4 affects critical path/milestone/safety → PM + client; safety items (R01) may pause the demo. Feeds the RAG report's risk panel: a triggered high risk = red headline.
