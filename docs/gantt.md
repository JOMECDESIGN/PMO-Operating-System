# gantt.md — Seam S3: 30-Week Schedule Baseline + Critical Path

> The progress baseline. Built on the real 30-week, 7-team plan with PMO overlays.

## What this adds over a raw plan
Three things the raw plan didn't make explicit:
1. **Critical-path highlight** — the chain that sets M7.
2. **Two-site gates** — interface-contract freeze (~W2–3) and real-hardware integration (W22–26).
3. **Cross-site dependency** — e.g. Kunshan "client-screen adaptation (W13–20)" is a prerequisite for Hangzhou "screen-UI integration."

## Critical path
styling-confirm → CAS modeling → frame design (W9) → frame build + QC buffer (W12–14) → body (W15–18) → trim (W17–19) → final assembly (W19–22) → integration (W22–26) → pre-acceptance (W26) → final acceptance (W30).
**Any slip on this chain slips M7. Watch buffer consumption weekly.**

> Frame *build* finishes ~W12; the W12–14 span is QC/buffer absorbed before the M4 gate (W14) in `docs/weekly-report.md` and `templates/milestone-tracker.csv`. If that buffer is ever consumed, M4 is at risk — flag it in the weekly report, don't silently let the gate date drift.

## Teams (swimlanes)
Styling · Hardware · Software (Hangzhou) · Embedded (Kunshan) · Demo-model · Test · Animation/Interaction.

## Landing in Feishu
Import the plan into Bitable, switch to **Gantt view** — time bars auto-generate from start/end weeks, colored by priority/status. Beats hand-coloring an Excel; change a date and the bar moves. `templates/gantt-schedule.csv` is the import seed (task / team / start-end week / dependency / critical-path flag / milestone gate) — maintain the Bitable copy once imported, per §6 of `CLAUDE.md`.

## 30-week compression — three most-likely delays (from the plan)
1. Client-supplied sample handover delay → hits hardware integration (see S1 / R02).
2. A-surface freeze late → hits trim machining (F1 / R08).
3. Software UI depends on interaction-design Figma → cross-site + cross-discipline seam.
