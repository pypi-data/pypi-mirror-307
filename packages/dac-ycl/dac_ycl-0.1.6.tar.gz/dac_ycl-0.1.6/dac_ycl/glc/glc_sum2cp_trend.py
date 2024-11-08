import numpy as np
import pandas as pd

from dac_ycl.glc.utils.control_delta import get_expected_end_time, get_data_before_time
from dac_ycl.glc.utils.ycl_abandon_abnormal import get_time_str, get_time

INTERVAL_MINS = 2  # cron间隔时间
LAY_TIME = 2  # 单位分钟，查2分钟前的数据
TIME_SHIFT = 40  # cron正向偏移秒数
ALARM_RULE_ID = 2041  # 告警ID,用于Redis唯一状态标识
ALIAS = "SUM2_CP"  # 界面上以及表格里期望的别名
VALUE_ALIAS = "SUM2_CP.VALUE"

def pre(data, global_result_dict):
    # 去重
    unique_data = []
    for row in data:
        time = row["time"]
        value = float(row["value"])
        if not unique_data or abs(value - float(unique_data[-1]["value"])) > 0.00001:
            unique_data.append({"time": get_time_str(get_time(time)), "value": value})
    return unique_data


def do_new(data, global_result: dict):
    print("SUM2CP first time is %s, last time is %s" % (data[0]["time"], data[-1]["time"]))
    # state_dict_slope = {
    #     '快速上升': lambda value: 22 < value,
    #     '缓慢上升': lambda value: 7.5 < value <= 22,
    #     '平稳': lambda value: -7.5 <= value <= 7.5,
    #     '缓慢下降': lambda value: -22 <= value < -7.5,
    #     '快速下降': lambda value: value < -22
    # }
    state_dict_slope = {
        "上升": lambda value: 10 < value,
        "无趋势": lambda value: -10 <= value <= 10,
        "下降": lambda value: value < -10,
    }
    end_time = get_expected_end_time(f"{ALARM_RULE_ID}_state", data[-1]["time"], INTERVAL_MINS, TIME_SHIFT, LAY_TIME)
    if end_time is None:  # 中断回路
        global_result[ALIAS] = None
        return
    data = get_data_before_time(data, end_time)
    df = pd.DataFrame(data)
    time = pd.to_datetime(df.iloc[:, 0])
    value = df.iloc[:, 1]

    # 将时间转换为时间戳（以秒为单位），然后转换为float类型的np.array
    time_float = np.array(time.astype(np.int64) / 10 ** 9, dtype=float)
    value_float = np.array(value, dtype=float)

    start_index_5min = -9
    slope1 = round(np.polyfit(time_float[start_index_5min:], value_float[start_index_5min:], 1)[0] * 10000, 4)

    start_index_10min = -21
    slope2 = round(
        np.polyfit(time_float[start_index_10min:start_index_5min], value_float[start_index_10min:start_index_5min], 1)[
            0
        ]
        * 10000,
        4,
    )

    delta = slope1 - slope2

    scene = 'ORI'
    state = '待定'
    threshold_slope = 5
    threshold_slope1 = 5.5
    threshold_slope2 = 7
    threshold_delta = 2.5
    threshold_delta2 = 5
    if delta > threshold_delta:
        if -threshold_slope2 < slope1 <= threshold_slope1:
            scene = 'SLOW_DOWN'
            state = '无趋势'
        if slope1 > threshold_slope1:
            scene = 'SPEED_UP'
            state = '上升'
        if slope1 <= -threshold_slope2:
            scene = 'SLOW_DOWN'
            state = '下降'
        if delta > threshold_delta2:
            if state == '下降':
                scene = 'SLOW_DOWN'
                state = '无趋势'

    if delta < -threshold_delta:
        if -threshold_slope1 <= slope1 < threshold_slope2:
            scene = 'SLOW_UP'
            state = '无趋势'
        if slope1 < -threshold_slope1:
            scene = 'SPEED_UP'
            state = '下降'
        if slope1 >= threshold_slope2:
            scene = 'SLOW_DOWN'
            state = '上升'
        if delta < -threshold_delta2:
            if state == '上升':
                scene = 'SLOW_UP'
                state = '无趋势'

    if -threshold_delta <= delta <= threshold_delta:
        scene = 'NORMAL'
        if slope1 > threshold_slope:
            state = '上升'
        elif slope1 < -threshold_slope:
            state = '下降'
        else:
            state = '无趋势'
    # state_str = f'{scene}<br>slope1={slope1}<br>slope_2={slope2}<br>slope_delta={delta}:{state}'
    # print(state_str)
    # 使用state而非state_str
    global_result[ALIAS] = state
    global_result[VALUE_ALIAS] = round(np.mean(value_float[-5:]), 3)


def do(data, global_result: dict):
    # 禁用了do_new的返回值
    do_new(data, global_result)
