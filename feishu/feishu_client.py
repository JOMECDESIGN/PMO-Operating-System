"""官方 lark-oapi SDK 的薄封装 —— PMO 业务只调这里的函数，不直接碰 SDK 细节。

只覆盖 PMO 用到的能力：建多维表格应用、建表、批量增/改/查记录、发消息。
所有失败统一抛 SystemExit，把 code/msg/log_id 打出来，便于排查。
"""

import json
import uuid

import lark_oapi as lark
from lark_oapi.api.bitable.v1 import (
    AppTableCreateHeader,
    AppTableFieldProperty,
    AppTableFieldPropertyOption,
    AppTableRecord,
    BatchCreateAppTableRecordRequest,
    BatchCreateAppTableRecordRequestBody,
    BatchUpdateAppTableRecordRequest,
    BatchUpdateAppTableRecordRequestBody,
    CreateAppRequest,
    CreateAppTableRequest,
    CreateAppTableRequestBody,
    ReqApp,
    ReqTable,
    SearchAppTableRecordRequest,
    SearchAppTableRecordRequestBody,
)
from lark_oapi.api.im.v1 import (
    CreateMessageRequest,
    CreateMessageRequestBody,
)

from config import settings


# --- 基础 ------------------------------------------------------------------
def get_client() -> lark.Client:
    if not settings.APP_ID or not settings.APP_SECRET:
        raise SystemExit(
            "[feishu] 缺少凭证：请先 export FEISHU_APP_ID / FEISHU_APP_SECRET。"
        )
    return (
        lark.Client.builder()
        .app_id(settings.APP_ID)
        .app_secret(settings.APP_SECRET)
        .log_level(lark.LogLevel.INFO)
        .build()
    )


def _check(resp, what: str):
    if not resp.success():
        raise SystemExit(
            f"[feishu] {what} 失败: code={resp.code} msg={resp.msg} "
            f"log_id={resp.get_log_id()}"
        )


# --- Bitable：建应用 / 建表 -------------------------------------------------
def create_app(client, name: str, folder_token: str = "") -> str:
    body = ReqApp.builder().name(name)
    if folder_token:
        body = body.folder_token(folder_token)
    req = CreateAppRequest.builder().request_body(body.build()).build()
    resp = client.bitable.v1.app.create(req)
    _check(resp, "app.create")
    return resp.data.app.app_token


def create_table(client, app_token: str, table_def: dict) -> str:
    headers = []
    for field in table_def["fields"]:
        name, ftype = field[0], field[1]
        hb = AppTableCreateHeader.builder().field_name(name).type(ftype)
        options = field[2] if len(field) > 2 else None
        if options:
            opts = [AppTableFieldPropertyOption.builder().name(o).build() for o in options]
            hb = hb.property(AppTableFieldProperty.builder().options(opts).build())
        headers.append(hb.build())

    req = (
        CreateAppTableRequest.builder()
        .app_token(app_token)
        .request_body(
            CreateAppTableRequestBody.builder()
            .table(
                ReqTable.builder()
                .name(table_def["name"])
                .default_view_name("Grid")
                .fields(headers)
                .build()
            )
            .build()
        )
        .build()
    )
    resp = client.bitable.v1.app_table.create(req)
    _check(resp, f"app_table.create({table_def['key']})")
    return resp.data.table_id


# --- Bitable：记录增 / 改 / 查 ---------------------------------------------
def batch_insert(client, app_token: str, table_id: str, rows: list[dict]) -> None:
    for i in range(0, len(rows), 500):
        chunk = rows[i : i + 500]
        records = [AppTableRecord.builder().fields(r).build() for r in chunk]
        req = (
            BatchCreateAppTableRecordRequest.builder()
            .app_token(app_token)
            .table_id(table_id)
            .request_body(
                BatchCreateAppTableRecordRequestBody.builder().records(records).build()
            )
            .build()
        )
        resp = client.bitable.v1.app_table_record.batch_create(req)
        _check(resp, "record.batch_create")


def batch_update(client, app_token: str, table_id: str, updates: list[dict]) -> None:
    """updates: [{"record_id": ..., "fields": {...}}, ...]"""
    recs = [
        AppTableRecord.builder().record_id(u["record_id"]).fields(u["fields"]).build()
        for u in updates
    ]
    for i in range(0, len(recs), 500):
        chunk = recs[i : i + 500]
        req = (
            BatchUpdateAppTableRecordRequest.builder()
            .app_token(app_token)
            .table_id(table_id)
            .request_body(
                BatchUpdateAppTableRecordRequestBody.builder().records(chunk).build()
            )
            .build()
        )
        resp = client.bitable.v1.app_table_record.batch_update(req)
        _check(resp, "record.batch_update")


def search_all(client, app_token: str, table_id: str) -> list[dict]:
    """拉全表，返回 [{"record_id":..., "fields":{...}}, ...]（自动翻页）。"""
    items: list[dict] = []
    page_token = None
    while True:
        b = (
            SearchAppTableRecordRequest.builder()
            .app_token(app_token)
            .table_id(table_id)
            .page_size(500)
            .request_body(SearchAppTableRecordRequestBody.builder().build())
        )
        if page_token:
            b = b.page_token(page_token)
        resp = client.bitable.v1.app_table_record.search(b.build())
        _check(resp, "record.search")
        data = resp.data
        for it in (data.items or []):
            items.append({"record_id": it.record_id, "fields": it.fields or {}})
        if getattr(data, "has_more", False) and data.page_token:
            page_token = data.page_token
        else:
            break
    return items


# --- 字段值归一化（Bitable 文本字段可能返回分段数组）-----------------------
def as_text(v) -> str:
    if v is None:
        return ""
    if isinstance(v, str):
        return v
    if isinstance(v, bool):
        return "✓" if v else ""
    if isinstance(v, (int, float)):
        return str(v)
    if isinstance(v, dict):
        return v.get("text") or v.get("name") or json.dumps(v, ensure_ascii=False)
    if isinstance(v, list):
        parts = []
        for x in v:
            if isinstance(x, dict):
                parts.append(x.get("text") or x.get("name") or "")
            else:
                parts.append(str(x))
        return "".join(parts)
    return str(v)


# --- 消息 ------------------------------------------------------------------
def send_text(client, receive_id: str, text: str, receive_id_type: str = "chat_id") -> None:
    req = (
        CreateMessageRequest.builder()
        .receive_id_type(receive_id_type)
        .request_body(
            CreateMessageRequestBody.builder()
            .receive_id(receive_id)
            .msg_type("text")
            .content(json.dumps({"text": text}))
            .uuid(str(uuid.uuid4()))
            .build()
        )
        .build()
    )
    resp = client.im.v1.message.create(req)
    _check(resp, "message.create")


def deliver(client, text: str, title: str = "alert") -> None:
    """统一投递：配了 ALERT_CHAT_ID 就发群，否则 dry-run 打印到终端。"""
    if settings.ALERT_CHAT_ID:
        send_text(client, settings.ALERT_CHAT_ID, text, "chat_id")
        print(f"[feishu] 已发送「{title}」→ chat {settings.ALERT_CHAT_ID}")
    else:
        print(f"[feishu] (dry-run) 未设 ALERT_CHAT_ID，「{title}」内容如下：\n{text}\n")
