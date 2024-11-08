import numpy as np
import pandas as pd

INTERVAL_MINS = 30
ALARM_RULE_ID = 2041  # 告警ID,用于Redis唯一状态标识
ALIAS = "BW1R"  # 界面上以及表格里期望的别名
VALUE_ALIAS = "BW1R.VALUE"


def pre(data, global_result: dict):
    # 去重
    unique_data = []
    for row in data:
        time = row["time"]
        value = float(row["value"])
        if not unique_data or abs(value - float(unique_data[-1]["value"])) > 0.00001:
            unique_data.append(row)
    return unique_data


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


def do(data, global_result: dict):
    # print("%s BW1R first time is %s, last time is %s" % (ALIAS, data[0]["time"], data[-1]["time"]))
    v1, v2 = -6, 6
    state_dict_slope = {
        '上升': lambda value: v2 < value,
        '平稳': lambda value: v1 <= value <= v2,
        '下降': lambda value: value < v1
    }

    if len(data) < (2 * (INTERVAL_MINS + 2) + 1):
        return

    df = pd.DataFrame(data)
    time = pd.to_datetime(df.iloc[:, 0])
    value = df.iloc[:, 1]

    # 将时间转换为时间戳（以秒为单位），然后转换为float类型的np.array
    time_float = np.array(time.astype(np.int64) / 10 ** 9, dtype=float)
    value_float = np.array(value, dtype=float)

    # insert lost value
    time_calc, value_calc = insert_lost_value(time_float, value_float, 30)

    value_series = pd.Series(value_calc)
    value_avg1 = value_series.rolling(window=51, center=True, min_periods=1).mean()
    value_avg = value_avg1.rolling(window=51, center=True, min_periods=1).mean()
    value_float = np.array(value_avg, dtype=float)

    # filtered_values = savgol_filter(value_calc, window_length=51, polyorder=3)
    # rolling_avg_values = pd.Series(filtered_values).rolling(window=9).mean()
    # value_float = np.array(rolling_avg_values, dtype=float)

    delta = (value_float[-1] - value_float[-25]) * 1000

    scene = 'avg'
    state_delta = next((key for key, func in state_dict_slope.items() if func(delta)), 'None')

    state_str = f'{scene}<br>delta={delta}:{state_delta}'
    print("GLC BW1R", state_str)
    global_result[ALIAS] = state_delta
    global_result[VALUE_ALIAS] = round(np.mean([float(item['value']) for item in data[-7:]]), 3)


###############
if __name__ == "__main__":
    import research.utils.influx_utils

    bw1r_data = research.utils.influx_utils.get_data('9', 'BW1R.UNIQUE', '2024-07-16 12:00:00', '2024-07-16 12:40:00')
    result = {}
    do(bw1r_data, result)
    print(result)
