from pyqueen import DataSource, Dingtalk
from settings import (
    SERVERS,
    ROBOTS,
    WF_LOG,
    T_WORKFLOW_LOG,
    DEV,
    T_ETL_SERVER,
    T_ETL_ROBOT,
)
import pandas as pd


def log(etl_log):
    log_field = ['py_path', 'func_name', 'start_time', 'end_time', 'duration', 'file_path', 'sql_text', 'server_id', 'db_name', 'table_name']
    if DEV:
        print(etl_log)
    try:
        etl_log = {k: [v] for k, v in etl_log.items() if k in log_field}
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
        where id = '{ding_id}'
        '''
        df = __ds.read_sql(sql)
        if df.empty is False:
            return Dingtalk(access_token=df['access_token'].to_list()[0], secret=df['secret'].to_list()[0])


def get_ds(server_id):
    if T_ETL_SERVER is None:
        ds = DataSource(**SERVERS[server_id])
        if WF_LOG:
            ds.set_logger(logger=log, server_id=server_id)
        return ds
    else:
        server_id = str(server_id)
        t_ds = DataSource(**SERVERS['main'])
        sql = f'''
        select conn_type,host,username,password,port,db_name
        from {T_ETL_SERVER}
        where server_id = {server_id}
        '''
        cfg = t_ds.read_sql(sql).to_dict(orient='records')[0]
        ds = DataSource(**cfg)
        if WF_LOG:
            ds.set_logger(logger=log, server_id=server_id)
        return ds


def msg_robot(robot_id, msg):
    if DEV:
        print(msg)
    else:
        try:
            ding = get_dingtalk(robot_id)
            ding.send(content=msg)
        except Exception as e:
            ding = get_dingtalk("devops")
            if ding is not None:
                ding.send(content='发送失败: ' + str(e)[0:100])
