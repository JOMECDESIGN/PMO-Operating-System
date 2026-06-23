"""查应用所在的群 chat_id —— 回填 config/settings.py 的 ALERT_CHAT_ID。

前置：把应用拉进目标群（飞书群 → 设置 → 机器人 → 添加）。
"""

import _bootstrap  # noqa: F401

import feishu_client as fc
from lark_oapi.api.im.v1 import ListChatRequest


def run(client=None) -> None:
    client = client or fc.get_client()
    page_token = None
    print("群名 -> chat_id（把要发告警的群填进 settings.ALERT_CHAT_ID）")
    while True:
        b = ListChatRequest.builder().page_size(100).types("group")
        if page_token:
            b = b.page_token(page_token)
        resp = client.im.v1.chat.list(b.build())
        fc._check(resp, "chat.list")
        for c in (resp.data.items or []):
            print(f"  {c.name:30s}  {c.chat_id}")
        if getattr(resp.data, "has_more", False) and resp.data.page_token:
            page_token = resp.data.page_token
        else:
            break


if __name__ == "__main__":
    run()
