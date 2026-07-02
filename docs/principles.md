# principles.md — Six Execution Principles (六大执行原则)

> Six management principles the team runs on, adapted to this project's tooling reality: **no Feishu Project license** — everywhere the original principles say "飞书项目", we land on **Bitable + Approval + Automation + Wiki** instead. The principles survive the tool swap unchanged; only the landing changes.
>
> Each principle maps to a seam (S1–S3) or freeze line (F1/F2) — that's the test that it's real PMO work, not ceremony.

## The six at a glance

| # | Principle | One-liner | Protects | Governing docs |
|---|-----------|-----------|----------|----------------|
| P1 | 过程管理 Process & status flow | Short stages (3 days–1 week), each with a goal and a review | S3 critical path | `gantt.md`, `weekly-report.md` |
| P2 | 以事找人 Task→people | Fine-grained tasks with 责任人/协同人/关注人 | S2/S3 seams | `framework.md` (RACI), `two-site.md` |
| P3 | 数据版本 Data versioning | One authoritative version per artifact; version-labeled access | F1 + F2 | `change-control.md` |
| P4 | 量化标准 Standardized, quantified tasks | Done-checkable goals; quality gate before stage exit | S3 + M-gates | `weekly-report.md`, `gantt.md` |
| P5 | 问题管理 Issue (defect) management | Ranked issue list; solve important before important+urgent | All seams | `risk-register.md` |
| P6 | 采购需求 Procurement from task demand | Standardized, owned, approval-flowed procurement | S1 + supplier risks | `interface-sop.md` |

---

## P1 — 过程管理: status flow, short stages, version iteration

**Rule.** Never track a critical-path task as one long bar. Decompose into **3-day (max 1-week) status-flow segments**, each with a set goal, and review at each segment boundary. Progress is expressed as **version iteration** ("frame CAD v0.3 → v0.4, mounting points closed"), not "still in progress."

**Why.** A 2-week task discovered late is a 2-week slip on the critical path (M4/M7 chain). A 3-day segment can slip at most 3 days before it's visible.

**Landing (no Feishu Project).**
- Bitable task tracker: every critical-path task carries `segment goal` + `segment due` fields; the **gantt view** renders the flow.
- Weekly meeting reviews segment goals hit/missed — this feeds the "planned N / delivered M" line of the RAG report (data, not vibes).
- Deliverables carry a version string in Wiki; latest version linked from the Bitable record.

## P2 — 以事找人: fine tasks, explicit owner / collaborators / watchers

**Rule.** Decompose until each task is assignable and done-checkable (WBS), then attach three person fields: **责任人 (owner, exactly one)** · **协同人 (collaborators)** · **关注人 (watchers)**. Progress updates land in the tracker; automation pushes to the people attached. Breaking department walls is the point — 网格化协同 across the two sites, not chains of command.

**Why.** ~70% of delay risk lives in the seams. A task with no explicit owner is a seam failure waiting to happen ("I thought you had it"). Writing detailed task descriptions for stage milestones **is each team lead's co-management duty**, not PMO doing it for them.

**Landing.**
- Bitable person-type fields for the three roles on every tracker (task, interface, risk, change, procurement).
- Automation notifies owner + collaborators on status change, watchers via **daily digest** — never per-record pushes (automation quota, §7 of `CLAUDE.md`).
- PMO audits weekly: any record with an empty owner field gets chased before the meeting.

## P3 — 数据版本: clear versions, single source, no version drift

**Rule.** Every process artifact (CAS data, interface contract, IO table, Gantt baseline) has **exactly one authoritative home and a visible version label**. All data access goes through that home — no copies on personal drives, no "the version I have." Standard formats and standard-angle views (数据格式 / 版本描述 / 标准角度图示) so anyone can verify at a glance which version they hold.

**Why.** This is the two freeze lines in daily-work form. F2 exists precisely because one side building against a stale contract version blows up integration at W22–26; F1 because a stale CAS version cascades styling→frame→mechanism→software.

**Landing.**
- Bitable is the single source of truth for trackers; Wiki for documents; each frozen artifact's record carries `version` + `frozen? (F1/F2)` fields.
- Version bumps to frozen artifacts happen **only** as step 5 of the change-control flow, with a broadcast ("contract vX changed, both sides update code/Mock").
- Before any team consumes data, it cites the version it consumed — recorded in the task tracker.

## P4 — 量化标准: standardized tasks, quantified goals, quality-gated exit

**Rule.** Task descriptions are standardized and **quantified** — a done-checkable target, a short-cycle deadline, a named owner (责任 & 自驱力). This makes performance evaluable from the tracker itself. **A stage task that misses its quality bar does not exit the stage** — the owner closes the gap (加班完成完善 if that's what it takes) before downstream work builds on it.

**Why.** The milestone gates (M1–M7) are quantified for a reason: "A-class 100% · B ≥90% · 8h×3 zero A-faults" can be checked; "basically done" cannot. Letting an under-quality deliverable exit a stage just moves the rework to a later, more expensive point on the critical path.

**Landing.**
- Bitable task fields: `quantified goal`, `due`, `owner`, `quality check result`. The dashboard view aggregates on-time/on-quality rates per team — that's the performance-quantification input.
- Segment reviews (P1) apply the gate: missed quality → task stays open, blocker flagged, buffer impact stated in days.

## P5 — 问题管理: ranked issue list, important before important+urgent

**Rule.** Maintain a live **issue (defect) list**, distinct from the risk register (risk = not yet happened; issue = happened). Rank by importance referencing the hard-point development flow (硬点开发流程) — issues on the critical path or touching A-class functions rank first. Spend effort on **important** issues while they're still non-urgent; an important issue left to become important **and** urgent is a firefight you chose.

**Why.** This is the risk-forward pillar applied downstream: triggered risks become issues (risk lifecycle: monitoring → **triggered**), and untreated important issues become schedule slips at integration (W22–26), where fixes cost the most.

**Landing.**
- Bitable issue tracker (or a `triggered/issue` view on the risk register): `severity (A/B/C impact)`, `critical-path? `, `owner`, `due`, `status`.
- Weekly meeting reviews the top-ranked open issues right after triggered risks; the RAG report's risk panel counts open A-impact issues — any open A-impact issue caps overall health at amber.

## P6 — 采购需求: procurement derived from task demand, standardized and approval-flowed

**Rule.** Procurement requests are **derived from work-task demand** — no task, no purchase. Every request carries the three person roles (P2), plus **required standardized fields**: specific technical requirements, quantity, need-by date (back-computed from the critical path), supplier, and acceptance criteria. Supplier management and receiving/acceptance (接收验收) are part of the record, and the whole thing runs through a **documented approval flow** — never verbal orders.

**Why.** Late or wrong-spec parts hit the same seams as late client interfaces: R13 (client-supplied late arrival) and R16 (CMF batch consistency) are procurement-shaped risks. A purchase without acceptance criteria is an integration surprise scheduled for W22.

**Landing.**
- Bitable procurement tracker — import seed: `templates/procurement-tracker.csv`; link each request to its originating task record.
- Feishu **Approval** flow for submission (conditional branch by amount/category), synced back to Bitable; acceptance result recorded on the same record before it closes.
- PMO watches `need-by vs. lead time` — a procurement whose lead time eats critical-path buffer gets flagged in the weekly report.

---

## How the PMO uses these

- **Planning a stage** → apply P1 (segment it) + P2 (attach people) + P4 (quantify goals) before the stage starts.
- **Anyone hands data to anyone** → P3: cite the version; if it's frozen content, route via `change-control.md`.
- **Something broke** → P5: log it as an issue, rank it, don't let important age into urgent.
- **Someone needs to buy something** → P6: derive from the task, standardize the fields, run the Approval flow.
- **Weekly meeting** → P1/P4 supply the data ("planned N, delivered M, buffer −X days"); P5 supplies the issue review; all six feed the RAG report.
