from pyqueen import DataSource, Dingtalk
from settings import (
    SERVERS,
    ROBOTS,
    T_WORKFLOW_LOG,
    DEV,
    T_ETL_SERVER,
    T_ETL_ROBOT,
)
import pandas as pd


def log(etl_log):
    try:
        etl_log = {k: [v] for k, v in etl_log.items()}
        df = pd.DataFrame(etl_log)
        ds_log = DataSource(**SERVERS['main'])
        ds_log.to_db(df, T_WORKFLOW_LOG)
    except Exception as e:
        print(e)


def get_dingtalk(ding_id):
    if T_ETL_ROBOT is None:
        return Dingtalk(**ROBOTS[ding_id])
    else:
        ding_id = str(ding_id)
        __ds = DataSource(**SERVERS['main'])
        sql = f'''
        select access_token,secret
        from {T_ETL_ROBOT}
        where id = {ding_id}
        '''
        df = __ds.read_sql(sql)
        return Dingtalk(access_token=df['access_token'].to_list()[0], secret=df['secret'].to_list()[0])


def get_ds(server_id):
    if T_ETL_SERVER is None:
        return DataSource(**SERVERS[server_id])
    else:
        server_id = str(server_id)
        __ds = DataSource(**SERVERS['main'])
        sql = f'''
        select conn_type,host,username,password,port,db_name
        from {T_ETL_SERVER}
        where server_id = {server_id}
        '''
        cfg = __ds.read_sql(sql).to_dict(orient='records')[0]
        return DataSource(**cfg)


def msg_robot(robot_id, msg):
    if DEV:
        print(msg)
    else:
        try:
            ding = get_dingtalk(robot_id)
            ding.send(content=msg)
        except Exception as e:
            ding = get_dingtalk("devops")
            ding.send(content='发送失败: ' + str(e)[0:100])
