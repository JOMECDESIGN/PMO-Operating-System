"""PMO 三大追踪表 + 变更台账的 Bitable 表结构定义（中文版）。

字段名与 templates/*.csv 表头逐字一致，seed_data.py 据此把 CSV 灌进表。
英文技术缩写（P-HUD / CAS / CAN FD / CMF / IMSE / NTC / SDK / M1–M7 / F1·F2 等）保留。
自动化通过本文件底部的「字段/选项常量」读取，避免在代码里散落中文字面量。

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
# fields 每项：(字段名, 类型) 或 (字段名, SELECT, [选项...])；列表第一个字段为主字段(文本)。

INTERFACE = {
    "key": "interface",
    "name": "S1 接口澄清追踪",
    "seed": "interface-tracker.csv",
    "fields": [
        ("编号", TEXT),
        ("部件", TEXT),
        ("待确认规格", TEXT),
        ("影响阻塞", TEXT),
        ("优先级", SELECT, ["最高", "高", "中"]),
        ("供货类型", SELECT, ["甲供-样件", "甲供-量产"]),
        ("状态", SELECT, ["未提供", "已提供待确认", "已确认冻结", "逾期"]),
        ("客户对接人", TEXT),
        ("我方负责人", TEXT),
        ("截止日", DATETIME),
        ("确认日", DATETIME),
        ("规格文件", TEXT),
        ("审批编号", TEXT),
        ("备注", TEXT),
    ],
}

RISK = {
    "key": "risk",
    "name": "风险登记册",
    "seed": "risk-register.csv",
    "fields": [
        ("编号", TEXT),
        ("等级", SELECT, ["高", "中"]),
        ("类别", TEXT),
        ("风险", TEXT),
        ("描述", TEXT),
        ("概率", SELECT, ["高", "中", "低"]),
        ("影响", TEXT),
        ("缓解措施", TEXT),
        ("负责人", TEXT),
        ("触发里程碑", TEXT),
        ("状态", SELECT, ["未开始", "监控中", "进行中", "已触发", "已缓解", "已关闭"]),
        ("最近评审", DATETIME),
        ("备注", TEXT),
    ],
}

MILESTONE = {
    "key": "milestone",
    "name": "里程碑 M1–M7",
    "seed": "milestone-tracker.csv",
    "fields": [
        ("编号", TEXT),
        ("里程碑", TEXT),
        ("周次", TEXT),
        ("月份", TEXT),
        ("通过标准", TEXT),
        ("关键前置", TEXT),
        ("负责团队", TEXT),
        ("状态", SELECT, ["未到达", "进行中", "已达成"]),
        ("健康度", SELECT, ["绿", "黄", "红"]),
        ("阻塞备注", TEXT),
    ],
}

# 变更台账（F1/F2）—— 无 CSV 种子，建空表。配合飞书审批回填，auto_4 据此校验广播。
CHANGE = {
    "key": "change",
    "name": "变更台账 F1/F2",
    "seed": None,
    "fields": [
        ("编号", TEXT),
        ("标题", TEXT),
        ("冻结线", SELECT, ["F1", "F2"]),
        ("类型", SELECT, ["轻微", "重大", "跨站点"]),
        ("提交人", TEXT),
        ("原因", TEXT),
        ("影响范围", TEXT),
        ("状态", SELECT, ["已提交", "评估中", "已批准", "已驳回", "已执行", "已关闭"]),
        ("杭州签字", CHECKBOX),
        ("昆山签字", CHECKBOX),
        ("契约版本", TEXT),
        ("已同步", CHECKBOX),
        ("提交日", DATETIME),
        ("备注", TEXT),
    ],
}

TABLES = [INTERFACE, RISK, MILESTONE, CHANGE]

DATE_FIELDS = {
    name for t in TABLES for (name, *rest) in t["fields"] if rest and rest[0] == DATETIME
}

# ---------------------------------------------------------------------------
# 字段名常量 —— 自动化只引用这些，不写中文字面量
# ---------------------------------------------------------------------------
# 接口表
IF_ID, IF_PART, IF_SPEC, IF_AFFECTS = "编号", "部件", "待确认规格", "影响阻塞"
IF_PRIORITY, IF_STATUS, IF_OWNER, IF_DUE = "优先级", "状态", "我方负责人", "截止日"
# 风险表
RK_ID, RK_LEVEL, RK_RISK, RK_MIT = "编号", "等级", "风险", "缓解措施"
RK_OWNER, RK_TRIGGER, RK_STATUS = "负责人", "触发里程碑", "状态"
# 里程碑表
MS_ID, MS_NAME, MS_WEEK, MS_HEALTH, MS_BLOCK = "编号", "里程碑", "周次", "健康度", "阻塞备注"
# 变更表
CG_ID, CG_TITLE, CG_FREEZE, CG_STATUS = "编号", "标题", "冻结线", "状态"
CG_HZ, CG_KS, CG_VER, CG_SYNCED = "杭州签字", "昆山签字", "契约版本", "已同步"

# 选项值常量
IF_ST_FROZEN, IF_ST_OVERDUE = "已确认冻结", "逾期"
IF_PRIORITY_RANK = {"最高": 0, "高": 1, "中": 2}
RK_LV_HIGH = "高"
RK_ST_TRIGGERED, RK_ST_WATCH = "已触发", ("未开始", "监控中")
MS_HEALTH_RANK = {"红": 2, "黄": 1, "绿": 0}
MS_HEALTH_EMOJI = {"红": "🔴", "黄": "🟡", "绿": "🟢"}
CG_ST_DONE = ("已批准", "已执行")
