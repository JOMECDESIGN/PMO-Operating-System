"""PMO 飞书统一入口（给 Claude Skill / 命令行用）。

  python pmo_feishu.py build       一键搭建 4 张表
  python pmo_feishu.py seed        灌入 CSV 种子
  python pmo_feishu.py chats       查群 chat_id
  python pmo_feishu.py users       查成员 open_id
  python pmo_feishu.py interface   跑 S1 接口逾期催办
  python pmo_feishu.py risk        跑风险预警
  python pmo_feishu.py milestone   跑里程碑健康
  python pmo_feishu.py change      跑变更广播(F1/F2)
  python pmo_feishu.py report      汇总三表 → RAG 周报骨架（整体=最差分量）
  python pmo_feishu.py all         一次跑完 4 个自动化
"""

import _bootstrap  # noqa: F401

import sys

import feishu_client as fc


def _report():
    """从三张表拼出 RAG 周报骨架（不发群，打印到终端供 PMO 润色）。"""
    import auto_2_risk_review as risk
    import auto_3_milestone_health as ms

    client = fc.get_client()
    print("=" * 60)
    print("PMO RAG 周报骨架（整体健康 = 最差分量）")
    print("=" * 60)
    print("\n【1. 里程碑】")
    print(ms.run(client))
    print("\n【2. 风险告警】")
    print(risk.run(client))
    print("\n【3. 关键路径 / 本周完成 / 决策项】—— 由 PMO 据 Gantt 补全（见 weekly-report.md 6 段式）。")


def main():
    cmd = sys.argv[1] if len(sys.argv) > 1 else "help"

    if cmd == "build":
        import build_workspace; build_workspace.run()
    elif cmd == "seed":
        import seed_data; seed_data.run()
    elif cmd == "chats":
        import get_chat_ids; get_chat_ids.run()
    elif cmd == "users":
        import get_user_ids; get_user_ids.run()
    elif cmd == "interface":
        import auto_1_interface_overdue as a; a.run()
    elif cmd == "risk":
        import auto_2_risk_review as a; a.run()
    elif cmd == "milestone":
        import auto_3_milestone_health as a; a.run()
    elif cmd == "change":
        import auto_4_change_control as a; a.run()
    elif cmd == "all":
        client = fc.get_client()
        import auto_1_interface_overdue, auto_2_risk_review
        import auto_3_milestone_health, auto_4_change_control
        for mod in (auto_1_interface_overdue, auto_2_risk_review,
                    auto_3_milestone_health, auto_4_change_control):
            mod.run(client)
    elif cmd == "report":
        _report()
    else:
        print(__doc__)


if __name__ == "__main__":
    main()
