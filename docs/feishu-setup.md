# feishu-setup.md — 飞书集成落地指引

> 把 PMO 三大追踪器 + 变更台账搭进飞书，配好四个自动化，并接通 Claude Code 自然语言操作。
> 代码在 `feishu/`，底座是官方 `lark-oapi` SDK。

## 0. 前置：建飞书应用 + 开权限

1. 飞书开放平台 → 创建**自建应用** → 拿到 **App ID / App Secret**。
2. 开通权限（开发配置 → 权限管理）：
   - `bitable:app`（多维表格读写）
   - `im:message`、`im:message:send_as_bot`（发消息/@）
   - `im:chat`、`im:chat:readonly`（查群/群成员）
   - （可选）`approval:approval` —— 若用飞书审批驱动变更控制
3. 发布应用版本并通过审核（企业内自建一般自助通过）。
4. 把应用以**机器人**身份拉进「PMO 告警群」。

## 1. 装依赖 + 配凭证

```bash
pip install -r feishu/requirements.txt
export FEISHU_APP_ID=cli_xxx
export FEISHU_APP_SECRET=xxx
# 可选：建到指定云空间文件夹
export FEISHU_FOLDER_TOKEN=fldxxx
```

## 2. 一键搭建 + 灌种子

```bash
cd feishu
python build_workspace.py     # 建 interface / risk / milestone / change 四张表 → 生成 config/ids.json
python seed_data.py           # 把 templates/*.csv 灌进前三张表
```

打开飞书，应能看到 `PMO 作战室` 多维表格应用与四张表的数据。

## 3. 手动补一次（飞书 API 不支持的部分）

- **视图**：给 milestone 表加「看板」（按 Health 分组）、给 interface/gantt 数据加「甘特」视图。
- **公式/查找引用字段**：如需「剩余天数」「关联里程碑」等，在飞书界面加（API 不支持，一次性几分钟）。

## 4. 回填群与成员

```bash
python get_chat_ids.py    # 群名 -> chat_id，挑告警群填进 config/settings.py 的 ALERT_CHAT_ID
python get_user_ids.py    # 成员名 -> open_id，填进 settings.MEMBERS（@ 催办用）
```

也可用环境变量 `FEISHU_ALERT_CHAT_ID` / `FEISHU_PM_OPEN_ID`。

## 5. 跑自动化

```bash
python pmo_feishu.py interface    # S1 接口逾期催办
python pmo_feishu.py risk         # 风险预警
python pmo_feishu.py milestone    # 里程碑健康（整体=最差分量）
python pmo_feishu.py change       # F1/F2 变更广播（F2 强制双签）
python pmo_feishu.py all          # 四个一起
python pmo_feishu.py report       # 三表汇总 → RAG 周报骨架
```

未设 `ALERT_CHAT_ID` → dry-run，仅打印不发群。

## 6. 定时运行（每日摘要，省配额）

用任意定时器调用，**每天一次**即可（对齐 §7：daily-digest，不要 per-record）：

```cron
# 每个工作日 09:00 推送 PMO 四项摘要
0 9 * * 1-5  cd /path/to/PMO-Operating-System/feishu && /usr/bin/python pmo_feishu.py all >> /var/log/pmo_feishu.log 2>&1
```

GitHub Actions / 飞书自动化定时触发亦可。

## 7. 变更控制（F1/F2）怎么接

- 团队在**飞书审批**提「变更请求」（条件分支按 F1/F2 与 minor/major/cross-site 路由；F2 用**并行分支**让杭州+昆山同时签）。
- 审批通过后，把记录回填到 `变更台账` 表（飞书审批可配「审批结果写入多维表格」；或人工录）。
- `auto_4_change_control.py` 扫描已批未广播的变更：
  - **F2** 必须 `HZ sign-off` + `KS sign-off` 双勾才广播「契约 vX 变更，两侧同步」，缺签拦下；
  - **F1** 广播级联评估 frame→mechanism→software。
  - 广播后置 `Synced=✓`，避免重发。

## 8. 用 Claude Code 说人话操作

仓库根目录已带技能 **`feishu-pmo`**。在 Claude Code 里直接说：
- 「搭建飞书 PMO 工作台」「灌一下种子数据」
- 「跑一下接口逾期催办」「出本周 RAG 周报骨架」
- 「昆山要改一个 CAN FD 字段」→ 技能会提醒走 F2 双签流程

技能背后调 `feishu/pmo_feishu.py`。需要临时、零散地查飞书数据时，也可叠加官方 **larksuite/cli**（`lark` 命令，专为 AI Agent 设计，覆盖 Base/IM/Docs）。
