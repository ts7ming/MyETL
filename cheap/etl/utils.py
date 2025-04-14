import inspect

from pyqueen import DataSource, Dingtalk
from settings import (
    SERVERS,
    ROBOTS,
    WF_LOG,
    DEV,
    T_ETL_SERVER,
    T_ETL_ROBOT,
)

from cheap.models import session_context, EtlWorkflowLog, EtlRobot, EtlServer


def log(etl_log):
    log_field = ['py_path', 'func_name', 'start_time', 'end_time', 'duration', 'file_path', 'sql_text', 'server_id', 'db_name', 'table_name']
    if DEV:
        print(etl_log)
    etl_log = {k: [v] for k, v in etl_log.items() if k in log_field}
    new_log = EtlWorkflowLog(**etl_log)
    with session_context() as session:
        session.add(new_log)
        session.commit()


def get_dingtalk(ding_id):
    if T_ETL_ROBOT is None:
        return Dingtalk(**ROBOTS[ding_id])
    else:
        ding_id = str(ding_id)
        with session_context() as session:
            ding_cfg = session.query(EtlRobot).filter(id=ding_id).first()
            if ding_cfg is not None:
                return Dingtalk(access_token=ding_cfg.access_token, secret=ding_cfg.secret)


def get_ds(server_id):
    if T_ETL_SERVER is None:
        ds = DataSource(**SERVERS[server_id])
        if WF_LOG:
            ds.set_logger(logger=log, server_id=server_id)
        return ds
    else:
        server_id = str(server_id)
        with session_context() as session:
            cfg = session.query(EtlServer).filter(id=server_id).first()
            params = {k: v for k, v in vars(cfg).items() if not k.startswith('_')}
            ds = DataSource(**params)
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
