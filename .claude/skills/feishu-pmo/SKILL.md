---
name: feishu-pmo
description: >-
  Operate the PMO Feishu/Lark workspace by plain-language request — build the
  Bitable trackers, seed them, run the four PMO automations (interface-overdue,
  risk review, milestone health, change-control broadcast), or assemble the RAG
  weekly report. Use when the user (in Chinese or English) asks to set up Feishu,
  push reminders, check risks/milestones, walk a styling (F1) or interface (F2)
  change, or generate the weekly report for the Huaxiang NICE smart-cockpit
  program. Backs onto feishu/pmo_feishu.py (official lark-oapi SDK).
---

# feishu-pmo — 用人话操作 PMO 飞书工作台

把用户的自然语言映射到 `feishu/pmo_feishu.py` 的子命令。所有命令在 `feishu/` 目录下运行，
依赖环境变量 `FEISHU_APP_ID` / `FEISHU_APP_SECRET`（缺失时先提醒用户配置，见 `docs/feishu-setup.md`）。

## 意图 → 命令

| 用户说（示例） | 执行 |
|---|---|
| 搭建/初始化飞书工作台、建表 | `cd feishu && python pmo_feishu.py build` |
| 灌种子/导入示例数据 | `python pmo_feishu.py seed` |
| 查群 chat_id / 成员 open_id | `python pmo_feishu.py chats` / `python pmo_feishu.py users` |
| 接口逾期催办、甲供件进度 | `python pmo_feishu.py interface` |
| 风险预警、本周风险 | `python pmo_feishu.py risk` |
| 里程碑健康、整体红黄绿 | `python pmo_feishu.py milestone` |
| 变更广播、F1/F2 同步 | `python pmo_feishu.py change` |
| 出周报、RAG 报告骨架 | `python pmo_feishu.py report` |
| 把四项都推一遍 | `python pmo_feishu.py all` |

## 关键纪律（执行前必守，源自 CLAUDE.md）

- **整体健康 = 最差分量**。汇报时任一里程碑 Red / 任一高风险 Triggered → 整体即 Red，不报假绿。
- **F2 接口契约变更必须杭州+昆山双签**。用户说「昆山/杭州要改 CAN FD / WebSocket / IO 表 / 场景 API」→
  这是 F2：先走 `docs/change-control.md`，在变更台账登记并确认双签，再 `python pmo_feishu.py change` 广播。**绝不单边放行。**
- **造型/CAS/A 面变更 = F1**：登记 → 级联评估 frame→mechanism→software → 客户书面确认 → PM 批准。
- **每日摘要，非每条触发**：自动化按天跑一次即可，别建 per-record 触发（§7 配额戒律）。
- **未配 `ALERT_CHAT_ID` 时是 dry-run**：命令只打印不发群，可放心先演示。

## 叠加：larksuite/cli（可选）

需要临时、零散地查飞书数据（某条记录、某个群、某篇文档）时，可用官方 **`lark` CLI**
（larksuite/cli，专为 AI Agent 设计，覆盖 Base/IM/Docs 200+ 命令）。结构化的 PMO 操作仍走
`pmo_feishu.py`（逻辑固定、可复现）；`lark` CLI 适合一次性查询。

## 出错时

- 报 `缺少凭证` → 让用户 export `FEISHU_APP_ID/SECRET`。
- 报 `config/ids.json 不存在` → 先 `build`。
- 发消息失败（权限）→ 检查应用 `im:message` 权限及是否已把机器人拉进群。
