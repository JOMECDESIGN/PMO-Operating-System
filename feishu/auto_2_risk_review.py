"""自动化② 风险周评审预警（每日摘要）。

红：任何 Triggered 风险（= 已成 issue，按 risk-register.md 升级）。
黄：High 且仍 Not started/Monitoring（进窗口前确认缓解到位）。
触发的 High 风险即 RAG 周报的红色头条。
"""

import _bootstrap  # noqa: F401

import feishu_client as fc
import notify
import schema
from config import settings


def run(client=None) -> str:
    client = client or fc.get_client()
    ids = settings.load_ids()
    rows = [r["fields"] for r in
            fc.search_all(client, ids["app_token"], ids["tables"][schema.RISK["key"]])]

    triggered = [f for f in rows if fc.as_text(f.get("Status")) == "Triggered"]
    watch = [f for f in rows
             if fc.as_text(f.get("Level")) == "High"
             and fc.as_text(f.get("Status")) in ("Not started", "Monitoring")]

    if not triggered and not watch:
        text = "✅ 风险登记册：无触发、无高风险待监控。"
        fc.deliver(client, text, "risk-review")
        return text

    lines = []
    if triggered:
        lines.append(f"🔴 已触发风险（{len(triggered)} 项，已成 issue，需处置+升级）")
        for f in triggered:
            owner = fc.as_text(f.get("Owner"))
            at = notify.at_name(owner) if owner else "@(未指派)"
            lines.append(
                f"· [{fc.as_text(f.get('ID'))}|{fc.as_text(f.get('Level'))}] "
                f"{fc.as_text(f.get('Risk'))} ｜缓解: {fc.as_text(f.get('Mitigation'))} ｜{at}"
            )
    if watch:
        lines.append(f"🟡 高风险待监控（{len(watch)} 项，进触发窗口前锁定缓解）")
        for f in watch:
            lines.append(
                f"· [{fc.as_text(f.get('ID'))}] {fc.as_text(f.get('Risk'))} "
                f"｜窗口: {fc.as_text(f.get('Trigger milestone'))} "
                f"｜状态: {fc.as_text(f.get('Status'))}"
            )
    if triggered:
        lines.append(f"升级：高风险触发 → {notify.at_pm()} + 处置计划（risk-register.md L3）。")
    text = "\n".join(lines)
    fc.deliver(client, text, "risk-review")
    return text


if __name__ == "__main__":
    run()
