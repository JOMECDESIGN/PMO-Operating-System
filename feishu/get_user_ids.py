"""查告警群成员的 open_id —— 回填 config/settings.py 的 MEMBERS（名字->open_id）。

按 settings.ALERT_CHAT_ID 列出群成员；未设则提示先跑 get_chat_ids.py。
"""

import _bootstrap  # noqa: F401

import feishu_client as fc
from lark_oapi.api.im.v1 import GetChatMembersRequest
from config import settings


def run(client=None) -> None:
    if not settings.ALERT_CHAT_ID:
        raise SystemExit("先设置 settings.ALERT_CHAT_ID（运行 get_chat_ids.py 查）。")
    client = client or fc.get_client()
    page_token = None
    print("成员名 -> open_id（填进 settings.MEMBERS 用于 @ 催办）")
    while True:
        b = (GetChatMembersRequest.builder()
             .chat_id(settings.ALERT_CHAT_ID)
             .member_id_type("open_id")
             .page_size(100))
        if page_token:
            b = b.page_token(page_token)
        resp = client.im.v1.chat_members.get(b.build())
        fc._check(resp, "chat_members.get")
        for m in (resp.data.items or []):
            print(f'  "{m.name}": "{m.member_id}",')
        if getattr(resp.data, "has_more", False) and resp.data.page_token:
            page_token = resp.data.page_token
        else:
            break


if __name__ == "__main__":
    run()
