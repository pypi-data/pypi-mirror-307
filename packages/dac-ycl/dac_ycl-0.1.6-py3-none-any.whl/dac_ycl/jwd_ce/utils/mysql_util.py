import pymysql
from dac_ycl.jwd_ce.utils.config import MYSQL_HOST, MYSQL_NAME, MYSQL_PORT, MYSQL_USER, MYSQL_PASSWORD
import json

pymysql.install_as_MySQLdb()


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