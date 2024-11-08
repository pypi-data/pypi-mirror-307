# 告警类型
# Todo 命名上，，要考虑。整合的话，不整合就算了。
ALARM_THRESHOLD_TYPE = 1  # 阈值告警
ALARM_REPOSITORY_TYPE = 2  # 告警码告警
ALARM_TIMING_TYPE = 3  # 趋势告警
ALARM_THRESHOLD_OVER_TYPE = 4  # 阈值结束告警
ALARM_VALUE_CHANGE_TYPE = 5  # 值变化告警
ALARM_VARIABLE_CHANGE_TYPE = 6  # 变量变化告警
ALARM_DEVICE_STATUS_CHANGE_TYPE = 7  # 设备状态变化告警
ALARM_SEGMENT_THRESHOLD_TYPE = 8  # 分段告警/函数告警
ALARM_SEGMENT_OVER_THRESHOLD_TYPE = 9  # 分段结束告警/函数结束告警
ALARM_CALC_TYPE = 10  # 计算+规则字典告警

# 告警等级
ALARM_LEVEL_S1 = 1
ALARM_LEVEL_S2 = 2
ALARM_LEVEL_S3 = 3
ALARM_LEVEL_S4 = 4
ALARM_LEVEL_LIST = ['S1','S2','S3','S4']
ALARM_LEVEL_MAP = dict(S1=1, S2=2, S3=3, S4=4)

# 告警状态
ALARM_STATUS_CLEARED = 0
ALARM_STATUS_ALARMING = 1
ALARM_STATELESS = 2

# 阈值告警窗口类型
ALARM_THRESHOLD_START_WINDOW_TYPE = {1: "滑动点数窗口", 2: "滑动时间窗口"}
ALARM_OPERATOR_TYPE = {1: "=", 2: "≠", 3: "<", 4: ">", 5: "≤", 6: "≥", 7: "∈[]", 8: "∉[]", 9: "∈(]", 10: "∉(]",
                       11: "∈[)", 12: "∉[)", 13: "∈()", 14: "∉()"}

# 执行动作
# Todo 命名规范需要重新整一下.
# 动作大类型

EX_TYPE_COUNTER_CONTROL = 1  # 反控设备
EX_TYPE_RELATE_RULES = 2  # 关联规则动作
EX_TYPE_API = 3  # 调用API服务
EX_TYPE_DATASET = 4  # 调用数据表

EX_SET_PROPERTY = 1  # 反控设备--属性设置
EX_INVOKE_SERVICE = 2  # 反控设备--服务调用
EX_INVOKE_RULES = 3  # 关联规则动作--关联规则动作
EX_GATEWAY_SERVICE = 4  # 网关反控-调用网关服务
EX_INVOKE_API = 5  # 调用API
EX_INVOKE_DATASET = 6  # 调用数据表

EX_TARGET_DEVICE = 0  # 反控目标设备
EX_TARGET_PRODUCT = 1  # 反控目标产品

EX_INVOKE_RULE_TRIGGER = 1  # 关联规则动作触发
EX_INVOKE_RULE_ENABLE = 2  # 关联规则动作启用
EX_INVOKE_RULE_DISABLE = 3  # 关联规则动作禁用

EX_INVOKE_API_PARAMS = [
    {'value': '//alarm_info', 'label': '告警详情', 'describe': '即告警中心-告警详情中的告警详细信息'},
    {'value': '//inform_info', 'label': '告警概述',
     'describe': '对告警规则的概述，内容为：触发`规则名称`，触发时间为`触发时间`'},
    {'value': '//rule_name', 'label': '规则名称', 'describe': '触发该告警的联动规则名称'},
    {'value': '//target_name', 'label': ' 告警对象（名称）',
     'describe': '告警详情中的告警对象的名称，即触发该告警的设备名称，例如：机器人A'},
    {'value': '//target_identifier', 'label': '告警对象（标识符）',
     'describe': '告警详情中的告警对象的标识符，即触发该告警的设备标识符，例如：c1034dc0-8595-11ed-a74e-56786ccd726c'},
    {'value': '//target_id', 'label': '告警对象（id）',
     'describe': '告警详情中的告警对象的id，即触发该告警的设备id，例如：127'},
    {'value': '//alarm_value', 'label': '属性值', 'describe': '该告警触发时刻的告警属性的属性值'},
    {'value': '//attribute_time_end', 'label': '属性时间-结束(yyyy-MM-dd HH:mm:ss.ms)',
     'describe': '结束该告警的属性的属性上报时间，格式为yyyy-MM-dd HH:mm:ss.ms，例如：2022-12-07 15:21:59.123'},
    {'value': '//attribute_time', 'label': '属性时间-触发(yyyy-MM-dd HH:mm:ss.ms)',
     'describe': '触发该告警的属性的属性上报时间，格式为yyyy-MM-dd HH:mm:ss.ms，例如：2022-12-07 15:21:59.123'},
    {'value': '//property', 'label': '属性', 'describe': '触发该告警的属性名称'},
    {'value': '//alarm_time_iso', 'label': '触发时间(ISO 8601)', 'describe': '该告警的触发时间，格式为ISO 8601'},
    {'value': '//alarm_time', 'label': '触发时间(yyyy-MM-dd HH:mm:ss)',
     'describe': '该告警的触发时间，格式为yyyy-MM-dd HH:mm:ss，例如：2022-12-07 15:21:59'},
    {'value': '//time_now', 'label': '当前时间(yyyy-MM-dd HH:mm:ss)',
     'describe': '系统当前的时间，格式为yyyy-MM-dd HH:mm:ss，例如：2022-12-07 15:21:59'},
    {'value': '//threshold', 'label': '阈值', 'describe': '（对阈值告警）该告警规则的阈值范围'},
    {'value': '//alarm_id', 'label': '告警码', 'describe': '（对告警码告警）触发的告警码'},

]

# 告警条件类型
AlARM_TREND_CONDITION_TYPE = 1
AlARM_NO_DATA_CONDITION_TYPE = 2
AlARM_PROPERTY_COMPARE_CONDITION_TYPE = 3
ALARM_CALC_CONDITION_TYPE = 4

# 趋势告警条件判断类型对照字典
ALARM_TREND_CONDITION_DIFFERENCE_TYPE = 1
ALARM_TREND_CONDITION_AVERAGE_TYPE = 2
ALARM_TREND_CONDITION_MAXIMUM_TYPE = 3
ALARM_TREND_CONDITION_MINIMUM_TYPE = 4
ALARM_TREND_CONDITION_MID_TYPE = 5
ALARM_TREND_CONDITION_EXTREME_TYPE = 6
ALARM_TREND_CONDITION_LATEST_TYPE = 7
CONDITION_OPERATOR_TYPE = {1: "变化值", 2: "平均值", 3: "最大值", 4: "最小值", 5: "中值", 6: "极值"}

# 告警处理类型handleOperation
HANDLE_CLEAR_ALARM = 1
HANDLE_INPUT_SUGGESTION = 2
HANDLE_OPERATION_TYPE = {1: "手动清除, 录入处理意见", 2: "录入处理意见", 3: "归档", 4: "还原"}

# 禁用定时告警标识符
DENY_TIMING_ALARM_CONTENT = 'never'

GATEWAY_REPOSITORY_CONTROL_CODE = {'001': '调用restartAll.exe', '002': '重启网关系统', '003': '重启某个子程序',
                                   '004': '启动Influxdb Server', None: '无动作'}

CALC_TYPE_MAP_ZH = {
    0: "CUSTOM",
    1: "变化量",
    2: "最新值",
    3: "平均斜率",
    4: "单向累计差值",
    5: "单向变化量",
    6: "单向平均斜率",
    7: "平均值",
    8: "最大值",
    9: "最小值"
}

CALC_TYPE_CUSTOM = 0 # CUSTOM类型计算

MYSQL_HOST = "192.168.3.149"
MYSQL_NAME = "tm"
MYSQL_PORT = 32305
MYSQL_USER = "zeusroot"
MYSQL_PASSWORD = "zhanwanzhanchi"