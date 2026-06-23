"""自动化⑤ 工作项健康度（每日摘要）：阻塞项 + 逾期未完成。

阻塞：状态=阻塞 —— 依赖未清，需排障。
逾期未完成：计划完成 < 今天 且 状态 ∉ (已完成/已取消)。
关键路径项优先标红（逾期即吃关键路径缓冲 → 直接威胁 M7）。按 R负责 @ 到人。
"""

import _bootstrap  # noqa: F401

import datetime as dt

import feishu_client as fc
import notify
import schema
from config import settings

WI_ST_BLOCKED = "阻塞"
WI_ST_DONE = ("已完成", "已取消")


def _date(ms) -> str:
    if isinstance(ms, (int, float)):
        return dt.datetime.fromtimestamp(ms / 1000).strftime("%Y-%m-%d")
    return "—"


def _at(f) -> str:
    owner = fc.as_text(f.get(schema.WI_R))
    return notify.at_name(owner) if owner else "@(未指派)"


def _tag(f) -> str:
    return "🔴关键路径 " if f.get(schema.WI_CP) is True else ""


def run(client=None) -> str:
    client = client or fc.get_client()
    ids = settings.load_ids()
    rows = [r["fields"] for r in
            fc.search_all(client, ids["app_token"], ids["tables"][schema.WORKITEM["key"]])]
    now = int(dt.datetime.now().timestamp() * 1000)

    blocked = [f for f in rows if fc.as_text(f.get(schema.WI_STATUS)) == WI_ST_BLOCKED]
    overdue = [f for f in rows
               if isinstance(f.get(schema.WI_PLAN_END), (int, float))
               and f[schema.WI_PLAN_END] < now
               and fc.as_text(f.get(schema.WI_STATUS)) not in WI_ST_DONE]

    if not blocked and not overdue:
        text = "✅ 工作项：无阻塞、无逾期未完成。"
        fc.deliver(client, text, "workitem-health")
        return text

    # 关键路径优先排前
    key = lambda f: (f.get(schema.WI_CP) is not True, fc.as_text(f.get(schema.WI_ID)))
    lines = []
    if blocked:
        lines.append(f"⛔ 阻塞工作项（{len(blocked)} 项，依赖未清需排障）")
        for f in sorted(blocked, key=key):
            lines.append(
                f"· {_tag(f)}[{fc.as_text(f.get(schema.WI_ID))}] {fc.as_text(f.get(schema.WI_NAME))} "
                f"｜{_at(f)} ｜原因: {fc.as_text(f.get(schema.WI_NOTE)) or '—'}"
            )
    if overdue:
        lines.append(f"🔴 逾期未完成（{len(overdue)} 项）")
        for f in sorted(overdue, key=key):
            days = (now - f[schema.WI_PLAN_END]) // 86_400_000
            lines.append(
                f"· {_tag(f)}[{fc.as_text(f.get(schema.WI_ID))}] {fc.as_text(f.get(schema.WI_NAME))} "
                f"｜计划完成 {_date(f.get(schema.WI_PLAN_END))} 逾期 {days} 天 "
                f"｜进度 {fc.as_text(f.get(schema.WI_PROGRESS))}% ｜{_at(f)}"
            )
    cp_hit = [f for f in blocked + overdue if f.get(schema.WI_CP) is True]
    lines.append(
        f"处置：阻塞项先清依赖；关键路径逾期即吃缓冲（{len(cp_hit)} 项命中）→ "
        f"超阈值升级 {notify.at_pm()}。"
    )
    text = "\n".join(lines)
    fc.deliver(client, text, "workitem-health")
    return text


if __name__ == "__main__":
    run()
