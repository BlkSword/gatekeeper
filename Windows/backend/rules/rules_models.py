# 数据库模型

from tortoise import fields, Model

class Rule(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=255)          # 规则名称
    description = fields.TextField()                 # 规则描述
    rule_type = fields.CharField(max_length=50)       # 规则类型（command/file/service/registry/python_script）
    params = fields.JSONField()                      # 规则参数
    expected_result = fields.TextField()             # 预期结果
    baseline_standard = fields.TextField()           # 基线标准
    severity_level = fields.CharField(max_length=10) # 等级（high/medium/low）
    created_at = fields.DatetimeField(auto_now_add=True)
    risk_description = fields.TextField()            # 风险描述
    solution = fields.TextField()                    # 解决方案
    tip = fields.TextField()                         # 温馨提示

    class Meta:
        table = "security_rules"
        using_db = "rules_db" 

class Task(Model):
    id = fields.CharField(max_length=36, pk=True)  # UUID 作为主键
    status = fields.CharField(max_length=20, default="pending") # 任务状态（running/completed/failed）
    progress = fields.IntField(default=0)          # 当前进度
    total = fields.IntField(default=0)             # 总规则数
    created_at = fields.DatetimeField(auto_now_add=True)
    completed_at = fields.DatetimeField(null=True)

    class Meta:
        table = "scan_tasks"
        using_db = "rules_db" 

class TaskResult(Model):
    id = fields.IntField(pk=True)
    task = fields.ForeignKeyField("rules_app.Task", related_name="results")
    rule = fields.ForeignKeyField("rules_app.Rule", related_name="check_results")
    output = fields.TextField()                    # 检测输出
    is_compliant = fields.BooleanField()           # 是否合规
    executed_at = fields.DatetimeField(auto_now_add=True)

    class Meta:
        table = "task_results"
        using_db = "rules_db"  