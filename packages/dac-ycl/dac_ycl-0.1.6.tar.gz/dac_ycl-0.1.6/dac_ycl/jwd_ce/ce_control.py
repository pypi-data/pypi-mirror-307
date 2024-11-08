import datetime

import numpy as np

from dac_ycl.jwd_ce.utils.dac_facade import default_cache, get_data, MysqlConnection as mysql_conn
from dac_ycl.jwd_ce.utils.ycl_abandon_abnormal import get_time_str, get_time, abandon_abnormal_ycl
from scipy.signal import find_peaks
from typing import Optional, List

import pandas as pd

ALARM_ID = 2043
CR11R_15MIN_THRESHOLD = 0.13
CR11R_15MIN_THRESHOLD2 = 0.02
CR11R_30MIN_THRESHOLD = 0.17 #0.07 到 0.17
CR11R_30MIN_THRESHOLD2 = 0.22
CR11R_15MIN_FAST_THRESHOLD = 0.2
CE_BL4SH_KEY = "CE_BL4SH_POSITION"
CE_CONTROL_KEY = "CE_CONTROL"
CE_LAST_ACTION_KEY = "CE_LAST_ACTION"
CE_LAST_ACTION_TIME = "CE_LAST_ACTION_TIME"
CE_YCL_LAST_ACTION_TIME = "CE_YCL_LAST_ACTION_TIME"
CR11R_LAST_15MIN_DELTA = "CR11R_LAST_15MIN_DELTA"
YCL_GUAIDIAN_VALUE = "YCL_GUAIDIAN_VALUE"
CE_ARTIFICIAL_KEY = "CE_ARTIFICIAL_KEY"
CE_AVOID_MINUTE = 60  # 通过redis的ttl进行保护
YCL_TREND_THRESHOLD = 0.50
# BD4R_HIGH_LIMIT = 1228
# BD4R_LOW_LIMIT = 1223.5

# YCL_HIGH_THRESHOLD = 1044.5
# YCL_LOW_THRESHOLD = 1035.5
# YCL_MIDDLE_VALUE = 1040

# CURRENT_LIMIT_CETH_HIGH = 6
# CURRENT_LIMIT_CETH_LOW = 2
# CURRENT_CETH_NAME = "PC2_CETH.CURRENT.PV"

YCL_LIMIT_LOW = 1038
YCL_LIMIT_HIGH = 1042

YCL_LIMIT_LOW_LOW = 1034
YCL_LIMIT_HIGH_HIGH = 1047

YCL_10MIN_THRESHOLD = 0.5
CR11R_YCL_THRESHOLD = 0.04
LIMIT_TIME = 15
ARTIFICIAL_AVOID_MINUTE = 10
# ycl高位cr11r下降斜率
ACTION_LEVEL1 = 0.7
ACTION_LEVEL2 = 0.8
ACTION_LEVEL3 = 1

YCL_LIMIT_ENABLE = 0
OPENING_SUPPLEMENT1 = 0.1
OPENING_SUPPLEMENT2 = 0.1
OPENING_SUPPLEMENT3 = 0

YCL_10MIN_FAST_THRESHOLD = 0.9
YCL_AVOID_THRESHOLD = 0.3
YCL_AVOID_THRESHOLD2 = 0.15

SWITCH_ARTIFICIAL = 0
class Fxxk:
    outer_delta = None  # 使用类来操作对外暴露的变量，保证外部能访问到新的值
    d_ds_data = []


outer = Fxxk()


def get_config(alarm_rule_id):
    global CE_AVOID_MINUTE, CR11R_15MIN_THRESHOLD, CR11R_15MIN_THRESHOLD2, CR11R_30MIN_THRESHOLD, CR11R_30MIN_THRESHOLD2, \
        CR11R_15MIN_FAST_THRESHOLD, YCL_LIMIT_LOW, YCL_LIMIT_HIGH, YCL_LIMIT_LOW_LOW, YCL_LIMIT_HIGH_HIGH, YCL_10MIN_THRESHOLD, \
        CR11R_YCL_THRESHOLD, LIMIT_TIME, ARTIFICIAL_AVOID_MINUTE,ACTION_LEVEL1,ACTION_LEVEL2,ACTION_LEVEL3, SWITCH_ARTIFICIAL
    global YCL_LIMIT_ENABLE, OPENING_SUPPLEMENT1, OPENING_SUPPLEMENT2, OPENING_SUPPLEMENT3,YCL_AVOID_THRESHOLD,YCL_AVOID_THRESHOLD2
    config_result = mysql_conn.query_config_by_alarm_rule_id(alarm_rule_id)
    config = config_result.get('CE', {})

    CE_AVOID_MINUTE = config.get('退避时间存储时长', CE_AVOID_MINUTE)
    LIMIT_TIME = config.get('退避时间', LIMIT_TIME)
    ARTIFICIAL_AVOID_MINUTE = config.get('人工退避时间', ARTIFICIAL_AVOID_MINUTE)
    CR11R_15MIN_THRESHOLD = config.get('SJ_CR11R十五分钟第一个阈值', CR11R_15MIN_THRESHOLD)
    CR11R_15MIN_THRESHOLD2 = config.get('SJ_CR11R十五分钟第二个阈值', CR11R_15MIN_THRESHOLD2)
    CR11R_30MIN_THRESHOLD = config.get('SJ_CR11R三十分钟阈值', CR11R_30MIN_THRESHOLD)
    CR11R_30MIN_THRESHOLD2 = config.get('SJ_CR11R三十分钟第二个阈值', CR11R_30MIN_THRESHOLD2)
    CR11R_15MIN_FAST_THRESHOLD = config.get('SJ_CR11R十五分钟快速变化阈值', CR11R_15MIN_FAST_THRESHOLD)
    YCL_LIMIT_LOW = config.get('GY_YCL下限', YCL_LIMIT_LOW)
    YCL_LIMIT_HIGH = config.get('GY_YCL上限', YCL_LIMIT_HIGH)
    YCL_LIMIT_LOW_LOW = config.get('GY_YCL底线', YCL_LIMIT_LOW_LOW)
    YCL_LIMIT_HIGH_HIGH = config.get('GY_YCL顶线', YCL_LIMIT_HIGH_HIGH)
    YCL_10MIN_THRESHOLD = config.get('SJ_YCL十分钟阈值', YCL_10MIN_THRESHOLD)
    CR11R_YCL_THRESHOLD = config.get('SJ_CR11R与ycl关系阈值', CR11R_YCL_THRESHOLD)
    YCL_LIMIT_ENABLE = config.get('YCL力度差开关', YCL_LIMIT_ENABLE)
    OPENING_SUPPLEMENT1 = config.get('LD_高位动作补偿1', OPENING_SUPPLEMENT1)
    OPENING_SUPPLEMENT2 = config.get('LD_高位动作补偿2', OPENING_SUPPLEMENT2)
    OPENING_SUPPLEMENT3 = config.get('LD_高位动作补偿3', OPENING_SUPPLEMENT3)
    ACTION_LEVEL1 = config.get('LD_CE力度一', ACTION_LEVEL1)
    ACTION_LEVEL2 = config.get('LD_CE力度二', ACTION_LEVEL2)
    ACTION_LEVEL3 = config.get('LD_CE力度三', ACTION_LEVEL3)
    YCL_AVOID_THRESHOLD = config.get('SJ_YCL对冲退避阈值一', YCL_AVOID_THRESHOLD)
    YCL_AVOID_THRESHOLD2 = config.get('SJ_YCL对冲退避阈值二', YCL_AVOID_THRESHOLD2)
    SWITCH_ARTIFICIAL = config.get('人工避让开关', SWITCH_ARTIFICIAL)
    print(config)
    return config


def get_mean(data, end_time):
    before_time = end_time - datetime.timedelta(seconds=60 * 3 + 10)
    end_time = end_time + datetime.timedelta(seconds=10)
    before_time = get_time_str(before_time)
    end_time = get_time_str(end_time)
    values = np.array([float(item["value"]) for item in data if before_time <= item["time"] <= end_time])
    return round(np.mean(values), 2)


def get_real_delta(data, current_time, other_time, global_result):
    try:
        before_time = current_time - datetime.timedelta(seconds=60 * 3 + 10)
        end_time = current_time + datetime.timedelta(seconds=10)
        before_time = get_time_str(before_time)
        end_time = get_time_str(end_time)
        values = np.array([float(item["value"]) for item in data if before_time <= item["time"] <= end_time])
        current_max_value = round(np.max(values), 2)
        current_min_value = round(np.min(values), 2)

        before_time = other_time - datetime.timedelta(seconds=60 * 3 + 10)
        end_time = other_time + datetime.timedelta(seconds=10)
        before_time = get_time_str(before_time)
        end_time = get_time_str(end_time)
        values = np.array([float(item["value"]) for item in data if before_time <= item["time"] <= end_time])
        other_max_value = round(np.max(values), 2)
        other_min_value = round(np.min(values), 2)

        if abs(current_max_value - other_min_value) > abs(current_min_value - other_max_value):
            return current_max_value - other_min_value
        else:
            return current_min_value - other_max_value
    except Exception as e:
        global_result['错误信息'] = str(e)


def get_datetime(time_str):
    if len(time_str) <= 19:
        return datetime.datetime.strptime(time_str, '%Y-%m-%d %H:%M:%S')
    else:
        return datetime.datetime.strptime(time_str, '%Y-%m-%d %H:%M:%S.%f')


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
        if last_turning_point is None or (get_datetime(df['time'][point]) - get_datetime(
                df['time'][last_turning_point])).total_seconds() / 60 > time_diff:
            filtered_turning_points.append(point)
            last_turning_point = point

    slopes = []
    for point in filtered_turning_points:
        if point >= 2 and point <= len(df) - 2:  # ensure enough data points on both sides
            slopes.append((df['time'][point], df['value'][point]))

    if slopes:
        return slopes[-1][1]
    return data[0][1]


def fix_action(this_delta, cr11r_delta_15min, ycl_10min_delta, ycl_15min_delta, global_result):
    global_result['动作规避'] = f'15分钟cr11r变化量：{cr11r_delta_15min}, 10分钟ycl变化量：{ycl_10min_delta}, 15分钟ycl变化量:{ycl_15min_delta}, 动作：{this_delta}'
    if cr11r_delta_15min * ycl_10min_delta < 0:
        if this_delta * ycl_10min_delta > 0 and abs(ycl_10min_delta) <= YCL_AVOID_THRESHOLD:
            pass
        else:
            this_delta = 0
    else:
        if abs(ycl_10min_delta) <= YCL_AVOID_THRESHOLD2 and abs(ycl_15min_delta) <= YCL_AVOID_THRESHOLD2:
            this_delta = 0


    return this_delta


def ce_ycl_control(is_stable, this_delta, last_delta, cur_ycl, ycl_delta_10min, last_action_time_str, cur_time):
    last_action_time = get_time(last_action_time_str)
    diff_minutes = (cur_time - last_action_time).total_seconds() / 60

    last_action = default_cache.get(CE_LAST_ACTION_KEY, 0)

    action = 0
    if diff_minutes >= 9:
        if ycl_delta_10min > YCL_10MIN_THRESHOLD:
            if this_delta >= last_delta >= 0:
                action = -ACTION_LEVEL1
            elif 0 >= this_delta >= -CR11R_YCL_THRESHOLD:
                action = 0
            elif this_delta <= -CR11R_YCL_THRESHOLD:
                action = -ACTION_LEVEL1

        elif ycl_delta_10min < -YCL_10MIN_THRESHOLD:
            if last_delta <= this_delta <= 0:
                action = ACTION_LEVEL1
            elif 0 <= this_delta <= CR11R_YCL_THRESHOLD:
                action = 0
            elif CR11R_YCL_THRESHOLD <= this_delta:
                action = ACTION_LEVEL1
        elif cur_ycl >= YCL_LIMIT_HIGH and ycl_delta_10min >= -YCL_10MIN_THRESHOLD:
            if last_delta >= -CR11R_YCL_THRESHOLD:
                action = -ACTION_LEVEL1
        elif cur_ycl <= YCL_LIMIT_LOW and ycl_delta_10min <= YCL_10MIN_THRESHOLD:
            if last_delta <= CR11R_YCL_THRESHOLD:
                action = ACTION_LEVEL1
        elif last_action != 0:
            if last_action > 0:
                if this_delta <= -CR11R_15MIN_THRESHOLD + 0.01:
                    action = ACTION_LEVEL1
            else:
                if this_delta >= CR11R_15MIN_THRESHOLD - 0.01:
                    action = ACTION_LEVEL1

    if action != 0:
        default_cache.set(CE_YCL_LAST_ACTION_TIME, get_time_str(cur_time), 3600)
        default_cache.set(CR11R_LAST_15MIN_DELTA, this_delta, 3600)
    return action


def ce_stable_action(is_stable, action, this_delta, ycl_now, ycl_delta_10min):
    threshold_increment = 0.1
    # cr11r上升，ycl上升，但是变化不大，不调整
    if 0 <= this_delta <= CR11R_15MIN_THRESHOLD and ycl_delta_10min <= YCL_10MIN_THRESHOLD - 0.2:
        if action < 0:
            return 0
    # cr11下降 , ycl 下降，但是ycl下降的趋势不大时，不调整
    elif -CR11R_15MIN_THRESHOLD <= this_delta <= 0 and -YCL_10MIN_THRESHOLD + 0.2 <= ycl_delta_10min <= 0:
        if action > 0:
            return 0
    # 在最高阈值线以上，增大斜率要求
    elif ycl_now > YCL_LIMIT_HIGH_HIGH and this_delta <= CR11R_15MIN_FAST_THRESHOLD:
        if action > 0 and ycl_delta_10min > 0:
            return 0
    elif ycl_now < YCL_LIMIT_LOW_LOW and this_delta >= -CR11R_15MIN_FAST_THRESHOLD:
        if action < 0 and ycl_delta_10min < 0:
            return 0

    # if action >= 0.8 and ycl_now >= YCL_LIMIT_HIGH:
    #     action = ACTION_LEVEL1
    # elif action >= 0.5 and ycl_now <= YCL_LIMIT_LOW:
    #     action = ACTION_LEVEL1 + ACTION_LEVEL3
    # elif action <= -0.5 and ycl_now <= YCL_LIMIT_LOW:
    #     action = -ACTION_LEVEL1
    # elif action <= -0.5 and ycl_now >= YCL_LIMIT_HIGH:
    #     action = -ACTION_LEVEL1 - ACTION_LEVEL3
    return action


def is_allow_by_time(has_last_action, current_time, last_action_time, last_action, this_action):
    if has_last_action != "":
        if last_action * this_action > 0:
            return current_time - last_action_time > datetime.timedelta(minutes=LIMIT_TIME)
    return True


def get_artificial_control(current_time):
    is_artificial_control = False
    history_dds_data = get_data('8', "CETHTC", get_time_str(current_time - datetime.timedelta(minutes=2)),
                                get_time_str(current_time))
    dds_data = round(float(history_dds_data[-1]['value']), 2)
    dds_after_last_action = default_cache.get(CE_ARTIFICIAL_KEY, dds_data)
    if abs(dds_after_last_action - dds_data) >= 0.2:
        is_artificial_control = True
    if is_artificial_control:
        default_cache.set("CE_ARTIFICIAL_CONTROL", True, ARTIFICIAL_AVOID_MINUTE * 60)
    else:
        is_artificial_control = default_cache.get("CE_ARTIFICIAL_CONTROL", False)
    return dds_data, is_artificial_control


def do(cr11r_data, global_result):
    """
    CR11R判断15分钟上升/下降趋势
    不和供料槽反向执行
    不用来调引出量
    """
    get_config(ALARM_ID)
    cur_time = get_time(cr11r_data[-1]['time'])
    cr11r_now = get_mean(cr11r_data, cur_time)
    cr11r_15min = get_mean(cr11r_data, cur_time + datetime.timedelta(minutes=-15))
    cr11r_delta_15min = round(cr11r_now - cr11r_15min, 2)
    cr11r_30min = get_mean(cr11r_data, cur_time + datetime.timedelta(minutes=-30))
    cr11r_delta_30min = round(cr11r_now - cr11r_30min, 2)
    global_result["CR11R_当前"] = cr11r_now
    global_result["CR11R_15分钟前"] = cr11r_15min
    global_result["CR11R_15分钟差值"] = cr11r_delta_15min
    global_result["CR11R_30分钟前"] = cr11r_30min
    global_result["CR11R_30分钟差值"] = cr11r_delta_30min
    # ycl_value = global_result['LQD_YCLJS.VALUE']

    ycl_data = get_data("9", "YCL.UNIQUE", get_time_str(cur_time + datetime.timedelta(minutes=-60)),
                        get_time_str(cur_time))
    ycl_data = abandon_abnormal_ycl(ycl_data)
    ycl_now = get_mean(ycl_data, cur_time)
    ycl_10min = get_mean(ycl_data, cur_time + datetime.timedelta(minutes=-10))
    ycl_15min = get_mean(ycl_data, cur_time + datetime.timedelta(minutes=-15))
    ycl_delta_10min = round(ycl_now - ycl_10min, 2)
    ycl_delta_15min = round(ycl_now - ycl_15min, 2)
    ycl_real_delta_10min = get_real_delta(ycl_data, cur_time, cur_time + datetime.timedelta(minutes=-10), global_result)
    ycl_real_delta_15min = get_real_delta(ycl_data, cur_time, cur_time + datetime.timedelta(minutes=-15), global_result)
    global_result["YCL_当前"] = ycl_now
    global_result["YCL_10分钟前"] = ycl_10min
    global_result["YCL_10分钟差值"] = ycl_delta_10min
    ycl_state = 0
    if ycl_delta_10min > YCL_TREND_THRESHOLD:
        ycl_state = 1
    elif ycl_delta_10min < -YCL_TREND_THRESHOLD:
        ycl_state = -1
    # 拐头？

    this_delta = 0
    do_case = ''
    if cr11r_delta_15min > CR11R_15MIN_THRESHOLD:
        this_delta = -ACTION_LEVEL3
        do_case = '1'
    elif cr11r_delta_15min < -CR11R_15MIN_THRESHOLD:
        this_delta = +ACTION_LEVEL3
        do_case = '2'
    elif cr11r_delta_30min > CR11R_30MIN_THRESHOLD2 and cr11r_delta_15min > CR11R_15MIN_THRESHOLD2:
        this_delta = -ACTION_LEVEL3
        do_case = '3'
    elif cr11r_delta_30min > CR11R_30MIN_THRESHOLD and cr11r_delta_15min > CR11R_15MIN_THRESHOLD2:
        this_delta = -ACTION_LEVEL2
        do_case = '4'
    elif cr11r_delta_30min < -CR11R_30MIN_THRESHOLD2 and cr11r_delta_15min < -CR11R_15MIN_THRESHOLD2:
        this_delta = +ACTION_LEVEL3
        do_case = '5'
    elif cr11r_delta_30min < -CR11R_30MIN_THRESHOLD and cr11r_delta_15min < -CR11R_15MIN_THRESHOLD2:
        this_delta = +ACTION_LEVEL2
        do_case = '6'

    if this_delta < 0 and ycl_state < 0:
        if cr11r_delta_15min <= CR11R_15MIN_THRESHOLD:
            this_delta = 0
    elif this_delta > 0 and ycl_state > 0:
        if cr11r_delta_15min >= -CR11R_15MIN_THRESHOLD:
            this_delta = 0

    cur_ycl = float(ycl_data[-1]['value'])
    try:
        if this_delta * ycl_state > 0:  # 引出量与CE调整同向了，CE先不调
            guaidian = centered_guaidian(ycl_data, 5)
            last_guaidian = default_cache.get(YCL_GUAIDIAN_VALUE, None)
            cur_ycl = float(ycl_data[-1]['value'])
            global_result['ce_ycl退避逻辑'] = f'cur_ycl为{cur_ycl},guaidian值为{guaidian}'
            if last_guaidian is None:
                if abs(cur_ycl - guaidian) < 1:
                    global_result['ycl距离拐点变化小于1'] = f'ycl为{cur_ycl},guaidian值为{guaidian}'
                    this_delta = 0
                    default_cache.set(YCL_GUAIDIAN_VALUE, guaidian, 3600)
            else:
                if abs(cur_ycl - last_guaidian) < 1:
                    global_result['ycl距离拐点变化小于1'] = f'ycl为{cur_ycl},guaidian值为{guaidian}'
                    this_delta = 0
                else:
                    default_cache.set(YCL_GUAIDIAN_VALUE, guaidian, 3600)

            global_result['ycl距离拐点差值'] = abs(cur_ycl - guaidian)
    except Exception as e:
        global_result['计算拐点逻辑错误'] = str(e)
        print(e)

    last_ce_ycl_action_time = default_cache.get(CE_YCL_LAST_ACTION_TIME, get_time_str(cur_time))
    last_delta = default_cache.get(CR11R_LAST_15MIN_DELTA, cr11r_delta_15min)
    ycl_flag = False
    is_stable = True
    try:
        if this_delta == 0:
            action = ce_ycl_control(is_stable, cr11r_delta_15min, last_delta, cur_ycl, ycl_delta_10min,
                                    last_ce_ycl_action_time, cur_time)
            if action != 0:
                this_delta = action
                do_case = '7'
                global_result[
                    'ce变化不大，根据ycl调整'] = f"""cr11r_delta_15min{cr11r_delta_15min}, last_delta:{last_delta},
                ycl_delta_10min: {ycl_delta_10min}, last_ce_ycl_action_time:{last_ce_ycl_action_time}, cur_time:{cur_time}"""
                ycl_flag = True
        else:
            action = ce_stable_action(is_stable, this_delta, cr11r_delta_15min, ycl_now, ycl_delta_10min)
            if action != this_delta:
                do_case = '8'
                global_result[
                    '对冲逻辑修正'] = f'cr11r_delta_15min:{cr11r_delta_15min}, ycl_delta_10min:{ycl_delta_10min},this_delta:{this_delta}, cur_action:{action}'
                this_delta = action
    except Exception as e:
        global_result['变化不大调整逻辑错误'] = str(e)

    last_action = default_cache.get(CE_LAST_ACTION_KEY, 0)
    last_action_time_str = default_cache.get(CE_LAST_ACTION_TIME, get_time_str(cur_time))
    global_result[
        '基本信息'] = f'last_action:{last_action}, this_delta:{this_delta}, cur_time:{get_time_str(cur_time)}, last_action_time:{last_action_time_str}'

    # 力度调整
    try:
        if YCL_LIMIT_ENABLE != 0:
            current_control_d3lr = this_delta
            if get_mean(ycl_data, cur_time) >= YCL_LIMIT_HIGH:
                if this_delta < 0:
                    this_delta = this_delta - OPENING_SUPPLEMENT1
                elif this_delta > 0:
                    this_delta = this_delta - OPENING_SUPPLEMENT2
            elif get_mean(ycl_data, cur_time) <= YCL_LIMIT_LOW:
                if this_delta < 0:
                    this_delta = this_delta + OPENING_SUPPLEMENT2
                elif this_delta > 0:
                    this_delta = this_delta + OPENING_SUPPLEMENT1
            elif YCL_LIMIT_LOW < get_mean(ycl_data, cur_time) < YCL_LIMIT_HIGH:
                if this_delta < 0:
                    this_delta = this_delta - OPENING_SUPPLEMENT3
                elif this_delta > 0:
                    this_delta = this_delta + OPENING_SUPPLEMENT3

            if current_control_d3lr != this_delta:
                global_result['触发力度调整'] = f'将力度{current_control_d3lr}, 改为{this_delta}'
    except Exception as e:
        global_result['力度调整出错'] = str(e)

    try:
        action = fix_action(this_delta, cr11r_delta_15min, ycl_real_delta_10min, ycl_real_delta_15min, global_result)
        if action != this_delta:
            global_result['动作退避'] = f'ce和ycl对冲，先不调，等等看'
            this_delta = action
    except Exception as e:
        global_result['逻辑报错'] = str(e)

    try:
        last_action_time = cur_time
        if last_action_time_str != get_time_str(cur_time):
            last_action_time = get_time(last_action_time_str)
        global_result[
            '退避条件'] = f'last_action_time_str:{last_action_time_str}, cur_time:{get_time_str(cur_time)}, last_action:{last_action_time}, last_action:{last_action}, this_delta:{this_delta}'

        if not is_allow_by_time(last_action_time_str, cur_time, last_action_time, last_action, this_delta):
            global_result["出现同向调整，退避"] = True
            this_delta = 0
    except Exception as e:
        global_result['退避错误'] = str(e)


    try:
        if SWITCH_ARTIFICIAL != 0:
            dds_data, is_artificial_control = get_artificial_control(cur_time)
            if is_artificial_control:
                global_result["人工操作退避"] = f"发生人工干预，本次不调，原先动作为{this_delta}"
                this_delta = 0

            dds_after_this = dds_data + this_delta
            global_result[CE_ARTIFICIAL_KEY] = dds_after_this
            default_cache.set(CE_ARTIFICIAL_KEY, dds_after_this, 3600)
    except Exception as e:
        print("get dds after excp", e)

    global_result['do_case'] = do_case
    global_result[CE_CONTROL_KEY] = this_delta

    outer.outer_delta = this_delta
    # current_pv = get_data("9", CURRENT_CETH_NAME, )
    # 设置同向退避时间，默认15分钟
    if this_delta != 0:
        default_cache.set(CE_LAST_ACTION_KEY, this_delta, CE_AVOID_MINUTE * 60)
        default_cache.set(CE_LAST_ACTION_TIME, get_time_str(cur_time), CE_AVOID_MINUTE * 60)

    print(f"CE global_result={global_result}")
