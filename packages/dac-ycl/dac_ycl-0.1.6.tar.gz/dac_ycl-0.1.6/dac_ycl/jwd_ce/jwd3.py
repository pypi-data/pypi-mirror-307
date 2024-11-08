import datetime
from typing import List, Optional

import numpy as np
import pandas as pd
from scipy.signal import find_peaks

from dac_ycl.jwd_ce.utils.control_delta import centered_ewm
from dac_ycl.jwd_ce.utils.dac_facade import default_cache, get_data, MysqlConnection as mysql_conn
from dac_ycl.jwd_ce.utils.ycl_abandon_abnormal import get_time, get_time_str, abandon_abnormal_ycl

"""
降温段控制算法
A-1 初次调整场景，基于状态判断动作，0.3/0.5/1.0
A-2 拉拐头场景，0.5/1.0
B   补动作，基于：情况变好/变坏，或者差值+阈值，0.5/1.0
C   位置跟随，D3LR上次调整完每变化一个单位，调整一个单位
D   YCL快速变化补充调整，+-0.3

context结构
JWD_LAST_TIME: 上次调整时间（只有场景A需要记录）
JWD_LAST_ACTION: 上次调整量（只有场景A需要记录）
JWD_TOTAL_ACTION: 用于跟踪调整量是否足够
JWD_PREV_D3LR: 用于位置跟随调整(C)
JWD_CONTINUE: 持续调整至拐头flag，0表示无需求，1表示需要加至d3lr向上，-1表示需要减至d3lr向下
"""

STAGE_C_VALUE_THRESHOLD = 350
ALIAS = "CONTROL"
TTL = 3600

# JWD_RULE_ID = 2040
JWD_RULE_ID = 2

CONTEXT_KEY_LAST_TIME = "JWD_LAST_TIME"
CONTEXT_KEY_YCL_LAST_TIME = "JWD_YCL_LAST_TIME"
CONTEXT_KEY_CONTINUE = "JWD_CONTINUE"
CONTEXT_KEY_LAST_ACTION = "JWD_LAST_ACTION"
CONTEXT_KEY_LAST_ACTION_D3LR = "CONTEXT_KEY_LAST_ACTION_D3LR"
CONTEXT_KEY_TOTAL_ACTION = "JWD_TOTAL_ACTION"
CONTEXT_KEY_PREV_VALUE = "JWD_PREV_D3LR"
CONTEXT_KEY_YCL_FAST_CHANGE = "JWD_YCL_FAST_CHANGE"
CONTEXT_KEY_YCL_DIRECTION = "JWD_YCL_DIRECTION"
CONTEXT_KEY_WAIT_ONCE = "JWD_WAIT_ONCE"
CONTEXT_KEY_DDS_TIME = "JWD_DDS_TIME"
CONTEXT_KEY_DDS = "JWD_DDS"
CONTEXT_KEY_DDS_TOTAL = "JWD_DDS_TOTAL"
CONTEXT_KEY_OPPOSITE_ACTION_TIME = "JWD_OPPOSITE_ACTION_TIME"
CONTEXT_KEY_ACTION_BACK = 'JWD_ACTION_BACK'
CONTEXT_KEY_LAST_SCENE = 'JWD_LAST_SCENE'
CONTEXT_CENTER_TEMP = 'JWD_CENTER_TEMP'


PERIOD_MIN = 3  # 3分钟平均值作为某一时间的值

LIMIT_TIME = 17  # min

YCL_CHECK_MIN = 20
YCL_CHECK_THRESHOLD = 0.5  # n分钟只要没变化超过一定值，就认为冷却段不被限制调整

YCL_STABLE_MIN = 10
YCL_STABLE_THRESHOLD = 0.2

D3LR_CONTINUE_THRESHOLD1 = 0.08
D3LR_CONTINUE_THRESHOLD2 = 0.04
D3LR_FAST_MIN = 10
D3LR_FAST_THRESHOLD = 0.18
D3LR_20MIN_THRESHOLD = 0.11
D3LR_15MIN_THRESHOLD = 0.06
SINGLE_TREND_THRESHOLD = 0.03

FLAG_CANCEL_THRESHOLD = 0.02  # 拐头flag取消条件，6分钟差值反向超过门限
FLAG_SET_THRESHOLD = 0.04  # 拐头flag设置条件，6分钟差值超过门
FLAG_NO = 0
FLAG_POS = 1
FLAG_NEG = -1

STAGE_A1_D3LR_MIN = 15
STAGE_A1_YCL_MIN = 10
STAGE_A1_YCL_MAX = 20
STAGE_A1_D3LR_THRESHOLD1 = 0.06 # 0.08 to 0.06
STAGE_A1_D3LR_THRESHOLD2 = 0.11 # 0.12 to 0.11
STAGE_A1_YCL_THRESHOLD1 = 0.80  # 8/1 提高到0.55
STAGE_A1_YCL_THRESHOLD2 = 1.10
STAGE_A1_YCL_THRESHOLD3 = 0.45  # 10/8 减低到0.45
STAGE_A2_THIS_THRESHOLD = 0.03
STAGE_B_THIS_THRESHOLD = 0.05 # 0.08 to 0.07 0.06
STAGE_B_CHANGE_THRESHOLD = 0.07


STAGE_B_CHANGE_THRESHOLD3 = 0.02
STAGE_C_ACTION = 0.3
D2TR_THRESHOLD = 0 # 0.01 -> 0
D2TR_THRESHOLD2 = 0.05
# YCL规避阈值
YCL_AVOID_THRESHOLD = 0.36
YCL_AVOID_THRESHOLD2 = 0.15
D3LR_AVOID_THRESHOLD = 0.02
# 调整量阈值
ADJUST_THRESHOLD = 0

ARTIFICIAL_AVOID_MINUTE = 8

YCL_LIMIT_LOW = 1039
YCL_LIMIT_HIGH = 1043.5

YCL_LIMIT_LOW_LOW = 1034
YCL_LIMIT_HIGH_HIGH = 1047
YCL_LIMIT_D3LR_10MIN_DELTA = 0.02
D3LR_LIMIT_HIGH = 1470
D3LR_LIMIT_LOW = 1468
CENTER_ENABLE = 0
YCL_LIMIT_ENABLE = 1

YCL_10MIN_FAST_THRESHOLD = 0.9

JWD_LEVEL1 = 0.5
JWD_LEVEL2 = 0.6
JWD_LEVEL3 = 0.8

HALF_HOUR_OPENING = 1
ONE_HOUR_OPENING = 2

OPENING_SUPPLEMENT1 = 0.2
OPENING_SUPPLEMENT2 = 0
OPENING_SUPPLEMENT3 = 0
CENTER_OPENING1 = 0.2
CENTER_OPENING2 = 0.1

SWITCH_ARTIFICIAL = 0
# 20241014
LAILIAO_THRESHOLD1 = 0.1
LAILIAO_THRESHOLD2 = 0.2
LAILIAO_THRESHOLD3 = 0.3
LAILIAO_LEVEL1 = 0.1
LAILIAO_LEVEL2 = 0.2
LAILIAO_LEVEL3 = 0.3
D3LR_15MIN_FAST_ADJUST = 0.6
STAGE_B_CHANGE_THRESHOLD2 = 0.03
STAGE_B_ACTION_BACK_THRESHOLD = 0.03

YCL_30MIN_FAST_CHANGE = 1.3
YCL_40MIN_FAST_CHANGE = 1.07
YCL_50MIN_FAST_CHANGE = 1.07
YCL_FAST_CHANGE_ACTION = 0.1

# 20241022 中心值温度
TEMP_BUTTON = 0
MEAN_TEMP_BUTTON = 0
D3LR_TARGET_TEMP = 1470.2
D3LR_TEMP_THRESHOLD = 0.38
D3LR_TEMP_THRESHOLD2 = 0.2
TEMP_LEVEL1 = 0.3
TEMP_MAX = 0.8
TARGET_TEMP_SUPPLEMENT1 = 0.1
CENTER_BUTTON = 1
D3LR_CENTER_THRESHOLD = 0.06

# 阈值偏差
THRESHOLD_BIAS = 0.3

# 电流限幅
CURRENT_LIMIT_UP = 32
CURRENT_LIMIT_DOWN = 21
CURRENT_THRESHOLD = 0

class Fxxk:
    outer_delta = None  # 使用类来操作对外暴露的变量，保证外部能访问到新的值
    d_ds_data = []


outer = Fxxk()


def centered_guaidian(data: List[dict], time_diff: Optional[float] = 15):
    df = pd.DataFrame(data)
    if df.empty:
        return None
    peaks, _ = find_peaks(df['value'])
    troughs, _ = find_peaks(-df['value'])
    turning_points = np.sort(np.concatenate((peaks, troughs)))

    filtered_turning_points = []
    last_turning_point = None

    for point in turning_points:
        if last_turning_point is None or (
                get_time(df['time'][point]) - get_time(
            df['time'][last_turning_point])).total_seconds() / 60 > time_diff:
            filtered_turning_points.append(point)
            last_turning_point = point

    slopes = []
    for point in filtered_turning_points:
        if point >= 2 and point <= len(df) - 2:  # ensure enough data points on both sides
            slopes.append((df['time'][point], df['value'][point]))

    if slopes:
        return slopes[-1]
    return None


def ycl_pre(data):
    # 去重
    unique_data = []
    for row in data:
        time = row["time"]
        value = float(row["value"])
        if not unique_data or abs(value - float(unique_data[-1]["value"])) > 0.00001:
            unique_data.append({"time": get_time_str(get_time(time)), "value": value})
    return unique_data


def get_config(alarm_rule_id):
    global STAGE_C_VALUE_THRESHOLD, LIMIT_TIME, YCL_CHECK_MIN, YCL_CHECK_THRESHOLD
    global D3LR_CONTINUE_THRESHOLD1, D3LR_CONTINUE_THRESHOLD2, D3LR_FAST_MIN, D3LR_FAST_THRESHOLD
    global STAGE_A1_D3LR_MIN, STAGE_A1_YCL_MIN, STAGE_A1_D3LR_THRESHOLD1, STAGE_A1_D3LR_THRESHOLD2
    global STAGE_A1_YCL_THRESHOLD1, STAGE_A1_YCL_THRESHOLD2, STAGE_A1_YCL_THRESHOLD3
    global STAGE_B_THIS_THRESHOLD, STAGE_B_CHANGE_THRESHOLD, STAGE_B_CHANGE_THRESHOLD2
    global STAGE_C_ACTION, D2TR_THRESHOLD, D2TR_THRESHOLD2, JWD_LEVEL1, JWD_LEVEL2, JWD_LEVEL3
    global ARTIFICIAL_AVOID_MINUTE, HALF_HOUR_OPENING, D3LR_LIMIT_HIGH, D3LR_LIMIT_LOW, CENTER_OPENING1, CENTER_OPENING2
    global OPENING_SUPPLEMENT1, OPENING_SUPPLEMENT2, SWITCH_ARTIFICIAL, CENTER_ENABLE, OPENING_SUPPLEMENT3, YCL_LIMIT_ENABLE
    global YCL_LIMIT_LOW, YCL_LIMIT_HIGH, YCL_10MIN_FAST_THRESHOLD, LAILIAO_THRESHOLD1, LAILIAO_THRESHOLD2, LAILIAO_THRESHOLD3
    global D3LR_15MIN_FAST_ADJUST, LAILIAO_LEVEL1, LAILIAO_LEVEL2, LAILIAO_LEVEL3, YCL_AVOID_THRESHOLD, YCL_AVOID_THRESHOLD2
    global YCL_30MIN_FAST_CHANGE, YCL_40MIN_FAST_CHANGE, YCL_50MIN_FAST_CHANGE, YCL_FAST_CHANGE_ACTION
    global CURRENT_LIMIT_UP, CURRENT_LIMIT_DOWN, CURRENT_THRESHOLD, TEMP_BUTTON, MEAN_TEMP_BUTTON, D3LR_TARGET_TEMP, D3LR_TARGET_TEMP, D3LR_TEMP_THRESHOLD
    global TEMP_LEVEL1, TEMP_MAX
    global THRESHOLD_BIAS, CENTER_BUTTON, TARGET_TEMP_SUPPLEMENT1, D3LR_CENTER_THRESHOLD, STAGE_B_ACTION_BACK_THRESHOLD
    config_result = mysql_conn.query_config_by_alarm_rule_id(alarm_rule_id)
    config = config_result.get('降温段', {})

    if 'stage_c_value_threshold' in config:
        STAGE_C_VALUE_THRESHOLD = int(config['stage_c_value_threshold'] * 1000)
    LIMIT_TIME = config.get('程序退避时间', LIMIT_TIME)
    # YCL_CHECK_MIN = config.get('引出量检查时间', YCL_CHECK_MIN)
    # YCL_CHECK_THRESHOLD = config.get('引出量检查阈值', YCL_CHECK_THRESHOLD)
    D3LR_CONTINUE_THRESHOLD1 = config.get('SJ_d3lr拉拐阈值一', D3LR_CONTINUE_THRESHOLD1)
    D3LR_CONTINUE_THRESHOLD2 = config.get('SJ_d3lr拉拐阈值二', D3LR_CONTINUE_THRESHOLD2)
    D3LR_FAST_MIN = config.get('d3lr快速变化时长', D3LR_FAST_MIN)
    D3LR_FAST_THRESHOLD = config.get('SJ_d3lr快速变化阈值', D3LR_FAST_THRESHOLD)
    STAGE_A1_D3LR_MIN = config.get('d3lr场景一阈值间隔', STAGE_A1_D3LR_MIN)
    STAGE_A1_YCL_MIN = config.get('ycl场景一阈值间隔', STAGE_A1_YCL_MIN)
    STAGE_A1_D3LR_THRESHOLD1 = config.get('SJ_d3lr场景a1阈值一', STAGE_A1_D3LR_THRESHOLD1)
    STAGE_A1_D3LR_THRESHOLD2 = config.get('SJ_d3lr场景a1阈值二', STAGE_A1_D3LR_THRESHOLD2)
    STAGE_A1_YCL_THRESHOLD1 = config.get('SJ_ycl场景a1阈值一', STAGE_A1_YCL_THRESHOLD1)
    STAGE_A1_YCL_THRESHOLD2 = config.get('SJ_ycl场景a1阈值二', STAGE_A1_YCL_THRESHOLD2)
    STAGE_A1_YCL_THRESHOLD3 = config.get('SJ_ycl场景a1阈值三', STAGE_A1_YCL_THRESHOLD3)
    STAGE_B_THIS_THRESHOLD = config.get('SJ_d3lr场景b阈值', STAGE_B_THIS_THRESHOLD)
    STAGE_B_CHANGE_THRESHOLD = config.get('SJ_d3lr场景b阈值差值一', STAGE_B_CHANGE_THRESHOLD)
    STAGE_B_CHANGE_THRESHOLD2 = config.get('SJ_d3lr场景b阈值差值二', STAGE_B_CHANGE_THRESHOLD2)
    STAGE_B_ACTION_BACK_THRESHOLD = config.get('SJ_d3lr场景b动作回调', STAGE_B_ACTION_BACK_THRESHOLD)
    STAGE_C_ACTION = config.get('场景C动作', STAGE_C_ACTION)
    D2TR_THRESHOLD = config.get('SJ_d2tr阈值一', D2TR_THRESHOLD)
    D2TR_THRESHOLD2 = config.get('SJ_d2tr阈值二', D2TR_THRESHOLD2)
    ARTIFICIAL_AVOID_MINUTE = config.get('人工退避时间', ARTIFICIAL_AVOID_MINUTE)
    JWD_LEVEL1 = config.get('LD_降温段力度一', JWD_LEVEL1)
    JWD_LEVEL2 = config.get('LD_降温段力度二', JWD_LEVEL2)
    JWD_LEVEL3 = config.get('LD_降温段力度三', JWD_LEVEL3)
    HALF_HOUR_OPENING = config.get('半小时开度保护', HALF_HOUR_OPENING)
    D3LR_LIMIT_HIGH = config.get('GY_d3lr上限', D3LR_LIMIT_HIGH)
    D3LR_LIMIT_LOW = config.get('GY_d3lr下限', D3LR_LIMIT_LOW)
    CENTER_OPENING1 = config.get('GY_中心调控1', CENTER_OPENING1)
    CENTER_OPENING2 = config.get('GY_中心调控2', CENTER_OPENING2)
    YCL_LIMIT_ENABLE = config.get('YCL力度差开关', YCL_LIMIT_ENABLE)
    OPENING_SUPPLEMENT1 = config.get('LD_高位动作补偿1', OPENING_SUPPLEMENT1)
    OPENING_SUPPLEMENT2 = config.get('LD_高位动作补偿2', OPENING_SUPPLEMENT2)
    OPENING_SUPPLEMENT3 = config.get('LD_高位动作补偿3', OPENING_SUPPLEMENT3)
    SWITCH_ARTIFICIAL = config.get('是否启用人工退避', SWITCH_ARTIFICIAL)
    CENTER_ENABLE = config.get('中心值开关', 0)
    YCL_LIMIT_LOW = config.get('GY_引出量下限', YCL_LIMIT_LOW)
    YCL_LIMIT_HIGH = config.get('GY_引出量上限', YCL_LIMIT_HIGH)
    YCL_10MIN_FAST_THRESHOLD = config.get('SJ_YCL十分钟快速变化', YCL_10MIN_FAST_THRESHOLD)
    LAILIAO_THRESHOLD1 = config.get('SJ_来料第一阈值', LAILIAO_THRESHOLD1)
    LAILIAO_THRESHOLD2 = config.get('SJ_来料第二阈值', LAILIAO_THRESHOLD2)
    LAILIAO_THRESHOLD3 = config.get('SJ_来料第三阈值', LAILIAO_THRESHOLD3)
    D3LR_15MIN_FAST_ADJUST = config.get('LD_d3lr十五分钟快速调整', D3LR_15MIN_FAST_ADJUST)
    LAILIAO_LEVEL1 = config.get('LD_来料力度1', LAILIAO_LEVEL1)
    LAILIAO_LEVEL2 = config.get('LD_来料力度2', LAILIAO_LEVEL2)
    LAILIAO_LEVEL3 = config.get('LD_来料力度3', LAILIAO_LEVEL3)
    YCL_AVOID_THRESHOLD = config.get('SJ_YCL对冲退避阈值一', YCL_AVOID_THRESHOLD)
    YCL_AVOID_THRESHOLD2 = config.get('SJ_YCL对冲退避阈值二', YCL_AVOID_THRESHOLD2)
    YCL_30MIN_FAST_CHANGE = config.get('SJ_YCL三十分钟变化量', YCL_30MIN_FAST_CHANGE)
    YCL_40MIN_FAST_CHANGE = config.get('SJ_YCL四十分钟变化量', YCL_40MIN_FAST_CHANGE)
    YCL_50MIN_FAST_CHANGE = config.get('SJ_YCL五十分钟变化量', YCL_50MIN_FAST_CHANGE)
    YCL_FAST_CHANGE_ACTION = config.get('LD_YCL快速变化补偿力度', YCL_FAST_CHANGE_ACTION)
    CURRENT_LIMIT_UP = config.get('GY_电流限幅上限', CURRENT_LIMIT_UP)
    CURRENT_LIMIT_DOWN = config.get('GY_电流限幅下限', CURRENT_LIMIT_DOWN)
    CURRENT_THRESHOLD = config.get('GY_电流限幅阈值', CURRENT_THRESHOLD)
    TEMP_BUTTON = config.get("温度设定值开关", TEMP_BUTTON)
    MEAN_TEMP_BUTTON = config.get("温度中位数开关", MEAN_TEMP_BUTTON)
    D3LR_TARGET_TEMP = config.get("人工设定值", D3LR_TARGET_TEMP)
    D3LR_TEMP_THRESHOLD = config.get("SJ_温度阈值", D3LR_TEMP_THRESHOLD)
    TEMP_LEVEL1 = config.get("LD_温度调控基础力度", TEMP_LEVEL1)
    TEMP_MAX = config.get("设定温度差", TEMP_MAX)
    # 中心值回拉
    THRESHOLD_BIAS = config.get("中心温度偏差", THRESHOLD_BIAS)
    CENTER_BUTTON = config.get("中心温度调整开关", CENTER_BUTTON)
    TARGET_TEMP_SUPPLEMENT1 = config.get("目标温度力度补偿", TARGET_TEMP_SUPPLEMENT1)
    D3LR_CENTER_THRESHOLD = config.get("SJ_中心温度阈值", D3LR_CENTER_THRESHOLD)
    print(config)
    return config


def is_avoid(this_action, d_ds_data):
    # 检测近n分钟内是否有同向的调整
    # 获取最近20分钟内调整
    avoid_by_hist = False
    if this_action > 0:
        hist_delta = d_ds_data[-1] - np.min(d_ds_data)
        if hist_delta > 0.2:
            avoid_by_hist = True
    else:
        hist_delta = d_ds_data[-1] - np.max(d_ds_data)
        if hist_delta < -0.2:
            avoid_by_hist = True
    return avoid_by_hist


def is_acceptable(cur_ycl, ycl_state_minor, this_action, this_delta_10min):
    if this_action > 0:
        if cur_ycl >= YCL_LIMIT_HIGH and this_delta_10min > -YCL_LIMIT_D3LR_10MIN_DELTA:
            return False
    elif this_action < 0:
        if cur_ycl <= YCL_LIMIT_LOW and this_delta_10min < YCL_LIMIT_D3LR_10MIN_DELTA:
            return False
    return True


def check_ycl_direction(check_time, ycl_data, direction_up):
    # TODO 改成基于20分钟差值+阈值，防止意外的情况统一用差值
    time_ycl = pd.Series([pd.Timestamp(item["time"]) for item in ycl_data])
    v_ycl = pd.Series([float(item["value"]) for item in ycl_data])
    time1 = check_time - pd.Timedelta(seconds=60 * 3 + 5)
    time2 = check_time - pd.Timedelta(seconds=60 * YCL_CHECK_MIN - 5)
    time3 = check_time - pd.Timedelta(seconds=60 * (YCL_CHECK_MIN + 3) + 5)

    mask1 = (time_ycl >= time1) & (time_ycl <= check_time)
    mask2 = (time_ycl >= time3) & (time_ycl <= time2)
    avg_value1 = v_ycl[mask1].mean()
    avg_value2 = v_ycl[mask2].mean()
    ycl_delta = avg_value1 - avg_value2
    if direction_up:
        return ycl_delta >= -YCL_CHECK_THRESHOLD
    else:
        return ycl_delta <= YCL_CHECK_THRESHOLD


def check_data_change(check_time, data, direction_up, time_min, value_threshold):
    # TODO 改成基于20分钟差值+阈值，防止意外的情况统一用差值
    data_time = pd.Series([pd.Timestamp(item["time"]) for item in data])
    data_value = pd.Series([float(item["value"]) for item in data])
    time1 = check_time - pd.Timedelta(seconds=60 * 3 + 5)
    time2 = check_time - pd.Timedelta(seconds=60 * time_min - 5)
    time3 = check_time - pd.Timedelta(seconds=60 * (time_min + 3) + 5)

    mask1 = (data_time >= time1) & (data_time <= check_time)
    mask2 = (data_time >= time3) & (data_time <= time2)
    avg_value1 = round(data_value[mask1].mean(), 2)
    avg_value2 = round(data_value[mask2].mean(), 2)
    value_delta = avg_value1 - avg_value2
    print(f"JWD value before={avg_value2}, after={avg_value1}, delta={value_delta}")
    if direction_up:
        return value_delta >= value_threshold
    else:
        return value_delta <= -value_threshold


def get_mean(data, end_time):
    before_time = end_time - datetime.timedelta(seconds=60 * 3 + 10)
    end_time = end_time + datetime.timedelta(seconds=10)
    before_time = get_time_str(before_time)
    end_time = get_time_str(end_time)
    values = np.array([float(item["value"]) for item in data if before_time <= item["time"] <= end_time])
    return round(np.mean(values), 2)


def get_one_hour_mean(data, end_time):
    before_time = end_time - datetime.timedelta(hours=1)
    end_time = end_time + datetime.timedelta(seconds=10)
    before_time = get_time_str(before_time)
    end_time = get_time_str(end_time)
    values = np.array([float(item["value"]) for item in data if before_time <= item["time"] <= end_time])
    return round(np.mean(values), 2)


def get_real(data, end_time):
    before_time = end_time - datetime.timedelta(seconds=120)
    end_time = end_time + datetime.timedelta(seconds=10)
    before_time = get_time_str(before_time)
    end_time = get_time_str(end_time)
    values = np.array([float(item["value"]) for item in data if before_time <= item["time"] <= end_time])
    return round(np.mean(values), 2)


def get_ycl_data(current_time):
    ycl_data = get_data("9", "YCL.UNIQUE",
                        get_time_str(current_time - datetime.timedelta(minutes=60)),
                        get_time_str(current_time + datetime.timedelta(seconds=10)))
    ycl_data = abandon_abnormal_ycl(ycl_pre(ycl_data))
    alpha = 0.142857
    ycl_data = centered_ewm(ycl_data, alpha=alpha)
    return ycl_data


def get_f1l1rb_data(current_time):
    f1l1rb_data = get_data("9", "F1L1RB",
                           get_time_str(current_time - datetime.timedelta(minutes=70)),
                           get_time_str(current_time + datetime.timedelta(seconds=10)))
    alpha = 0.142857
    f1l1rb_data = centered_ewm(f1l1rb_data, alpha=alpha)
    return f1l1rb_data


def get_d2tr_data(current_time):
    d2tr_data = get_data("9", "D2TR.UNIQUE", get_time_str(current_time - datetime.timedelta(minutes=60)),
                         get_time_str(current_time + datetime.timedelta(seconds=10)))
    alpha = 0.142857
    return centered_ewm(d2tr_data, alpha=alpha)


def is_allow_by_time(has_last_action, current_time, last_action_time, last_action, this_action):
    if has_last_action:
        if last_action * this_action > 0:
            return current_time - last_action_time > datetime.timedelta(minutes=LIMIT_TIME)
    return True


def is_opening_protect(current_time, global_result):
    """开度保护"""
    last_dds_time = default_cache.get(CONTEXT_KEY_DDS_TIME, get_time_str(current_time))
    d_ds_data = get_data('8', "D_DSPC", get_time_str(current_time - datetime.timedelta(minutes=2)),
                                get_time_str(current_time))
    dds_data = round(float(d_ds_data[-1]['value']), 2)
    last_d_ds = default_cache.get(CONTEXT_KEY_DDS, dds_data)

    if get_time(last_dds_time) == current_time:
        default_cache.set(CONTEXT_KEY_DDS_TIME, get_time_str(current_time), 1800)
        default_cache.set(CONTEXT_KEY_DDS, dds_data, 1800)
    else:
        if (get_time(last_dds_time) - current_time).seconds / 60 <= 30:
            if abs(d_ds_data - last_d_ds) > HALF_HOUR_OPENING:
                global_result['结论'] = global_result['结论'] + f' 上一次时间为{last_dds_time},开度为{last_d_ds} -- 当前时间为{current_time},开度为{d_ds_data},触发开度保护'
                return True
        # elif (get_time(last_dds_time) - get_time(current_time)).seconds / 60 < 60:
        #     if abs(d_ds_data - last_d_ds) > ONE_HOUR_OPENING:
        #         global_result[
        #             '开度保护信息'] = f'上一次时间为{last_dds_time},开度为{last_d_ds} -- 当前时间为{current_time},开度为{d_ds_data}'
        #         return True


def control_d3lr_temperature(d3lr_value, d3lr_median, global_result):
    d3lr_control = 0

    d3lr_target_temp = D3LR_TARGET_TEMP
    if MEAN_TEMP_BUTTON != 0:
        d3lr_target_temp = d3lr_median
    global_result['温度设定值debug'] = f'温度目标位{d3lr_target_temp - D3LR_TEMP_THRESHOLD} ~ {d3lr_target_temp + D3LR_TEMP_THRESHOLD}, d3lr当前温度值为{d3lr_value}'
    if d3lr_value >= d3lr_target_temp + D3LR_TEMP_THRESHOLD:
        temp_diff = d3lr_value - (d3lr_target_temp + D3LR_TEMP_THRESHOLD)
        temp_diff_percent = temp_diff / TEMP_MAX
        d3lr_control = round(-TEMP_LEVEL1 - round(TEMP_LEVEL1 * temp_diff_percent, 1), 1)
    elif d3lr_value <= d3lr_target_temp - D3LR_TEMP_THRESHOLD:
        temp_diff = (d3lr_target_temp - D3LR_TEMP_THRESHOLD) - d3lr_value
        temp_diff_percent = temp_diff / TEMP_MAX
        d3lr_control = round(TEMP_LEVEL1 + round(TEMP_LEVEL1 * temp_diff_percent, 1), 1)

    return d3lr_control


def get_temperature_median(data_list):
    # 提取所有'value'并放入一个列表中
    values = [item['value'] for item in data_list]

    # 对值进行排序
    values.sort()

    # 计算列表的长度
    n = len(values)

    # 如果元素个数为奇数，中位数是中间那个元素
    if n % 2 == 1:
        median = values[n // 2]
        # 如果元素个数为偶数，中位数是中间两个元素的平均值
    else:
        median = (values[n // 2 - 1] + values[n // 2]) / 2

    return median


def get_d3lr_temperature_mean(this_d3lr, this_ycl, d3lr_data, current_time):
    d3lr_one_hour_mean = get_one_hour_mean(d3lr_data, current_time)
    if this_ycl < YCL_LIMIT_LOW and this_d3lr < d3lr_one_hour_mean:
        target_temp = get_one_hour_mean(d3lr_data, current_time) + THRESHOLD_BIAS
    elif this_ycl > YCL_LIMIT_HIGH and this_d3lr > d3lr_one_hour_mean:
        target_temp = get_one_hour_mean(d3lr_data, current_time) - THRESHOLD_BIAS
    else:
        target_temp = get_one_hour_mean(d3lr_data, current_time)
    return target_temp


def control_d3lr_temperature_center(this_d3lr, d3lr_15min_delta, d3lr_target_temp, ycl_flag, global_result):
    d3lr_control = 0
    is_center = False

    if ycl_flag == 1:
        if this_d3lr >= d3lr_target_temp and abs(d3lr_15min_delta) < D3LR_CENTER_THRESHOLD:
            is_center = True
            temp_diff = this_d3lr - d3lr_target_temp
            temp_diff_percent = temp_diff / TEMP_MAX
            d3lr_control = round(-TEMP_LEVEL1 - round(TEMP_LEVEL1 * temp_diff_percent, 1), 1)
    else:
        if this_d3lr <= d3lr_target_temp and abs(d3lr_15min_delta) < D3LR_CENTER_THRESHOLD:
            is_center = True
            temp_diff = d3lr_target_temp - this_d3lr
            temp_diff_percent = temp_diff / TEMP_MAX
            d3lr_control = round(TEMP_LEVEL1 + round(TEMP_LEVEL1 * temp_diff_percent, 1), 1)

    if is_center:
        global_result['结论'] = global_result['结论'] + f'。 触发温度中心值调控，d3lr当前温度值为{this_d3lr}，温度目标位{d3lr_target_temp}，动作为{d3lr_control}'
    return round(d3lr_control, 1)


def do(d3lr_data, global_result):
    get_config(JWD_RULE_ID)
    # 测试使用

    alpha = 0.142857

    # 测试代码，线上需要注释掉
    # from jwd2 import test_do2
    # global_result = test_do2(d3lr_data, global_result)

    d3lr_data = centered_ewm(d3lr_data, alpha=alpha)
    d3lr_median = round(get_temperature_median(d3lr_data), 2)
    current_time = get_time(d3lr_data[-1]["time"])
    current_time_ = pd.Timestamp(current_time)
    this_d3lr = get_mean(d3lr_data, current_time)
    pre_value = round(default_cache.get(CONTEXT_KEY_PREV_VALUE, this_d3lr), 2)
    ycl_data = get_ycl_data(current_time)

    # 测试代码，线上需要注释掉
    # from jwd1 import test_do1
    # global_result = test_do1(ycl_data, global_result)

    d2tr_data = get_d2tr_data(current_time)
    d_ds_data = get_data('8', "D_DSPC", get_time_str(current_time - datetime.timedelta(minutes=LIMIT_TIME)),
                         get_time_str(current_time + datetime.timedelta(seconds=10)))
    d_ds_data = [float(item["value"]) for item in d_ds_data]

    f1l1rb_data = get_f1l1rb_data(current_time)
    this_f1l1rb = get_mean(f1l1rb_data, current_time)
    f1l1rb_1h_data = get_mean(f1l1rb_data, current_time - datetime.timedelta(hours=1))
    f1l1rb_delta = this_f1l1rb - f1l1rb_1h_data

    # d_ds_data = outer.d_ds_data
    # TODO:注释掉
    # global_result["JWD_YCLJS.VALUE"] = get_mean(ycl_data, current_time)
    this_ycl = round(global_result["JWD_YCLJS.VALUE"], 2)
    # this_ycl = get_real(ycl_data, current_time)

    print(f"JWD control new time is: {current_time_} pre_value={pre_value}, current={this_d3lr}")
    global_result['LAST_ACTION_D3LR'] = pre_value
    global_result['THIS_D3LR'] = this_d3lr
    global_result['THIS_YCL'] = this_ycl

    last_action_time = default_cache.get(CONTEXT_KEY_LAST_TIME, '')
    has_last_action = last_action_time != ''
    if has_last_action:
        last_action_time = get_time(last_action_time)
    last_action = default_cache.get(CONTEXT_KEY_LAST_ACTION, 0)
    last_action_d3lr = default_cache.get(CONTEXT_KEY_LAST_ACTION_D3LR, this_d3lr)
    total_action = float(default_cache.get(CONTEXT_KEY_TOTAL_ACTION, 0))
    print(f"JWD last_action_time: {last_action_time}, last_action: {last_action}")
    global_result['JWD_LAST_ACTION_TIME'] = f'JWD last_action_time: {last_action_time}, last_action: {last_action}'

    # TODO: 注释掉
    # global_result["JWD_YCLJS"] = '平稳'
    # global_result["JWD_YCLJS_MINOR"] = '平稳'
    # global_result["JWD_D3LR"] = '平稳'

    ycl_state = global_result["JWD_YCLJS"]
    ycl_state_minor = global_result["JWD_YCLJS_MINOR"]
    d3lr_state = global_result["JWD_D3LR"]
    d3lr_3min = get_mean(d3lr_data, current_time - datetime.timedelta(seconds=3 * 60))
    d3lr_6min = get_mean(d3lr_data, current_time - datetime.timedelta(seconds=6 * 60))
    d3lr_12min = get_mean(d3lr_data, current_time - datetime.timedelta(seconds=12 * 60))
    d3lr_10min = get_mean(d3lr_data, current_time - datetime.timedelta(seconds=10 * 60))
    d3lr_20min = get_mean(d3lr_data, current_time - datetime.timedelta(seconds=20 * 60))
    this_d2tr = get_mean(d2tr_data, current_time)
    d2tr_10min = get_mean(d2tr_data, current_time - datetime.timedelta(seconds=10 * 60))
    this_delta_3min = round(this_d3lr - d3lr_3min, 2)
    last_delta_3min = round(d3lr_6min - d3lr_3min, 2)
    this_delta_6min = round(this_d3lr - d3lr_6min, 2)
    last_delta_6min = round(d3lr_6min - d3lr_12min, 2)
    this_delta_10min = round(this_d3lr - d3lr_10min, 2)
    last_delta_10min = round(d3lr_10min - d3lr_20min, 2)
    d2tr_delta_10min = round(this_d2tr - d2tr_10min, 2)
    change_delta_3min = round(abs(this_delta_3min) - abs(last_delta_3min), 2)
    change_delta_6min = round(this_delta_6min - last_delta_6min, 2)
    d3lr_15min_delta = round(get_mean(d3lr_data, current_time) - get_mean(d3lr_data, current_time - datetime.timedelta(
        minutes=15)), 2)
    global_result["CHANGE_DELTA"] = change_delta_6min
    global_result["THIS_DELTA_6MIN"] = this_delta_6min
    global_result["LAST_DELTA_6MIN"] = last_delta_6min
    global_result["THIS_DELTA_10MIN"] = this_delta_10min
    global_result["LAST_DELTA_10MIN"] = last_delta_10min
    global_result["D2TR_DELTA_10MIN"] = d2tr_delta_10min
    global_result['guaidian_adjust'] = 0
    global_result['THIS_DELTA_3MIN'] = this_delta_3min
    global_result['CHANGE_DELTA_3MIN'] = change_delta_3min
    global_result['结论'] = ''

    print(
        f"时间：{current_time} JWDycl_state={ycl_state} d3lr_state={d3lr_state} ycl_minor={ycl_state_minor} change delta={change_delta_6min}"
        f" this_delta_6min={this_delta_6min} last_delta_6min={last_delta_6min}"
        f" this_delta_10min={this_delta_10min} last_delta_10min={last_delta_10min}"
        f" d2tr_delta_10min={d2tr_delta_10min}")

    control_d3lr = 0
    set_value = pre_value  # 初始
    do_scene = ""

    d3lr_target_temp = get_d3lr_temperature_mean(this_d3lr, this_ycl, d3lr_data, current_time)

    # TODO 记得消除flag
    continue_flag = default_cache.get(CONTEXT_KEY_CONTINUE, 0)
    global_result['当前拐点标识'] = f"JWD continue_flag={continue_flag}"
    # if stage_a_condition:
    # stage-A1
    try:
        # if continue_flag == 0:
        control_a1 = get_action_by_states_stage_a1(current_time, d3lr_data, this_ycl, ycl_data, d2tr_delta_10min, global_result)
        print(f"JWD after STAGE-A1 action={control_a1}")
        if is_allow_by_time(has_last_action, current_time, last_action_time, last_action, control_a1):
            global_result['是否触发同向调整回避'] = '否'
        else:
            global_result['是否触发同向调整回避'] = '是'
        # 防止人工调整
        if (control_a1 != 0
                and is_allow_by_time(has_last_action, current_time, last_action_time, last_action, control_a1)
                # and not is_avoid(control_a1, d_ds_data)
                and is_acceptable(this_ycl, ycl_state_minor, control_a1, this_delta_10min)):
            global_result["场景A1"] = "识别到趋势，触发调整"
            control_d3lr = control_a1
            set_value = this_d3lr
            do_scene = "A1"

            # stage-A2
        # else:  # flag不为空
        #     control_a2 = get_action_stage_a2(change_delta_6min, this_delta_6min, current_time, d3lr_data, ycl_data,
        #                                      continue_flag, last_action_d3lr, this_d3lr, d2tr_delta_10min)
        #     print(f"JWD after STAGE-A2 action={control_a2}")
        #     if (control_a2 != 0
        #             and is_allow_by_time(has_last_action, current_time, last_action_time, last_action, control_a2)
        #             # and not is_avoid(control_a2, d_ds_data)
        #             and is_acceptable(this_ycl, ycl_state_minor, control_a2, this_delta_10min)):
        #         global_result["场景A2"] = "D3LR继续变化，持续调整"
        #         control_d3lr = control_a2
        #         set_value = this_d3lr
        #         do_scene = "A2"
    except Exception as e:
        global_result['a1和a2场景程序错误'] = str(e)

    last_scene = default_cache.get(CONTEXT_KEY_LAST_SCENE, 'B')

    if control_d3lr == 0:
        # stage-B
        # control_b = get_action_stage_b(change_delta_6min, current_time, last_action, last_action_time,
        #                                this_delta_6min, global_result)
        control_b = get_action_stage_b(change_delta_3min, change_delta_6min, current_time, last_action, last_action_time,
                                       this_delta_6min, global_result)
        if control_b != 0 and is_acceptable(this_ycl, ycl_state_minor, control_b, this_delta_10min) and last_scene != 'B':
            global_result["场景B"] = "D3LR调整后继续变化，追加动作"
            control_d3lr = control_b
            set_value = this_d3lr
            do_scene = "B"

    # stage-C
    if control_d3lr == 0:
        control_c, stage_c_set_value = get_action_by_pos_stage_c(this_d3lr, current_time, global_result, pre_value,
                                                                 ycl_data)
        print(f"JWD after STAGE-C action={control_c}")
        if (control_c != 0
                and not is_avoid(control_c, d_ds_data)
                and is_acceptable(this_ycl, ycl_state_minor, control_c, this_delta_10min)
                and is_allow_by_time(has_last_action, current_time, last_action_time, last_action, control_c)):
            control_d3lr = control_c
            set_value = stage_c_set_value
            do_scene = "C"

    # increment = add_action_by_ycl(last_action, control_d3lr, this_d3lr, d3lr_data, this_ycl, ycl_data, current_time,
    #                               global_result)
    # print(f"{current_time} JWD after increment={increment}")
    # if increment != 0:
    #     # 在YCL快速变化时 以YCL对应的调整量为主
    #     if abs(control_d3lr) < abs(increment):
    #         control_d3lr = increment
    #     do_scene = "D"

    # try:
    #     # 场景E，连续一个小时趋势下降或上升
    #     single_action = ycl_single_trend(current_time, d3lr_data)
    #     if (control_d3lr == 0 and is_allow_by_time(has_last_action, current_time, last_action_time, last_action,
    #                                                single_action)
    #             and is_acceptable(this_ycl, ycl_state_minor, single_action, this_delta_10min)):
    #         print(f"场景E，action{single_action}")
    #         control_d3lr = single_action
    #         do_scene = "E"
    # except Exception as e:
    #     global_result['程序出错'] = str(e)

    try:
        if CENTER_BUTTON != 0:
            if control_d3lr == 0 and (this_ycl < YCL_LIMIT_LOW or this_ycl > YCL_LIMIT_HIGH):
                if this_ycl < YCL_LIMIT_LOW:
                    ycl_flag = -1
                else:
                    ycl_flag = 1
                global_result['温度调控debug'] = f'当前d3lr为{this_d3lr}, d3lr目标温度位{d3lr_target_temp}'
                action = control_d3lr_temperature_center(this_d3lr, d3lr_15min_delta, d3lr_target_temp, ycl_flag, global_result)
                if is_allow_by_time(has_last_action, current_time, last_action_time, last_action, action):
                    global_result['结论'] = global_result['结论'] + f' 触发温度中心值调控，当前d3lr为调控值为{this_d3lr}, d3lr目标温度位{d3lr_target_temp}，动作为{action}。'
                    control_d3lr = action
                    do_scene = 'F'
    except Exception as e:
        global_result['温度中心值调整报错'] = str(e)

    try:
        action = fix_key_action(control_d3lr, this_d3lr, d3lr_data, this_ycl, ycl_data, f1l1rb_delta, d3lr_target_temp, current_time, global_result)
        if is_allow_by_time(has_last_action, current_time, last_action_time, last_action, action):
            global_result['是否触发同向调整回避'] = '否'
        else:
            global_result['是否触发同向调整回避'] = '是'
        if (action != control_d3lr and
                is_allow_by_time(has_last_action, current_time, last_action_time, last_action,
                                                   action)):
            print(f"动作修正,action {action}")
            global_result['触发阈值线下调整保护'] = f'控制值为{control_d3lr}，修改值为{action}'
            control_d3lr = action
            do_scene = 'E'
        elif action != control_d3lr and action == 0:
            print(f"动作修正,action {action}")
            global_result['触发阈值线下调整保护'] = f'控制值为{control_d3lr}，修改值为{action}'
            control_d3lr = action
            do_scene = 'E'

    except Exception as e:
        global_result['程序出错'] = str(e)

    try:
        if TEMP_BUTTON != 0:
            control_d3lr = control_d3lr_temperature(this_d3lr, d3lr_median, global_result)
            if is_allow_by_time(has_last_action, current_time, last_action_time, last_action, control_d3lr) and not is_opening_protect(current_time, global_result):
                global_result['结论'] = global_result['结论'] + f"。 触发温度设定值调控，调控力度位{control_d3lr}"
                do_scene = 'G'
            else:
                control_d3lr = 0
                global_result['结论'] = global_result['结论'] + ', 触发开度保护或同向退避逻辑'
    except Exception as e:
        global_result['基于温度设定值调控报错'] = str(e)

    global_result["do_scene"] = do_scene

    # 电流安全限幅检查
    CURRENT_ATTR = "PC2_D_DS.CURRENT.PV"
    action_before_current_safety = control_d3lr
    is_safety = True
    if control_d3lr != 0:
        current_data = get_data('7', CURRENT_ATTR, get_time_str(current_time - datetime.timedelta(minutes=5)),
                                get_time_str(current_time))
        current_value = float(current_data[-1]['value'])
        if CURRENT_LIMIT_DOWN + CURRENT_THRESHOLD < current_value < CURRENT_LIMIT_UP - CURRENT_THRESHOLD:
            pass
        elif current_value > CURRENT_LIMIT_UP:
            if control_d3lr > 0:
                is_safety = False
                control_d3lr = 0
        elif current_value < CURRENT_LIMIT_DOWN:
            if control_d3lr < 0:
                is_safety = False
                control_d3lr = 0
        if not is_safety:
            global_result[
                "电流安全"] = f"JWD 当前一次电流为{current_value}，原先动作为{action_before_current_safety}，限幅后动作为{control_d3lr}"

    # 力度调整
    try:
        if YCL_LIMIT_ENABLE != 0:
            current_control_d3lr = control_d3lr
            if get_mean(ycl_data, current_time) >= YCL_LIMIT_HIGH:
                if control_d3lr < 0:
                    control_d3lr = control_d3lr - OPENING_SUPPLEMENT1
                elif control_d3lr > 0:
                    control_d3lr = control_d3lr - OPENING_SUPPLEMENT2
            elif get_mean(ycl_data, current_time) <= YCL_LIMIT_LOW:
                if control_d3lr < 0:
                    control_d3lr = control_d3lr + OPENING_SUPPLEMENT2
                elif control_d3lr > 0:
                    control_d3lr = control_d3lr + OPENING_SUPPLEMENT1
            elif YCL_LIMIT_LOW < get_mean(ycl_data, current_time) < YCL_LIMIT_HIGH:
                if control_d3lr < 0:
                    control_d3lr = control_d3lr + OPENING_SUPPLEMENT3
                elif control_d3lr > 0:
                    control_d3lr = control_d3lr + OPENING_SUPPLEMENT3

            if current_control_d3lr != control_d3lr:
                global_result['触发力度调整'] = f'将力度{current_control_d3lr}, 改为{control_d3lr}'
    except Exception as e:
        global_result['力度调整出错'] = str(e)

    try:
        if CENTER_ENABLE == 1:
            current_control_d3lr = control_d3lr
            if get_mean(d3lr_data, current_time) >= D3LR_LIMIT_HIGH:
                if control_d3lr < 0:
                    control_d3lr = control_d3lr - CENTER_OPENING1
                elif control_d3lr > 0:
                    control_d3lr = control_d3lr - CENTER_OPENING2
            elif get_mean(d3lr_data, current_time) <= D3LR_LIMIT_LOW:
                if control_d3lr < 0:
                    control_d3lr = control_d3lr + CENTER_OPENING2
                elif control_d3lr > 0:
                    control_d3lr = control_d3lr + CENTER_OPENING1
            else:
                if control_d3lr < 0:
                    control_d3lr = control_d3lr
                elif control_d3lr > 0:
                    control_d3lr = control_d3lr
            if current_control_d3lr != control_d3lr:
                global_result['触发中心线回位调整'] = f'将力度{current_control_d3lr}, 改为{control_d3lr}'
    except Exception as e:
        global_result['中心线调整出错'] = str(e)

    # 开度保护
    try:
        if is_opening_protect(current_time, global_result):
            global_result['触发开度保护退避'] = f'应调整{control_d3lr}, 开度修改后为0'
            control_d3lr = 0
    except Exception as e:
        global_result['开度保护报错'] = str(e)

    # 记录当下开度
    try:
        if SWITCH_ARTIFICIAL != 0:
            dds_data, is_artificial_control = get_artificial_control(current_time, global_result)
            if is_artificial_control:
                global_result["人工操作退避"] = f"发生人工干预，本次不调，原先动作为{control_d3lr}"
                control_d3lr = 0

            dds_after_this = dds_data + control_d3lr
            global_result["DDS_AFTER_THIS"] = dds_after_this
            default_cache.set('DDS_AFTER_THIS', dds_after_this, TTL)
    except Exception as e:
        print("get dds after excp", e)

    if control_d3lr != 0:  # update context
        total_action = total_action + control_d3lr
        print(f"JWD current_time={current_time}, do_scene={do_scene}, total_action={total_action}")
        global_result['action_context'] = f'JWD current_time={current_time}, do_scene={do_scene}, total_action={total_action}'
        default_cache.set(CONTEXT_KEY_TOTAL_ACTION, total_action, TTL)
        if do_scene == "A1" or do_scene == "A2" or do_scene == "E" or do_scene == "B" or do_scene == 'G' or do_scene == 'F':
            default_cache.set(CONTEXT_KEY_LAST_TIME, get_time_str(current_time), TTL)
            default_cache.set(CONTEXT_KEY_LAST_ACTION, control_d3lr, TTL)
            default_cache.set(CONTEXT_KEY_LAST_ACTION_D3LR, this_d3lr, TTL)
            default_cache.set(CONTEXT_KEY_LAST_SCENE, do_scene, TTL)
    default_cache.set(CONTEXT_KEY_PREV_VALUE, set_value, TTL)

    # 结果输出
    global_result[ALIAS] = control_d3lr
    outer.outer_delta = control_d3lr

    # 最后一步，设置或清空flag
    if continue_flag == FLAG_POS:
        if this_delta_6min >= FLAG_CANCEL_THRESHOLD:
            continue_flag = 0
    elif continue_flag == FLAG_NEG:
        if this_delta_6min <= -FLAG_CANCEL_THRESHOLD:
            continue_flag = 0
    elif continue_flag == FLAG_NO:
        if last_action > 0 and this_d3lr < last_action_d3lr and this_delta_6min <= -FLAG_SET_THRESHOLD:
            continue_flag = FLAG_POS
        elif last_action < 0 and this_d3lr > last_action_d3lr and this_delta_6min >= FLAG_SET_THRESHOLD:
            continue_flag = FLAG_NEG
    default_cache.set(CONTEXT_KEY_CONTINUE, continue_flag, TTL)
    global_result["NEW_FLAG"] = continue_flag


def get_artificial_control(current_time, global_result):
    is_artificial_control = False
    history_dds_data = get_data('8', "D_DSPC", get_time_str(current_time - datetime.timedelta(minutes=2)),
                                get_time_str(current_time))
    dds_data = round(float(history_dds_data[-1]['value']), 2)
    dds_after_last_action = default_cache.get('DDS_AFTER_THIS', dds_data)
    global_result['人工退避debug'] = f'当前开度为{dds_data}，上次动作后为{dds_after_last_action}'
    if abs(dds_after_last_action - dds_data) >= 0.2:
        is_artificial_control = True
    if is_artificial_control:
        default_cache.set("JWD_ARTIFICIAL_CONTROL", True, ARTIFICIAL_AVOID_MINUTE * 60)
    else:
        is_artificial_control = default_cache.get("JWD_ARTIFICIAL_CONTROL", False)
    return dds_data, is_artificial_control


def find_last_peak(data, window=None, min_distance=None, min_height=None, prominence=None):
    # 使用find_peaks函数查找峰值
    peaks, _ = find_peaks(data,
                          distance=min_distance,
                          height=min_height,
                          prominence=prominence,
                          width=window)
    if len(peaks) > 0:
        return peaks[-1]
    else:
        return None


def find_ycl_turning_point(ycl_filtered_values):
    window = 8
    min_distance = 40
    peak_ = find_last_peak(ycl_filtered_values, window=window, min_distance=min_distance)
    valley_ = find_last_peak(-ycl_filtered_values, window=window, min_distance=min_distance)
    if peak_ and valley_:
        return max(peak_, valley_)
    elif peak_:
        return peak_
    elif valley_:
        return valley_
    else:
        return None


def get_action_by_states_stage_a1(current_time, d3lr_data, this_ycl, ycl_data, d2tr_delta_10min, global_result):
    # A1阶段
    control_d3lr = 0
    # TODO 看15min差值 改为如果拐点在15min以内 看拐点到现在的差值
    d3lr_df = pd.DataFrame(data=d3lr_data)
    d3lr_values = d3lr_df.iloc[:, 1]
    d3lr_turning_index = find_ycl_turning_point(d3lr_values)
    if not d3lr_turning_index:
        d3lr_turning_index = -31

    # TODO: 注释掉
    # d3lr_turning_index = 0
    print(f'd3lr_turning_index: {d3lr_turning_index}')
    guai_dian_time, guai_dian_value = ycl_data[d3lr_turning_index]['time'], ycl_data[d3lr_turning_index]['value']
    global_result["D3LR拐点时间"] = guai_dian_time
    global_result["D3LR拐点值"] = guai_dian_value

    guai_dian_time = get_time(guai_dian_time)
    delta_minutes = current_time - guai_dian_time

    if delta_minutes >= datetime.timedelta(minutes=STAGE_A1_D3LR_MIN):
        d3lr_delta = round(get_mean(d3lr_data, current_time) - get_mean(d3lr_data, current_time - datetime.timedelta(
            minutes=STAGE_A1_D3LR_MIN)), 2)
    elif delta_minutes >= datetime.timedelta(minutes=6):
        # 把拐点到现在的值进行15min折算 * 系数0.8（防止过于灵敏
        if delta_minutes >= datetime.timedelta(minutes=10):
            coefficient = STAGE_A1_D3LR_MIN / (delta_minutes.seconds / 60)
        else:
            coefficient = STAGE_A1_D3LR_MIN / (delta_minutes.seconds / 60) * 0.9
        d3lr_delta = round((get_mean(d3lr_data, current_time) - get_mean(d3lr_data, guai_dian_time)) * coefficient, 2)
    else:
        d3lr_delta = 0
        global_result['场景A1'] = '拐点在6min钟以内，退避等待！'
    global_result['d3lr_15min_delta'] = d3lr_delta
    ycl_delta = round(this_ycl - get_mean(ycl_data,
                                                    current_time - datetime.timedelta(minutes=STAGE_A1_YCL_MIN)),
        2)
    print(f"JWD A1 ycl_delta={ycl_delta}, d3lr_delta={d3lr_delta}")
    adjust_threshold = ADJUST_THRESHOLD
    if ycl_delta * d3lr_delta < 0:
         adjust_threshold = 0.02

    global_result['根据ycl修正后的阈值为'] = f'a1场景原阈值为{STAGE_A1_D3LR_THRESHOLD1},修正后的阈值为{STAGE_A1_D3LR_THRESHOLD1} + {adjust_threshold}'
    if -STAGE_A1_D3LR_THRESHOLD1 <= d3lr_delta < STAGE_A1_D3LR_THRESHOLD1 + adjust_threshold:
        global_result['结论'] = global_result['结论'] + f'15分钟d3lr不满足阈值{-STAGE_A1_D3LR_THRESHOLD1}, {STAGE_A1_D3LR_THRESHOLD1 + adjust_threshold}, 不触发调整'
        control_d3lr = 0
    elif STAGE_A1_D3LR_THRESHOLD1 + adjust_threshold <= d3lr_delta < STAGE_A1_D3LR_THRESHOLD2 + adjust_threshold:
        if ycl_delta <= -STAGE_A1_YCL_THRESHOLD3:
            global_result['结论'] = global_result['结论'] + f'15分钟d3lr满足阈值>={STAGE_A1_D3LR_THRESHOLD1 + adjust_threshold}，<{STAGE_A1_D3LR_THRESHOLD2 + adjust_threshold}, ycl<={-STAGE_A1_YCL_THRESHOLD3}, 不调整'
            control_d3lr = 0
        elif ycl_delta <= STAGE_A1_YCL_THRESHOLD1:
            control_d3lr = -JWD_LEVEL1
        else:
            control_d3lr = -JWD_LEVEL2
        if control_d3lr != 0 and d2tr_delta_10min <= D2TR_THRESHOLD:
            global_result['场景A1'] = 'd2tr变化不满足要求：d2tr_delta_10min:{d2tr_delta_10min}, 阈值：{D2TR_THRESHOLD}'
            print(f"JWD STAGE-A1 d2tr opposite direction, cancel {control_d3lr}")
            control_d3lr = 0
    elif d3lr_delta >= STAGE_A1_D3LR_THRESHOLD2 + adjust_threshold:
        if ycl_delta <= -STAGE_A1_YCL_THRESHOLD3:
            control_d3lr = 0
        elif ycl_delta <= STAGE_A1_YCL_THRESHOLD1:
            control_d3lr = -JWD_LEVEL1
        elif ycl_delta <= STAGE_A1_YCL_THRESHOLD2:
            control_d3lr = -JWD_LEVEL2
        else:
            control_d3lr = -JWD_LEVEL3
        if control_d3lr != 0 and d2tr_delta_10min <= D2TR_THRESHOLD:
            print(f"JWD STAGE-A1 d2tr opposite direction, cancel {control_d3lr}")
            control_d3lr = 0
    elif -(STAGE_A1_D3LR_THRESHOLD2 + adjust_threshold) <= d3lr_delta < -(STAGE_A1_D3LR_THRESHOLD1 + adjust_threshold):
        if ycl_delta >= STAGE_A1_YCL_THRESHOLD3:
            global_result['结论'] = global_result[
                                        '结论'] + f'15分钟d3lr满足阈值>={-(STAGE_A1_D3LR_THRESHOLD2 + adjust_threshold)}，<{-(STAGE_A1_D3LR_THRESHOLD1 + adjust_threshold)}, ycl>={STAGE_A1_YCL_THRESHOLD3}, 不调整'
            control_d3lr = 0
        elif ycl_delta >= -STAGE_A1_YCL_THRESHOLD1:
            control_d3lr = +JWD_LEVEL1
        else:
            control_d3lr = +JWD_LEVEL1
        if control_d3lr != 0 and d2tr_delta_10min >= -D2TR_THRESHOLD:
            global_result['结论'] = global_result['结论'] + f'JWD STAGE-A1 d2tr opposite direction, cancel {control_d3lr}, 不调整'
            print(f"JWD STAGE-A1 d2tr opposite direction, cancel {control_d3lr}")
            control_d3lr = 0
    elif d3lr_delta <= -(STAGE_A1_D3LR_THRESHOLD2 + adjust_threshold):
        if ycl_delta >= STAGE_A1_YCL_THRESHOLD3:
            global_result['结论'] = global_result[
                                        '结论'] + f'15分钟d3lr<={-(STAGE_A1_D3LR_THRESHOLD2 + adjust_threshold)}, ycl>={STAGE_A1_YCL_THRESHOLD3} 不调整'
            control_d3lr = 0
        elif ycl_delta >= -STAGE_A1_YCL_THRESHOLD1:
            control_d3lr = JWD_LEVEL1
        elif ycl_delta >= -STAGE_A1_YCL_THRESHOLD2:
            control_d3lr = JWD_LEVEL2
        else:
            control_d3lr = JWD_LEVEL2
        if control_d3lr != 0 and d2tr_delta_10min >= -D2TR_THRESHOLD:
            print(f"JWD STAGE-A1 d2tr opposite direction, cancel {control_d3lr}")
            global_result['结论'] = global_result['结论'] + f'JWD STAGE-A1 d2tr opposite direction, cancel {control_d3lr}, 不调整。'
            control_d3lr = 0

    global_result['结论'] = global_result['结论'] + f'，经过a1场景判断后，动作位{control_d3lr}。'
    return control_d3lr


def get_action_stage_a2(change_delta, this_delta_6min, current_time, d3lr_data, ycl_data, continue_flag,
                        last_action_d3lr, this_d3lr, d2tr_delta_10min):
    control_d3lr = 0
    use = True
    # 对引出量的限制复用A1场景
    ycl_delta = round(
        get_mean(ycl_data, current_time) - get_mean(ycl_data,
                                                    current_time - datetime.timedelta(minutes=STAGE_A1_YCL_MIN)),
        2)

    print(f"JWD STAGE-A2 change_delta={change_delta}, ycl_delta={ycl_delta}")
    # TODO 参考D2TR趋势
    if use:
        # 尝试拉拐头
        if continue_flag > 0:
            # if ycl_delta >= STAGE_A1_YCL_THRESHOLD3:
            #     control_d3lr = 0
            if this_delta_6min < -D3LR_CONTINUE_THRESHOLD1:
                # TODO 根据d3lr变化量来判断追加多少
                if check_data_change(pd.Timestamp(current_time), d3lr_data, False, D3LR_FAST_MIN,
                                     D3LR_FAST_THRESHOLD):
                    control_d3lr = +JWD_LEVEL3
                else:
                    control_d3lr = +JWD_LEVEL1
            elif this_delta_6min < -D3LR_CONTINUE_THRESHOLD2:
                control_d3lr = JWD_LEVEL1
            if control_d3lr != 0 and d2tr_delta_10min >= -D2TR_THRESHOLD:
                print(f"JWD STAGE-A2 d2tr opposite direction, cancel {control_d3lr}")
                control_d3lr = 0
        elif continue_flag < 0:
            # if ycl_delta <= -STAGE_A1_YCL_THRESHOLD3:
            #     control_d3lr = 0
            if this_delta_6min > D3LR_CONTINUE_THRESHOLD1:
                if check_data_change(pd.Timestamp(current_time), d3lr_data, True, D3LR_FAST_MIN,
                                     D3LR_FAST_THRESHOLD):
                    control_d3lr = -JWD_LEVEL3
                else:
                    control_d3lr = -JWD_LEVEL1
            elif this_delta_6min > D3LR_CONTINUE_THRESHOLD2:
                control_d3lr = -JWD_LEVEL1
            if control_d3lr != 0 and d2tr_delta_10min <= D2TR_THRESHOLD:
                print(f"JWD STAGE-A2 d2tr opposite direction, cancel {control_d3lr}")
                control_d3lr = 0
    else:
        control_b = 0
        if continue_flag > 0:
            if this_delta_6min < -STAGE_B_THIS_THRESHOLD:  # 保持高速变化
                control_b = +1
            elif change_delta <= -STAGE_B_CHANGE_THRESHOLD:  # delta增加很多
                control_b = +1
            elif change_delta < -0.01:  # delta增加但变化量不大
                control_b = +0.5
            else:
                # if this_delta < -STAGE_A2_THIS_THRESHOLD:
                control_b = 0
        elif continue_flag < 0:
            if this_delta_6min > STAGE_B_THIS_THRESHOLD:  # 保持高速变化
                control_b = -1
            elif change_delta >= STAGE_B_CHANGE_THRESHOLD:  # delta增加很多
                control_b = -1
            elif change_delta > 0.01:  # delta增加但变化量不大
                control_b = -0.5
            else:
                control_b = 0

        # A2场景 增加D2TR对调整量的影响
        if (control_b == JWD_LEVEL1 or control_b == 0.5) and d2tr_delta_10min < -D2TR_THRESHOLD2:
            control_b += JWD_LEVEL1
            print(f"JWD increase action due to d2tr change")
        elif (control_b == -JWD_LEVEL1 or control_b == -0.5) and d2tr_delta_10min > D2TR_THRESHOLD2:
            control_b -= JWD_LEVEL1
            print(f"JWD increase action due to d2tr change")

        control_d3lr = control_b
    return control_d3lr


def get_action_stage_b(change_delta_3min, change_delta_6min, current_time, last_action, last_action_time, this_delta_6min, global_result):
    control_b = 0
    control_d3lr = 0
    if not last_action_time:
        global_result['场景B没有获取到上次动作时间'] = '不触发'
        return control_b
    last_delta_min = (current_time - last_action_time).total_seconds() / 60
    global_result['场景B'] = f'{last_delta_min}分钟变化量为{this_delta_6min}，两次变化差值为{change_delta_6min}'
    if 5 <= last_delta_min <= 7:
        # 调整6分钟后，决定是否要追加动作，看d3lr的10分钟差值时是否减小
        if last_action > 0:
            if this_delta_6min <= -STAGE_B_THIS_THRESHOLD:  # 保持高速变化
                if last_action < 1 and change_delta_6min <= -STAGE_B_CHANGE_THRESHOLD:
                    control_b = +1
                # elif change_delta_6min <= -STAGE_B_CHANGE_THRESHOLD:
                else:
                    control_b = +0.5
            elif change_delta_6min <= -STAGE_B_CHANGE_THRESHOLD:  # delta增加很多
                control_b = +0.5
            elif change_delta_6min <= -STAGE_B_CHANGE_THRESHOLD2:  # delta增加但变化量不大
                control_b = +0.5
            # 踩在拐点退避
            elif this_delta_6min >= STAGE_B_ACTION_BACK_THRESHOLD:
                control_b = -1 * last_action
                global_result['guaidian_adjust'] = 1
                global_result['结论'] = global_result['结论'] + f'上次动作下发到拐点上，进行回调。'
                default_cache.set(CONTEXT_KEY_ACTION_BACK, 1, 300)
            else:
                control_b = 0
        elif last_action < 0:
            if this_delta_6min > STAGE_B_THIS_THRESHOLD:  # 保持高速变化
                if last_action > -1 and change_delta_6min >= STAGE_B_CHANGE_THRESHOLD:
                    control_b = -1
                # elif change_delta_6min >= STAGE_B_CHANGE_THRESHOLD:
                else:
                    control_b = -0.5

            elif change_delta_6min >= STAGE_B_CHANGE_THRESHOLD:  # delta增加很多
                control_b = -0.5
            elif change_delta_6min >= STAGE_B_CHANGE_THRESHOLD2:  # delta增加但变化量不大
                control_b = -0.5
            elif this_delta_6min <= -STAGE_B_ACTION_BACK_THRESHOLD:
                control_b = -1 * last_action
                global_result['guaidian_adjust'] = 1
                global_result['结论'] = global_result['结论'] + f'上次动作下发到拐点上，进行回调。'
                default_cache.set(CONTEXT_KEY_ACTION_BACK, 1, 300)
            else:
                control_b = 0
        # if abs(control_b) > abs(last_action):
        #     control_d3lr = control_b - last_action
        # 20241014
        # if last_action > 0 and control_b > 0:
        #     if change_delta_3min <= STAGE_B_CHANGE_THRESHOLD3:
        #         global_result['3min变化变缓'] = '是'
        #         control_b = 0
        # elif last_action < 0 and control_b < 0:
        #     if change_delta_3min <= STAGE_B_CHANGE_THRESHOLD3:
        #         control_b = 0
        #         global_result['3min变化变缓'] = '否'
        print(
            f"JWD STAGE-B last_action={last_action}, control_b={control_b}, this_delta={this_delta_6min}, change_delta={change_delta_6min}")
        global_result['stage_b'] = f'JWD STAGE-B last_action={last_action}, control_b={control_b}, this_delta={this_delta_6min}, change_delta={change_delta_6min}'
        print(f"JWD after STAGE-B action={control_d3lr}")
    return control_b


def get_action_stage_f(action_control, ycl_data, current_time, last_action_time, global_result):
    ycl_10min_delta = round(get_mean(ycl_data, current_time) - get_mean(ycl_data,
                                                                        current_time - datetime.timedelta(
                                                                            minutes=STAGE_A1_YCL_MIN)), 2)

    # TODO last_action_time='' 会报错
    if last_action_time == '':
        return action_control
    last_delta_min = (current_time - last_action_time).total_seconds() / 60
    control_f = 0
    if 5 <= last_delta_min <= 7:
        if ycl_10min_delta > YCL_10MIN_FAST_THRESHOLD:
            if action_control <= 0:
                control_f = -0.5
        elif ycl_10min_delta < -YCL_10MIN_FAST_THRESHOLD:
            if action_control >= 0:
                control_f = 1

    if control_f != 0:
        last_ycl_direction = default_cache.get(CONTEXT_KEY_YCL_DIRECTION, 0)
        if last_ycl_direction * control_f < 0:
            default_cache.set(CONTEXT_KEY_YCL_FAST_CHANGE, 0)
        last_change = default_cache.get(CONTEXT_KEY_YCL_FAST_CHANGE, 0)
        if last_change <= 2:
            global_result['触发快速调控'] = f'当前执行次数{last_change}, 开合度{last_change}'
            default_cache.set(CONTEXT_KEY_YCL_FAST_CHANGE, last_change + 1, TTL)
            default_cache.set(CONTEXT_KEY_YCL_DIRECTION, control_f, TTL)
        else:
            control_f = 0

    return action_control if control_f == 0 else control_f


# C阶段
def get_action_by_pos_stage_c(this_d3lr, current_time, global_result, pre_value, ycl_data):
    control_d3lr = 0
    # 调整及更新
    diff = 1000 * (pre_value - this_d3lr)
    set_value = pre_value
    if abs(diff) > STAGE_C_VALUE_THRESHOLD:
        delta = round(diff / STAGE_C_VALUE_THRESHOLD)
        # 0717 基于位置的调整增加引出量方向的保护
        if check_ycl_direction(pd.Timestamp(current_time), ycl_data, delta < 0):
            set_value = pre_value - delta * STAGE_C_VALUE_THRESHOLD / 1000
            print(
                f"JWD STAGE-C trigger control delta={delta}, diff={diff}, this_d3lr={this_d3lr}, pre_value={pre_value}")
            control_d3lr = delta * STAGE_C_ACTION
            if control_d3lr > 1:
                control_d3lr = 1
            elif control_d3lr < -1:
                control_d3lr = -1
            global_result["触发"] = "位置"
    return control_d3lr, set_value


def add_action_by_ycl(last_action, control_d3lr, this_d3lr, d3lr_data, this_ycl, ycl_data, current_time, global_result):
    ycl_20min_delta = round(
        get_mean(ycl_data, current_time) - get_mean(ycl_data,
                                                    current_time - datetime.timedelta(minutes=STAGE_A1_YCL_MAX)), 2)
    ycl_10min_delta = round(get_mean(ycl_data, current_time) - get_mean(ycl_data,
                                                                        current_time - datetime.timedelta(
                                                                            minutes=STAGE_A1_YCL_MIN)), 2)

    d3lr_20min_data = get_mean(d3lr_data, current_time - datetime.timedelta(seconds=20 * 60))
    d3lr_20min_delta = round(this_d3lr - d3lr_20min_data, 2)
    global_result["ycl_20min_delta"] = ycl_20min_delta

    last_action_time = default_cache.get(CONTEXT_KEY_LAST_TIME, '')
    last_ycl_action_time = default_cache.get(CONTEXT_KEY_YCL_LAST_TIME, '')

    global_result["JWD_YCL_LAST_TIME"] = last_ycl_action_time
    if last_action_time:
        last_action_time = get_time(last_action_time)
    if last_ycl_action_time:
        last_ycl_action_time = get_time(last_ycl_action_time)
    action = 0
    # 此处变化量阈值还需要调整
    if abs(ycl_20min_delta) > 1.8:
        # 6min内调整过等一等
        if last_action_time:
            # 15min内调整过 补动作
            if last_action_time + datetime.timedelta(minutes=LIMIT_TIME) > current_time:
                if control_d3lr < 0.5:
                    action = 0.3
            # 15min 没有调，此处根据YCL差值来调
        else:
            if 1.8 <= abs(ycl_20min_delta) < 2.2:
                action = 0.5
            elif 2.2 <= abs(ycl_20min_delta) < 2.7:
                action = 0.8
            else:
                action = 1

    if abs(ycl_10min_delta) > 1.5:
        action = 1

    if abs(d3lr_20min_delta) > D3LR_20MIN_THRESHOLD:
        if 0 > control_d3lr > -0.5:
            action = -0.5
        elif 0 < control_d3lr < 0.5:
            action = 0.5

    increment = 0
    if this_ycl < 1040 and ycl_20min_delta < 0 and '下降' in global_result['JWD_YCLJS']:
        increment = action
    if this_ycl > 1040 and ycl_20min_delta > 0 and '上升' in global_result['JWD_YCLJS']:
        increment = -action

    if increment != 0:
        if last_ycl_action_time and last_ycl_action_time + datetime.timedelta(minutes=LIMIT_TIME) > current_time:
            global_result["场景D"] = "引出量快速变化联合调整————退避"
            return 0
        global_result["场景D"] = f"引出量快速变化联合调整{increment}"
        default_cache.set(CONTEXT_KEY_YCL_LAST_TIME, get_time_str(current_time), TTL)
        if increment >= 0.5:
            default_cache.set(CONTEXT_KEY_LAST_TIME, get_time_str(current_time), TTL)
            default_cache.set(CONTEXT_KEY_LAST_ACTION, control_d3lr, TTL)
            default_cache.set(CONTEXT_KEY_LAST_ACTION_D3LR, this_d3lr, TTL)
    return increment


def fix_key_action(control_d3lr, this_d3lr, d3lr_data, this_ycl, ycl_data, f1l1rb_1h_delta, d3lr_target_temp, current_time, global_result):
    """在危险区，是否要下动作"""
    ycl_10min_delta = round(this_ycl - get_mean(ycl_data, current_time - datetime.timedelta(
                                                                            minutes=STAGE_A1_YCL_MIN)), 2)
    ycl_15min_delta = round(this_ycl - get_mean(ycl_data, current_time - datetime.timedelta(minutes=STAGE_A1_YCL_MIN + 5)), 2)

    real_ycl = get_real(ycl_data, current_time)
    ycl_30min_delta = round(real_ycl - get_real(ycl_data, current_time - datetime.timedelta(minutes=30)), 2)
    ycl_40min_delta = round(real_ycl - get_real(ycl_data, current_time - datetime.timedelta(minutes=40)), 2)
    ycl_50min_delta = round(real_ycl - get_real(ycl_data, current_time - datetime.timedelta(minutes=50)), 2)
    global_result['ycl_检测值'] = f"""当前ycl：{get_mean(ycl_data, current_time)}， 10分钟前的ycl:{get_mean(ycl_data,current_time - datetime.timedelta(minutes=STAGE_A1_YCL_MIN))}，
    30分钟前的ycl:{ycl_30min_delta}, 40分钟前的ycl:{ycl_40min_delta}, 50分钟前的ycl:{ycl_50min_delta}"""
    d3lr_threshold_increment = 0
    extra_action = 0
    if YCL_LIMIT_LOW_LOW <= this_ycl <= YCL_LIMIT_LOW or YCL_LIMIT_HIGH <= this_ycl <= YCL_LIMIT_HIGH_HIGH:
        d3lr_threshold_increment = 0.02
        extra_action = 0.2
    elif this_ycl <= YCL_LIMIT_LOW_LOW or this_ycl >= YCL_LIMIT_HIGH_HIGH:
        extra_action = 0.3
        d3lr_threshold_increment = 0.03
    elif YCL_LIMIT_LOW <= this_ycl <= YCL_LIMIT_HIGH:
        extra_action = 0.1
        d3lr_threshold_increment = 0.01

    d3lr_15min = get_mean(d3lr_data, current_time - datetime.timedelta(seconds=15 * 60))
    d3lr_15min_delta = round(this_d3lr - d3lr_15min, 2)
    if control_d3lr < 0 and this_ycl < YCL_LIMIT_LOW:
        if 0 < d3lr_15min_delta < D3LR_15MIN_THRESHOLD - d3lr_threshold_increment:
            global_result[
                '动作修正，触发ycl阈值逻辑'] = f'0 < {d3lr_15min_delta} < {D3LR_15MIN_THRESHOLD - d3lr_threshold_increment}, ycl:{this_ycl}'
            return 0
    if control_d3lr > 0 and this_ycl > YCL_LIMIT_HIGH:
        if 0 > d3lr_15min_delta > -D3LR_15MIN_THRESHOLD - d3lr_threshold_increment:
            global_result[
                '动作修正，触发ycl阈值逻辑'] = \
                f'0 > {d3lr_15min_delta} >= {-D3LR_15MIN_THRESHOLD - d3lr_threshold_increment}, ' \
                f'ycl:{this_ycl}'
            return 0

    if control_d3lr == 0:
        if (d3lr_15min_delta > D3LR_15MIN_THRESHOLD - d3lr_threshold_increment) and this_ycl >= YCL_LIMIT_HIGH and ycl_10min_delta >= 0:
            return -0.5
        if (d3lr_15min_delta < -D3LR_15MIN_THRESHOLD + d3lr_threshold_increment) and this_ycl <= YCL_LIMIT_LOW and ycl_10min_delta <= 0:
            return 0.5
        global_result['动作修正，逻辑补充'] = f'd3lr_10min_delta:{d3lr_15min_delta}, ycl_10min_delta:{ycl_10min_delta}'

    # d3lr与ycl不同向，等等看
    # wait_times = default_cache.get(CONTEXT_KEY_WAIT_ONCE, 0)

    if LAILIAO_THRESHOLD1 <= abs(f1l1rb_1h_delta) < LAILIAO_THRESHOLD2:
        extra_action = LAILIAO_LEVEL1
    elif LAILIAO_THRESHOLD2 <= abs(f1l1rb_1h_delta) < LAILIAO_THRESHOLD3:
        extra_action = LAILIAO_LEVEL2
    elif abs(f1l1rb_1h_delta) >= LAILIAO_THRESHOLD3:
        extra_action = LAILIAO_LEVEL3
    else:
        extra_action = 0

    global_result[
        '来料阈值逻辑'] = f'来料差值:{f1l1rb_1h_delta}, 来料第一阈值:{LAILIAO_THRESHOLD1}, 来料第二阈值:{LAILIAO_THRESHOLD2}, 来料第三阈值:{LAILIAO_THRESHOLD3}'

    if control_d3lr < 0 and f1l1rb_1h_delta < 0:
        global_result['触发来料调整'] = f'调整值{control_d3lr + extra_action}'
        control_d3lr = control_d3lr + extra_action
    elif control_d3lr > 0 and f1l1rb_1h_delta > 0:
        global_result['触发来料调整'] = f'调整值{control_d3lr - extra_action}'
        control_d3lr =  control_d3lr - extra_action
    elif control_d3lr > 0 and f1l1rb_1h_delta < 0:
        global_result['触发来料调整'] = f'调整值{control_d3lr + extra_action}'
        control_d3lr =  control_d3lr + extra_action
    elif control_d3lr < 0 and f1l1rb_1h_delta > 0:
        global_result['触发来料调整'] = f'调整值{control_d3lr - extra_action}'
        control_d3lr =  control_d3lr - extra_action

    if this_ycl >= YCL_LIMIT_HIGH and control_d3lr > 0.5:
        control_d3lr = 0.5
    elif this_ycl <= YCL_LIMIT_LOW and control_d3lr < -0.5:
        control_d3lr = -0.5

    # ycl剧烈变化，但d3lr变化不明时，进行判断
    if ycl_10min_delta > YCL_10MIN_FAST_THRESHOLD and d3lr_15min_delta >= D3LR_15MIN_THRESHOLD - 0.01:
        if control_d3lr == 0:
            global_result['触发ycl剧烈变化,d3lr变化不快'] = '是'
            control_d3lr = -D3LR_15MIN_FAST_ADJUST
    elif ycl_10min_delta <= -YCL_10MIN_FAST_THRESHOLD and d3lr_15min_delta <= -D3LR_15MIN_THRESHOLD + 0.01:
        if control_d3lr == 0:
            global_result['触发ycl剧烈变化,d3lr变化不快'] = '是'
            control_d3lr = D3LR_15MIN_FAST_ADJUST

    fast_flag = 0
    if control_d3lr > 0:
        if ycl_30min_delta >= YCL_30MIN_FAST_CHANGE or ycl_40min_delta >= YCL_40MIN_FAST_CHANGE or ycl_50min_delta >= YCL_50MIN_FAST_CHANGE:
            control_d3lr = control_d3lr - YCL_FAST_CHANGE_ACTION
            fast_flag = 1
        elif ycl_30min_delta <= -YCL_30MIN_FAST_CHANGE or ycl_40min_delta <= -YCL_40MIN_FAST_CHANGE or ycl_50min_delta <= -YCL_50MIN_FAST_CHANGE:
            control_d3lr = control_d3lr + YCL_FAST_CHANGE_ACTION
            fast_flag = 1
    elif control_d3lr < 0:
        if ycl_30min_delta >= YCL_30MIN_FAST_CHANGE or ycl_40min_delta >= YCL_40MIN_FAST_CHANGE or ycl_50min_delta >= YCL_50MIN_FAST_CHANGE:
            control_d3lr = control_d3lr - YCL_FAST_CHANGE_ACTION
            fast_flag = 1
        elif ycl_30min_delta <= -YCL_30MIN_FAST_CHANGE or ycl_40min_delta <= -YCL_40MIN_FAST_CHANGE or ycl_50min_delta <= -YCL_50MIN_FAST_CHANGE:
            control_d3lr = control_d3lr + YCL_FAST_CHANGE_ACTION
            fast_flag = 1

    if fast_flag == 1:
        global_result['结论'] = global_result['结论'] + 'YCL快速变化补偿触发，同向补偿0.1反向补偿-0.1'


    # d3lr中心值
    control_temp_d3lr = 0
    global_result['温度中心力度调整debug'] = f'当前d3lr为{this_d3lr}, d3lr目标温度为{d3lr_target_temp}'
    if TEMP_BUTTON != 0:
        if this_d3lr > d3lr_target_temp and (this_ycl > YCL_LIMIT_HIGH or this_ycl < YCL_LIMIT_LOW):
            if control_d3lr > 0:
                control_temp_d3lr = round(control_d3lr - TARGET_TEMP_SUPPLEMENT1, 1)
            elif control_d3lr < 0:
                control_temp_d3lr = round(control_d3lr - TARGET_TEMP_SUPPLEMENT1, 1)
            global_result['结论'] = global_result['结论'] + f'。 d3lr温度中心值补偿， 原始动作{control_d3lr},补偿后{control_temp_d3lr}'
            control_d3lr = control_temp_d3lr
        elif this_d3lr < d3lr_target_temp and (this_ycl > YCL_LIMIT_HIGH or this_ycl < YCL_LIMIT_LOW):
            if control_d3lr > 0:
                control_temp_d3lr = round(control_d3lr + TARGET_TEMP_SUPPLEMENT1, 1)
            elif control_d3lr < 0:
                control_temp_d3lr = round(control_d3lr + TARGET_TEMP_SUPPLEMENT1, 1)
            global_result['结论'] = global_result[
                                        '结论'] + f'。 d3lr温度中心值补偿， 原始动作{control_d3lr},补偿后{control_temp_d3lr}'

            control_d3lr = control_temp_d3lr


    global_result['动作规避'] = f'15分钟d3lr变化量：{d3lr_15min_delta}, 10分钟ycl变化量：{ycl_10min_delta}, 15分钟ycl变化量:{ycl_15min_delta}, 动作：{control_d3lr}'
    if d3lr_15min_delta * ycl_10min_delta < 0:
        if control_d3lr * ycl_10min_delta > 0 and abs(ycl_10min_delta) <= YCL_AVOID_THRESHOLD:
            if global_result['guaidian_adjust'] == 1:
                pass
        else:
            global_result['结论'] = global_result['结论'] + f'd3lr与ycl反向退避，不调整'
            control_d3lr = 0
    else:
        if abs(ycl_10min_delta) <= YCL_AVOID_THRESHOLD and abs(ycl_15min_delta) <= YCL_AVOID_THRESHOLD2:
            global_result['结论'] = global_result['结论'] + f'd3lr与ycl同向，但ycl趋势不明显，不确定是否能看作同向还是反向，不调整'
            control_d3lr = 0

    return control_d3lr


def ycl_single_trend(current_time, d3lr_data):
    d3lr_60min_delta = round(get_mean(d3lr_data, current_time) - get_mean(d3lr_data, current_time - datetime.timedelta(
        minutes=60)), 2)

    d3lr_60min_mean = get_mean(d3lr_data, current_time - datetime.timedelta(minutes=60))

    d3lr_10min_delta = round(get_mean(d3lr_data, current_time) - get_mean(d3lr_data, current_time - datetime.timedelta(
        minutes=10)), 2)
    d3lr_10min_mean = get_mean(d3lr_data, current_time - datetime.timedelta(minutes=10))

    action = 0
    if d3lr_60min_delta > 0 and d3lr_10min_delta > SINGLE_TREND_THRESHOLD and d3lr_10min_mean - d3lr_60min_mean > 0.03:
        action = -0.3
    elif d3lr_60min_delta < 0 and d3lr_10min_delta < -SINGLE_TREND_THRESHOLD and d3lr_10min_mean - d3lr_60min_mean < -0.03:
        action = 0.3

    return action