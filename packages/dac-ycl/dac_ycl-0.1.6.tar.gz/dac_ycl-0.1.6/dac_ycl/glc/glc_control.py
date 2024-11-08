# 2024-10-25 BPAI-YCLCtl-1-0-2

import datetime
import json
import re
import traceback

import numpy as np
import pandas as pd
from scipy.signal import savgol_filter, find_peaks

from dac_ycl.glc.utils.dac_facade import query_actions, default_cache, get_data, mysql_conn, set_calculated_data
from dac_ycl.glc.utils.ycl_abandon_abnormal import get_time, get_time_str, abandon_abnormal_ycl, linear_regression

ALARM_RULE_ID = 2041
PATTERN = re.compile(r"([+\-*/])\s*(\d+\.?\d?)")  # 从反控动作中抽取出关键变化量
TTL = 3600  # 单位s，应该要比定时调度的间隔略大，取数原则是定时的间隔的1.5倍；供料槽定时间隔是6分钟，这里ttl就是9*60=540
INDEX_KEY = "last_index"  # 取个长名字,除非故意不然总不会撞上
INDEX_HISTORY = 'second_history'
CASE = 'CASE'
KEY_WORD = "__index__spec"
GLC_ACTION_THRESHOLD = 2.0
LIMIT_TIME = 28  # 限幅时间 0719修改为30分钟不超过2%
YCL_CHANGE_THRESHOLD = 0.21  # TODO 这个阈值是否合适待验证
YCL_STABLE_ACCU_THRESHOLD = 0.3
BD4R_STABLE_ACCU_THRESHOLD = 0.18
CASE_10_STABLE_THRESHOLD = 0.05

USE_MSU_STRATEGY = 1
MSU_OFFSET = 0.3
MSU_EFFECT_MIN = 10
MSU_TIME_WINDOW = 20
MSU_ACTION_LIMIT = 1.5

THREE_ACTION_SCENE = "THREE_ACTION_SCENE"  # 标记动作是由连续三次无调整通过差值校正判断的

YCL_DIRECTION_DELTA_CHANGE_THRESHOLD = 0.1
YCL_DELTA_THRESHOLD = 0.1

BD4R_LIMIT_HIGH = 1228
BD4R_LIMIT_LOW = 1223.5

# 阈值单位统一成每10分钟变化量
YCL_CHECK_THRESHOLD_1 = 1
BD4R_CHECK_THRESHOLD_1 = 0.04

YCL_CHECK_THRESHOLD_2 = 1.0
BD4R_CHECK_THRESHOLD_2 = 0.25

YCL_CHECK_THRESHOLD_3 = 2
BD4R_CHECK_THRESHOLD_3 = 0.1

YCL_CHECK_THRESHOLD_4 = 0.24
BD4R_CHECK_THRESHOLD_4 = 0.09

# SUM2_DELTA_THRESHOLD1 = 0.16
# SUM2_DELTA_THRESHOLD2 = 0.25
# BD4R_CHECK_SUM2_THRESHOLD = 0.12

BD4R_ACTION_THRESHOLD = 0.18
# 进行变化量和调整量的检查，去掉过多的调整
YCL_DELTA_THRESHOLD1 = 1.5
BLSH_DELTA_THRESHOLD1 = 1.0

YCL_DELTA_THRESHOLD2 = 3.0
BLSH_DELTA_THRESHOLD2 = 1.5

YCL_DELTA_THRESHOLD3 = 4.0
BLSH_DELTA_THRESHOLD3 = 2.0

YCL_UPPER_BOUND = 1043.5
YCL_LOWER_BOUND = 1037
EXTRA_ACTION_UPPER = 0.1
EXTRA_ACTION_LOWER = 0.2

YCL_OUT_UPPER_BOUND = 1043.5
YCL_OUT_LOWER_BOUND = 1037
DECREASE_ACTION_UPPER = 0.2
DECREASE_ACTION_LOWER = 0

F2R1RB_THRESHOLD = 0.03  # TODO 待定

YCL_PROTECT_UPPER = 1046
YCL_PROTECT_LOWER = 1037
YCL_PROTECT_ACTION_UPPER = 0.8
YCL_PROTECT_ACTION_LOWER = 0.8

COMP_BD4R_MINUTE = 20
COMP_BD4R_DELTA_THRESHOLD = 0.13  # TODO 待定  0.2 -> 0.13
COMP_BD4R_SLOPE_THRESHOLD = 0.2  # 0.2
COMP_ACTION = 0.8  # 0.3 -> 0.8
COMP_YCL_MINUTE = 25
COMP_YCL_DELTA_THRESHOLD = 1.8  # 3 -> 1.8
COMP_YCL_SLOPE_THRESHOLD = 0.8  # 1 -> 0.8

BW1R_SLOPE_THRESHOLD = 0.02


class Fxxk:
    outer_delta = None  # 使用类来操作对外暴露的变量，保证外部能访问到新的值


outer = Fxxk()


def pre(data, global_result: dict):
    pass


def get_config(alarm_rule_id):
    config_result = mysql_conn.query_config_by_alarm_rule_id(alarm_rule_id)
    config = config_result.get('供料槽', {})

    global GLC_ACTION_THRESHOLD, LIMIT_TIME, BD4R_LIMIT_HIGH, BD4R_LIMIT_LOW
    global YCL_STABLE_ACCU_THRESHOLD, BD4R_STABLE_ACCU_THRESHOLD

    global YCL_CHECK_THRESHOLD_1, YCL_CHECK_THRESHOLD_2, YCL_CHECK_THRESHOLD_3, YCL_CHECK_THRESHOLD_4
    global BD4R_CHECK_THRESHOLD_1, BD4R_CHECK_THRESHOLD_2, BD4R_CHECK_THRESHOLD_3, BD4R_CHECK_THRESHOLD_4, BD4R_ACTION_THRESHOLD
    # global SUM2_DELTA_THRESHOLD1
    # global SUM2_DELTA_THRESHOLD2, BD4R_CHECK_SUM2_THRESHOLD
    global YCL_DELTA_THRESHOLD1, BLSH_DELTA_THRESHOLD1, YCL_DELTA_THRESHOLD2, BLSH_DELTA_THRESHOLD2, YCL_DELTA_THRESHOLD3, BLSH_DELTA_THRESHOLD3
    global YCL_UPPER_BOUND, YCL_LOWER_BOUND, EXTRA_ACTION_UPPER, EXTRA_ACTION_LOWER
    global YCL_OUT_UPPER_BOUND, DECREASE_ACTION_UPPER, YCL_OUT_LOWER_BOUND, DECREASE_ACTION_LOWER
    global F2R1RB_THRESHOLD
    global YCL_PROTECT_UPPER, YCL_PROTECT_ACTION_UPPER, YCL_PROTECT_LOWER, YCL_PROTECT_ACTION_LOWER
    global COMP_BD4R_DELTA_THRESHOLD, COMP_BD4R_SLOPE_THRESHOLD, COMP_YCL_MINUTE, COMP_BD4R_MINUTE,\
        COMP_ACTION, COMP_YCL_DELTA_THRESHOLD, COMP_YCL_SLOPE_THRESHOLD
    global BW1R_SLOPE_THRESHOLD

    # config['glc_action_threshold'] = 2.0
    # config['limit_time'] = 28
    # config['ycl_stable_accu_threshold'] = 0.3
    # config['bd4r_stable_accu_threshold'] = 0.18
    # config['功率同向动作6分钟变化阈值'] = 0.25
    # config['功率同向动作BD4R10分钟变化阈值'] = 0.12

    # GLC_ACTION_THRESHOLD = config.get('glc_action_threshold', GLC_ACTION_THRESHOLD)
    # LIMIT_TIME = config.get('limit_time', LIMIT_TIME)
    # YCL_STABLE_ACCU_THRESHOLD = config.get('ycl_stable_accu_threshold', YCL_STABLE_ACCU_THRESHOLD)
    # BD4R_STABLE_ACCU_THRESHOLD = config.get('bd4r_stable_accu_threshold', BD4R_STABLE_ACCU_THRESHOLD)

    BD4R_LIMIT_HIGH = config.get('GY1_BD4R上限', BD4R_LIMIT_HIGH)
    BD4R_LIMIT_LOW = config.get('GY1_BD4R下限', BD4R_LIMIT_LOW)

    YCL_CHECK_THRESHOLD_1 = config.get('CJ1_引出量10分钟变化阈值', YCL_CHECK_THRESHOLD_1)
    BD4R_CHECK_THRESHOLD_1 = config.get('CJ1_BD4R10分钟变化阈值', BD4R_CHECK_THRESHOLD_1)
    YCL_CHECK_THRESHOLD_2 = config.get('CJ2_引出量10分钟变化阈值', YCL_CHECK_THRESHOLD_2)
    BD4R_CHECK_THRESHOLD_2 = config.get('CJ2_BD4R10分钟变化阈值', BD4R_CHECK_THRESHOLD_2)
    YCL_CHECK_THRESHOLD_3 = config.get('CJ3_引出量10分钟变化阈值', YCL_CHECK_THRESHOLD_3)
    BD4R_CHECK_THRESHOLD_3 = config.get('CJ3_BD4R10分钟变化阈值', BD4R_CHECK_THRESHOLD_3)
    YCL_CHECK_THRESHOLD_4 = config.get('CJ4_引出量10分钟变化阈值', YCL_CHECK_THRESHOLD_4)
    BD4R_CHECK_THRESHOLD_4 = config.get('CJ4_BD4R10分钟变化阈值', BD4R_CHECK_THRESHOLD_4)

    # SUM2_DELTA_THRESHOLD1 = config.get('功率反向屏蔽动作6分钟变化阈值', SUM2_DELTA_THRESHOLD1)
    # SUM2_DELTA_THRESHOLD2 = config.get('功率同向动作6分钟变化阈值', SUM2_DELTA_THRESHOLD2)
    # BD4R_CHECK_SUM2_THRESHOLD = config.get('功率同向动作BD4R10分钟变化阈值', BD4R_CHECK_SUM2_THRESHOLD)

    BD4R_ACTION_THRESHOLD = config.get('XF_BD4R阈值', BD4R_ACTION_THRESHOLD)
    YCL_DELTA_THRESHOLD1 = config.get('XF_引出量变化阈值1', YCL_DELTA_THRESHOLD1)
    BLSH_DELTA_THRESHOLD1 = config.get('XF_调整量阈值1', BLSH_DELTA_THRESHOLD1)
    YCL_DELTA_THRESHOLD2 = config.get('XF_引出量变化阈值2', YCL_DELTA_THRESHOLD2)
    BLSH_DELTA_THRESHOLD2 = config.get('XF_调整量阈值2', BLSH_DELTA_THRESHOLD2)
    YCL_DELTA_THRESHOLD3 = config.get('XF_引出量变化阈值3', YCL_DELTA_THRESHOLD3)
    BLSH_DELTA_THRESHOLD3 = config.get('XF_调整量阈值3', BLSH_DELTA_THRESHOLD3)

    YCL_UPPER_BOUND = config.get('ZX1_引出量高区', YCL_UPPER_BOUND)
    YCL_LOWER_BOUND = config.get('ZX1_引出量低区', YCL_LOWER_BOUND)
    EXTRA_ACTION_UPPER = config.get('ZX1_高区增加力度', EXTRA_ACTION_UPPER)
    EXTRA_ACTION_LOWER = config.get('ZX1_低区增加力度', EXTRA_ACTION_LOWER)

    YCL_OUT_UPPER_BOUND = config.get("ZX2_引出量上限", YCL_OUT_UPPER_BOUND)
    DECREASE_ACTION_UPPER = config.get("ZX2_向上动作减小量", DECREASE_ACTION_UPPER)
    YCL_OUT_LOWER_BOUND = config.get("ZX2_引出量下限", YCL_OUT_LOWER_BOUND)
    DECREASE_ACTION_LOWER = config.get("ZX2_向下动作减小量", DECREASE_ACTION_LOWER)

    YCL_PROTECT_UPPER = config.get("ZX3_引出量上限", YCL_PROTECT_UPPER)
    YCL_PROTECT_ACTION_UPPER = config.get("ZX3_上限回中心值力度", YCL_PROTECT_ACTION_UPPER)
    YCL_PROTECT_LOWER = config.get("ZX3_引出量下限", YCL_PROTECT_LOWER)
    YCL_PROTECT_ACTION_LOWER = config.get("ZX3_下限回中心值力度", YCL_PROTECT_ACTION_LOWER)
    # 回调
    F2R1RB_THRESHOLD = config.get("HT_F2R1RB温度10分钟变化阈值", F2R1RB_THRESHOLD)

    # 补充
    COMP_BD4R_MINUTE = config.get("BC1_BD4R变化量分钟", COMP_BD4R_MINUTE)
    COMP_BD4R_DELTA_THRESHOLD = config.get("BC1_BD4R变化量", COMP_BD4R_DELTA_THRESHOLD)
    COMP_BD4R_SLOPE_THRESHOLD = config.get("BC1_BD4R10min变化率", COMP_BD4R_SLOPE_THRESHOLD)
    COMP_ACTION = config.get("BC1_动作力度", COMP_ACTION)
    COMP_YCL_MINUTE = config.get("BC1_引出量变化量分钟", COMP_YCL_MINUTE)
    COMP_YCL_DELTA_THRESHOLD = config.get("BC1_引出量变化量", COMP_YCL_DELTA_THRESHOLD)
    COMP_YCL_SLOPE_THRESHOLD = config.get("BC1_引出量10min变化率", COMP_YCL_SLOPE_THRESHOLD)

    BW1R_SLOPE_THRESHOLD = config.get("WD1_BW1R10分钟变化率", BW1R_SLOPE_THRESHOLD)

    print(config)
    return config


def do_first(global_result: dict, delta):
    # update this index
    # 第一次处理
    global_result["multi"] = 1
    global_result["YCLJS"] = None
    global_result["delta"] = None


state_2_num = {
    "快速上升": 2,
    "缓慢上升": 1,
    "平稳": 0,
    "缓慢下降": -1,
    "快速下降": -2,
}
state_2_num_bw1r = {
    "上升": 1,
    "平稳": 0,
    "下降": -1,
}
state_2_num_d3lr = {
    "快速上升": 1,
    "缓慢上升": 1,
    "平稳": 0,
    "缓慢下降": -1,
    "快速下降": -1,
}
num_2_state = {
    2: "快速上升",
    1: "缓慢上升",
    0: "平稳",
    -1: "缓慢下降",
    -2: "快速下降",
}
state_mapping_1 = {
    # 场景1-1，平稳->缓慢变化，先放放
    (0, 0): {
        # 7/22 去除下面2条场景
        # (1, 0): 0,
        # (-1, 0): 0,
        (0, 1): 0,
        (0, -1): 0
    },
    # 7/12 bd4r上升没有引起引出量变化，不用急
    (0, 1): {
        (0, 1): 0,
        (1, 0): 0,  # 7/16 bd4r引起的变化，且bd4r已经平稳了，不用调
    },
    (0, -1): {
        (0, -1): 0,
        (-1, 0): 0,
    },
    # 场景1-4
    (1, 0): {
        (1, -1): 0,
        (1, -2): 0,
        (0, -1): 0,  # 0721
    },
    (1, -1): {
        (1, -2): 0
    },
    (-1, 0): {
        (-1, 1): 0,
        (-1, 2): 0,
        (0, 1): 0,
    },
    (-1, 1): {
        (-1, 2): 0
    },
    # 场景1-3 引出量走平
    (1, -1): {
        (0, -1): 0
    },
    (-1, 1): {
        (0, 1): 0
    },
    # 7/12 此时bd4r变好，等下效果
    (1, 2): {
        (1, 1): 0,
    },
    (-1, -2): {
        (-1, -1): 0,
    },
}
"""
    # 从mapping1中移除
    # 7/15 此时bd4r变好，等下效果
    (0, -2): {
        (-1, -1): 0,
        # 7/16 补充类似场景
        (-1, 0): 0,
    },
    (0, 2): {
        (1, 1): 0,
        (1, 0): 0,
    },
    (1, 1): {
        (2, 0): 0,
    },
    (-1, -1): {
        (-2, 0): 0,
    },
"""
# mapping2是ycl趋向稳定的时候，不调
state_mapping_2 = {
    # 场景1-2
    # 0: {
    #     0: 0
    # },
    # 场景1-3
    2: {
        # 0: 0,
        1: 0
    },
    -2: {
        # 0: 0,
        -1: 0
    }
}
# mapping3是为了避免重复的动作过度调整，当上一次做出符合方向的调整，且状况并没有恶化的情况下，此次不调
state_mapping_3 = {
    # 场景2-1
    (1, 0): {
        (1, 0): '-'
    },
    (-1, 0): {
        (-1, 0): '+'
    },
    (1, 1): {
        (1, 0): '-',
        (1, -1): '-',
        (0, 1): '-',  # 7/12 引出量变好了，不调
        (1, 1): '-',  # 7/15 同样场景，等下变化
        (2, 0): '-',  # 7/22 加一等一
    },
    (-1, -1): {
        (-1, 0): '+',
        (-1, 1): '+',
        (0, -1): '+',  # 7/12 引出量变好了，不调
        (-1, -1): '+',  # 7/15 同样场景，等下变化
        (-2, 0): '+',
    },
    # 7/12 避免过度调整，等下效果
    (1, 2): {
        (1, 2): '-',
        (1, 0): '-',  # 0721
    },
    (-1, -2): {
        (-1, -2): '+',
        (-1, 0): '+',
    },
    # 7/16 趋势变好，不要连续调
    (0, 2): {
        (0, 1): '-',
        (1, 1): '-',
        (1, 0): '-',
    },
    (0, -2): {
        (0, -1): '+',
        (-1, -1): '+',
        # 7/16 补充类似场景
        (-1, 0): '+',
    },
    # 7/17 增加快速变化场景
    (2, 1): {
        (2, 1): '-',
        (2, 0): '-',
    },
    (-2, -1): {
        (-2, -1): '+',
        (-2, 0): '+',
    },
    # 7/22 加一等一
    (2, 0): {
        (1, 1): '-',
        (2, 0): '-',  # 7/26
    },
    (-2, 0): {
        (-1, -1): '+',
        (-2, 0): '+',
    },
}
# mapping4是连续出现相同趋势，且上一次并无符合方向的调整时，追加一次动作
state_mapping_4 = {
    # 场景3-1，当前一次没有动作的时候，进行调整
    (1, 0): {
        (1, 0): '-'
    },
    (-1, 0): {
        (-1, 0): '+'
    },
    # 场景3-2，调整不足，当前一次无动作的情况，补充一次动作
    # 7/22 增加d3lr判断进行加一等一
    # (-1, 1): {
    #     (-1, 1): '+'
    # },
    # (1, -1): {
    #     (1, -1): '-'
    # }
}
state_mapping_5 = {
    # 场景3-2，调整量不足的情况，补充一下
    (-1, 2): {
        # (-1, 1): 0.5,  # 7/23 去除
        (-2, 1): 1,
    },
    (0, 1): {
        (-1, 1): 0.5
    },
    (1, -2): {
        # (1, -1): -0.5,
        (2, -1): -1,
    },
    (0, -1): {
        (1, -1): -0.5
    }
}
# mapping6是上一次调完趋势就扭转的情况，说明动作是多了，此次调回去
# 是对mapping2的补充，上次调整完，引出量从快速拐头的时候，说明上次调多了，退回上次动作
state_mapping_6 = {
    # 0718 (1,1) -> (0,0)无条件退回
    # (1, 1): {
    #     (0, 0): '-'
    # },
    # (-1, -1): {
    #     (0, 0): '+'
    # },
    (2, 1): {
        (0, 0): '-'
    },
    (-2, -1): {
        (0, 0): '+'
    },
    # (2, 0): {
    #     (2, -1): '-'
    # },
    # (-2, 0): {
    #     (-2, 1): '+'
    # }
}
# 7/12 mapping7是引出量加速变化的时候，保证连续两次调整量和为1
# 7/18 场景7需要加bw1r的保护
state_mapping_7 = {
    # (1, 1): {
    #     (2, 1): -1,
    # },
    # (-1, -1): {
    #     (-2, -1): +1,
    # },
    (0, 2): {
        (1, 2): -1,
    },
    (0, -2): {
        (-1, -2): +1,
    },
}

"""
# mapping7是连续快速变化的场景，后面一次的动作增加0.3
state_mapping_7 = {
    2: {
        2: -0.3
    },
    -2: {
        -2: +0.3
    }
}
# mapping8是ycl趋缓，bd4r也趋平稳，不要撤销当前的动作
state_mapping_8 = {
    (2, -1): {
        (1, 0): '-'
    },
    (-2, 1): {
        (-1, 0): '+'
    }
}
# mapping9是引出量加速变化的情况，加大本次动作
state_mapping_9 = {
    (1, 1): {
        (2, 0): -0.3,
        (2, 1): -0.3,
        (2, 2): -0.3
    },
    (1, 2): {
        (2, 2): -0.3
    },
    (-1, -1): {
        (-2, 0): +0.3,
        (-2, -1): +0.3,
        (-2, -2): +0.3
    },
    (-1, -2): {
        (-2, -2): +0.3
    }
}
# mapping10是引出量快速变化BD4R趋缓的时候，减少本次调控量
state_mapping_10 = {
    (-2, 1): {
        (1, 2): +0.3,
    },
    (2, -1): {
        (-1, -2): -0.3
    },
    (1, 2): {
        (2, 1): +0.3,
    },
    (-1, -2): {
        (-2, -1): -0.3
    },
    (2, 2): {
        (2, 1): -0,
    },
    (-2, -2): {
        (-2, -1): +0,
    }
}
# 快速变化过渡过程，优先级最高 0710
# 不看前面动作
state_mapping_fast_1 = {
    (1, -1): {
        (2, -1): -0.5,
        (2, -2): 0,
    },
    (2, -1): {
        (2, -2): 0,
    },
    (-1, 1): {
        (-2, 1): +0.5,
        (-2, 2): 0,
    },
    (-2, 1): {
        (-2, 2): 0,
    }
}
# 看前面1次的动作
state_mapping_fast_2 = {
    (2, -1): {
        (2, -1): {
            -0.5: 0,
            0: -0.5,
        }
    },
    (2, -2): {
        (2, -2): {
            -0.5: -0.3,
            -0.3: 0,
            0: -0.5,
        }
    },
    (-2, 1): {
        (-2, 1): {
            +0.5: 0,
            0: +0.5,
        }
    },
    (-2, 2): {
        (-2, 2): {
            +0.5: +0.3,
            +0.3: 0,
            0: +0.5,
        }
    }
}
"""

state_mapping_9_fast = {
    (2, 2, 2): -0.5,
    (-2, -2, -2): +0.5,
}
state_mapping_10 = {
    # 0718 调整变好，退回动作，不需要考虑d3lr或bw1r
    (-2, 1): {
        # 8/1 快速变缓慢，不回退
        # (-1, 1): '+',
        # 7/23
        (0, 0): '+',
    },
    (2, -1): {
        # (1, -1): '-',
        (0, 0): '-',
    },
    (-2, 0): {
        # 8/1 快速变缓慢，不回退
        # (-1, 1): '+',
        # 7/19
        (0, 2): '+',
        # 7/24
        (0, 1): '+',
    },
    (2, 0): {
        # (1, -1): '-',
        (0, -2): '-',
        (0, -1): '-',
    },
    (-1, 0): {
        (0, 2): '+',
        (0, 0): '+',  # 7/21
    },
    (1, 0): {
        (0, -2): '-',
        (0, 0): '-',
    },
    (1, 1): {
        (0, 0): '-',
    },
    (-1, -1): {
        (0, 0): '+',
    },
    (1, -1): {
        (0, 0): '-',
        (0, -1): '-',  # 7/28
    },
    (-1, 1): {
        (0, 0): '+',
        (0, 1): '-',
    },
}
state_mapping_11 = {
    # 0718 执行一次等一次
    (2, 0, 0, 1): {
        (2, 0, 0, 1): '-',
    },
    (-2, 0, 0, -1): {
        (-2, 0, 0, -1): '+',
    },
    (0, 0, 1, 1): {
        (0, 0, 1, 1): '-',
    },
    (0, 0, -1, -1): {
        (0, 0, -1, -1): '+',
    },
    # 0719 加一次之后等待
    (0, 0, 1, 1): {
        (0, 1, 1, 1): '-',
    },
    (0, 0, -1, -1): {
        (0, -1, -1, -1): '+',
    },
    # 0722 加一等一
    (0, 0, 1, 1): {
        (0, 0, 1, 1): '-',
    },
    (0, 0, -1, -1): {
        (0, 0, -1, -1): '+',
    },
    (1, 0, 0, 0): {
        (2, 0, 0, 0): '-',
    },
    (-1, 0, 0, 0): {
        (-2, 0, 0, 0): '+',
    },
}
state_mapping_12 = {
    # 0718 特殊场景下不要等了，执行规则的动作
    (0, -1, -1, -1): {
        (-1, 0, -1, -1): 0,
    },
    (0, 1, 1, 1): {
        (1, 0, 1, 1): 0,
    },
    (-2, 0, -1, -1): {
        (-2, 1, -1, -1): 0,
    },
    (2, 0, 1, 1): {
        (2, -1, 1, 1): 0,
    },
}
state_mapping_13 = {
    # 0718 执行一次等一次
    (-1, 0, -1): {
        (-1, 0, -1): '+',
    },
    (1, 0, 1): {
        (1, 0, 1): '-',
    },
}
state_mapping_14 = {
    # 0719 d3lr+bw1r组合
    (-1, -1): {
        (1, -1): '+',
    },
    (1, 1): {
        (-1, 1): '-',
    },
}
state_mapping_15 = {
    # 0722 情况变好时，不调整，不看上一个是否有动作
    (-1, 0): {
        (0, -1): 0,
    },
    (1, 0): {
        (0, 1): 0,
    },
    (-2, 1): {
        (0, 1): 0,
    },
    (2, -1): {
        (0, -1): 0,
    },
}
state_mapping_16 = {
    # 7/22 d3lr同向时，加一等一
    (1, -1, 1): {
        (1, -1, 1): -0.5,
    },
    (-1, 1, -1): {
        (-1, 1, -1): +0.5,
    },
    # 7/26 bd4r没有起来，加一等一
    (2, 0, 0): {
        (1, 0, 1): -0.5,
    },
    (-2, 0, 0): {
        (-1, 0, -1): +0.5,
    },
}
state_mapping_17 = {
    # 7/23 拐头之后bd4r仍快速变化，立即回调
    (1, -2): {
        (0, -2): +0.5,
    },
    (-1, 2): {
        (0, 2): -0.5,
    },
}
state_mapping_18 = {
    # 7/26 情况没有那么紧急，上次调整过等下效果
    (1, 0): {
        (2, 0): '-',  # BD4R还没有变化，不动作
    },
    (-1, 0): {
        (-2, 0): '+',
    },
    # 7/28 BD4R变化，等下效果
    (2, 2): {
        (2, 0): '-',
    },
    (-2, -2): {
        (-2, 0): '+',
    },
}
state_mapping_19 = {
    # 7/26 上次动作之后，d3lr好转，退回动作
    (0, 0, -1): {
        (0, 1, 0): '+',
    },
    (0, 0, 1): {
        (0, -1, 0): '-',
    },
}


def do_second(first_action, global_result, last_states, delta, data):
    global_result["delta"] = 0  # 默认值0，后面流程保护起来

    try:

        """
        1、进行行为的纠正
        2、进行case处理
        """
        if not first_action:
            first_delta = 0
        else:
            first_delta = float(first_action)

        history = last_states.get(INDEX_HISTORY, [])
        trigger_scene_list = []
        # 分析历史数据
        # print(f'do_second history={history}')
        this_delta = delta  # 初始默认下动作
        is_revert = False  # 本次是否回退动作，默认为False，回退场景中改为True，回退动作按理不会触发限幅
        last_action = 0
        this_ycl_value = global_result["YCLJS.VALUE"]
        this_bd4r_value = global_result["BD4R.VALUE"]
        if not history:
            this_delta = delta  # 本次确定最终执行的动作
        else:
            last_history = history[-1]
            last_action = float(last_history['action'])
            if "REVERT" in last_history:
                last_revert = last_history["REVERT"]
            else:
                last_revert = False
            last_ycl = state_2_num[last_history['YCLJS']]
            last_bd4r = state_2_num[last_history['BD4R']]
            last_d3lr = state_2_num_d3lr[last_history['D3LR']]
            last_bw1r = state_2_num_bw1r[last_history['BW1R']]
            this_ycl = state_2_num[global_result['YCLJS']]
            this_bd4r = state_2_num[global_result['BD4R']]
            this_d3lr = state_2_num_d3lr[global_result['D3LR']]
            if not global_result.get('BW1R'):
                print("bug_here")
            this_bw1r = state_2_num_bw1r[global_result['BW1R']]
            # print(
            #     f'last_action={last_action}, last_ycl={last_ycl}, last_bd4r={last_bd4r}, this_ycl={this_ycl}, this_bd4r={this_bd4r}')

            global_result['LAST_YCLJS'] = last_history['YCLJS']
            global_result['LAST_BD4R'] = last_history['BD4R']
            global_result['LAST_ACTION'] = last_action
            this_d3lr_state = global_result['D3LR']
            this_bw1r_state = global_result["BW1R"]
            is_bw1r_up = this_bw1r_state == "上升"
            is_bw1r_down = this_bw1r_state == "下降"
            if this_d3lr_state.find("上升") >= 0:
                this_d3lr_state = "上升"
            elif this_d3lr_state.find("下降") >= 0:
                this_d3lr_state = "下降"

            # 处理连续的平稳
            CONTEXT_KEY_STABLE_YCL = "STABLE_YCL_VALUE"
            CONTEXT_KEY_STABLE_BD4R = "STABLE_BD4R_VALUE"
            if len(history) >= 2:
                bd4r_delta = this_bd4r_value - history[-1]["BD4R.VALUE"]
                ycl_delta = this_ycl_value - history[-1]["YCLJS.VALUE"]
                pre_ycl_delta = history[-1]["YCLJS.VALUE"] - history[-2]["YCLJS.VALUE"]
                pre_bd4r_delta = history[-1]["BD4R.VALUE"] - history[-2]["BD4R.VALUE"]

            original_this_ycl = this_ycl
            original_this_bd4r = this_bd4r
            if this_ycl != 0:
                default_cache.delete(CONTEXT_KEY_STABLE_YCL)
                print(f"GLC clear context {CONTEXT_KEY_STABLE_YCL}")
            else:
                last_ycl_value = default_cache.get(CONTEXT_KEY_STABLE_YCL, -1)
                print(f"GLC get from context {CONTEXT_KEY_STABLE_YCL}={last_ycl_value}")
                if last_ycl_value == -1:
                    default_cache.set(CONTEXT_KEY_STABLE_YCL, this_ycl_value, TTL)
                    last_ycl_value = this_ycl_value
                ycl_value_delta = this_ycl_value - last_ycl_value
                if ycl_value_delta >= YCL_STABLE_ACCU_THRESHOLD:
                    this_ycl = 1
                elif ycl_value_delta <= -YCL_STABLE_ACCU_THRESHOLD:
                    this_ycl = -1
                global_result[
                    "YCL连续平稳场景"] = f"累计差值={ycl_value_delta}, 转换为{this_ycl}, 阈值为{YCL_STABLE_ACCU_THRESHOLD}"
                if this_ycl != 0:
                    default_cache.delete(CONTEXT_KEY_STABLE_YCL)
                    print(f"GLC clear context {CONTEXT_KEY_STABLE_YCL}")
            if this_bd4r != 0:
                default_cache.delete(CONTEXT_KEY_STABLE_BD4R)
                print(f"GLC clear context {CONTEXT_KEY_STABLE_BD4R}")
            else:
                last_bd4r_value = default_cache.get(CONTEXT_KEY_STABLE_BD4R, -1)
                print(f"GLC get from context {CONTEXT_KEY_STABLE_BD4R}={last_bd4r_value}")
                if last_bd4r_value == -1:
                    default_cache.set(CONTEXT_KEY_STABLE_BD4R, this_bd4r_value, TTL)
                    last_bd4r_value = this_bd4r_value
                bd4r_value_delta = this_bd4r_value - last_bd4r_value
                if bd4r_value_delta >= BD4R_STABLE_ACCU_THRESHOLD:
                    this_bd4r = 1
                elif bd4r_value_delta <= -BD4R_STABLE_ACCU_THRESHOLD:
                    this_bd4r = -1
                global_result[
                    "BD4R连续平稳场景"] = f"累计差值={bd4r_value_delta}, 转换为{this_bd4r}, 阈值为{BD4R_STABLE_ACCU_THRESHOLD}"
                if this_bd4r != 0:
                    default_cache.delete(CONTEXT_KEY_STABLE_BD4R)
                    print(f"GLC clear context {CONTEXT_KEY_STABLE_BD4R}")
            # TODO 是否应该更新global_result，并重新查询动作
            global_result["BD4R"] = num_2_state[this_bd4r]
            global_result["YCLJS"] = num_2_state[this_ycl]
            this_action = query_actions(global_result, ALARM_RULE_ID)
            # 计算此次调控量
            origin_delta = delta
            delta = get_delta(this_action, global_result)
            this_delta = delta  # FIX 7/30 保持一致再进行场景判断
            info = f"原来动作={origin_delta}, 更新的动作={delta}"
            print(info)
            global_result["动作修正"] = info

            if (last_ycl, last_bd4r) in state_mapping_1:
                map_result = state_mapping_1[(last_ycl, last_bd4r)].get((this_ycl, this_bd4r), 1)
                if map_result == 0:
                    if (this_ycl == 1 and (this_d3lr_state == "上升" or is_bw1r_up)) or (
                            this_ycl == -1 and (this_d3lr_state == "下降" or is_bw1r_down)):
                        this_delta = delta
                        info = "变化较小，但D3LR或BW1R同向，本次执行规则"
                    else:
                        this_delta = 0
                        info = "变化较小，可以等一等，本次不调"
                    trigger_scene_list.append(1)
                    print(f'GLC stage1 hit')
                    global_result[CASE + '1-变化较小等待进一步变化'] = info
            if last_ycl in state_mapping_2:
                map_result = state_mapping_2[last_ycl].get(this_ycl, 1)
                if map_result == 0:
                    this_delta = 0
                    print(f'GLC stage2 hit')
                    global_result[CASE + '2-引出量趋稳'] = '引出量变缓，不调'
                    trigger_scene_list.append(2)
            if (last_ycl, last_bd4r) in state_mapping_3:
                if (this_ycl, this_bd4r) in state_mapping_3[(last_ycl, last_bd4r)]:
                    direction = state_mapping_3[(last_ycl, last_bd4r)][(this_ycl, this_bd4r)]
                    if (direction == '+' and last_action > 0) or (direction == '-' and last_action < 0):
                        # 8/1 增加及bd4r差值的检查
                        # TODO 增加拐点到现在YCL变化及调整量的检查，避免量过大
                        do_revert = True
                        if len(history) >= 2:
                            CASE_3_BD4R_THRESHOLD = 0.10  # 原先为0
                            if this_ycl > 0 and last_ycl > 0 and ycl_delta > pre_ycl_delta and bd4r_delta >= CASE_3_BD4R_THRESHOLD:
                                do_revert = False
                            elif this_ycl < 0 and last_ycl < 0 and ycl_delta < pre_ycl_delta and bd4r_delta <= -CASE_3_BD4R_THRESHOLD:
                                do_revert = False

                        print(f'GLC stage3 hit')
                        if do_revert:
                            this_delta = 0
                            global_result[CASE + '3-情况未变差避免过度调整'] = "避免过度调整，本次跳过"
                            trigger_scene_list.append(3)
                        else:
                            global_result[CASE + '3-情况未变差避免过度调整'] = "BD4R同向，引出量变化变大，不跳过"

            if (last_ycl, last_bd4r) in state_mapping_4:
                if (this_ycl, this_bd4r) in state_mapping_4[(last_ycl, last_bd4r)]:
                    info = "连续趋势，上一次无动作，本次执行规则"
                    direction = state_mapping_4[(last_ycl, last_bd4r)][(this_ycl, this_bd4r)]
                    case_4_name = CASE + '4-连续趋势时上次无动作'
                    if direction == '+' and last_action <= 0:
                        print(f'GLC stage4(+) hit')
                        if delta > 0:
                            this_delta = delta
                            global_result[case_4_name] = info
                        else:
                            this_delta = 0.5
                            global_result[case_4_name] = info
                        trigger_scene_list.append(4)
                    if direction == '-' and last_action >= 0:
                        print(f'GLC stage4(-) hit')
                        if delta < 0:
                            this_delta = delta
                            global_result[case_4_name] = info
                        else:
                            this_delta = -0.5
                            global_result[case_4_name] = info
                        trigger_scene_list.append(4)
            if (last_ycl, last_bd4r) in state_mapping_5:
                if (this_ycl, this_bd4r) in state_mapping_5[(last_ycl, last_bd4r)]:
                    map_delta = state_mapping_5[(last_ycl, last_bd4r)][(this_ycl, this_bd4r)]
                    if last_ycl == 0 and original_this_ycl != this_ycl:
                        # 避免连续3次平稳通过差值修正了当前的ycl状态，结合了场景5做出多余的动作
                        pass
                    else:
                        print(f'GLC stage5 hit')
                        this_delta = map_delta
                        global_result[CASE + '5-调整量不足'] = "调整量不足，补充动作"
                    trigger_scene_list.append(5)
            if (last_ycl, last_bd4r) in state_mapping_6:
                if (this_ycl, this_bd4r) in state_mapping_6[(last_ycl, last_bd4r)]:
                    direction = state_mapping_6[(last_ycl, last_bd4r)][(this_ycl, this_bd4r)]
                    if (direction == '+' and last_action > 0) or (direction == '-' and last_action < 0):
                        # 退回动作
                        if (this_ycl > 0 and this_d3lr_state == '上升') or (
                                this_ycl < 0 and this_d3lr_state == '下降'
                        ):
                            # D3LR没有拐头，不退
                            this_delta = 0
                            info = "D3LR没有拐，继续等待变化"
                        else:
                            # 否则退回动作
                            this_delta = -last_action
                            # 0716 退回要看d3lr是不是同向
                            if (this_delta < 0 and this_d3lr_state == '下降') or (
                                    this_delta > 0 and this_d3lr_state == '上升'
                            ):
                                this_delta = 0
                                info = "D3LR没有拐，继续等待变化"
                            else:
                                info = "上次调整后情况立即变好，D3LR拐头，退回动作"
                                is_revert = True
                        print(f'GLC stage6 hit {info}')
                        global_result[CASE + '6-调整后立即拐头'] = info
                        trigger_scene_list.append(6)

            """
            if last_ycl in state_mapping_7:
                if this_ycl in state_mapping_7[last_ycl]:
                    extra_delta = state_mapping_7[last_ycl][this_ycl]
                    print(f'stage7 hit')
                    this_delta = delta + extra_delta
                    global_result[CASE + '7'] = 7
            if (last_ycl, last_bd4r) in state_mapping_8:
                if (this_ycl, this_bd4r) in state_mapping_8[(last_ycl, last_bd4r)]:
                    direction = state_mapping_8[(last_ycl, last_bd4r)][(this_ycl, this_bd4r)]
                    print(f'stage8 hit')
                    this_delta = delta
                    global_result[CASE + '8'] = 8
            if (last_ycl, last_bd4r) in state_mapping_9:
                if (this_ycl, this_bd4r) in state_mapping_9[(last_ycl, last_bd4r)]:
                    extra_delta = state_mapping_9[(last_ycl, last_bd4r)][(this_ycl, this_bd4r)]
                    print(f'stage9 hit')
                    this_delta = delta + extra_delta
                    global_result[CASE + '9'] = 9

            if (last_ycl, last_bd4r) in state_mapping_10:
                if (this_ycl, this_bd4r) in state_mapping_10[(last_ycl, last_bd4r)]:
                    extra_delta = state_mapping_10[(last_ycl, last_bd4r)][(this_ycl, this_bd4r)]
                    print(f'stage10 hit')
                    this_delta = delta + extra_delta
                    global_result[CASE + '10'] = 10
            """

            if (last_ycl, last_bd4r) in state_mapping_7:
                if (this_ycl, this_bd4r) in state_mapping_7[(last_ycl, last_bd4r)]:
                    total_delta = state_mapping_7[(last_ycl, last_bd4r)][(this_ycl, this_bd4r)]
                    trigger_scene_list.append(7)
                    if (total_delta > 0 and is_bw1r_up) or (total_delta < 0 and is_bw1r_down):
                        pass
                    else:
                        print(f'GLC stage7 hit')
                        this_delta = total_delta - last_action
                        global_result[CASE + '7-BD4R导致引出量变化'] = '保证两次连续调整不超过1'

            """if (this_ycl, this_bd4r) in state_mapping_fast_1.get((last_ycl, last_bd4r), {}):
                this_delta = state_mapping_fast_1[(last_ycl, last_bd4r)][(this_ycl, this_bd4r)]
                print(f'stage fast 1 hit')
                if this_delta != 0:
                    global_result[CASE + 'fast1'] = '情况变坏，追加调整'
                else:
                    global_result[CASE + 'fast1'] = '情况变好，等待走稳'
            if (this_ycl, this_bd4r) in state_mapping_fast_2.get((last_ycl, last_bd4r), {}):
                action_map = state_mapping_fast_2[(last_ycl, last_bd4r)][(this_ycl, this_bd4r)]
                if last_action in action_map:
                    print(f'stage fast 2 hit')
                    this_delta = action_map[last_action]
                    if this_delta != 0:
                        global_result[CASE + 'fast2'] = '无变化，追加调整'
                    else:
                        global_result[CASE + 'fast2'] = '无变化，等待调整效果'"""

            # 场景8
            last_change, this_change = 0, 0
            is_hist = len(history) >= 2
            if is_hist:
                this_change = float(global_result["YCLJS.VALUE"]) - float(history[-1]['YCLJS.VALUE'])
                last_change = float(history[-1]['YCLJS.VALUE']) - float(history[-2]['YCLJS.VALUE'])
            change_delta = this_change - last_change
            if (this_ycl, this_bd4r) == (2, -1) or (this_ycl, this_bd4r) == (-2, 1):
                # 0716 如果引出量变化剧烈了，需要追加动作，保证两次调整到1开度
                trigger_scene_list.append(8)
                # 7/24 增加变化量与调整量关系
                if is_hist:
                    # 18分钟变化量与调整量
                    BASE_ACTION = 0.5
                    TOTAL_CHANGE_THRESHOLD1 = 3
                    TOTAL_ACTION_TRHESHOLD1 = 1
                    TOTAL_CHANGE_THRESHOLD2 = 4
                    TOTAL_ACTION_TRHESHOLD2 = 1.5
                    total_change = float(global_result["YCLJS.VALUE"]) - float(history[-3]['YCLJS.VALUE'])
                    last_2_action = float(history[-2]["action"])
                    total_action = last_2_action + last_action  # 前两次动作
                    print(f"GLC CASE8 total_change={total_change}, total_action={total_action}")
                    abs_total_change = abs(total_change)
                    if abs_total_change < TOTAL_CHANGE_THRESHOLD1:
                        action_threshold = BASE_ACTION
                    elif abs_total_change < TOTAL_CHANGE_THRESHOLD2:
                        action_threshold = TOTAL_ACTION_TRHESHOLD1
                    else:
                        action_threshold = TOTAL_ACTION_TRHESHOLD2
                    if this_ycl > 0 and change_delta > YCL_CHANGE_THRESHOLD:
                        # 避免出现0~1之外的值，例如上一个动作是回退
                        this_delta = max(-1.0, min(0.0, -action_threshold - last_action))
                        global_result["CASE8-快速变化场景"] = f"速度加剧，追加动作，保证2次和为{action_threshold}"
                    if this_ycl < 0 and change_delta < -YCL_CHANGE_THRESHOLD:
                        this_delta = min(1.0, max(0.0, action_threshold - last_action))
                        global_result["CASE8-快速变化场景"] = f"速度加剧，追加动作，保证2次和为{action_threshold}"

            # 场景9
            if (this_ycl, this_bd4r) == (2, -2) or (this_ycl, this_bd4r) == (-2, 2):
                last_3_history = history[-3:]
                last_3_states = tuple([state_2_num[his['YCLJS']] for his in last_3_history])
                last_3_actions = [float(his['action']) for his in last_3_history]
                if last_3_states in state_mapping_9_fast:
                    to_do_action = state_mapping_9_fast[last_3_states]
                    recent_3_delta = sum(last_3_actions)
                    if (0 < to_do_action <= recent_3_delta) or (
                            0 > to_do_action >= recent_3_delta):
                        info = f'未达到连续3次不动作，不追加调整，等待变化'
                    else:
                        # 0716 如果变化减缓了同样不执行
                        if is_hist and (
                                (this_ycl > 0 and change_delta < -YCL_CHANGE_THRESHOLD) or
                                (this_ycl < 0 and change_delta > YCL_CHANGE_THRESHOLD)
                        ):
                            this_delta = 0
                            info = f"变化已放缓，快速变化时不追加动作"
                        else:
                            this_delta = to_do_action
                            info = f'连续3次无改善，追加调整'
                    global_result[CASE + '9-连续3次快速变化'] = info
                    trigger_scene_list.append(9)
                    print("GLC", info)
            cur_ycl = global_result["YCLJS.VALUE"]
            print(f"GLC ######## index=1, last_action={last_action}, action={this_delta}, ycl={cur_ycl}")

            if (last_ycl, last_bd4r) in state_mapping_10:
                if (this_ycl, this_bd4r) in state_mapping_10[(last_ycl, last_bd4r)]:
                    direction = state_mapping_10[(last_ycl, last_bd4r)][(this_ycl, this_bd4r)]
                    if (direction == '+' and last_action > 0) or (direction == '-' and last_action < 0):
                        # 7/24 增加ycl差值校验
                        if this_ycl == 0:
                            last_ycl_value = last_history["YCLJS.VALUE"]
                            ycl_delta = this_ycl_value - last_ycl_value
                            if (last_ycl > 0 and ycl_delta < CASE_10_STABLE_THRESHOLD) or (
                                    last_ycl < 0 and ycl_delta > -CASE_10_STABLE_THRESHOLD):
                                # 退回动作
                                this_delta = -last_action
                                info = "上次调整后情况立即变好，退回动作"
                                print(f'GLC stage10 hit {info}')
                                global_result[CASE + '10-调整后立即拐头'] = info
                                trigger_scene_list.append(10)
                                is_revert = True
                            else:
                                this_delta = 0
                                info = "没有完全拐头，继续等待变化"
                                print(f'GLC stage10 hit {info}')
                                global_result[CASE + '10-调整后立即拐头'] = info
                                trigger_scene_list.append(10)
                        else:
                            # 退回动作
                            this_delta = -last_action
                            info = "上次调整后情况立即变好，退回动作"
                            print(f'GLC stage10 hit {info}')
                            global_result[CASE + '10-调整后立即拐头'] = info
                            trigger_scene_list.append(10)
                            is_revert = True

            state_11_dict = state_mapping_11.get((last_ycl, last_bd4r, last_d3lr, last_bw1r), {})
            if (this_ycl, this_bd4r, this_d3lr, this_bw1r) in state_11_dict:
                direction = state_11_dict[(this_ycl, this_bd4r, this_d3lr, this_bw1r)]
                if (direction == '+' and last_action > 0) or (direction == '-' and last_action < 0):
                    this_delta = 0
                    print(f'GLC stage11 hit')
                    global_result[CASE + '11-情况未变差避免过度调整'] = "避免过度调整，本次跳过"
                    trigger_scene_list.append(11)

            state_12_dict = state_mapping_12.get((last_ycl, last_bd4r, last_d3lr, last_bw1r), {})
            if (this_ycl, this_bd4r, this_d3lr, this_bw1r) in state_12_dict:
                this_delta = delta
                print(f'GLC stage12 hit')
                global_result[CASE + '12-温度趋势'] = "持续调整不等待"
                trigger_scene_list.append(12)

            state_13_dict = state_mapping_13.get((last_ycl, last_bd4r, last_d3lr), {})
            if (this_ycl, this_bd4r, this_d3lr) in state_13_dict:
                direction = state_13_dict[(this_ycl, this_bd4r, this_d3lr)]
                if (direction == '+' and last_action > 0) or (direction == '-' and last_action < 0):
                    this_delta = 0
                    print(f'GLC stage13 hit')
                    global_result[CASE + '13-情况未变差避免过度调整'] = "避免过度调整，本次跳过"
                    trigger_scene_list.append(13)

            state_14_dict = state_mapping_14.get((last_d3lr, last_bw1r), {})
            if (this_d3lr, this_bw1r) in state_14_dict:
                direction = state_14_dict[(this_d3lr, this_bw1r)]
                if (direction == '+' and last_action > 0) or (direction == '-' and last_action < 0):
                    # 退回动作
                    this_delta = -last_action
                    info = "上次调整后d3lr反向，退回动作"
                    print(f'GLC stage14 hit {info}')
                    global_result[CASE + '14-调整后d3lr立即拐头'] = info
                    trigger_scene_list.append(14)
                    is_revert = True

            state_15_dict = state_mapping_15.get((last_ycl, last_bd4r), {})
            if (this_ycl, this_bd4r) in state_15_dict:
                this_delta = 0
                info = "情况变好，本次不调整"
                trigger_scene_list.append(15)
                print(f'GLC stage15 hit')
                global_result[CASE + '15-情况变好等待进一步变化'] = info

            state_16_dict = state_mapping_16.get((last_ycl, last_bd4r, last_d3lr), {})
            if (this_ycl, this_bd4r, this_d3lr) in state_16_dict:
                to_do_action = state_16_dict[(this_ycl, this_bd4r, this_d3lr)]
                if last_action == 0:  # 7/26 修复加一等一bug
                    this_delta = to_do_action
                    print(f'GLC stage16 hit')
                    global_result[CASE + '16-加一等一'] = "D3LR没拐头，加一等一"
                    trigger_scene_list.append(16)

            state_17_dict = state_mapping_17.get((last_ycl, last_bd4r), {})
            if (this_ycl, this_bd4r) in state_17_dict:
                this_delta = state_17_dict[(this_ycl, this_bd4r)]
                print(f'GLC stage17 hit')
                global_result[CASE + '17-拐头'] = "ycl拐头，回调bd4r"
                trigger_scene_list.append(17)

            state_18_dict = state_mapping_18.get((last_ycl, last_bd4r), {})
            if (this_ycl, this_bd4r) in state_18_dict:
                direction = state_18_dict[(this_ycl, this_bd4r)]
                if (direction == '+' and last_action > 0) or (direction == '-' and last_action < 0):
                    this_delta = 0
                    print(f'GLC stage18 hit')
                    global_result[CASE + '18-调整过等待效果'] = "避免过度调整，本次跳过"
                    trigger_scene_list.append(18)

            state_19_dict = state_mapping_19.get((last_ycl, last_bd4r, last_d3lr), {})
            if (this_ycl, this_bd4r, this_d3lr) in state_19_dict:
                direction = state_19_dict[(this_ycl, this_bd4r, this_d3lr)]
                if (direction == '+' and last_action > 0) or (direction == '-' and last_action < 0):
                    this_delta = -last_action
                    print(f'GLC stage19 hit')
                    global_result[CASE + '19-调整立即变化'] = "D3LR拐头，退回上次动作"
                    trigger_scene_list.append(18)
                    is_revert = True

            # 上次如果是退回动作，本次不要同向
            if last_revert and ((this_delta > 0 and last_action > 0) or (this_delta < 0 and last_action < 0)):
                this_delta = 0
                info = "上个动作是退回，本次同向不执行"
                global_result["DEBUG-回退动作规避场景"] = info
                print("GLC ", info)

            if THREE_ACTION_SCENE in last_history and this_delta * last_action > 0:
                this_delta = 0
                info = "上个动作是连续3次误动作纠正，本次不连续调"
                global_result["DEBUG-连续三次无动作纠正后退避"] = info

            # 引出量上下限附近保护
            YCL_LIMIT_PROTECT_UP = 1044
            YCL_LIMIT_PROTECT_LOW = 1036
            this_bd4r_delta = this_bd4r_value - last_history["BD4R.VALUE"]
            if this_ycl_value >= YCL_LIMIT_PROTECT_UP and (this_ycl == -1 or this_ycl == 0) and this_delta > 0:
                if this_bd4r_delta >= 0:
                    global_result["CASE20-上限保护"] = f"bd4r差值={this_bd4r_delta}"
                    this_delta = 0
            elif this_ycl_value <= YCL_LIMIT_PROTECT_LOW and (this_ycl == 1 or this_delta == 0) and this_delta < 0:
                if this_bd4r_delta <= 0:
                    global_result["CASE20-下限保护"] = f"bd4r差值={this_bd4r_delta}"
                    this_delta = 0

            # 统一的bw1r保护，有方向时，所有修改造成的动作变化都不应该与bw1r同向
            action_delta = this_delta - delta
            if is_bw1r_up and action_delta > 0:
                info = f"GLC warning: BW1R方向与场景对动作的修改同向"
                print("GLC ", info)
                global_result["DEBUG-触发场景告警"] = info

        action_before_fix = this_delta
        SWITCH_YCL_ACTION_PROTECT = True
        YCL_ACTION_PROTECT_UP = 1042
        YCL_ACTION_PROTECT_LOW = 1039

        YCL_ACTION_PROTECT_UP2 = 1043.3
        YCL_ACTION_PROTECT_LOW2 = 1037.5

        try:
            if SWITCH_YCL_ACTION_PROTECT:
                # fix1
                if len(history) >= 2:
                    if 'CASE10-调整后立即拐头' in global_result and this_delta == -last_action:
                        if this_ycl_value <= YCL_ACTION_PROTECT_UP and this_delta < 0 and bd4r_delta < 0.04:
                            global_result["CASE-去除动作"] = f"BD4R未拉起，原来动作={action_before_fix}"
                            this_delta = 0
                        elif this_ycl_value >= YCL_ACTION_PROTECT_LOW and this_delta > 0 and bd4r_delta > -0.04:
                            global_result["CASE-去除动作"] = f"BD4R未压下去，原来动作={action_before_fix}"
                            this_delta = 0
                # fix2
                if len(history) >= 2:
                    YCL_LOW_DELTA = 0.5
                    if this_ycl_value <= YCL_ACTION_PROTECT_LOW2 and ycl_delta < YCL_LOW_DELTA and this_delta < 0 and bd4r_delta > -0.08:
                        global_result["CASE-去除动作"] = f"引出量低位保护，未明显上升，原来动作={action_before_fix}"
                        # 动作减半
                        this_delta = round(this_delta * 0.6, 1)
                    elif this_ycl_value >= YCL_ACTION_PROTECT_UP2 and ycl_delta > -YCL_LOW_DELTA and this_delta > 0 and bd4r_delta < 0.08:
                        global_result["CASE-去除动作"] = f"引出量高位保护，未明显下降，原来动作={action_before_fix}"
                        this_delta = round(this_delta * 0.6, 1)
        except Exception as e:
            print("GLC fix action exception", e)

        last_action = 0
        if len(history) > 0:
            last_history = history[-1]
            last_action = float(last_history['action'])
        this_delta = check_bl4sh(this_delta, get_time(data[-1]["time"]), global_result, last_action)

        # 增加限幅保护
        # 取28分钟反控属性数据，若当下动作为正，检查最小值到现在的距离，如何加上准备执行动作之后超过阈值，限制执行
        cur_time = get_time(data[-1]['time']) + datetime.timedelta(seconds=10)
        before_limit = this_delta
        if this_delta != 0:
            bd4r_value = global_result["BD4R.VALUE"]
            hist_delta, this_delta = action_protect(cur_time, this_delta, bd4r_value)
            if before_limit != this_delta:
                global_result[
                    "DEBUG-LIMIT"] = f"限幅保护(已调整{hist_delta}, BD4R={bd4r_value})，{before_limit} -> {this_delta}"
                print(f"GLC 触发限幅保护，已调整{hist_delta}, bd4r={bd4r_value}, {before_limit} -> {this_delta}")

        # MSU调整场景 取10分钟内变化量
        msu_delta = get_msu_delta(cur_time)
        global_result["MSU_DELTA"] = msu_delta

        if is_revert and this_delta * last_action > 0:
            # 回退被优先级更高的场景取代了
            is_revert = False
        if is_revert and this_delta == 0:
            print("GLC 回退动作被限幅")
            is_revert = False
        global_result["REVERT"] = is_revert

        before_msu_limit = this_delta
        if (msu_delta > 140 and this_delta < 0) or (msu_delta < -140 and this_delta > 0):
            # if USE_MSU_STRATEGY == 1:
            #     this_delta = min(this_delta + MSU_OFFSET, 0)
            # else:
            #     this_delta = 0
            msu_hist_action, this_delta = limit_action(cur_time, this_delta, MSU_TIME_WINDOW, MSU_ACTION_LIMIT)
            global_result[
                "MSU调整限幅"] = f"GLC 触发MSU场景限幅保护，已调整{msu_hist_action}, {before_msu_limit} -> {this_delta}"

        SWITCH_ARTIFICIAL = True
        # 记录当下开度
        try:
            if SWITCH_ARTIFICIAL:
                bl4sh_data = get_data('8', "BL4SHPC", get_time_str(cur_time - datetime.timedelta(minutes=2)),
                                      get_time_str(cur_time), True)
                cur_bl4sh = round(float(bl4sh_data[-1]['value']), 2)
                if history:
                    bl4sh_after_last_action = history[-1].get("BL4SH_AFTER_THIS", cur_bl4sh)
                    if abs(cur_bl4sh - bl4sh_after_last_action) > 0.3:
                        global_result["人工操作退避"] = f"发生人工干预，本次不调，原先动作为{this_delta}"
                        this_delta = 0

                bl4sh_after_this = cur_bl4sh + this_delta
                global_result["BL4SH_AFTER_THIS"] = bl4sh_after_this

        except Exception as e:
            print("get bl4sh after except", e)

        offset = -first_delta + this_delta - delta
        global_result['THIS_ACTION'] = this_delta
        global_result['RULE_ACTION'] = delta
        global_result["multi"] = 0
        global_result["delta"] = offset
        global_result["触发场景"] = trigger_scene_list

        # 用于测试
        outer.outer_delta = this_delta

        this_history = {}
        this_history.update(global_result)
        this_history['action'] = this_delta
        history.append(this_history)
        last_states[INDEX_HISTORY] = history
    except Exception as e:
        print("do_second encounter exception", e)
        traceback.print_exc()


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
    window = 15
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


def check_bl4sh(action_before, current_time, global_result, last_action=0):
    try:
        debug_info = {}
        start_time = get_time_str(current_time - datetime.timedelta(minutes=90))
        end_time = get_time_str(current_time + datetime.timedelta(minutes=1))
        ycl_data = get_data("9", "YCL.UNIQUE", start_time, end_time)
        ycl_data = abandon_abnormal_ycl(ycl_data)
        ycl_df = pd.DataFrame(ycl_data)
        ycl_time = list(ycl_df.iloc[:, 0])
        ycl_filtered_values = savgol_filter(ycl_df.iloc[:, 1], window_length=51, polyorder=3)

        start_time = get_time_str(current_time - datetime.timedelta(minutes=180))
        end_time = get_time_str(current_time + datetime.timedelta(minutes=1))
        bd4r_data = get_data("9", "BD4R.UNIQUE", start_time, end_time)
        bd4r_df = pd.DataFrame(bd4r_data)
        bd4r_filtered_values = savgol_filter(bd4r_df.iloc[:, 1], window_length=51, polyorder=3)
        bd4r_df['value'] = bd4r_filtered_values
        bw1r_data = get_data("9", "BW1R.UNIQUE", start_time, end_time)
        bw1r_df = pd.DataFrame(bw1r_data)
        bw1r_filtered_values = savgol_filter(bw1r_df.iloc[:, 1], window_length=51, polyorder=3)
        current_ycl = round(ycl_filtered_values[-1], 2)
        bw1r_delta_15min = round(bw1r_filtered_values[-1] - bw1r_filtered_values[-31], 2)
        turning_index = find_ycl_turning_point(ycl_filtered_values)
        if not turning_index:  # 1小时内持续趋势没有拐点
            turning_index = 0
        turning_time = ycl_time[turning_index]
        turning_value = round(ycl_filtered_values[turning_index], 2)
        trend_delta = current_ycl - turning_value
        trend_points = len(ycl_filtered_values) - turning_index
        trend_minutes = int((current_time - get_time(turning_time)).seconds / 60)
        cur_time = ycl_time[-1]
        info = f"GLC 上个拐点时间: {turning_time}, 值为:{turning_value}，当前时间: {cur_time}, 当前值: {current_ycl}"
        debug_info["上个拐点"] = info
        print(info)
        fixed_interval = 21
        ycl_interval = fixed_interval
        bd4r_interval = 21
        bd4r_interval_short = 11
        if trend_points < fixed_interval:
            ycl_interval = trend_points
        ycl_slope, _, _, _ = linear_regression(ycl_filtered_values[-ycl_interval:])
        ycl_slope_short, _, _, _ = linear_regression(ycl_filtered_values[-bd4r_interval_short:])
        bd4r_slope, _, _, _ = linear_regression(bd4r_filtered_values[-bd4r_interval:])
        bd4r_slope_short, _, _, _ = linear_regression(bd4r_filtered_values[-bd4r_interval_short:])
        bw1r_slope, _, _, _ = linear_regression(bw1r_filtered_values[-41:])
        ycl_slope = round(ycl_slope * 2 * 10, 2)

        ###
        """for i in range(20):
            time_i = current_time-datetime.timedelta(minutes=i*6-2)
            bw1r_slope_i, mse_i, mean_dis_i, _ = linear_regression(bw1r_filtered_values[-41-i*12:len(bw1r_filtered_values)-i*12])
            bw1r_slope_i = round(bw1r_slope_i * 20, 3)
            mse_i = round(mse_i * 10000, 3)
            mean_dis_i = round(mean_dis_i * 10000, 3)
            is_positive = abs(bw1r_slope_i) >= 0.02
            if is_positive:
                print(f"bw1r slope at {time_i} = {bw1r_slope_i}, {mse_i}, positive = {is_positive}")
            else:
                print(f"bw1r slope at {time_i} = {bw1r_slope_i}, {mse_i}")"""
        ###

        ycl_slope_short = round(ycl_slope_short * 2 * 10, 2)
        bd4r_slope = round(bd4r_slope * 2 * 10, 3)
        bd4r_slope_short = round(bd4r_slope_short * 2 * 10, 3)
        bw1r_slope = round(bw1r_slope * 2 * 10, 4)
        info = (f"GLC ycl {(ycl_interval - 1) / 2}分钟斜率: {ycl_slope},"
                f" 5分钟斜率 {ycl_slope_short}, bd4r {(bd4r_interval - 1) / 2} 分钟斜率: {bd4r_slope},"
                f" 5分钟斜率: {bd4r_slope_short}, bw1r变化:{bw1r_delta_15min}, 10分钟斜率: {bw1r_slope}")

        is_positive = abs(bw1r_slope) >= BW1R_SLOPE_THRESHOLD
        print(info)
        debug_info["DEBUG-检查bd4r场景斜率情况"] = info

        new_action = action_before
        bd4r_scene_4 = False
        BW1R_15MIN_THRESHOLD = 0.04
        # 场景1 引出量在一定幅度以内，不要让bd4r斜率加剧
        if 0 < ycl_slope < YCL_CHECK_THRESHOLD_1 and bd4r_slope < -BD4R_CHECK_THRESHOLD_1:
            if action_before < 0 and bw1r_delta_15min < BW1R_15MIN_THRESHOLD:
                if global_result['YCLJS'] != "快速上升":
                    new_action = 0
                    print(f"GLC 场景一触发，不继续加大bd4r斜率")
                    debug_info["DEBUG-检查bd4r场景"] = "GLC 场景一触发，不继续加大bd4r斜率"
        elif YCL_CHECK_THRESHOLD_1 <= ycl_slope < YCL_CHECK_THRESHOLD_3 and bd4r_slope < -BD4R_CHECK_THRESHOLD_3:
            if action_before < 0 and bw1r_delta_15min < BW1R_15MIN_THRESHOLD:
                if global_result['YCLJS'] != "快速上升":
                    new_action = 0
                    print(f"GLC 场景三触发，不继续加大bd4r斜率")
                    debug_info["DEBUG-检查bd4r场景"] = "GLC 场景三触发，不继续加大bd4r斜率"
        if 0 < ycl_slope < YCL_CHECK_THRESHOLD_2 and bd4r_slope <= -BD4R_CHECK_THRESHOLD_2:
            if action_before <= 0:
                new_action = +0.5
                print(f"GLC 场景二触发，bd4r斜率过大回调")
                debug_info["DEBUG-检查bd4r场景"] = "GLC 场景二触发，bd4r斜率过大回调"
            if current_ycl >= YCL_OUT_UPPER_BOUND:  # 10/12: 超过一定值场景二不要加那么多
                new_action = round(new_action * 0.6, 1)
        if ycl_slope > 0 and bd4r_slope > 0 and action_before > 0:
            new_action = 0
            print(f"GLC 场景三触发，拐头不加剧bd4r")
            debug_info["DEBUG-检查bd4r场景"] = f"GLC 场景三触发，拐头不加剧bd4r"
        if ycl_slope > YCL_CHECK_THRESHOLD_4 and bd4r_slope > BD4R_CHECK_THRESHOLD_4:
            bd4r_scene_4 = True
            if action_before >= 0:
                new_action = -0.5
                print(f"GLC 场景四触发，同向变化调整")
                debug_info["DEBUG-检查bd4r场景"] = f"GLC 场景四触发，同向变化调整"

        if -YCL_CHECK_THRESHOLD_1 < ycl_slope < 0 and bd4r_slope > BD4R_CHECK_THRESHOLD_1:
            if action_before > 0 and bw1r_delta_15min > -BW1R_15MIN_THRESHOLD:
                if global_result['YCLJS'] != "快速下降":
                    new_action = 0
                    print(f"GLC 场景一触发，不继续加大bd4r斜率")
                    debug_info["DEBUG-检查bd4r场景"] = "GLC 场景一触发，不继续加大bd4r斜率"
        elif -YCL_CHECK_THRESHOLD_3 < ycl_slope <= -YCL_CHECK_THRESHOLD_1 and bd4r_slope > BD4R_CHECK_THRESHOLD_3:
            if action_before > 0 and bw1r_delta_15min > -BW1R_15MIN_THRESHOLD:
                if global_result['YCLJS'] != "快速下降":
                    new_action = 0
                    print(f"GLC 场景三触发，不继续加大bd4r斜率")
                    debug_info["DEBUG-检查bd4r场景"] = "GLC 场景三触发，不继续加大bd4r斜率"
        if -YCL_CHECK_THRESHOLD_2 < ycl_slope < 0 and bd4r_slope >= BD4R_CHECK_THRESHOLD_2 and action_before >= 0:
            new_action = -0.5
            print(f"GLC 场景二触发，bd4r斜率过大回调")
            debug_info["DEBUG-检查bd4r场景"] = "GLC 场景二触发，bd4r斜率过大回调"
        if ycl_slope < 0 and bd4r_slope < 0 and action_before < 0:
            new_action = 0
            print(f"GLC 场景三触发，拐头不加剧bd4r")
            debug_info["DEBUG-检查bd4r场景"] = f"GLC 场景三触发，拐头不加剧bd4r"
        if ycl_slope < -YCL_CHECK_THRESHOLD_4 and bd4r_slope < -BD4R_CHECK_THRESHOLD_4:
            bd4r_scene_4 = True
            if action_before <= 0:
                new_action = +0.5
                print(f"GLC 场景四触发，同向变化调整")
                debug_info["DEBUG-检查bd4r场景"] = f"GLC 场景四触发，同向变化调整"
        info = f"GLC 检查前动作: {action_before}, 检查后动作: {new_action}"
        print(info)
        debug_info["DEBUG-检查bd4r"] = info

        ycl_delta = trend_delta
        time_window_minutes = trend_minutes + 10

        # 检查功率
        # try:
        #     sum2_data = get_data('9', "SUM2.UNIQUE", get_time_str(current_time - datetime.timedelta(minutes=30)),
        #                          get_time_str(current_time + datetime.timedelta(minutes=1)))
        #     # 取6分钟差值，判断方向
        #     # 变化0.4kW，对应BLSH的0.5开度
        #     sum2_values = pd.DataFrame(sum2_data).iloc[:, 1].values
        #     sum2_minutes = 6
        #     sum2_delta = round(sum2_values[-1] - sum2_values[-(2 * sum2_minutes + 1)], 2)
        #     action_before_sum2 = new_action
        #     if new_action > 0 and sum2_delta <= -SUM2_DELTA_THRESHOLD1:
        #         if not bd4r_scene_4 and ycl_slope >= -YCL_CHECK_THRESHOLD_2:
        #             new_action = 0
        #     elif new_action < 0 and sum2_delta >= SUM2_DELTA_THRESHOLD1:
        #         if not bd4r_scene_4 and ycl_slope <= YCL_CHECK_THRESHOLD_2:
        #             new_action = 0
        #     # if new_action == 0 and ycl_slope >= YCL_CHECK_THRESHOLD_4 and sum2_delta <= -SUM2_DELTA_THRESHOLD2:
        #     #     # 引出量快速上升，检查bd4r斜率是否快速向下
        #     #     if bd4r_slope >= -BD4R_CHECK_SUM2_THRESHOLD:
        #     #         action_unit = int(abs(sum2_delta) / SUM2_DELTA_THRESHOLD2)
        #     #         new_action = -0.5 * action_unit
        #     # if new_action == 0 and ycl_slope <= -YCL_CHECK_THRESHOLD_4 and sum2_delta >= SUM2_DELTA_THRESHOLD2:
        #     #     if bd4r_slope <= BD4R_CHECK_SUM2_THRESHOLD:
        #     #         action_unit = int(abs(sum2_delta) / SUM2_DELTA_THRESHOLD2)
        #     #         new_action = +0.5 * action_unit
        #     debug_info[
        #     # global_result[
        #         "SUM2检查"] = f"GLC 功率{sum2_minutes}分钟变化{sum2_delta}，检查前动作{action_before_sum2}，检查后动作{new_action}"
        #     print(f"GLC 功率{sum2_minutes}分钟变化{sum2_delta}，检查前动作{action_before_sum2}，检查后动作{new_action}")
        # except Exception as e:
        #     print("GLC get sum2 record error", e)

        # 根据引出量位置增加额外的调整量
        MIN_ACTION = 0.3
        if current_ycl >= YCL_UPPER_BOUND and new_action < 0:
            new_action = max(-1.0, new_action - EXTRA_ACTION_UPPER)
        elif current_ycl <= YCL_LOWER_BOUND and new_action > 0:
            new_action = min(+1.0, new_action + EXTRA_ACTION_LOWER)
        if current_ycl >= YCL_OUT_UPPER_BOUND and new_action > MIN_ACTION:
            new_action = max(MIN_ACTION, new_action - DECREASE_ACTION_UPPER)
        elif current_ycl <= YCL_OUT_LOWER_BOUND and new_action < -MIN_ACTION:
            new_action = min(-MIN_ACTION, new_action + DECREASE_ACTION_LOWER)
        new_action = round(new_action, 2)

        before_bw1r = new_action
        negative_delta = 0.2
        if not is_positive:
            # 幅度减小0.2
            if abs(new_action) > MIN_ACTION:
                if new_action > 0:
                    new_action = new_action - negative_delta
                else:
                    new_action = new_action + negative_delta
        info = f"GLC BW1R斜率:{bw1r_slope}({BW1R_SLOPE_THRESHOLD}) 检查前动作:{before_bw1r}, 检查后动作{new_action}"
        debug_info["BW1R稳定场景"] = info
        print(info)

        # F2R1RB趋势判断是否要回调
        start_time = get_time_str(current_time - datetime.timedelta(minutes=130))
        end_time = get_time_str(current_time - datetime.timedelta(minutes=120))
        print(f"GLC F2R1RB time is {start_time} ~ {end_time}")
        f2r1rb_data = get_data("9", "F2R1RB", start_time, end_time)
        f2r1rb_df = pd.DataFrame(f2r1rb_data)
        f2r1rb_filtered_values = f2r1rb_df.iloc[:, 1]
        f2r1rb_slope, _, _, _ = linear_regression(f2r1rb_filtered_values)
        f2r1rb_slope = round(f2r1rb_slope * 2 * 10, 3)  # 折合成10分钟变化率
        ycl_30min_delta = round(current_ycl - ycl_filtered_values[-61], 2)
        ycl_max = round(max(ycl_filtered_values[-61:]), 2)
        ycl_min = round(min(ycl_filtered_values[-61:]), 2)
        before_temp = new_action
        if ycl_30min_delta > 2 and new_action > 0 and current_ycl - ycl_max > -1:
            # 趋势未反转，来料温度也没有拐头
            if not (f2r1rb_slope < -F2R1RB_THRESHOLD):
                new_action = round(new_action / 2, 1)
        elif ycl_30min_delta < -2 and new_action < 0 and current_ycl - ycl_min < 1:
            if not (f2r1rb_slope > F2R1RB_THRESHOLD):
                new_action = round(new_action / 2, 1)
        info = (f"GLC F2R1RB 130分钟前斜率: {f2r1rb_slope}, ycl30分钟变化{ycl_30min_delta},"
                f"最大值{ycl_max},最小值{ycl_min},当前值{current_ycl},来料检查前{before_temp},检查后{new_action}")
        debug_info["DEBUG-F2R1RB"] = info
        print(info)

        action_filtered = new_action
        hist_action = 0
        if (ycl_slope > 0 and bd4r_slope > 0 and last_action >= 0) or (
                ycl_slope < 0 and bd4r_slope < 0 and last_action <= 0):
            pass
        else:
            if new_action > 0 and bd4r_slope >= -BD4R_ACTION_THRESHOLD:
                # 检查ycl掉了多少
                # ycl_delta = ycl_filtered_values[-1] - max(ycl_data_20min)
                if ycl_delta >= -YCL_DELTA_THRESHOLD1:
                    hist_action, action_filtered = limit_action(current_time, new_action,
                                                                time_window=time_window_minutes,
                                                                action_threshold=BLSH_DELTA_THRESHOLD1)
                elif ycl_delta >= -YCL_DELTA_THRESHOLD2:
                    hist_action, action_filtered = limit_action(current_time, new_action,
                                                                time_window=time_window_minutes,
                                                                action_threshold=BLSH_DELTA_THRESHOLD2)
                elif ycl_delta >= -YCL_DELTA_THRESHOLD3:
                    hist_action, action_filtered = limit_action(current_time, new_action,
                                                                time_window=time_window_minutes,
                                                                action_threshold=BLSH_DELTA_THRESHOLD3)
            elif new_action < 0 and bd4r_slope <= BD4R_ACTION_THRESHOLD:
                # ycl_delta = ycl_filtered_values[-1] - min(ycl_data_20min)
                if ycl_delta <= YCL_DELTA_THRESHOLD1:
                    hist_action, action_filtered = limit_action(current_time, new_action,
                                                                time_window=time_window_minutes,
                                                                action_threshold=BLSH_DELTA_THRESHOLD1)
                elif ycl_delta <= YCL_DELTA_THRESHOLD2:
                    hist_action, action_filtered = limit_action(current_time, new_action,
                                                                time_window=time_window_minutes,
                                                                action_threshold=BLSH_DELTA_THRESHOLD2)
                elif ycl_delta <= YCL_DELTA_THRESHOLD3:
                    hist_action, action_filtered = limit_action(current_time, new_action,
                                                                time_window=time_window_minutes,
                                                                action_threshold=BLSH_DELTA_THRESHOLD3)
        info = f"GLC 调整量检查前: {new_action}, 已调整{hist_action}， 检查后动作: {action_filtered}"
        print(info)
        debug_info["DEBUG-检查调整量"] = info

        # 超过一定时间趋势没有足够的对抗，补充0.2/0.3的动作，放在动作限幅之后，用来兜底
        try:
            ycl_comp_delta = round(ycl_filtered_values[-1] - ycl_filtered_values[-(2 * COMP_YCL_MINUTE) - 1], 2)
            bd4r_comp_delta = round(bd4r_filtered_values[-1] - bd4r_filtered_values[-(2 * COMP_BD4R_MINUTE) - 1], 2)
            before_comp = action_filtered
            if (ycl_comp_delta > COMP_YCL_DELTA_THRESHOLD and ycl_slope > COMP_YCL_SLOPE_THRESHOLD
                    and not (bd4r_comp_delta < -COMP_BD4R_DELTA_THRESHOLD or bd4r_slope < -COMP_BD4R_SLOPE_THRESHOLD)
                    and action_filtered == 0):
                if last_action < 0:
                    action_filtered = round(min(0.0, -COMP_ACTION - last_action), 1)
                else:
                    action_filtered = -COMP_ACTION
                # if last_action >= 0:  # and current_ycl > 1038?
                #     action_filtered = -COMP_ACTION
            elif (ycl_comp_delta < -COMP_YCL_DELTA_THRESHOLD and ycl_slope < -COMP_YCL_SLOPE_THRESHOLD
                  and not (bd4r_comp_delta > COMP_BD4R_DELTA_THRESHOLD or bd4r_slope > COMP_BD4R_SLOPE_THRESHOLD)
                  and action_filtered == 0):
                if current_ycl < 1043:
                    # if last_action <= 0 and current_ycl < 1043:
                    #     action_filtered = +COMP_ACTION
                    if last_action > 0:
                        action_filtered = round(max(0.0, +COMP_ACTION - last_action), 1)
                    else:
                        action_filtered = +COMP_ACTION
            info = (f"GLC ycl_{COMP_YCL_MINUTE}min_delta={ycl_comp_delta}({COMP_YCL_DELTA_THRESHOLD}), ycl_slope={ycl_slope}({COMP_YCL_SLOPE_THRESHOLD}), "
                    f"bd4r_{COMP_BD4R_MINUTE}min_delta={bd4r_comp_delta}({COMP_BD4R_DELTA_THRESHOLD}), bd4r_slope={bd4r_slope}({COMP_BD4R_SLOPE_THRESHOLD}), "
                    f"last_action={last_action}, 检查前动作:{before_comp}, 检查后:{action_filtered}")
            print(info)
            debug_info["DEBUG-长时间无对抗检查"] = info

            # 联合场景识别1：供料槽没必要再调
            BIG_TREND_KEY = "BIG_TREND"
            BIG_TREND_BD4R_THRESHOLD = 0.35  # TODO 待定
            bd4r_30min_delta = round(bd4r_filtered_values[-1] - bd4r_filtered_values[-61], 2)
            if ycl_delta > COMP_YCL_DELTA_THRESHOLD and trend_minutes >= 30 \
                    and ycl_slope > COMP_YCL_SLOPE_THRESHOLD and bd4r_30min_delta < -BIG_TREND_BD4R_THRESHOLD:
                # set flag
                default_cache.set(BIG_TREND_KEY, get_time_str(current_time), 60 * 60)
                debug_info["DEBUG-大趋势设置flag"] = True
                print("GLC 大趋势设置flag")
            elif ycl_delta < -COMP_YCL_DELTA_THRESHOLD and trend_minutes >= 30 \
                    and ycl_slope < -COMP_YCL_SLOPE_THRESHOLD and bd4r_30min_delta > +BIG_TREND_BD4R_THRESHOLD:
                default_cache.set(BIG_TREND_KEY, get_time_str(current_time), 60 * 60)
                debug_info["DEBUG-大趋势设置flag"] = True
                print("GLC 大趋势设置flag")
            else:
                # 否则清除flag
                default_cache.delete(BIG_TREND_KEY)

        #     # 联合场景识别2：供料槽调了效果不明显
        #     start_time = get_time_str(current_time - datetime.timedelta(minutes=180))
        #     end_time = get_time_str(current_time + datetime.timedelta(minutes=1))
        #     actual_bl4sh_data = get_data("7", "PC2_BL4SH.PIDA.OP", start_time, end_time)
        #     # 反馈 + 评价
        #     # 找到一个动作：条件是 前半小时无动作，后10分钟无动作
        #     action_df = find_action(actual_bl4sh_data)
        #     # print(action_df)
        #     feedback_factor_key = "GLC_FEEDBACK_FACTOR_V1"
        #     current_feedback_factor = default_cache.get(feedback_factor_key, None)
        #     if len(action_df) > 0:
        #         action = action_df.iloc[0]
        #         action_time = action['time_']
        #         action_delta = action['diff']
        #         bd4r_df['time_'] = pd.to_datetime(bd4r_df['time'])
        #         slope_before = round(get_slope(bd4r_df, action_time), 3)
        #         slope_after = round(get_slope(bd4r_df, action_time + pd.Timedelta(minutes=17)), 3)
        #         slope_delta = slope_after - slope_before
        #         action_effect = round(slope_delta / action_delta, 3)  # 动作起的效果 / 动作大小
        #         print(
        #             f"action time={action_time}, action={action_delta}, bd4r slope before={slope_before}, slope after={slope_after}, action effect={action_effect}")
        # # 场景识别3：供料槽调了就有效果

        except Exception as e:
            print("长期无对抗场景异常", e)
            traceback.print_exc()

        # 过高或过低补动作，往中心值拉
        # ycl超过1047，上一次无动作，当前非下降，执行-0.8
        try:
            CENTER_KEY = "GLC_CENTER_ACTION"  # 保留10分钟
            before_center = action_filtered
            last_center_action = default_cache.get(CENTER_KEY, None)
            CENTER_AVOID_MINUTE = 22

            if current_ycl >= YCL_PROTECT_UPPER and not last_center_action:
                if global_result["YCLJS"].find("下降") < 0:
                    # if action_filtered >= 0:
                    if last_action < 0:
                        action_filtered = round(min(0.0, -1 - last_action), 1)
                    else:
                        action_filtered = -YCL_PROTECT_ACTION_UPPER
                default_cache.set(CENTER_KEY, action_filtered, CENTER_AVOID_MINUTE * 60)
            elif current_ycl <= YCL_PROTECT_LOWER and not last_center_action:
                if global_result["YCLJS"].find("上升") < 0:
                    # if action_filtered <= 0:
                    if last_action > 0:
                        action_filtered = round(max(0.0, +1 - last_action), 1)
                    else:
                        action_filtered = +YCL_PROTECT_ACTION_LOWER
                    default_cache.set(CENTER_KEY, action_filtered, CENTER_AVOID_MINUTE * 60)
            # 退避期间1040以下时 不下调
            info1 = ""
            if last_center_action and current_ycl < 1040 and action_filtered < 0:
                action_filtered = 0
                info1 = f", 1040以下，下调动作退避"
            info = f"GLC ycl={current_ycl},中心值检查前动作:{before_center},检查后:{action_filtered} {info1}"
            debug_info["DEBUG-中心值"] = info
            print(info)
        except Exception as e:
            print("中心值场景异常", e)
            traceback.print_exc()

        global_result['DEBUG-INFO'] = debug_info
        return action_filtered
    except Exception as e:
        print("未捕获的check_bl4sh异常", e)
        traceback.print_exc()
        return action_before


def get_slope(df, slope_time, minutes=10):
    slope_start = slope_time - pd.Timedelta(minutes=minutes)
    values = df[(df['time_'] >= slope_start) & (df['time_'] <= slope_time + pd.Timedelta(minutes=1))]
    slope, _, _, _ = linear_regression(values.loc[:, 'value'])
    return slope * 2 * 10


def find_action(bl4sh_data):
    df = pd.DataFrame(bl4sh_data)
    df['diff'] = df['value'].diff().round(1)
    filtered_df = df[(df['diff'].notna()) & (df['diff'].abs() > 0.2)].copy()  # copy()避免对view操作
    filtered_df['time_'] = pd.to_datetime(filtered_df['time'])
    threshold = pd.Timedelta(minutes=2)
    filtered_df['is_close'] = filtered_df['time_'].diff() < threshold
    groups = (filtered_df['is_close'] != True).cumsum()
    merged_diff_df = filtered_df.groupby(groups).agg({'time_': 'first', 'diff': 'sum'}).reset_index(drop=True).copy()
    forward_threshold = pd.Timedelta(minutes=30)
    backward_threshold = pd.Timedelta(minutes=10)
    merged_diff_df['diff_forward'] = merged_diff_df['time_'].diff()
    merged_diff_df['diff_backward'] = merged_diff_df['diff_forward'].shift(-1)
    action_df = merged_diff_df[
        (merged_diff_df['diff_forward'] > forward_threshold) & (merged_diff_df['diff_backward'] > backward_threshold)]
    return action_df[['time_', 'diff']]


def get_msu_delta(cur_time):
    msu_data = get_data('7', 'PC3_MU1L.PIDA.SP', get_time_str(cur_time - datetime.timedelta(minutes=MSU_EFFECT_MIN)),
                        get_time_str(cur_time))
    msu_values = np.array([float(item['value']) for item in msu_data])
    max_time_index = np.argmax(msu_values)
    min_time_index = np.argmin(msu_values)
    max_time = msu_data[max_time_index]['time']
    min_time = msu_data[min_time_index]['time']
    if msu_values[max_time_index] == msu_values[-1]:
        max_time_index = -1
    if msu_values[min_time_index] == msu_values[-1]:
        min_time_index = -1
    last_index = max(max_time_index, min_time_index)
    msu_delta = msu_values[-1] - msu_values[last_index]
    print(f"GLC msu maxtime={max_time}, mintime={min_time}, last_index={last_index}, msu_delta={msu_delta}")
    return msu_delta


def limit_action(cur_time, this_delta, time_window, action_threshold):
    """
    限制动作幅度，根据时间窗内内允许的变化幅度进行限制
    """
    # TODO 人工退避不要计入历史动作里
    auto_data = get_data("8", "AUTO_GL", get_time_str(cur_time - datetime.timedelta(minutes=2)), get_time_str(cur_time))
    is_auto = float(auto_data[-1]['value']) == 0
    if is_auto:
        bl4sh_data = get_data('7', "PC2_BL4SH.PIDA.OP",
                              get_time_str(cur_time - datetime.timedelta(minutes=time_window)),
                              get_time_str(cur_time))
    else:
        bl4sh_data = get_data('8', "BL4SHPC", get_time_str(cur_time - datetime.timedelta(minutes=time_window)),
                              get_time_str(cur_time), True)
    bl4sh_data = [float(item["value"]) for item in bl4sh_data]
    if this_delta > 0:
        hist_delta = round(bl4sh_data[-1] - np.min(bl4sh_data), 1)
        if hist_delta > action_threshold:
            this_delta = 0
        elif this_delta + hist_delta > action_threshold:
            this_delta = round(action_threshold - hist_delta, 1)
    else:
        hist_delta = round(bl4sh_data[-1] - np.max(bl4sh_data), 1)
        if hist_delta < -action_threshold:
            this_delta = 0
        elif this_delta + hist_delta < -action_threshold:
            this_delta = round(-action_threshold - hist_delta, 1)
    return hist_delta, this_delta


def action_protect(cur_time, this_delta, cur_bd4r):
    hist_delta, this_delta = limit_action(cur_time, this_delta, time_window=LIMIT_TIME,
                                          action_threshold=GLC_ACTION_THRESHOLD)

    # 0718 增加bd4r保护
    if cur_bd4r >= BD4R_LIMIT_HIGH and this_delta > 0:
        this_delta = 0
    elif cur_bd4r <= BD4R_LIMIT_LOW and this_delta < 0:
        this_delta = 0
    return hist_delta, this_delta


def do_third(global_result, last_states):
    # clear context
    # aging
    # 第三次处理
    global_result.update({"multi": 1, "delta": 0})
    history = last_states.get(INDEX_HISTORY, [])
    # update cache
    retain_num = 10
    # up to down
    history = history[-retain_num:]
    last_states[INDEX_HISTORY] = history


def update_index(index_state, index):
    index_state[KEY_WORD] = index


def do(data, global_result: dict):
    config = get_config(ALARM_RULE_ID)
    action_key = f"{ALARM_RULE_ID}_actions_v1"
    state_key = f"{ALARM_RULE_ID}_states_v1"
    index_key = f"{ALARM_RULE_ID}_state"

    last_action = default_cache.get(action_key, "")
    last_states = json.loads(default_cache.get(state_key, "{}"))
    index_state = json.loads(default_cache.get(index_key, "{}"))
    # print(f"    last_states={last_states}, last_action={last_action}, index_state={index_state}")

    if INDEX_HISTORY not in last_states:
        last_states[INDEX_HISTORY] = []

    last_index = index_state.get(KEY_WORD, -1)
    global_result["last_index"] = last_index  # 界面上展示的状态

    this_action = query_actions(global_result, ALARM_RULE_ID)
    # 计算此次调控量
    delta = get_delta(this_action, global_result)
    update_bl4shpc(global_result, delta)
    if last_index == -1:
        update_index(index_state, 1)
        do_first(global_result, delta)
        delta = 0
    elif last_index == 1:
        update_index(index_state, 2)
        do_second(last_action, global_result, last_states, delta, data)
    elif last_index == 2:
        update_index(index_state, -1)
        do_third(global_result, last_states)

    default_cache.set(action_key, str(delta), TTL)
    default_cache.set(state_key, json.dumps(last_states), TTL)
    default_cache.set(index_key, json.dumps(index_state), TTL)

def update_bl4shpc(global_result, delta):
    start = global_result.get("start")
    end = global_result.get("end")
    set_calculated_data("BL4SHPC", start, end, delta)

def get_delta(actions, global_result):
    delta = 0
    for attr, action in actions.items():
        formula = action["变化量"]  # @{BL1SHPC}+@{delta}-1.00+@{NEG_FACTOR}
        # prop = action["反控属性"]
        matches = PATTERN.findall(formula)
        # print(f'    formula={formula}')
        if matches:
            # print(matches)
            phase = "0+" + " ".join([f"{ele[0]}{ele[1]}" for ele in matches])
            if '@{NEG_FACTOR}' in formula:
                phase = phase + "+" + str(global_result['NEG_FACTOR'])
            if '@{POS_FACTOR}' in formula:
                phase = phase + "+" + str(global_result['POS_FACTOR'])
            delta = eval(phase)
            # print("    phase=", phase)
        else:
            delta = 0
        # 供料槽动作是重复的计算完一个调控量后退出
        return delta
    return delta
