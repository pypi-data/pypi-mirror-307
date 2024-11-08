import numpy as np
import pandas as pd

INTERVAL_MINS = 10
ALIAS = "JWD_D3LR"  # 界面上以及表格里期望的别名


def pre(data, global_result: dict):
    # 去重
    unique_data = []
    for row in data:
        time = row["time"]
        value = float(row["value"])
        if not unique_data or abs(value - float(unique_data[-1]["value"])) > 0.00001:
            unique_data.append(row)
    return unique_data


def get_state_by_data(value, time_array, start_idx, end_idx, window_min):
    v1, v2, v3, v4 = -1.8, -0.7, 0.7, 1.8
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


def do_new_recheck(data, global_result, recheck_min, filter_type, window, with_fix):
    print('JWD D3LR first time is %s, last time is %s' % (data[0]['time'], data[-1]['time']))

    if len(data) < (2 * (INTERVAL_MINS + 2) + 1):
        return '', 'None'

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
    end_idx = length - 2 * recheck_min - 1
    now = time_calc[end_idx]
    cmp_time = (INTERVAL_MINS * 60) - 3
    for i in range(start_idx + 3, 0, -1):
        if now - time_calc[i] >= cmp_time:
            start_idx = i
            break

    # print(f'len={length}, start_idx={start_idx}, end_idx={end_idx} start_time={senconds_to_time_str(time_calc[start_idx])}, end_time={senconds_to_time_str(time_calc[end_idx])}, v_calc={value_calc[start_idx:end_idx]}')
    if end_idx - start_idx < 2 * INTERVAL_MINS:
        return '', ''

    value_series = pd.Series(value_calc)

    ewm2_value_float = None
    if filter_type == 'mean':
        ewm2_value_float = value_series.rolling(window=window, center=True).mean()
    elif filter_type == 'ewm2':
        ewm_value = value_series.ewm(span=window, adjust=False).mean()
        reversed_series = value_series[::-1]
        ewm_reversed = reversed_series.ewm(span=window, adjust=False).mean()
        ewm_value_lookahead = ewm_reversed[::-1]
        ewm2_value = 0.5 * ewm_value + 0.5 * ewm_value_lookahead
        ewm2_value_float = np.array(ewm2_value, dtype=float)
    elif filter_type == 'ewm':
        ewm_value = value_series.ewm(span=window, adjust=False).mean()
        ewm2_value_float = np.array(ewm_value, dtype=float)

    slope, slope_delta, slope_mix, state_slope, state_slope_delta, state_slope_mix = get_state_by_data(ewm2_value_float,
                                                                                                       time_calc,
                                                                                                       start_idx,
                                                                                                       end_idx,
                                                                                                       INTERVAL_MINS)
    state_slope_final = state_slope_mix
    scene = 'ORI'

    try:
        delta20 = round(ewm2_value_float[-1] - ewm2_value_float[-41], 2)
        delta15 = round(ewm2_value_float[-1] - ewm2_value_float[-31], 2)
        delta10 = round(ewm2_value_float[-1] - ewm2_value_float[-21], 2)
    except Exception as e:
        delta20 = round(ewm2_value_float[-1] - ewm2_value_float[-41] if len(ewm2_value_float) >= 41 else ewm2_value_float[-len(ewm2_value_float)], 2)
        delta15 = round(ewm2_value_float[-1] - ewm2_value_float[-31] if len(ewm2_value_float) >= 31 else ewm2_value_float[-len(ewm2_value_float)], 2)
        delta10 = round(ewm2_value_float[-1] - ewm2_value_float[-21] if len(ewm2_value_float) >= 21 else ewm2_value_float[-len(ewm2_value_float)], 2)
    delta_delta = 0
    if with_fix == 1:
        # slope1,slope_delta1,slope_mix1,state_slope1,state_slope_delta1,state_slope_mix1 = get_state_by_data(ewm2_value_float, time_calc, start_idx - 6, end_idx, INTERVAL_MINS+3)
        # slope2,slope_delta2,slope_mix2,state_slope2,state_slope_delta2,state_slope_mix2 = get_state_by_data(ewm2_value_float, time_calc, start_idx - 12, end_idx, INTERVAL_MINS+6)
        delta_delta = round(delta15 - delta10, 2)
        if state_slope_mix == '缓慢下降':
            if -0.08 <= delta15 and -0.04 <= delta10:
                scene = 'FIX-1-1'
                state_slope_final = '平稳'
            elif -0.06 <= delta15 <= -0.04 and -0.06 <= delta10:
                scene = 'FIX-1-2'
                state_slope_final = '平稳'
            elif delta_delta <= -0.1 and delta15 <= 2 * delta10:
                scene = 'FIX-1-3'
                state_slope_final = '平稳'
        elif state_slope_mix == '缓慢上升':
            if delta15 <= 0.08 and delta10 <= 0.04:
                scene = 'FIX-2-1'
                state_slope_final = '平稳'
            elif 0.04 <= delta15 <= 0.06 and delta10 <= 0.06:
                scene = 'FIX-2-2'
                state_slope_final = '平稳'
            elif 0.1 <= delta_delta and 2 * delta10 <= delta15:
                scene = 'FIX-2-3'
                state_slope_final = '平稳'
        elif state_slope_mix == '平稳':
            if delta10 <= -0.07:
                scene = 'FIX-3'
                state_slope_final = '缓慢下降'
            elif 0.07 <= delta10:
                scene = 'FIX-3'
                state_slope_final = '缓慢上升'

    state_str = f'{scene}<br>delta20={delta20}<br>delta15={delta15}<br>delta10={delta10}<br>delta_delta={delta_delta}<br>slope_mix={state_slope_mix}({slope_mix}):{state_slope_final}'
    print(state_str)
    # return f'{slope}', state_str
    # return state_slope_final
    global_result[ALIAS] = state_slope_final


def do(data, global_result):
    do_new_recheck(data, global_result, 2, 'ewm', 13, 1)
