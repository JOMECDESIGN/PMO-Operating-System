# meegle-cli — Borrowable Methods & a Supplement to the PMO Philosophy

> **Status:** ready to publish as a child doc under the Feishu Wiki node
> `https://wu35s592xy.feishu.cn/wiki/KX5TwFxEPipfE0kXymQcxEmPnNd`.
> **Premise:** We do **not** use Meegle / 飞书项目 (no Feishu Project license — CLAUDE.md §7).
> We are **not** borrowing the product. We are borrowing the **methods** its CLI embodies — and using them to *supplement this repo's operating philosophy*, not replace it.
> Execution layer remains `larksuite/cli` (see `docs/feishu-cli.md`). `meegle-cli` is the **command-style blueprint**.

---

## 0. Why a doc about a tool we don't use

The constitution (CLAUDE.md) answers **what** PMO work is: get the right info to the right people at the right time so they make the right decision (the Prime Directive), defended across three seams (S1/S2/S3) and two freeze lines (F1/F2).

What it under-specifies is **how that becomes machine-executable and safe** once Claude Code starts *operating* the single source of truth instead of just describing it. `meegle-cli` — an agent-native CLI built by the larksuite team — has already solved that "how" cleanly. Its design choices are, in effect, a set of **operating methods**. This doc extracts them and grafts them onto our philosophy.

Read this as: *"the constitution says transparency, coordination, risk-forward; here is the discipline that makes those real when an agent holds the keyboard."*

---

## 1. The eleven borrowable methods

Each method below is described completely, with the concrete `meegle-cli` form on the left and **why it serves a PMO pillar** on the right. Where it maps to a constitution rule, the rule is named.

### M1 — Agent-native structured output
- **The method:** every command can emit machine-readable output — `--format json` (default), `ndjson` (one record per line, for streaming/piping), `table` (humans), `raw`. The tool is built so a machine is a first-class operator, not an afterthought.
- **Why it matters here:** this is the literal mechanism behind **"data, not vibes"** (CLAUDE.md §5.1). When Claude pulls the three trackers as JSON, it can *compute* critical-path buffer, count planned-vs-delivered, and flag overdue rows — instead of paraphrasing a screenshot. Transparency stops being a human-read dashboard and becomes a queryable surface.

### M2 — Dry-run before any side effect
- **The method:** `--dry-run` previews a mutating operation (write record, raise approval, send message) and prints exactly what *would* change, without changing it. Preview first, commit second.
- **Why it matters here:** this is **freeze-line discipline (F1/F2) extended to the tooling layer**. The constitution forbids silent edits to a frozen baseline (§3, §5.2). Dry-run makes "see the impact before you commit" the *default behaviour of the keyboard*, not a habit you hope the operator remembers. Adopt as: **every side-effectful command runs dry-run first; the output is reviewed; only then for-real.**

### M3 — Two-layer parameters (ergonomic flag + `--params @file.json`)
- **The method:** simple calls use readable flags (`--priority P1`); complex payloads (nested `fields[]`, multi-field change sets) come from a JSON file via `--params @change.json`, avoiding shell-escaping hell.
- **Why it matters here:** a change request to a frozen baseline is a **structured, archivable artifact**, not a one-liner. Keeping the payload in a file means the *exact* change set is reviewable, diff-able, and attachable to the Approval record — supporting **single source of truth** (§5.1) and the change-control paper trail (`docs/change-control.md`).

### M4 — Field projection with dot-path + array broadcast (`--select`)
- **The method:** `--select "list.work_item_info.work_item_name"` pulls just the named field out of every record in an array. You fetch precisely the fields you need, nothing else.
- **Why it matters here:** PMO output exists to **enable a decision, not to narrate** (§9). Projection is how a weekly pull stays decision-shaped: grab `status`, `owner`, `buffer_days`, `due` — not the whole row. Less noise, faster signal, lower token/API cost (relevant to the §7 quota caution).

### M5 — Envelope + request id (`--envelope`, `meta.logid`)
- **The method:** wrap any response as `{ data, meta, error }`, where `meta.logid` is the server-side request id for tracing.
- **Why it matters here:** **traceability of every tracker change** (§9 "state the impact in concrete terms"). When a contract row flips versions, the logid ties the edit to a specific call — so "who changed what, when, via which request" is answerable. This is auditability for the freeze lines.

### M6 — Auth-guard before business commands
- **The method:** the bundled skill **refuses to run any business command until `auth status` succeeds.** No silent half-authenticated operations.
- **Why it matters here:** direct expression of **"never invent status"** (§5.2). If the tool can't confirm it's connected with the right identity and scopes, it must not pretend to act. We adopt this as the first line of our `feishu-pmo` skill, and extend it: until the IT checklist (`docs/feishu-cli-it-checklist.md`) is signed, the guard also forces read-only/dry-run mode.

### M7 — Headless auth + secret hygiene
- **The method:** device-code flow for browserless environments (prints a URL/QR, waits for authorization); OS-keychain credential storage; `${VAR}` env-var templating so **secrets never land in a config file**.
- **Why it matters here:** lets the agent operate from CI or a remote sandbox *and* keeps credentials out of the repo — a security baseline for any tool that can write to the single source of truth. No token ever gets committed.

### M8 — Multi-profile isolation (staging / prod)
- **The method:** named profiles, each with its own host + credentials; `--profile` switches without disturbing the default.
- **Why it matters here:** prevents the worst single-source-of-truth failure — **a write landing in the wrong tenant/base.** One profile = the demo project's tenant. Isolation by construction, not by carefulness.

### M9 — Domain-grouped, noun-verb command taxonomy
- **The method:** ~16 business domains, each a noun namespace, each verb a clear operation: `workitem create`, `workflow transition`, `comment add`. Predictable, discoverable, self-documenting.
- **Why it matters here:** **coordination runs on shared vocabulary.** The constitution already does this with M1–M7, S1–S3, F1/F2, A/B/C tiers — a fixed lexicon everyone maps to. A command taxonomy is the same idea at the tooling layer: when commands are predictable, both humans and the agent reason about them without a manual. We mirror the convention when we wrap `lark-cli`.

### M10 — Scenario / sugar commands (`+` prefix)
- **The method:** the `+` prefix marks composite, client-side commands that bundle several API calls into one ergonomic operation (e.g. `workitem +batch-get`).
- **Why it matters here:** the **weekly flywheel** (§5.3) is exactly such composites — "pull all three trackers + compute buffer" is many calls behind one intent. Modeling our skill playbooks (P1–P4 in `feishu-pmo`) as scenario commands means **one cadence step = one invocation**, which is what keeps the 30-minute weekly meeting from becoming status theater.

### M11 — A tool that ships its own operating manual
- **The method:** `meegle-cli` bundles an AI Agent Skill containing a full command reference, the query-language (MQL) syntax, and **step-by-step playbooks** ("create a work item," "transition a node"). The tool teaches the agent how to use it.
- **Why it matters here:** this is **literally the architecture of this repository** — CLAUDE.md is the constitution, the `docs/` are the rules, and `.claude/skills/feishu-pmo/` is the playbook. meegle-cli validates the pattern: *governance + an executable skill that refuses to act outside the governance.* We are not inventing a structure; we are conforming to a proven one.

---

## 2. Supplement to the basic philosophy

The constitution's three value pillars — **Transparency, Coordination, Risk-forward** — describe the *ends*. The eleven methods above contribute a fourth, instrumental value that describes the *means* once an agent operates the trackers:

> ### Fourth value — **Operability** (proposed)
> *Status is not only visible; it is machine-operable — queryable, computable, previewable, and traceable — and no action runs outside verified authority.*

Operability doesn't compete with the three pillars; it is **how they survive contact with automation.** Concretely it adds three operating principles, each a direct extension of an existing rule:

| New principle | Extends | One-line rule |
|---------------|---------|---------------|
| **P-A · Operable transparency** | "Data, not vibes" (§5.1) | Project status must be pullable as structured data and computed, not paraphrased. (M1, M4, M9) |
| **P-B · Previewable change** | F1/F2 freeze discipline (§3) | Every side effect is dry-run-able and is previewed before it lands. Preview is the default, not the exception. (M2, M3, M5) |
| **P-C · Gated, traceable action** | "Never invent status" (§5.2) | No command acts without verified auth + scope; every action carries a traceable id. (M5, M6, M7, M8) |

These three slot under the existing **§5 Operating Rules** without changing any seam, freeze line, or milestone. They govern *the agent's hands*, where the original rules govern *the PMO's judgment*.

---

## 3. What we explicitly do NOT borrow

To keep the freeze line between "blueprint" and "product" sharp:

- **Not the product.** No Meegle / 飞书项目 tenant, license, work-items, or workflows. Our data stays in **Feishu Bitable** (§7).
- **Not its domains.** `workitem`, `workflow`, `WBS plan table`, `deliverables` are Meegle concepts; our nouns are Bitable tables, Approval instances, Wiki docs.
- **Not its API surface.** We call `larksuite/cli` against the 企业版 Open Platform. meegle-cli's endpoints are irrelevant to us.

The borrow is **methods and conventions only** — the *grammar* of a good agent-native CLI, applied to our own execution layer.

---

## 4. Where these methods already live in the repo

| Method | Landed in |
|--------|-----------|
| M1, M2, M3, M4, M5 (house command style) | `docs/feishu-cli.md` §3 |
| M6, M2 (auth-guard + dry-run default) | `.claude/skills/feishu-pmo/SKILL.md` |
| M7, M8 (secret hygiene, profiles) | `docs/feishu-cli.md` §4 + `docs/feishu-cli-it-checklist.md` |
| M10, M11 (scenario playbooks, self-documenting skill) | `.claude/skills/feishu-pmo/` (P1–P4) |
| P-A / P-B / P-C (the philosophy supplement) | **this doc** → fold into CLAUDE.md §5 when ratified |

---

*Proposed supplement to the PMO constitution. Ratify by adding P-A/P-B/P-C under CLAUDE.md §5, then archive this doc on the Wiki shelf beside `framework.md`.*
