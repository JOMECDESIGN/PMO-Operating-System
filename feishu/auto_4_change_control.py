"""自动化④ 变更回填与广播（F1/F2）。

飞书审批通过的变更回填到「变更台账」后，本脚本：
  · F2（接口契约）：必须 杭州签字 + 昆山签字 双勾才广播「契约 vX 变更，两侧同步」；
    缺签 → 拦下并提示，绝不单边放行（CLAUDE.md §3 铁律）。
  · F1（CAS/A 面）：广播级联评估 frame → mechanism → software。
广播后置「已同步=✓」，避免重发。对应 change-control.md 的收口质量门。
"""

import _bootstrap  # noqa: F401

import feishu_client as fc
import schema
from config import settings


def _checked(v) -> bool:
    return v is True or fc.as_text(v) in ("true", "True", "✓", "1")


def run(client=None) -> str:
    client = client or fc.get_client()
    ids = settings.load_ids()
    app_token = ids["app_token"]
    table_id = ids["tables"][schema.CHANGE["key"]]
    rows = fc.search_all(client, app_token, table_id)

    pending = [r for r in rows
               if fc.as_text(r["fields"].get(schema.CG_STATUS)) in schema.CG_ST_DONE
               and not _checked(r["fields"].get(schema.CG_SYNCED))]

    if not pending:
        text = "✅ 变更台账：无待广播的已批变更。"
        fc.deliver(client, text, "change-control")
        return text

    out, to_mark = [], []
    for r in pending:
        f = r["fields"]
        cid = fc.as_text(f.get(schema.CG_ID))
        title = fc.as_text(f.get(schema.CG_TITLE))
        line = fc.as_text(f.get(schema.CG_FREEZE))

        if line == "F2":
            if not (_checked(f.get(schema.CG_HZ)) and _checked(f.get(schema.CG_KS))):
                missing = []
                if not _checked(f.get(schema.CG_HZ)):
                    missing.append("杭州")
                if not _checked(f.get(schema.CG_KS)):
                    missing.append("昆山")
                out.append(f"⛔ [{cid}] {title}：F2 变更缺{' / '.join(missing)}签字，"
                           f"暂不广播（接口契约严禁单边放行）。")
                continue
            ver = fc.as_text(f.get(schema.CG_VER)) or "vX"
            out.append(f"📣 [{cid}] F2 接口契约变更 {ver}：{title} —— "
                       f"两侧立即同步代码/Mock，并确认「双侧已同步」后关闭。")
            to_mark.append(r["record_id"])
        elif line == "F1":
            out.append(f"📣 [{cid}] F1 CAS/A 面变更已批：{title} —— "
                       f"级联评估 frame → mechanism → software，更新数据版本。")
            to_mark.append(r["record_id"])
        else:
            out.append(f"⚠️ [{cid}] {title}：未标注冻结线(F1/F2)，请补全后再处理。")

    if to_mark:
        fc.batch_update(client, app_token, table_id,
                        [{"record_id": rid, "fields": {schema.CG_SYNCED: True}} for rid in to_mark])

    text = "变更控制广播（F1/F2）\n" + "\n".join(out)
    fc.deliver(client, text, "change-control")
    return text


if __name__ == "__main__":
    run()
