"""自动化① S1 甲供件接口逾期催办（每日摘要，非每条触发）。

逾期判定：未 Confirmed-frozen 且（已过 Due date 或 Status=Overdue）。
按责任人 @ 汇总成一条摘要发到告警群 —— 对齐 CLAUDE.md §7「daily-digest, not per-record」配额戒律。
对应 R02 / interface-sop.md 的 L1 催办。
"""

import _bootstrap  # noqa: F401

import datetime as dt

import feishu_client as fc
import notify
import schema
from config import settings


def _overdue(fields: dict, now_ms: int) -> bool:
    status = fc.as_text(fields.get("Status"))
    if status == "Confirmed-frozen":
        return False
    if status == "Overdue":
        return True
    due = fields.get("Due date")
    return isinstance(due, (int, float)) and due < now_ms


def run(client=None) -> str:
    client = client or fc.get_client()
    ids = settings.load_ids()
    rows = fc.search_all(client, ids["app_token"], ids["tables"][schema.INTERFACE["key"]])
    now_ms = int(dt.datetime.now().timestamp() * 1000)

    overdue = [r["fields"] for r in rows if _overdue(r["fields"], now_ms)]
    if not overdue:
        text = "✅ S1 接口澄清：无逾期项。"
        fc.deliver(client, text, "interface-overdue")
        return text

    # 最高优先级排前
    rank = {"Highest": 0, "High": 1, "Mid": 2}
    overdue.sort(key=lambda f: rank.get(fc.as_text(f.get("Priority")), 9))

    lines = [f"🔴 S1 接口逾期催办（{len(overdue)} 项）—— 直接威胁 M2/M3 数据路径"]
    for f in overdue:
        owner = fc.as_text(f.get("Our owner"))
        at = notify.at_name(owner) if owner else "@(未指派 owner)"
        lines.append(
            f"· [{fc.as_text(f.get('ID'))}|{fc.as_text(f.get('Priority'))}] "
            f"{fc.as_text(f.get('Part'))} — {fc.as_text(f.get('Spec to confirm'))} "
            f"｜阻塞: {fc.as_text(f.get('Affects'))} ｜{at}"
        )
    lines.append("处置：L1 催 owner；逾期超窗 → L2 正式知会客户+经理（见 interface-sop.md）。")
    text = "\n".join(lines)
    fc.deliver(client, text, "interface-overdue")
    return text


if __name__ == "__main__":
    run()
