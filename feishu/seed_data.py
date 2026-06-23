"""把 templates/*.csv 的种子数据灌进对应 Bitable 表（一次性）。

字段名与 CSV 表头逐字对应（见 schema.py）。日期列尝试解析为 epoch ms，空值跳过。
导入后请维护 Bitable 那一份，不要再回头改 CSV（单一真源原则）。
"""

import _bootstrap  # noqa: F401

import csv
import datetime as dt
import pathlib

import feishu_client as fc
import schema
from config import settings

TEMPLATES = pathlib.Path(__file__).resolve().parents[1] / "templates"

_DATE_FORMATS = ("%Y-%m-%d", "%Y/%m/%d", "%Y.%m.%d", "%Y-%m-%dT%H:%M:%S")


def _to_ms(text: str):
    text = text.strip()
    if not text:
        return None
    for fmt in _DATE_FORMATS:
        try:
            return int(dt.datetime.strptime(text, fmt).timestamp() * 1000)
        except ValueError:
            continue
    return None  # 非日期文本（如 "W5"/"2026.07-early"）由对应文本字段承载，这里不处理


def _row_to_fields(row: dict, table_def: dict) -> dict:
    fields = {}
    for field in table_def["fields"]:
        name, ftype = field[0], field[1]
        raw = (row.get(name) or "").strip()
        if not raw:
            continue
        if ftype == schema.DATETIME:
            ms = _to_ms(raw)
            if ms is not None:
                fields[name] = ms
        else:
            fields[name] = raw
    return fields


def run() -> None:
    client = fc.get_client()
    ids = settings.load_ids()

    for table_def in schema.TABLES:
        if not table_def["seed"]:
            continue
        csv_path = TEMPLATES / table_def["seed"]
        if not csv_path.exists():
            print(f"[seed] 跳过 {table_def['key']}：找不到 {csv_path}")
            continue
        with csv_path.open(encoding="utf-8-sig", newline="") as fh:
            rows = [_row_to_fields(r, table_def) for r in csv.DictReader(fh)]
        rows = [r for r in rows if r]
        table_id = ids["tables"][table_def["key"]]
        fc.batch_insert(client, ids["app_token"], table_id, rows)
        print(f"[seed] {table_def['key']:9s} 灌入 {len(rows)} 行 -> {table_id}")

    print("[seed] 完成。打开飞书查看数据效果。")


if __name__ == "__main__":
    run()
