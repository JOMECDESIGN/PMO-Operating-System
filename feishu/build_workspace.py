"""一键搭建：在飞书里建好 PMO 多维表格应用 + 4 张表，落盘 config/ids.json。

用法：
    cd feishu && python build_workspace.py
前置：export FEISHU_APP_ID / FEISHU_APP_SECRET（应用需开通 bitable 读写权限）。
"""

import _bootstrap  # noqa: F401

import feishu_client as fc
import schema
from config import settings


def run() -> dict:
    client = fc.get_client()

    print(f"[build] 创建多维表格应用：{settings.WORKSPACE_NAME}")
    app_token = fc.create_app(client, settings.WORKSPACE_NAME, settings.FOLDER_TOKEN)
    print(f"[build] app_token = {app_token}")

    tables = {}
    for table_def in schema.TABLES:
        table_id = fc.create_table(client, app_token, table_def)
        tables[table_def["key"]] = table_id
        seed = table_def["seed"] or "(空表)"
        print(f"[build] 建表 {table_def['key']:9s} -> {table_id}   {table_def['name']}  [{seed}]")

    ids = {"app_token": app_token, "tables": tables}
    settings.save_ids(ids)
    print(f"[build] 已写入 {settings._IDS_PATH}")
    print(
        "\n下一步：\n"
        "  1) python seed_data.py            # 灌入 templates/*.csv 种子\n"
        "  2) 在飞书界面给 Bitable 切出 看板/甘特 视图，并补公式字段（API 不支持公式，需手动一次）\n"
        "  3) python get_chat_ids.py / get_user_ids.py 回填 config/settings.py 的群与成员\n"
    )
    return ids


if __name__ == "__main__":
    run()
