"""把已部署的 4 张表重建为中文版（在同一多维表格应用内，wiki 链接不变）。

做法：用现有 app_token 新建 4 张中文表 → 灌中文种子 → 删除旧的英文表 →
保留 alert_chat_id，写回 config/ids.json。table_id 会变化（脚本自动更新）。

用法：cd feishu && python localize_rebuild.py
"""

import _bootstrap  # noqa: F401

import feishu_client as fc
import schema
import seed_data
from config import settings
from lark_oapi.api.bitable.v1 import DeleteAppTableRequest


def run() -> dict:
    client = fc.get_client()
    ids = settings.load_ids()
    app_token = ids["app_token"]
    old_tables = dict(ids.get("tables", {}))
    alert = ids.get("alert_chat_id")

    print("[localize] 在应用内新建 4 张中文表 …", app_token)
    new_tables = {}
    for td in schema.TABLES:
        tid = fc.create_table(client, app_token, td)
        new_tables[td["key"]] = tid
        print(f"  + {td['key']:9s} {td['name']} -> {tid}")

    # 先写回新 ids，再灌种子（seed_data 读 settings.load_ids()）
    ids = {"app_token": app_token, "tables": new_tables}
    if alert:
        ids["alert_chat_id"] = alert
    settings.save_ids(ids)

    print("[localize] 灌入中文种子 …")
    seed_data.run()

    print("[localize] 删除旧英文表 …")
    for key, tid in old_tables.items():
        req = DeleteAppTableRequest.builder().app_token(app_token).table_id(tid).build()
        fc.invoke(client.bitable.v1.app_table.delete, req, f"app_table.delete({key})")
        print(f"  - {key:9s} {tid} 已删除")

    print("[localize] 完成。table_id 已更新；wiki 链接与 alert_chat_id 不变。")
    return ids


if __name__ == "__main__":
    run()
