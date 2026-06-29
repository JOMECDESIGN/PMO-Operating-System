# feishu-cli.md — Feishu Execution Layer (`larksuite/cli`)

> The CLI that lets Claude Code **operate** the single source of truth, not just write rules about it.
> Execution layer = [`larksuite/cli`](https://github.com/larksuite/cli) (official, MIT, agent-native).
> Command-style blueprint = [`larksuite/meegle-cli`](https://github.com/larksuite/meegle-cli) — borrowed conventions only; **we do not use Meegle / 飞书项目** (no Feishu Project license, see CLAUDE.md §7).

---

## 1. Why this tool (and not meegle-cli)

Two sibling CLIs from the larksuite team, mirror images for this project:

| CLI | Targets | Our stack? | Role here |
|-----|---------|-----------|-----------|
| **`larksuite/cli`** | Feishu **企业版** Open Platform — Base, Approval, Wiki, Messenger, Docs, Tasks, Meetings… | ✅ exactly our §7 stack | **Execution layer** — adopt |
| `meegle-cli` | Meegle / 飞书项目 (separate licensed product) | ❌ we don't license it | **Design blueprint only** — its command conventions, not its commands |

`larksuite/cli` covers **18 business domains**; nearly every Feishu component CLAUDE.md §7 names has a command domain. Standard 企业版 OAuth login — **no Feishu Project / Meegle license required.**

---

## 2. Domain → PMO mapping (what we actually use)

Only the domains that serve a seam, a freeze line, or the weekly flywheel. Everything traces back to §2/§3 of the constitution.

| CLI domain | PMO use | Serves |
|------------|---------|--------|
| **Base** (Bitable) | Read/write the three trackers (interface · risk · milestone) + Gantt + dashboard | §5.3 flywheel, S1/S2/S3 |
| **Approval** | Raise & track change requests; verify **F2 parallel two-site sign-off** before contract changes | F1, F2, change-control |
| **Wiki / Drive** | Publish the weekly RAG report; the team's single shelf | §5.3 step 3 |
| **Messenger** | Overdue chasing + escalation ladder (daily digest, not per-record — quota §7) | §5.3 step 4 |
| **Meetings / Minutes** (妙记) | Pull auto-minutes → convert action items to Tasks | §5.3 cadence |
| **Tasks** | Action-item tracking out of the weekly meeting | §5.3 |
| **Docs / Sheets** | Interface-contract docs, SOPs (read-mostly) | S1, S2 |
| **Contacts** | Resolve owner / team for a tracker row | all trackers |

Out of scope for now: Calendar, Mail, OKR, Attendance, Slides — no PMO leverage on this project.

---

## 3. House command style (blueprint borrowed from meegle-cli)

`meegle-cli` has the cleaner agent-native conventions. We adopt them as the **house style** for every command we script or put in a skill — applied to `lark-cli`'s actual commands. Confirm exact syntax against `lark-cli <domain> --help`; do **not** invent flags.

| Convention | Rule | Why it matters to PMO |
|------------|------|-----------------------|
| **Structured output** | Default `--format json`; `ndjson` for piping, `table` for humans | Claude reads state reliably — "data, not vibes" (§5.1) |
| **Field projection** | Prefer narrow `--select`-style dot-paths over dumping whole records | Pull just the buffer/owner/status fields the report needs |
| **Dry-run first** | Any side-effectful op (write record, raise approval, send message) runs **`--dry-run` first**, output reviewed, then for-real | Never a silent edit to a frozen baseline (§3, §5.2) |
| **Two-layer params** | Ergonomic `--flag` for simple calls; `--params @file.json` for complex payloads | F2 contract changes carry structured payloads — keep them in files, not shell-escaped |
| **Envelope + logid** | Capture the request id on writes | Traceability for any tracker change (§9) |
| **Headless auth** | Device-code / token-env for CI & this remote sandbox; never secrets in config files | Runs without a browser |
| **Profiles** | One profile = the demo project tenant | No cross-tenant accidents |

---

## 4. Prerequisites — confirm with IT before first real write

This is a **gated** rollout. Per §5.2 "never invent status," treat the following as **unconfirmed** until IT signs off:

1. **App + scopes** — a Feishu custom app with Open API permissions for **Base** (read/write records), **Approval** (create/query instances), **Wiki/Drive**, **Messenger**, **Tasks**. 企业版 does not grant these by default.
2. **API rate/quota** — CLI calls hit Open API rate limits, **separate from** the Automation run quota in §7. Design for **daily-digest batch calls**, not per-record loops.
3. **Identity** — bot identity for chasing/automation; PMO user identity for reports (CLI supports identity switching).
4. **Tenant/host** — the correct host (e.g. `feishu.cn`) set in the CLI profile.

Until 1–4 are confirmed, the skill runs in **`--dry-run` / read-only** mode only.

---

## 5. How it lands in the weekly flywheel (§5.3)

| Cadence step | CLI action |
|--------------|-----------|
| **Before meeting** | `Base` read → pull three trackers + Gantt; compute critical-path buffer, find overdue rows |
| **Change control (F1/F2)** | `Approval` create (dry-run → confirm); for F2 **assert both Hangzhou + Kunshan sign-offs present** before marking contract changed |
| **After meeting** | Assemble 6-section RAG report (worst-component = overall); `Wiki` publish; `Messenger` CC client |
| **Daily** | `Messenger` digest of overdue items + escalation per the ladder |

Bot wiring (the skill) lives at `.claude/skills/feishu-pmo/`. This doc is the **rules**; the skill is the **playbook**.

---

## 6. Guardrails (non-negotiable)

- **No write to a frozen-baseline row** (F1 styling/CAS, F2 contract) without routing through `docs/change-control.md` first — the CLI does not bypass change control.
- **F2 writes require parallel two-site sign-off** verified in `Approval` — never one site (CLAUDE.md §5.2).
- **Single source of truth** — the CLI edits **Bitable in place**; never export a second copy that can drift (§5.1).
- **Read-only until §4 confirmed.** Dry-run is the default, not the exception.
