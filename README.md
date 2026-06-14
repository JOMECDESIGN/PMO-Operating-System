# PMO Operating System — `CLAUDE.md` for Project Management Offices

A **Claude Code–ready project constitution** for running a Project Management Office (PMO) on a complex, multi-team, two-site hardware/software delivery program. Built from a real engagement — the Huaxiang NICE smart-cockpit auto-show demo (30-week timeline, Hangzhou software + Kunshan embedded/hardware, client-supplied parts) — and generalized so you can adapt it to your own program.

The core artifact is [`CLAUDE.md`](./CLAUDE.md): a governing rule-set that Claude Code reads on entry and follows when doing any PMO work in the repo — tracking interfaces, guarding freeze lines, writing weekly RAG reports, running change control, and managing the seams between teams.

---

## Why this exists

Most PMO knowledge is trapped in Word decks and human habit. When you put a PMO assistant (Claude Code) to work, it needs **instruction-style knowledge**: structured, parseable, and prescriptive — not prose a human skims. This repo encodes a PMO's operating rules as a `CLAUDE.md` constitution plus a set of domain docs, so the assistant behaves like a disciplined PMO every time.

The design philosophy follows the broader Claude Code community consensus: a **sharp, short `CLAUDE.md`** that states rules and where things live, with details pushed into linked docs (progressive disclosure) rather than one giant speculative file.

---

## How to use it with Claude Code

1. **Copy `CLAUDE.md` to your repo root.** Claude Code auto-loads it on entry and treats it as governing context.
2. **Adapt the specifics** — milestones (M1–M7), the two sites, the freeze lines, the seam map — to your own program. Keep the *structure*; swap the *content*.
3. **Fill the `docs/` stubs** with your project's real SOPs and trackers (this repo ships the structure; the real engagement's detailed SOPs live in the team's Feishu Wiki).
4. **Drop in the `templates/`** CSVs as import seeds for your trackers (designed for Feishu Bitable, but plain CSV works anywhere).
5. **Then just ask** — *"draft this week's RAG report," "a styling change came in, walk me through it," "how's the project doing?"* — and Claude Code will follow the constitution.

> **Tip (community best practice):** grow `CLAUDE.md` organically. Start from this template, and each time Claude Code does something a real PMO wouldn't, add a line or two to correct it. A constitution that grows from real misfires beats one written speculatively.

---

## Repo structure

```
.
├── CLAUDE.md                  # The PMO constitution — Claude Code reads this first
├── README.md                  # This file
├── docs/
│   ├── framework.md           # PMO role, knowledge, methods, Feishu tooling (the "how it all works")
│   ├── interface-sop.md       # Seam S1: client-supplied interface clearance
│   ├── two-site.md            # Seam S2: Hangzhou ↔ Kunshan dependency map + interface contract
│   ├── gantt.md               # Seam S3: 30-week schedule baseline + critical path
│   ├── change-control.md      # Freeze lines F1 (CAS data) + F2 (interface contract)
│   ├── risk-register.md       # 17-risk register + weekly review cadence
│   └── weekly-report.md       # Milestones M1–M7 + RAG weekly report template
└── templates/
    ├── interface-tracker.csv  # Import seed → Feishu Bitable
    ├── risk-register.csv       # Import seed → Feishu Bitable
    └── milestone-tracker.csv   # Import seed → Feishu Bitable
```

---

## Core concepts (the spine of the constitution)

- **Prime directive** — *the right information to the right people at the right time.* The PMO is the PM's leverage and the project's information hub, not a team's executor.
- **Three seams (S1/S2/S3)** — supply (client↔us), cross-site (Hangzhou↔Kunshan), inter-team (critical path). ~70% of delay risk lives here.
- **Two freeze lines (F1/F2)** — CAS/A-surface data, and the interface contract. After freeze, nothing changes without change control. F2 changes need **both sites** to sign.
- **RAG weekly report** — overall health = the *worst* component (milestones, critical-path buffer, risks). Honest amber/red beats cosmetic green.
- **Feishu landing** — everything runs on Bitable + Approval + Automation + Wiki. **No Feishu Project license needed.**

---

## Recommended open-source references

Curated, verified resources this repo's structure draws on. Two buckets: **how to write a great `CLAUDE.md`**, and **project-management domain content** you can fold into the `docs/`. Star counts move — check the repos for current numbers.

### A. Writing effective `CLAUDE.md` / Claude Code setup

| Repo / resource | What it gives you |
|-----------------|-------------------|
| [`josix/awesome-claude-md`](https://github.com/josix/awesome-claude-md) | Curated collection of exemplary real-world `CLAUDE.md` files with analyses, best practices, and templates — the best starting point for studying patterns. |
| [`hesreallyhim/awesome-claude-code`](https://github.com/hesreallyhim/awesome-claude-code) | The main "awesome" list for the whole Claude Code ecosystem — commands, hooks, skills, `CLAUDE.md` files. |
| [`MuhammadUsmanGM/claude-code-best-practices`](https://github.com/MuhammadUsmanGM/claude-code-best-practices) | A comprehensive best-practices wiki: 30+ guides, `CLAUDE.md` templates across 11 stacks, starter kits, a `CLAUDE.md` generator/linter, and a minimal "80/20" example to start from. |
| [`abhishekray07/claude-md-templates`](https://github.com/abhishekray07/claude-md-templates) | `CLAUDE.md` templates plus a well-curated reading list of the authoritative Anthropic guidance and community write-ups. |
| [`shanraisshan/claude-code-best-practice`](https://github.com/shanraisshan/claude-code-best-practice) | Reference implementation of skills, subagents, hooks, and commands, with a tips-and-tricks section sourced from the Claude team and community. |
| [`rohitg00/awesome-claude-code-toolkit`](https://github.com/rohitg00/awesome-claude-code-toolkit) | A very large toolkit — agents, skills, commands, plugins, hooks, rules, templates, MCP configs — if you want to go deep on automation. |

### B. Project-management domain content (markdown)

| Repo / resource | What it gives you |
|-----------------|-------------------|
| [`jerzydziewierz/PMBOK-doc-templates`](https://github.com/jerzydziewierz/PMBOK-doc-templates) | PMBOK 6th-ed. document structure in CommonMark markdown — project charter, WBS, risk register, change control, stakeholder docs — as editable stubs. Maps cleanly onto the `docs/` here. |
| [`Josee9988/project-template`](https://github.com/Josee9988/project-template) | A polished GitHub repo template (issue templates, labels, README, bots) with MarkdownLint-clean docs — good hygiene reference for the repo around your `CLAUDE.md`. |
| [GitHub `project-management` topic](https://github.com/topics/project-management) | Browse live: agile/waterfall/hybrid templates, risk-management, stakeholder-management, PMBOK resources. |
| [GitHub `pmbok` topic](https://github.com/topics/pmbok) | PMBOK-specific markdown template collections and course material. |

### C. Authoritative Anthropic guidance

- **Claude Code Best Practices** — official guidance, the include/exclude table, and rule-writing patterns: <https://www.anthropic.com/engineering/claude-code-best-practices>
- **Manage Claude's memory** (`CLAUDE.md` hierarchy, project vs. user memory): <https://docs.claude.com/en/docs/claude-code/memory>

---

## Adapting to a different project

This constitution is opinionated toward a **two-site, hardware+software, fixed-deadline** program. To reuse it:

- **One site?** Drop seam S2 and freeze line F2; keep S1/S3 and F1.
- **Pure software?** Replace the CAS/A-surface freeze (F1) with your design/spec freeze; the interface-contract freeze (F2) often still applies between services or teams.
- **Agile cadence?** Swap the milestone gates for sprint/release boundaries; the RAG report and seam discipline carry over unchanged.
- **Different toolchain?** The Feishu section (§7) is the only tool-specific part — swap it for Jira/Linear/Notion. Everything else is tool-agnostic.

---

## License

Suggest **MIT** or **CC BY 4.0** if you publish this — both let others reuse and adapt freely. Add a `LICENSE` file before pushing to GitHub.

---

*Built by Studio Operations (PMO) for the Huaxiang NICE smart-cockpit program, generalized for reuse. The constitution is meant to be lived in and versioned — start here, then let it grow from real-world misfires.*
