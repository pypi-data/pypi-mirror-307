# dac门面类，所有对dac的依赖替换成此类
import csv
import json
import os

import pymysql

from dac_ycl.glc.utils.ycl_abandon_abnormal import get_time, get_time_str

import datetime

use_dac = False
if use_dac:
    import common.redis
    import dac_ycl.glc.utils.control_delta
    import dac_ycl.glc.views.alarm_timing_utils
else:
    import dac_ycl.glc.utils.fake_cache
    # import research.utils.influx_utils

pymysql.install_as_MySQLdb()


class DacFacade:
    def __init__(self):
        pass

    def get(self, key, default=None):
        if use_dac:
            return common.redis.default_cache.get(key, default)
        else:
            return dac_ycl.glc.utils.fake_cache.default_cache.get(key, default)

    def set(self, key, value, timeout):
        if use_dac:
            return common.redis.default_cache.set(key, value, timeout)
        else:
            return dac_ycl.glc.utils.fake_cache.default_cache.set(key, value, timeout)

    def delete(self, key):
        if use_dac:
            return common.redis.default_cache.delete(key)
        else:
            return dac_ycl.glc.utils.fake_cache.default_cache.delete(key)

    def clear(self):
        if not use_dac:
            dac_ycl.glc.utils.fake_cache.default_cache.clear()


default_cache = DacFacade()

action_dict = {  # 简化版规则表，只看引出量与bd4r
    (0, 0): 0, (0, 1): -0.5, (0, -1): +0.5, (0, 2): -0.5, (0, -2): +0.5,
    (1, 0): -0.5, (1, 1): -0.5, (1, -1): 0, (1, 2): -1, (1, -2): 0,
    (-1, 0): +0.5, (-1, -1): +0.5, (-1, 1): 0, (-1, -2): +1, (-1, 2): 0,
    (2, 0): -0.5, (2, 1): -0.8, (2, -1): -0.3, (2, 2): -1, (2, -2): 0,
    (-2, 0): +0.5, (-2, -1): +0.8, (-2, 1): +0.3, (-2, -2): +1, (-2, 2): 0,
}
state_2_num = {
    "快速上升": 2,
    "缓慢上升": 1,
    "平稳": 0,
    "缓慢下降": -1,
    "快速下降": -2,
}
num_2_state = {
    2: "快速上升",
    1: "缓慢上升",
    0: "平稳",
    -1: "缓慢下降",
    -2: "快速下降",
}


# 线上运行
# def query_actions(global_result, alarm_rule_id: int) -> dict:
#     if use_dac:
#         return dac_ycl.glc.utils.control_delta.query_actions(global_result, alarm_rule_id)
#     else:
#         # print(f"global_result={global_result}")
#         action = action_dict[(state_2_num[global_result['YCLJS']], state_2_num[global_result['BD4R']])]
#         if action >= 0:
#             return {'BL1SH': {'变化量': "@{BL1SHPC}+" + str(action)}}
#         else:
#             return {'BL1SH': {'变化量': "@{BL1SHPC}" + str(action)}}

def query_actions(global_result, alarm_rule_id: int) -> dict:
    if use_dac:
        return dac_ycl.glc.utils.control_delta.query_actions(global_result, alarm_rule_id)
    else:
        return match_actions_at_local(global_result)


local_data_dict = {}

def match_rule_id_by_state(rule_table, input_state_dict):
    property_list = list(input_state_dict.keys())
    for rule_obj in rule_table:
        is_equal = True
        for property in property_list:
            if rule_obj.get(property) != input_state_dict.get(property):
                is_equal = False
        if is_equal:
            return rule_obj.get("ID")
    return ""

def match_actions_at_local(global_result) -> dict:
    rule_json = os.path.join(os.getenv("ycl_data"), "rule.json")
    with open(rule_json, 'r', encoding='utf-8') as f:
        rule_dict = json.load(f)
        rule_table = rule_dict['rule_table']
        action_table = rule_dict['action_table']
        property_list = list(rule_table[0].keys())[2:]
        input_state_dict = {key: global_result.get(key) for key in property_list}
        
        rule_id = match_rule_id_by_state(rule_table, input_state_dict)
        matched_action_dict = {}
        if rule_id:
            for action in action_table:
                if action.get("规则ID") == rule_id:
                    property_name = action.get("反控属性")
                    # property_value = action.get("变化量")
                    # if "POS_FACTOR" in property_value or "NEG_FACTOR" in property_value:
                    #     property_value = ("+").join(property_value.split("+")[:-1])
                    matched_action_dict[property_name] = action
        return matched_action_dict

# def get_data(measurement, field, start, end):
#     kwargs = {
#         "group": "0010",
#         "feature": "",
#         "device_identifier": "",
#         "device_id": measurement,
#         "variable": field,  # 看情况改
#         "start": start,
#         "end": end,
#     }
#     return get_and_deal_rule_dict_data(180, **kwargs)

# replace for automation test
def get_data(measurement, field, start, end, from_calculated=False):
    kwargs = {
        "group": "0010",
        "feature": "",
        "device_identifier": "",
        "device_id": measurement,
        "variable": field,  # 看情况改
        "start": start,
        "end": end,
    }
    if field == "AUTO_GL":
        return [{'time': '', 'value': 1}]
    if field == "BL4SHPC" and from_calculated:
        return get_calculated_data(field, start, end)
    return get_and_deal_rule_dict_data(180, **kwargs)

# add for automation test
def set_calculated_data(field, start, end, delta):
    cal_field = f"{field}_CAL"
    if not local_data_dict.get(cal_field):
        local_data_dict[cal_field] = []
        initial_local_data = get_data("", field, start, end)
        latest_item = initial_local_data[-1]
        cal_item = {
            "time": latest_item["time"],
            "value": eval(f"{latest_item.get("value")}+{delta}")
        }
        local_data_dict[cal_field].append(cal_item)
    else:
        latest_item = local_data_dict[cal_field][-1]
        start_time = get_time(latest_item.get("time"))
        end_time = get_time(end)
        latest_value = eval(f"{latest_item.get("value")}+{delta}")  
        while start_time <= end_time:
            start_time_str = get_time_str(start_time)
            cal_item = {
                "time": start_time_str,
                "value": latest_value
            }
            local_data_dict[cal_field].append(cal_item)
            start_time = start_time + datetime.timedelta(seconds=30)


# add for automation test
def get_calculated_data(field, start, end):
    cal_field = f"{field}_CAL"
    local_data = local_data_dict.get(cal_field) or []
    return [item for item in local_data if start <= item['time'] <= end]

# def get_and_deal_rule_dict_data(period, **kwargs):
#     variable = kwargs["variable"]
#     start = kwargs["start"]
#     end = kwargs["end"]
#     if use_dac:
#         return dac_ycl.glc.views.alarm_timing_utils.get_and_deal_rule_dict_data(period, **kwargs)
#         # points = research.utils.influx_utils.influxClient.query_by_time(kwargs['measurement'], kwargs['field'],
#         #                                                                 kwargs['start'], kwargs['end'])
#         # return points[kwargs['field']]
#     else:

#         # start_date = get_time(start)
#         end_date = get_time(end)
#         # date_dir = datetime.datetime.strftime(end_date, "%m%d")
#         # directory = r"C:\Workspace\wxy\Code\hy_auto_control\data\\" + date_dir
#         directory = os.path.join(os.getenv("ycl_data"), end_date.date().strftime("%m%d"))
#         if variable in local_data_dict:
#             local_data = local_data_dict[variable]
#         else:
#             local_data = []
#             # print('start read ', f"{directory}/{variable}.csv")
#             with open(f"{directory}/{variable}.csv", 'r', encoding='utf-8') as csvfile:
#                 reader = csv.reader(csvfile, delimiter=',')
#                 next(reader)
#                 for row in reader:
#                     index = row[0]
#                     time = row[1]
#                     value = float(row[2])
#                     local_data.append({'time': time, 'value': value})
#             local_data_dict[variable] = local_data
#         return [item for item in local_data if start <= item['time'] <= end]

def get_and_deal_rule_dict_data(period, **kwargs):
    variable = kwargs["variable"]
    start = kwargs["start"]
    end = kwargs["end"]
    if use_dac:
        return dac_ycl.glc.views.alarm_timing_utils.get_and_deal_rule_dict_data(period, **kwargs)
        # points = research.utils.influx_utils.influxClient.query_by_time(kwargs['measurement'], kwargs['field'],
        #                                                                 kwargs['start'], kwargs['end'])
        # return points[kwargs['field']]
    else:
        date = get_time(end).date().strftime("%m%d")
        directory = os.path.join(os.getenv("ycl_data"), date)
        local_date = local_data_dict.get(f"{variable}_local_date")
        if local_date != date:
            local_data_dict[f"{variable}_local_date"] = date
            local_data = []
            if not isinstance(start, str):
                start = get_time_str(start)
            if not isinstance(end, str):
                end = get_time_str(end)
            # print('start read ', f"{directory}/{variable}.csv")
            with open(f"{directory}/{variable}.csv", 'r', encoding='utf-8') as csvfile:
                reader = csv.reader(csvfile, delimiter=',')
                next(reader)
                for row in reader:
                    index = row[0]
                    time = row[1]
                    value = float(row[2])
                    local_data.append({'time': time, 'value': value})
            if not local_data_dict.get(variable):
                local_data_dict[variable] = []
            local_data_dict[variable] = local_data_dict[variable] + local_data
            
        return [item for item in local_data_dict[variable] if start <= item['time'] <= end]


MYSQL_HOST = ""
MYSQL_NAME = ""
MYSQL_PORT = 0
MYSQL_USER = ""
MYSQL_PASSWORD = ""


class MysqlConnection:
    @staticmethod
    def mysql_conn():
        try:
            return pymysql.connect(host=MYSQL_HOST, user=MYSQL_USER, passwd=MYSQL_PASSWORD,
                                   db=MYSQL_NAME, port=int(MYSQL_PORT), charset="utf8")
        except Exception as e:
            print('Mysql Connection error: ' + str(e))

    @staticmethod
    def execute(sql, conn):
        result = {"Count": 0, "Data": [], "Status": False, "Field": []}
        try:
            cursor = conn.cursor()
            cursor.execute(sql)
            rows = cursor.fetchall()
            if sql.startswith("select") or sql.startswith("SELECT"):
                result["Data"] = [[x for x in line] for line in rows]
                result["Field"] = [i[0] for i in cursor.description]
                result["Count"] = len(result["Data"])
            else:
                result["Count"] = cursor.lastrowid
            result["Status"] = True
            cursor.close()
            conn.commit()
        except Exception as e:
            result["error_msg"] = str(e)
        finally:
            conn.close()
        return result

    @staticmethod
    def query_config_by_alarm_rule_id(alarm_rule_id):
        if use_dac:
            sql = "select object_name,json_config from al_custom_config where object_id={}".format(alarm_rule_id)
            conn = MysqlConnection.mysql_conn()
            query_result = MysqlConnection.execute(sql, conn)
            if 'error_msg' in query_result:
                return query_result
            else:
                data = query_result['Data']
                result = {}
                for el in data:
                    if not el[1]:
                        el[1] = '{}'
                    result[el[0]] = json.loads(el[1])
                return result
        else:
            return {'冷却段':
                        {
                            'd3lr_threshold': 0.25,
                            'd3lr_action_unit': 0.05,
                            'bw1r_threshold': 0.2,
                            'bw1r_action_unit': 0.1,
                            'bw1r_guaidian_threshold': 0.05
                        }
                    }


mysql_conn = MysqlConnection()
