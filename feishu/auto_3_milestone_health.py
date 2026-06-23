"""自动化③ 里程碑健康度（每日摘要）。

整体健康 = 最差分量（任一红 → 整体红；否则任一黄 → 黄）。
这正是 weekly-report.md 的「Overall = the worst component」收口规则。
"""

import _bootstrap  # noqa: F401

import feishu_client as fc
import schema
from config import settings


def run(client=None) -> str:
    client = client or fc.get_client()
    ids = settings.load_ids()
    rows = [r["fields"] for r in
            fc.search_all(client, ids["app_token"], ids["tables"][schema.MILESTONE["key"]])]

    if not rows:
        text = "里程碑表为空 —— 先 python seed_data.py。"
        fc.deliver(client, text, "milestone-health")
        return text

    worst = max((fc.as_text(f.get(schema.MS_HEALTH)) or "绿" for f in rows),
                key=lambda h: schema.MS_HEALTH_RANK.get(h, 0))
    overall = schema.MS_HEALTH_EMOJI.get(worst, "🟢")

    reds = [f for f in rows if fc.as_text(f.get(schema.MS_HEALTH)) == "红"]
    ambers = [f for f in rows if fc.as_text(f.get(schema.MS_HEALTH)) == "黄"]

    lines = [f"{overall} 里程碑整体健康 = {worst}（= 最差分量）"]
    for tag, bucket in (("🔴 红", reds), ("🟡 黄", ambers)):
        for f in bucket:
            lines.append(
                f"{tag} [{fc.as_text(f.get(schema.MS_ID))}|{fc.as_text(f.get(schema.MS_WEEK))}] "
                f"{fc.as_text(f.get(schema.MS_NAME))} — {fc.as_text(f.get(schema.MS_BLOCK))}"
            )
    if not reds and not ambers:
        lines.append("全部 🟢，按计划推进。")
    text = "\n".join(lines)
    fc.deliver(client, text, "milestone-health")
    return text


if __name__ == "__main__":
    run()
