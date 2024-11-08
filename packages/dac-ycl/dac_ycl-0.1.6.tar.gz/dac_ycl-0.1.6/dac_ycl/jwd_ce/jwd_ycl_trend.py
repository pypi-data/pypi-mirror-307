import datetime
import numpy as np
import pandas as pd

from dac_ycl.jwd_ce.utils.control_delta import get_expected_end_time, get_data_before_time
from dac_ycl.jwd_ce.utils.ycl_abandon_abnormal import abandon_abnormal_ycl, get_time_str, get_time

INTERVAL_MINS = 6  # cron间隔时间
CRON_MINS = 2
LAY_TIME = 2  # 单位分钟，查2分钟前的数据
TIME_SHIFT = 40  # cron正向偏移秒数
ALARM_RULE_ID = 2041  # 告警ID,用于Redis唯一状态标识
ALIAS = "JWD_YCLJS"  # 界面上以及表格里期望的别名
VALUE_ALIAS = "JWD_YCLJS.VALUE"
ALIAS_2 = "JWD_YCLJS_MINOR"


def pre(data, global_result: dict):
    # 去重
    unique_data = []
    for row in data:
        time = row["time"]
        value = float(row["value"])
        if not unique_data or abs(value - float(unique_data[-1]["value"])) > 0.00001:
            unique_data.append({"time": get_time_str(get_time(time)), "value": value})
    return unique_data


def senconds_to_time_str(timestamp):
    timezone_offset = datetime.timedelta(hours=-8)
    dt_object = datetime.datetime.fromtimestamp(timestamp) + timezone_offset
    return dt_object.strftime("%Y-%m-%d %H:%M:%S")


def insert_lost_value(time, value, seconds=30):
    time_new = []
    value_new = []

    time_new.append(time[0])
    value_new.append(value[0])
    length = len(time)
    for i in range(1, length):
        delta_time = time[i] - time[i - 1]
        if delta_time > seconds + 20:
            num = int(delta_time / 30)
            inc_time = int(delta_time / (num + 1))
            inc_value = round((value[i] - value[i - 1]) / (num + 1), 4)
            # print(f'num={num} inc_time={inc_time}({senconds_to_time_str(time[i-1])}) inc_value={inc_value} {value[i]} {value[i-1]}')
            for j in range(0, num):
                time_new.append(time[i - 1] + j * inc_time)
                value_new.append(round(value[i - 1] + j * inc_value, 4))

        time_new.append(time[i])
        value_new.append(value[i])

    return time_new, value_new


def get_state_by_data(value, time_array, start_idx, end_idx, window_min):
    v1, v2, v3, v4 = -28, -10, 10, 28
    state_dict_slope = {
        '快速上升': lambda value: v4 < value,
        '缓慢上升': lambda value: v3 < value <= v4,
        '平稳': lambda value: v2 <= value <= v3,
        '缓慢下降': lambda value: v1 <= value < v2,
        '快速下降': lambda value: value < v1
    }
    delta = value[end_idx] - value[start_idx]
    slope_delta = round(delta * 10000 / (window_min * 60), 4)
    slope = round(np.polyfit(time_array[start_idx:end_idx + 1], value[start_idx:end_idx + 1], 1)[0] * 10000, 4)
    slope_mix = round(0.5 * slope_delta + 0.5 * slope, 4)

    state_slope = next((key for key, func in state_dict_slope.items() if func(slope)), 'None')
    state_slope_delta = next((key for key, func in state_dict_slope.items() if func(slope_delta)), 'None')
    state_slope_mix = next((key for key, func in state_dict_slope.items() if func(slope_mix)), 'None')

    return slope, slope_delta, slope_mix, state_slope, state_slope_delta, state_slope_mix


# ADJUST
# 原先是异常处理,再插数据,再中心加权平均的逻辑的话,中间时间格式变来变去..最后都是散着的需要写额外的函数来处理(这个你们来吧)
# 改起来不太方便,顺序调整为 先进行异常值处理,再进行中心加权平均,再插数据,跑通流程
def do_new(data, global_result: dict):
    print("YCL first time is %s, last time is %s" % (data[0]["time"], data[-1]["time"]))
    if len(data) < (2 * INTERVAL_MINS + 1):
        global_result[ALIAS] = '平稳'
        global_result[VALUE_ALIAS] = float(data[-1]["value"])
        global_result[ALIAS_2] = '平稳'
        return "", "None"

    # fixed, data1 = abandon_abnormal_ycl_new(data)
    # if fixed == 1:
    #     data = data1
    data = abandon_abnormal_ycl(pre(data, global_result))


    df = pd.DataFrame(data)
    forward_ewm = df["value"].ewm(span=11, adjust=False).mean()
    # backward_ewm = df["value"][::-1].ewm(alpha=alpha, span=span, adjust=adjust).mean()[::-1]
    df["value"] = forward_ewm
    data = df.to_dict(orient="records")
    # data = centered_ewm(data, span=5, adjust=False)


    # end_time = get_expected_end_time(f"{ALARM_RULE_ID}_state", data[-1]["time"], CRON_MINS, TIME_SHIFT, LAY_TIME)
    # if end_time is None:  # 中断回路
    #     global_result[ALIAS] = None
    #     return
    # data = get_data_before_time(data, end_time)
    df = pd.DataFrame(data)
    time = pd.to_datetime(df.iloc[:, 0])
    value = df.iloc[:, 1]

    # 将时间转换为时间戳（以秒为单位），然后转换为float类型的np.array
    time_float = np.array(time.astype(np.int64) / 10 ** 9, dtype=float)
    value_float = np.array(value, dtype=float)

    # insert lost value
    time_calc, value_calc = insert_lost_value(time_float, value_float, 30)

    # find start index for 300 seconds ago
    start_idx = -1 - (2 * INTERVAL_MINS)
    length = len(time_calc)
    now = time_calc[-1]
    end_idx = length - 1
    cmp_time = (INTERVAL_MINS * 60) - 3
    for i in range(length - 2, 0, -1):
        if now - time_calc[i] >= cmp_time:
            start_idx = i
            break

    # print(senconds_to_time_str(time_calc[start_idx]), senconds_to_time_str(time_calc[-1]), value_calc[start_idx:])

    value_series = pd.Series(value_calc)

    ewm2_value_float = np.array(value_series, dtype=float)
    slope, slope_delta, slope_mix, state_slope, state_slope_delta, state_slope_mix = get_state_by_data(ewm2_value_float,
                                                                                                       time_calc,
                                                                                                       start_idx,
                                                                                                       end_idx,
                                                                                                       INTERVAL_MINS)

    # slope_delta = round(delta * 10000 / (INTERVAL_MINS * 60), 4)
    # slope = round(np.polyfit(time_calc[start_idx:], ewm2_value_float[start_idx:], 1)[0] * 10000, 4)
    # slope_mix = round(0.5 * slope_delta + 0.5 * slope, 4)
    #
    # state_slope = next((key for key, func in state_dict_slope.items() if func(slope)), "None")
    # state_slope_delta = next((key for key, func in state_dict_slope.items() if func(slope_delta)), "None")
    # state_slope_mix = next((key for key, func in state_dict_slope.items() if func(slope_mix)), "None")
    scene = 'ORI'

    # state_str = f'{scene}<br>{senconds_to_time_str(time_calc[end_idx])}<br>slope={state_slope}({slope})<br>slope_delta={state_slope_delta}({slope_delta})<br>slope_mix={state_slope_mix}({slope_mix}):{state_slope_mix}'

    # if state_slope_mix == '缓慢上升' or state_slope_mix == '缓慢下降':
    #     slope_pre, slope_delta_pre, slope_mix_pre, state_slope_pre, state_slope_delta_pre, state_slope_mix_pre = get_state_by_data(
    #         ewm2_value_float, time_calc, start_idx - 12, end_idx - 12, INTERVAL_MINS)
    #     if state_slope_mix == '缓慢下降' and (state_slope_mix_pre == '缓慢下降' or state_slope_mix_pre == '快速下降'):
    #         slope_d, slope_delta_d, slope_mix_d, state_slope_d, state_slope_delta_d, state_slope_mix_d = get_state_by_data(
    #             ewm2_value_float, time_calc, start_idx - 12, end_idx, 2 * INTERVAL_MINS)
    #         scene = 'SCENE-1'
    #         # state_str = f'{scene}<br>{senconds_to_time_str(time_calc[end_idx])}<br>slope_mix_pre={state_slope_mix_pre}({slope_mix_pre})<br>slope_mix={state_slope_mix}({slope_mix})<br>slope_mix_d={state_slope_mix_d}({slope_mix_d}):{state_slope_mix_d}'
    #         state_slope_mix = state_slope_mix_d
    #     elif state_slope_mix == '缓慢上升' and (state_slope_mix_pre == '缓慢上升' or state_slope_mix_pre == '快速上升'):
    #         slope_d, slope_delta_d, slope_mix_d, state_slope_d, state_slope_delta_d, state_slope_mix_d = get_state_by_data(
    #             ewm2_value_float, time_calc, start_idx - 12, end_idx, 2 * INTERVAL_MINS)
    #         scene = 'SCENE-1'
    #         # state_str = f'{scene}<br>{senconds_to_time_str(time_calc[end_idx])}<br>slope_mix_pre={state_slope_mix_pre}({slope_mix_pre})<br>slope_mix={state_slope_mix}({slope_mix})<br>slope_mix_d={state_slope_mix_d}({slope_mix_d}):{state_slope_mix_d}'
    #         state_slope_mix = state_slope_mix_d
    # scene = "ORI"

    # state_str = f"{scene}<br>slope={state_slope}({slope})<br>slope_delta={state_slope_delta}({slope_delta})<br>slope_mix={state_slope_mix}({slope_mix}):{state_slope_mix}"
    global_result[ALIAS] = state_slope_mix
    global_result[VALUE_ALIAS] = round(np.mean(np.array(value_calc[-5:])), 3)
    minor_threshold = 5
    if slope_mix > minor_threshold:
        minor_state = "上升"
    elif slope_mix < -minor_threshold:
        minor_state = "下降"
    else:
        minor_state = "平稳"
    global_result[ALIAS_2] = minor_state


def do(data, global_result: dict):
    # 禁用了do_new的返回值
    do_new(data, global_result)
