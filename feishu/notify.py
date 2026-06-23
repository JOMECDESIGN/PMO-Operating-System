"""消息构造助手：@ 提醒 + 升级阶梯文案。"""

import _bootstrap  # noqa: F401

from config import settings


def at(open_id: str, name: str = "") -> str:
    """飞书文本消息里的 @ 某人。"""
    return f'<at user_id="{open_id}">{name}</at>'


def at_name(name: str) -> str:
    """按显示名查 open_id 并 @；查不到则退化为纯文本 @名字。"""
    open_id = settings.MEMBERS.get(name)
    return at(open_id, name) if open_id else f"@{name}"


def at_pm() -> str:
    return at(settings.PM_OPEN_ID, "PM") if settings.PM_OPEN_ID else "@PM"
