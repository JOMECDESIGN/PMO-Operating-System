"""在现有多维表格应用上**新增一张表**并灌入其种子（不动其它表）。

用法：cd feishu && python add_table.py workitem
"""

import _bootstrap  # noqa: F401

import csv
import pathlib
import sys

import feishu_client as fc
import schema
import seed_data
from config import settings

TEMPLATES = pathlib.Path(__file__).resolve().parents[1] / "templates"


def run(key: str) -> str:
    td = next((t for t in schema.TABLES if t["key"] == key), None)
    if not td:
        raise SystemExit(f"未知表 key: {key}（可选: {[t['key'] for t in schema.TABLES]}）")

    client = fc.get_client()
    ids = settings.load_ids()

    tid = ids.get("tables", {}).get(key)
    if tid:
        print(f"[add] 表 {key} 已存在 -> {tid}（跳过建表，仅尝试灌种子）")
    else:
        tid = fc.create_table(client, ids["app_token"], td)
        ids.setdefault("tables", {})[key] = tid
        settings.save_ids(ids)
        print(f"[add] 已建表 {key} · {td['name']} -> {tid}")

    if td["seed"]:
        csv_path = TEMPLATES / td["seed"]
        with csv_path.open(encoding="utf-8-sig", newline="") as fh:
            rows = [seed_data._row_to_fields(r, td) for r in csv.DictReader(fh)]
        rows = [r for r in rows if r]
        fc.batch_insert(client, ids["app_token"], tid, rows)
        print(f"[add] 灌入 {len(rows)} 行 -> {tid}")

    return tid


if __name__ == "__main__":
    run(sys.argv[1] if len(sys.argv) > 1 else "workitem")
