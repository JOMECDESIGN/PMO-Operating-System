"""PMO 飞书集成 · 唯一配置入口。

凭证从环境变量读取，绝不写进仓库（见 feishu/.gitignore）。
成员/群/联系人映射在搭好工作台后回填（用 get_chat_ids.py / get_user_ids.py 查）。
"""

import json
import os
import pathlib

# --- 应用凭证（飞书开放平台 → 自建应用）-----------------------------------
# export FEISHU_APP_ID=cli_xxx ; export FEISHU_APP_SECRET=xxx
APP_ID = os.environ.get("FEISHU_APP_ID", "")
APP_SECRET = os.environ.get("FEISHU_APP_SECRET", "")

# 多维表格建在哪个文件夹（云空间 folder_token）。留空 = 应用自身空间根目录。
FOLDER_TOKEN = os.environ.get("FEISHU_FOLDER_TOKEN", "")

# 工作台（Bitable 应用）显示名
WORKSPACE_NAME = "PMO 作战室 · Huaxiang NICE Smart-Cockpit Demo"

# --- 告警投递 --------------------------------------------------------------
# 周会/告警群的 chat_id（运行 get_chat_ids.py 查）。
# 未设置时，自动化脚本进入 dry-run，只把消息打印到终端，不发飞书。
ALERT_CHAT_ID = os.environ.get("FEISHU_ALERT_CHAT_ID", "")

# 升级阶梯 L2+ 的 PM open_id（运行 get_user_ids.py 查）
PM_OPEN_ID = os.environ.get("FEISHU_PM_OPEN_ID", "")

# owner 显示名 -> open_id，用于逾期催办时 @ 责任人。
# 例：{"张三": "ou_xxx", "李四": "ou_yyy"}
MEMBERS: dict[str, str] = {}

# --- ids.json（由 build_workspace.py 生成，存 app_token + 各表 table_id）----
_IDS_PATH = pathlib.Path(__file__).with_name("ids.json")


def load_ids() -> dict:
    if _IDS_PATH.exists():
        return json.loads(_IDS_PATH.read_text(encoding="utf-8"))
    raise SystemExit(
        "[feishu] config/ids.json 不存在 —— 先运行 `python build_workspace.py` 搭建工作台。"
    )


def save_ids(data: dict) -> None:
    _IDS_PATH.write_text(
        json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8"
    )
