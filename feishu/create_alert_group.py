"""建「PMO 报警群」并把成员拉进来，chat_id 落进 config/ids.json 的 alert_chat_id。

用法：
    python create_alert_group.py                       # 用 settings.PMO_MEMBER_EMAILS
    python create_alert_group.py a@x.com b@x.com        # 临时指定成员邮箱
    python create_alert_group.py --alert               # 建群后立刻发一条真实报警

前提：成员必须与本应用在**同一飞书租户**，否则邮箱解析不到、无法拉入（会明确报出）。
应用需 im:chat（建群）+ contact:user.base:readonly（解析邮箱）权限。
"""

import _bootstrap  # noqa: F401

import sys

import feishu_client as fc
from config import settings


def run(emails=None, send_alert=False) -> str:
    emails = emails or settings.PMO_MEMBER_EMAILS
    client = fc.get_client()

    found, missing = fc.resolve_users(client, emails)
    for e in emails:
        print(f"  {e} -> {found.get(e, '❌ 未找到（不在本应用租户）')}")
    if missing:
        raise SystemExit(
            "以下成员不在本应用所属租户，无法拉入群：\n  " + "\n  ".join(missing) +
            "\n→ 飞书机器人只能在自己租户内建群拉人。请确认应用与成员同租户，"
            "或改用其在本租户登录的邮箱/手机号/open_id。"
        )

    chat_id = fc.create_group(
        client,
        settings.PMO_GROUP_NAME,
        list(found.values()),
        "PMO 自动化报警：接口逾期(S1) / 风险 / 里程碑健康 / 变更(F1·F2)。",
    )
    print(f"✅ 已建群「{settings.PMO_GROUP_NAME}」chat_id = {chat_id}")

    ids = settings.load_ids()
    ids["alert_chat_id"] = chat_id
    settings.save_ids(ids)
    print("已写入 config/ids.json（自动化将自动发往此群，无需再设环境变量）。")

    if send_alert:
        import auto_3_milestone_health as ms
        import auto_2_risk_review as risk
        fc.send_text(client, chat_id, "🔔 PMO 报警群已就绪 —— 下面是首条自动化播报。", "chat_id")
        ms.run(client)
        risk.run(client)
        print("已发送首条真实报警。")
    return chat_id


if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    run(emails=args or None, send_alert="--alert" in sys.argv)
