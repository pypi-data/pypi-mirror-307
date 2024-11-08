# dac门面类，所有对dac的依赖替换成此类
import csv
import os
from redis import Redis
import datetime

import pymysql
from dac_ycl.jwd_ce.utils.config import MYSQL_HOST, MYSQL_NAME, MYSQL_PORT, MYSQL_USER, MYSQL_PASSWORD
import json
import numpy as np

from dac_ycl.jwd_ce.utils.ycl_abandon_abnormal import get_time

pymysql.install_as_MySQLdb()

use_dac = False

if use_dac:
    import common.redis
    import dac_ycl.jwd_ce.utils.control_delta
    import alarm.views.alarm_timing_utils
# else:
#     import dac_ycl.jwd_ce.utils.fake_cache
    # import research.utils.influx_utils

r = Redis(host='10.168.2.92', port=6379, db=0, decode_responses=True)


class DacFacade:
    def __init__(self):
        self.clear()

    def get(self, key, default):
        if use_dac:
            return common.redis.default_cache.get(key, default)
        else:
            if not r.exists(key):
                return default
            value = r.get(key)
            if "." in value:
                return eval(value)
            return value           
        
    def set(self, key, value, ttl):
        if use_dac:
            return common.redis.default_cache.set(key, value, ttl)
        else:
            value = value or ""
            return r.set(key, value, ttl)

    def delete(self, key):
        if use_dac:
            return common.redis.default_cache.delete(key)
        else:
            return r.delete(key)

    def clear(self):
        # if not use_dac:
        #     dac_ycl.jwd_ce.utils.fake_cache.default_cache.clear()
        if not use_dac:
            # r.clear()
            keys = r.keys("*")
            for key in keys:
                r.delete(key)


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
def query_actions(global_result, alarm_rule_id: int) -> dict:
    if use_dac:
        return dac_ycl.jwd_ce.utils.control_delta.query_actions(global_result, alarm_rule_id)
    else:
        # print(f"global_result={global_result}")
        action = action_dict[(state_2_num[global_result['YCLJS']], state_2_num[global_result['BD4R']])]
        if action >= 0:
            return {'BL1SH': {'变化量': "@{BL1SHPC}+" + str(action)}}
        else:
            return {'BL1SH': {'变化量': "@{BL1SHPC}" + str(action)}}

local_data_dict = {}
def get_data(measurement, field, start, end):
    kwargs = {
        "group": "0010",
        "feature": "",
        "device_identifier": "",
        "device_id": measurement,
        "variable": field,  # 看情况改
        "start": start,
        "end": end,
    }
    return get_and_deal_rule_dict_data(180, **kwargs)


# def get_and_deal_rule_dict_data(period, **kwargs):
#     variable = kwargs["variable"]
#     start = kwargs["start"]
#     end = kwargs["end"]
#     if use_dac:
#         return alarm.views.alarm_timing_utils.get_and_deal_rule_dict_data(period, **kwargs)
#         # points = research.utils.influx_utils.influxClient.query_by_time(kwargs['measurement'], kwargs['field'],
#         #                                                                 kwargs['start'], kwargs['end'])
#         # return points[kwargs['field']]
#     else:
#         dir_date = datetime.datetime.strptime(start, '%Y-%m-%d %H:%M:%S')
#         dir_date_str = dir_date.strftime('%m%d')
#         # directory_start = f'C:\\Users\\haoyu.zheng\\Desktop\\DAC\\test\\csv\\{dir_date_str}'
#         directory_start = os.path.join(os.getenv("ycl_data"), dir_date_str)

#         dir_date = datetime.datetime.strptime(end, '%Y-%m-%d %H:%M:%S')
#         dir_date_str = dir_date.strftime('%m%d')
#         # directory_end = f'C:\\Users\\haoyu.zheng\\Desktop\\DAC\\test\\csv\\{dir_date_str}'
#         directory_end = os.path.join(os.getenv("ycl_data"), dir_date_str)
        
#         if variable in local_data_dict:
#             local_data = local_data_dict[variable]
#         else:
#             local_data = []
#             print('start read ', f"{directory_start}/{variable}.csv")
#             with open(f"{directory_start}/{variable}.csv", 'r', encoding='utf-8') as csvfile:
#                 reader = csv.reader(csvfile, delimiter=',')
#                 next(reader)
#                 for row in reader:
#                     index = row[0]
#                     time = row[1]
#                     value = row[2]
#                     local_data.append({'time': time, 'value': value})
#             if directory_start != directory_end:
#                 with open(f"{directory_end}/{variable}.csv", 'r', encoding='utf-8') as csvfile:
#                     reader = csv.reader(csvfile, delimiter=',')
#                     next(reader)
#                     for row in reader:
#                         index = row[0]
#                         time = row[1]
#                         value = row[2]
#                         local_data.append({'time': time, 'value': value})
#             local_data_dict[variable] = local_data
#         return [item for item in local_data if start <= item['time'] <= end]


def get_and_deal_rule_dict_data(period, **kwargs):
    variable = kwargs["variable"]
    start = kwargs["start"]
    end = kwargs["end"]
    if use_dac:
        return alarm.views.alarm_timing_utils.get_and_deal_rule_dict_data(period, **kwargs)
        # points = research.utils.influx_utils.influxClient.query_by_time(kwargs['measurement'], kwargs['field'],
        #                                                                 kwargs['start'], kwargs['end'])
        # return points[kwargs['field']]
    else:
        start_time = get_time(start)
        end_time = get_time(end)
        local_date = local_data_dict.get(f"{variable}_local_date")

        if local_date != end_time.date().strftime("%m%d"):
            if local_date:
                start_time = datetime.datetime.strptime(f"{start_time.year}-{local_date[:2]}-{local_date[2:]}", "%Y-%m-%d")
            while start_time.date() <= end_time.date():
                local_date = start_time.date().strftime("%m%d")
                directory = os.path.join(os.getenv("ycl_data"), local_date)
                local_data_dict[f"{variable}_local_date"] = local_date
                local_data = []
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
                start_time = start_time + datetime.timedelta(days=1)      
            
        return [item for item in local_data_dict[variable] if start <= item['time'] <= end]


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
    # @lru_cache(maxsize=128)
    def query_config_by_alarm_rule_id(alarm_rule_id):
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


mysql_conn = MysqlConnection.mysql_conn()
