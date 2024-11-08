import datetime

import numpy as np

from dac_ycl.glc.utils.control_delta import get_data_before_time, centered_ewm, get_expected_end_time
from dac_ycl.glc.utils.ycl_abandon_abnormal import get_time

TIME_FORMAT = "%Y-%m-%d %H:%M:%S.%f"

INTERVAL_MINS = 2  # cron间隔时间
LAY_TIME = 2  # 单位分钟，查2分钟前的数据
TIME_SHIFT = 40  # cron正向偏移秒数
ALARM_RULE_ID = 2041  # 告警ID,用于Redis唯一状态标识
ALIAS = "D3LR"  # 界面上以及表格里期望的别名
VALUE_ALIAS = "D3LR.VALUE"

def pre(data, global_result: dict):
    # 去重
    unique_data = []
    for row in data:
        time = row["time"]
        value = float(row["value"])
        if not unique_data or abs(value - float(unique_data[-1]["value"])) > 0.00001:
            unique_data.append(row)
    return unique_data


def do(data, global_result: dict):
    print("D3LR first time is %s, last time is %s" % (data[0]["time"], data[-1]["time"]))
    state_dict = {
        "快速上升": lambda value: value > 2.5,
        "缓慢上升": lambda value: 0.95 < value <= 2.5,
        "平稳": lambda value: -0.95 <= value <= 0.95,
        "缓慢下降": lambda value: -2.5 <= value < -0.95,
        "快速下降": lambda value: value < -2.5,
    }
    alpha = 0.142857
    data1 = centered_ewm(data, alpha=alpha)
    end_time = get_expected_end_time(f"{ALARM_RULE_ID}_state", data1[-1]["time"], INTERVAL_MINS, TIME_SHIFT, LAY_TIME)
    if end_time is None:  # 中断回路
        global_result[ALIAS] = None
        return
    data1 = get_data_before_time(data1, end_time)
    length = len(data1)
    x = []
    y = []
    for i in range(1, length):
        x.append(int(get_time(data1[i]["time"]).timestamp()))
        y.append(float(data1[i]["value"]))

    x = np.array(x)
    y = np.array(y)
    if len(y) < 30:
        return "", ""

    # 使用线性回归模型拟合数据
    # step1 = -10
    # step2 = -20
    step3 = -30

    # slope0_1 = round(np.polyfit(x[step1:], y[step1:], 1)[0] * 10000, 4)
    # slope1_2 = round(np.polyfit(x[step2:step1], y[step2:step1], 1)[0] * 10000, 4)
    # slope2_3 = round(np.polyfit(x[step3:step2], y[step3:step2], 1)[0] * 10000, 4)
    # slope0_2 = round(np.polyfit(x[step2:], y[step2:], 1)[0] * 10000, 4)
    # slope1_3 = round(np.polyfit(x[step3:step1], y[step3:step1], 1)[0] * 10000, 4)
    slope0_3 = round(np.polyfit(x[step3:], y[step3:], 1)[0] * 10000, 3)

    # slope1 = round(0.45 * slope0_1 + 0.35 * slope1_2 + 0.2 * slope2_3, 3)
    # slope2 = round(0.55 * slope0_2 + 0.45 * slope1_3, 3)
    # slope = round(0.45 * slope1 + 0.35 * slope2 + 0.2 * slope0_3, 2)
    slope = slope0_3

    total_state = next((key for key, func in state_dict.items() if func(slope)), "None")
    # 调试切换下面的代码
    # state_str = f"{slope1}|{slope2}|{slope0_3}|{slope}:{total_state}"
    state_str = f"{slope}:{total_state}"
    # state_str = total_state
    global_result[ALIAS] = total_state
    global_result[VALUE_ALIAS] = round(np.mean(y[-5:]), 3)
