import datetime
import json
import logging
from typing import Optional, List

import pandas as pd
import numpy as np
from dac_ycl.jwd_ce.utils.ycl_abandon_abnormal import get_time
# from common.redis import default_cache
from dac_ycl.jwd_ce.utils.dac_facade import default_cache
from scipy.signal import find_peaks


def get_execute_time(last_time, TIME_SHIFT: int, INTERVAL_MINS: int):
    # last_time是数组里最后一个数据的时间
    # TIME_SHIFT是cron表达式里第一位的偏移量
    # INTERVAL_MINS是cron表达式的间隔，表述每x分钟调度一次
    last_ref_time = last_time - datetime.timedelta(seconds=TIME_SHIFT)
    nearest_time = last_ref_time.minute // INTERVAL_MINS * INTERVAL_MINS
    execute_time = last_ref_time.replace(minute=nearest_time, second=0, microsecond=0) + datetime.timedelta(
        seconds=TIME_SHIFT
    )
    if execute_time < last_ref_time:
        execute_time += datetime.timedelta(minutes=INTERVAL_MINS)
    return execute_time


def get_time_by_shift(last_time, TIME_SHIFT: int, INTERVAL_MINS: int, LAY_TIME):
    execute_time = get_execute_time(last_time, TIME_SHIFT, INTERVAL_MINS)
    print(f'execute_time的类型为{type(execute_time)}')
    return execute_time - datetime.timedelta(minutes=LAY_TIME)


def bl4sh_pre(data):
    # 去重
    unique_data = []
    for row in data:
        time = row["time"]
        value = float(row["value"])
        if not unique_data or abs(value - float(unique_data[-1]["value"])) > 0.18:
            unique_data.append({"time": get_time(time), "value": value})
    return unique_data


def combine(data):
    # FIX-0703 合并间隔在x分钟以内的变化
    combine_minute = 4
    length = len(data)
    delta_data = []
    for i in range(1, length):
        post_item = data[i]
        prev_item = data[i - 1]
        delta_data.append({"time": post_item["time"], "value": float(post_item["value"]) - float(prev_item["value"])})
    combined_data = []
    for index, item in enumerate(delta_data):
        if not combined_data:
            combined_data.append(item)
        else:
            this_time = item["time"]
            prev_delta = combined_data[-1]
            prev_time = prev_delta["time"]
            if this_time - prev_time <= datetime.timedelta(minutes=combine_minute):
                # do combine
                combined_data = combined_data[:-1]
                sum_value = prev_delta["value"] + item["value"]
                if abs(sum_value) > 0.2:
                    combined_data.append({"time": this_time, "value": sum_value})
            else:
                combined_data.append(item)
    return combined_data


def get_bl4sh_delta(data):
    data = bl4sh_pre(data)
    # 往前遍历直至第一个方向不一致的位置为止，取变化量
    combined_delta = combine(data)
    print(f"combined data: {combined_delta}")
    # data.reverse()
    combined_delta.reverse()
    # if len(data) == 1:
    #     return 0
    # if len(data) == 2:
    #     return data[0]['value'] - data[1]['value']
    # product = data[0]['value'] - data[1]['value']
    # result = data[0]['value'] - data[1]['value']
    # current_value = data[1]['value']
    # for index, item in enumerate(data):
    #     if index < 2:
    #         continue
    #     delta = current_value - item['value']
    #     new_product = product * delta
    #     if new_product < 0:
    #         break
    #     product = product + delta
    #     current_value = item['value']
    #     result = data[0]['value'] - item['value']
    # print('result is {}, current is {}'.format(result, data[0]['value']))
    if combined_delta:
        if len(combined_delta) == 1:
            return combined_delta[0]["value"]
        else:
            result = 0
            is_positive = combined_delta[0]["value"] > 0
            for delta in combined_delta:
                if delta["value"] > 0 == is_positive:
                    result += delta["value"]
                else:
                    break
        return result
    else:
        return 0


def get_expected_end_time(key, last_time, TIME_SHIFT: int, INTERVAL_MINS: int, LAY_TIME) -> Optional[datetime.datetime]:
    state_dict = json.loads(default_cache.get(key, "{}"))
    index = state_dict.get("__index__spec", -1)
    # index = -1 表示为无数据
    # index = 1 表示为第一次判断已过,即将进行第二次判断
    # index = 2 表示为第二次判断已过,即将进行第三次判断
    # index = 3 表示为第三次判断 (实际不存在)
    if index == -1:
        return get_execute_time(last_time, TIME_SHIFT, INTERVAL_MINS)
    if index == 1:
        return get_time_by_shift(last_time, TIME_SHIFT, INTERVAL_MINS, LAY_TIME)
    if index == 2:
        return None  # 触发异常回调终止


def get_data_before_time(data: List[dict], end_time: datetime.datetime) -> list:
    res = []
    for ele in data:
        if get_time(ele["time"]) <= end_time:
            res.append(ele)
    return res


def centered_ewm(
    data: List[dict],
    span: Optional[float] = None,
    alpha: Optional[float] = None,
    adjust: bool = True,
):
    df = pd.DataFrame(data)
    forward_ewm = df["value"].ewm(alpha=alpha, span=span, adjust=adjust).mean()
    backward_ewm = df["value"][::-1].ewm(alpha=alpha, span=span, adjust=adjust).mean()[::-1]
    df["value"] = 0.5 * (forward_ewm + backward_ewm)
    data = df.to_dict(orient="records")
    return data

def get_datetime(time_str):
    if len(time_str) <=19:
        return


def centered_guaidian(
    data: List[dict],
    time_diff: Optional[float] = 15
):
    df = pd.DataFrame(data)
    if df.empty:
        return None
    df['value'] = df['value'].astype('float')

    peaks, _ = find_peaks(df['value'])
    troughs, _ = find_peaks(-df['value'])
    turning_points = np.sort(np.concatenate((peaks, troughs)))

    filtered_turning_points = []
    last_turning_point = None

    for point in turning_points:
        if last_turning_point is None or (datetime.datetime.strptime(df['time'][point], "%Y-%m-%d %H:%M:%S.%f") - datetime.datetime.strptime(df['time'][last_turning_point], "%Y-%m-%d %H:%M:%S.%f")).total_seconds() / 60 > time_diff:
            filtered_turning_points.append(point)
            last_turning_point = point

    slopes = []
    for point in filtered_turning_points:
        if point >= 2 and point <= len(df) - 2:  # ensure enough data points on both sides
            slopes.append((df['time'][point], df['value'][point]))

    if slopes:
        return slopes[-1][1]
    return data[0][1]

