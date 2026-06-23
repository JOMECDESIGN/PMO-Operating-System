# feishu/ — PMO 飞书集成层

把本仓的 PMO 宪法**落地成可运行的飞书工作台**：一键在飞书里建好三大追踪表 + 变更台账，
配好四个 PMO 自动化，并能用 Claude Code「说人话」操作。

> 底座：官方 **`lark-oapi`** SDK（覆盖全部 OpenAPI）。客户端不手写，PMO 只写业务逻辑。

---

## 它做什么

| 模块 | 对应 CLAUDE.md |
|---|---|
| `build_workspace.py` 建 4 张表 | 三大追踪器 + 变更台账（单一真源 → Bitable） |
| `seed_data.py` 灌 `templates/*.csv` | 导入种子，之后维护 Bitable 那一份 |
| `auto_1_interface_overdue.py` | S1 甲供件 15 日逾期催办（R02 / interface-sop.md） |
| `auto_2_risk_review.py` | 风险触发/临窗预警（risk-register.md） |
| `auto_3_milestone_health.py` | 里程碑 RAG，整体=最差分量（weekly-report.md） |
| `auto_4_change_control.py` | F1/F2 变更广播，F2 强制双签（§3 / change-control.md） |
| `pmo_feishu.py report` | 三表汇总 → RAG 周报骨架 |

四个自动化都是**每日摘要**（一条消息），不是每条记录触发 —— 对齐 §7 的 Automation 配额戒律。

---

## 文件结构

```
feishu/
├── requirements.txt            # 就一个 lark-oapi
├── config/
│   ├── settings.py             # 唯一要填：凭证(走环境变量)、群、成员、PM
│   ├── ids.example.json        # ids.json 的样例（真 ids.json 由搭建生成，不入库）
│   └── ids.json                # 【生成】app_token + 各表 table_id
├── schema.py                   # 4 张表结构（字段名与 templates/*.csv 逐字对齐）
├── feishu_client.py            # lark-oapi 薄封装：建表/增改查记录/发消息
├── build_workspace.py          # 一键搭建
├── seed_data.py                # 灌 CSV 种子
├── notify.py                   # @ 提醒/升级文案
├── get_chat_ids.py             # 查群 chat_id
├── get_user_ids.py             # 查成员 open_id
├── auto_1_interface_overdue.py
├── auto_2_risk_review.py
├── auto_3_milestone_health.py
├── auto_4_change_control.py
└── pmo_feishu.py               # 统一入口（Claude Skill 调它）
```

---

## 快速开始

```bash
pip install -r feishu/requirements.txt

export FEISHU_APP_ID=cli_xxx
export FEISHU_APP_SECRET=xxx          # 应用需开通 bitable + im 权限

cd feishu
python build_workspace.py             # 建 4 张表，生成 config/ids.json
python seed_data.py                   # 灌入种子数据
python get_chat_ids.py                # 拿告警群 chat_id → 填 settings.ALERT_CHAT_ID
python get_user_ids.py                # 拿成员 open_id → 填 settings.MEMBERS
python pmo_feishu.py all              # 跑一遍 4 个自动化
```

> 不设 `ALERT_CHAT_ID` 时，自动化进入 **dry-run**：只把消息打印到终端，不发飞书。便于先看效果。

详细步骤见 [`docs/feishu-setup.md`](../docs/feishu-setup.md)。用 Claude Code 说人话操作见根目录技能 `feishu-pmo`。

---

## 重要说明

- **凭证安全**：`APP_ID/APP_SECRET` 只走环境变量，不入库；`config/ids.json` 已 gitignore。
- **飞书限制**：API 能建表/字段/选项，但**公式字段、查找引用、甘特/看板视图需在飞书界面手动配一次**（一次性几分钟）。搭建脚本只负责表与字段。
- **单一真源**：导入后维护 Bitable，别再回头改 `templates/*.csv`。
