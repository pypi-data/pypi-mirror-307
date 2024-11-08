import datetime
import pandas as pd
import numpy as np

from dac_ycl.glc.utils.control_delta import get_expected_end_time, get_data_before_time

# from dac_ycl.glc.utils.ycl_abandon_abnormal import get_time

INTERVAL_MINS = 6  # cron间隔时间
CRON_MINS = 2
LAY_TIME = 2  # 单位分钟，查2分钟前的数据
TIME_SHIFT = 40  # cron正向偏移秒数
ALARM_RULE_ID = 2041  # 告警ID,用于Redis唯一状态标识
ALIAS = "BD4R"  # 界面上以及表格里期望的别名
VALUE_ALIAS = "BD4R.VALUE"


def t(date_time):
    FORMAT = "%Y-%m-%d %H:%M:%S"
    return datetime.datetime.strftime(date_time, FORMAT)


def pre(data, global_result: dict):
    # 去重
    unique_data = []
    for row in data:
        time = row["time"]
        value = float(row["value"])
        if not unique_data or abs(value - float(unique_data[-1]["value"])) > 0.00001:
            unique_data.append(row)
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
    v1, v2, v3, v4 = -4.6, -2, 2, 4.6
    state_dict_slope = {
        '快速上升': lambda value: v4 < value,
        '缓慢上升': lambda value: v3 < value <= v4,
        '平稳': lambda value: v2 <= value <= v3,
        '缓慢下降': lambda value: v1 <= value < v2,
        '快速下降': lambda value: value < v1
    }
    start_idx = 0 if start_idx < 0 else start_idx
    delta = value[end_idx] - value[start_idx]
    slope_delta = round(delta * 10000 / (window_min * 60), 4)
    slope = round(np.polyfit(time_array[start_idx:end_idx + 1], value[start_idx:end_idx + 1], 1)[0] * 10000, 4)
    slope_mix = round(0.5 * slope_delta + 0.5 * slope, 4)

    state_slope = next((key for key, func in state_dict_slope.items() if func(slope)), 'None')
    state_slope_delta = next((key for key, func in state_dict_slope.items() if func(slope_delta)), 'None')
    state_slope_mix = next((key for key, func in state_dict_slope.items() if func(slope_mix)), 'None')

    return slope, slope_delta, slope_mix, state_slope, state_slope_delta, state_slope_mix


def do_new(data, global_result: dict):
    print("BD4R first time is %s, last time is %s" % (data[0]["time"], data[-1]["time"]))

    # ewm_value = value_series.ewm(span=13, adjust=False).mean()
    # ewm2_value_float = np.array(ewm_value, dtype=float)

    df = pd.DataFrame(data)
    forward_ewm = df["value"].ewm(span=13, adjust=False).mean()
    # backward_ewm = df["value"][::-1].ewm(alpha=alpha, span=span, adjust=adjust).mean()[::-1]
    df["value"] = forward_ewm
    data = df.to_dict(orient="records")
    # data = centered_ewm(data, span=5, adjust=False)

    end_time = get_expected_end_time(f"{ALARM_RULE_ID}_state", data[-1]["time"], CRON_MINS, TIME_SHIFT, LAY_TIME)
    if end_time is None:
        global_result[ALIAS] = None
        return
    data = get_data_before_time(data, end_time)

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

    if end_idx - start_idx < 2 * INTERVAL_MINS:
        global_result[ALIAS] = None
        return

    # print(f'len={length}, start_idx={start_idx}, end_idx={end_idx} start_time={senconds_to_time_str(time_calc[start_idx])}, end_time={senconds_to_time_str(time_calc[end_idx])}, v_calc={value_calc[start_idx:end_idx]}')

    ewm2_value_float = np.array(value_calc, dtype=float)

    # ewm_value = value_series.ewm(span=5, adjust=False).mean()
    #
    # reversed_series = value_series[::-1]
    # ewm_reversed = reversed_series.ewm(span=5, adjust=False).mean()
    # ewm_value_lookahead = ewm_reversed[::-1]
    #
    # ewm2_value = 0.5 * ewm_value + 0.5 * ewm_value_lookahead
    '''
    ewm2_value_float = np.array(value_calc, dtype=float)

    delta = ewm2_value_float[-1] - ewm2_value_float[start_idx]
    slope_delta = round(delta * 10000 / (INTERVAL_MINS * 60), 4)
    slope = round(np.polyfit(time_calc[start_idx:], ewm2_value_float[start_idx:], 1)[0] * 10000, 4)
    slope_mix = round(0.5 * slope_delta + 0.5 * slope, 4)

    state_slope = next((key for key, func in state_dict_slope.items() if func(slope)), "None")
    state_slope_delta = next((key for key, func in state_dict_slope.items() if func(slope_delta)), "None")
    state_slope_mix = next((key for key, func in state_dict_slope.items() if func(slope_mix)), "None")

    scene = "ORI"

    # current_time = get_time(data[-1]["time"])
    # before_time = current_time - datetime.timedelta(minutes=40)
    # bl4sh_data_ = get_data("9", "BL4SHPC", t(before_time), t(current_time))
    # bl4sh_delta = get_bl4sh_delta(bl4sh_data_)
    slope_10min = round(np.polyfit(time_calc[-31:-10], ewm2_value_float[-31:-10], 1)[0] * 10000, 4)
    slope_20min = round(np.polyfit(time_calc[-51:-10], ewm2_value_float[-51:-10], 1)[0] * 10000, 4)
    # if slope_10min
    # slope_10min_threshold = 2
    # slope_mix_threshold = 1.0
    # if slope_10min > 2 and state_slope_mix == "平稳" and bl4sh_delta > 0.1:
    #     if slope_mix > -slope_mix_threshold:
    #         state_slope_mix = "缓慢上升"
    #         print("\t修正上升")
    #     else:
    #         state_slope_mix = "平稳"
    #         print("\t不修正")
    # if slope_10min < -2 and state_slope_mix == "平稳" and bl4sh_delta < -0.1:
    #     if slope_mix < slope_mix_threshold:
    #         state_slope_mix = "缓慢下降"
    #         print("\t修正下降")
    #     else:
    #         state_slope_mix = "平稳"
    #         print("\t不修正")
    # if slope_10min > 1 and state_slope_mix == "缓慢下降" and bl4sh_delta > 0.1:
    #     state_slope_mix = "平稳"
    #     print("\t#修正下降")
    # if slope_10min < -1 and state_slope_mix == "缓慢上升" and bl4sh_delta < -0.1:
    #     state_slope_mix = "平稳"
    #     print("\t#修正上升")
    # if -1 <= slope_10min <= 1 and state_slope_mix == "缓慢下降" and bl4sh_delta > 0.1:
    #     if slope_mix > -2.5:
    #         state_slope_mix = "平稳"
    #         print("\t$修正下降")
    # if -1 <= slope_10min <= 1 and state_slope_mix == "缓慢上升" and bl4sh_delta < -0.1:
    #     if slope_mix < 2.5:
    #         state_slope_mix = "平稳"
    #         print("\t$修正上升")
    state_str = (
        f"{scene}<br>slope={state_slope}({slope})<br>slope_delta={state_slope_delta}({slope_delta})<br>slope_mix={state_slope_mix}({slope_mix})"
        f"<br>slope_10min={slope_10min},slope_20min={slope_20min}:{state_slope_mix}"
    )
    print(state_str)
    '''
    
    slope, slope_delta, slope_mix, state_slope, state_slope_delta, state_slope_mix = get_state_by_data(ewm2_value_float,
                                                                                                       time_calc,
                                                                                                       start_idx,
                                                                                                       end_idx,
                                                                                                       INTERVAL_MINS)

    # slope1, slope_delta1, slope_mix1, state_slope1, state_slope_delta1, state_slope_mix1 = get_state_by_data(
    #     ewm2_value_float, time_calc, start_idx - 6, end_idx, INTERVAL_MINS + 3)
    #
    # slope2, slope_delta2, slope_mix2, state_slope2, state_slope_delta2, state_slope_mix2 = get_state_by_data(
    #     ewm2_value_float, time_calc, start_idx - 12, end_idx, INTERVAL_MINS + 6)
    #
    # state_slope_final = state_slope_mix2
    # if state_slope_mix == state_slope_mix1:
    #     state_slope_final = state_slope_mix
    # elif state_slope_mix2 == state_slope_mix1:
    #     state_slope_final = state_slope_mix2

    scene = 'ORI'
    # state_str = f'{scene}<br>slope_mix12={state_slope_mix2}({slope_mix2})<br>slope_mix1={state_slope_mix1}({slope_mix1})<br>slope_mix={state_slope_mix}({slope_mix}):{state_slope_final}'
    # print(state_str)
    global_result[ALIAS] = state_slope_mix
    global_result[VALUE_ALIAS] = round(np.mean(value_calc[-5:]), 3)


def do(data, global_result: dict):
    # 禁用了do_new的返回值
    do_new(data, global_result)
