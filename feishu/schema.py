"""PMO 三大追踪表 + 变更台账的 Bitable 表结构定义。

字段名与 templates/*.csv 的表头 **逐字一致**，seed_data.py 据此把 CSV 直接灌进表。
单选(SELECT)的可选项取「文档生命周期 ∪ CSV 实际取值」的并集，避免灌数时出现未定义选项。

Bitable 字段类型码：
  1=多行文本  2=数字  3=单选  4=多选  5=日期  7=复选框  11=人员  15=超链接
"""

TEXT = 1
NUMBER = 2
SELECT = 3
MULTISELECT = 4
DATETIME = 5
CHECKBOX = 7
USER = 11
URL = 15

# 每张表：key / name(飞书内显示) / seed(templates 下的 CSV，None=不灌种子) / fields
# fields 每项：(字段名, 类型) 或 (字段名, SELECT, [选项...])
# 列表中的第一个字段会成为表的「主字段」(必须文本类)。

INTERFACE = {
    "key": "interface",
    "name": "S1 接口澄清追踪 · Interface Tracker",
    "seed": "interface-tracker.csv",
    "fields": [
        ("ID", TEXT),
        ("Part", TEXT),
        ("Spec to confirm", TEXT),
        ("Affects", TEXT),
        ("Priority", SELECT, ["Highest", "High", "Mid"]),
        ("Supply type", SELECT, ["Client-ES", "Client-mass"]),
        ("Status", SELECT,
         ["Not provided", "Provided-pending-confirm", "Confirmed-frozen", "Overdue"]),
        ("Client contact", TEXT),
        ("Our owner", TEXT),
        ("Due date", DATETIME),
        ("Confirm date", DATETIME),
        ("Spec file", TEXT),
        ("Approval no.", TEXT),
        ("Notes", TEXT),
    ],
}

RISK = {
    "key": "risk",
    "name": "风险登记册 · Risk Register",
    "seed": "risk-register.csv",
    "fields": [
        ("ID", TEXT),
        ("Level", SELECT, ["High", "Mid"]),
        ("Category", TEXT),
        ("Risk", TEXT),
        ("Description", TEXT),
        ("Probability", SELECT, ["High", "Med", "Low"]),
        ("Impact", TEXT),
        ("Mitigation", TEXT),
        ("Owner", TEXT),
        ("Trigger milestone", TEXT),
        ("Status", SELECT,
         ["Not started", "Monitoring", "In progress", "Triggered", "Mitigated", "Closed"]),
        ("Last review", DATETIME),
        ("Notes", TEXT),
    ],
}

MILESTONE = {
    "key": "milestone",
    "name": "里程碑 · Milestones (M1–M7)",
    "seed": "milestone-tracker.csv",
    "fields": [
        ("ID", TEXT),
        ("Milestone", TEXT),
        ("Week", TEXT),
        ("Month ref", TEXT),
        ("Gate (pass criteria)", TEXT),
        ("Key prerequisite", TEXT),
        ("Owner team", TEXT),
        ("Status", SELECT, ["Not reached", "In progress", "Reached"]),
        ("Health", SELECT, ["Green", "Amber", "Red"]),
        ("Blocker/Notes", TEXT),
    ],
}

# 变更台账（F1/F2）—— 无 CSV 种子，由 build_workspace 建空表。
# 配合飞书 Approval：审批通过的变更回填到此表，auto_4 据此校验并广播。
CHANGE = {
    "key": "change",
    "name": "变更台账 · Change Control (F1/F2)",
    "seed": None,
    "fields": [
        ("ID", TEXT),
        ("Title", TEXT),
        ("Freeze line", SELECT, ["F1", "F2"]),
        ("Type", SELECT, ["minor", "major", "cross-site"]),
        ("Requester", TEXT),
        ("Reason", TEXT),
        ("Impact scope", TEXT),
        ("Status", SELECT,
         ["Submitted", "Assessing", "Approved", "Rejected", "Executed", "Closed"]),
        ("HZ sign-off", CHECKBOX),   # 杭州签字（F2 必需）
        ("KS sign-off", CHECKBOX),   # 昆山签字（F2 必需）
        ("Contract version", TEXT),
        ("Synced", CHECKBOX),        # auto_4 是否已广播/回填
        ("Submit date", DATETIME),
        ("Notes", TEXT),
    ],
}

TABLES = [INTERFACE, RISK, MILESTONE, CHANGE]

# 需要把 CSV 文本解析为日期(epoch ms)的字段
DATE_FIELDS = {
    name for t in TABLES for (name, *rest) in t["fields"] if rest and rest[0] == DATETIME
}
