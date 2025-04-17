from sqlalchemy.orm import sessionmaker

from settings import (
    TABLE_ETL_CHECK,
    TABLE_ETL_SYNC,
    TABLE_ETL_SYNC_LOG,
    TABLE_ETL_WORKFLOW_LOG,
    TABLE_ETL_JOB,
    TABLE_ETL_ROBOT,
    TABLE_ETL_SERVER
)

from sqlalchemy import Column, Integer, String, DateTime, create_engine
from sqlalchemy.ext.declarative import declarative_base
from cheap.utils import session_context

Base = declarative_base()


class JobStatus:
    """作业状态码"""
    pending = 0
    processing = 1
    running = 2
    success = 3
    error = -1


def get_sub_job_entity(job):
    m = {
        'workflow': EtlJob,
        'datasync': EtlDataSync,
        'datacheck': EtlDataCheck
    }
    return m[job.job_type]


def get_job_log_entity(job):
    m = {
        'workflow': EtlWorkflowLog,
        'datasync': EtlDataSyncLog,
        'datacheck': EtlDataCheckLog
    }
    return m[job.job_type]


class EtlJob(Base):
    __tablename__ = TABLE_ETL_JOB
    __table_args__ = {'comment': 'ETL-作业主表'}

    id = Column(Integer, primary_key=True)
    name = Column(String, doc='作业名称')
    job_type = Column(String, doc='作业类型: workflow,datasync,datacheck,python')
    work_dir = Column(String, doc='工作目录')
    params = Column(String, doc='作业参数')
    status = Column(Integer, doc='作业状态(0:待执行,1:执行中,2:执行完成;3执行出错;99:立即执行)')
    enabled = Column(Integer, doc='作业启用(0:停用, 1:启用)')
    depend = Column(String, doc='作业依赖(job_id)')
    robot_id = Column(Integer, doc='通知机器人(robot_id)')
    schedule_minute = Column(String, doc='作业计划-分钟(0-59)')
    schedule_hour = Column(String, doc='作业计划-小时(0-23)')
    schedule_day = Column(String, doc='作业计划-日期(1-31)')
    schedule_week = Column(String, doc='作业计划-星期(1-7)')
    schedule_month = Column(String, doc='作业计划-月份(1-12)')


class EtlDataSync(Base):
    __tablename__ = TABLE_ETL_SYNC
    __table_args__ = {'comment': 'ETL-数据同步作业'}

    id = Column(Integer, primary_key=True)
    from_server = Column(Integer, nullable=False, doc='来源服务器(server_id)')
    from_db = Column(String, doc='来源数据库')
    from_sql = Column(String, doc='取数sql')
    to_server = Column(Integer, nullable=False, doc='目标服务器(server_id)')
    to_db = Column(String, doc='目标数据库')
    to_table = Column(String, doc='目标表')
    before_write = Column(String, doc='写入前执行sql')


class EtlDataSyncLog(Base):
    __tablename__ = TABLE_ETL_SYNC_LOG
    __table_args__ = {'comment': 'ETL-数据同步作业日志'}

    id = Column(Integer, primary_key=True)
    job_id = Column(Integer, doc='作业日志(为空表示独立任务)')
    sync_id = Column(Integer, nullable=False)
    start_time = Column(DateTime, doc='开始时间')
    end_time = Column(DateTime, doc='结束时间')
    sync_rows = Column(Integer, doc='同步行数')
    status = Column(Integer, doc='作业状态(2:执行完成;3执行出错)')
    message = Column(String, doc='作业信息')


class EtlWorkflowLog(Base):
    __tablename__ = TABLE_ETL_WORKFLOW_LOG
    __table_args__ = {'comment': 'ETL-工作流日志'}

    id = Column(Integer, primary_key=True)
    job_id = Column(Integer, doc='作业日志(为空表示独立任务)')
    py_path = Column(String, doc='py脚本路径')
    func_name = Column(String, doc='函数名称')
    start_time = Column(DateTime, doc='开始时间')
    end_time = Column(DateTime, doc='结束时间')
    duration = Column(Integer, doc='耗时(秒)')
    file_path = Column(String, doc='文件路径')
    sql_String = Column(String, doc='sql')
    server_id = Column(String, doc='查询或操作的服务器(server_id)')
    db_name = Column(String, doc='查询或操作的数据库')
    table_name = Column(String, doc='操作表')
    status = Column(Integer, doc='作业状态(2:执行完成;3执行出错)')
    message = Column(String, doc='作业信息')


class EtlDataCheck(Base):
    __tablename__ = TABLE_ETL_CHECK
    __table_args__ = {'comment': 'ETL-数据校验作业'}

    id = Column(Integer, primary_key=True)
    server_id = Column(Integer, doc='服务器(server_id)')
    db_name = Column(String, doc='数据库')
    check_sql = Column(String, doc='校验sql')
    warning_message = Column(String, doc='通知信息(check_sql查询结果为 "1" 时发送')
    robot_id = Column(Integer, doc='通知机器人(robot_id)')


class EtlDataCheckLog(Base):
    __tablename__ = TABLE_ETL_CHECK
    __table_args__ = {'comment': 'ETL-数据校验作业日志'}

    id = Column(Integer, primary_key=True)
    server_id = Column(Integer, doc='服务器(server_id)')
    db_name = Column(String, doc='数据库')
    check_sql = Column(String, doc='校验sql')
    warning_message = Column(String, doc='通知信息(check_sql查询结果为 "1" 时发送')
    robot_id = Column(Integer, doc='通知机器人(robot_id)')
    status = Column(Integer, doc='作业状态(2:执行完成;3执行出错)')
    message = Column(String, doc='作业信息')


class EtlDevopsFrSql(Base):
    __tablename__ = 'etl_devops_fr_sql'
    __table_args__ = {'comment': 'ETL-帆软引用SQL解析'}

    id = Column(Integer, primary_key=True)
    fr_project = Column(String, doc='项目')
    fr_path = Column(String, doc='路径')
    server = Column(String, doc='数据集服务器')
    fr_dataset = Column(String, doc='数据集')
    sql = Column(String, doc='sql')


class EtlRobot(Base):
    __tablename__ = TABLE_ETL_ROBOT
    __table_args__ = {'comment': 'ETL-通知机器人'}

    id = Column(Integer, primary_key=True)
    access_token = Column(String, doc='机器人token')
    secret = Column(String, doc='加签模式')
    name = Column(String, doc='名称(非必须)')


class EtlServer(Base):
    __tablename__ = TABLE_ETL_SERVER
    __table_args__ = {'comment': 'ETL-服务器'}

    server_id = Column(Integer, primary_key=True)
    server_name = Column(String, doc='服务器名称(非必须)')
    conn_type = Column(String, doc='连接类型(DataSource.conn_type)')
    host = Column(String, doc='host')
    username = Column(String, doc='username')
    password = Column(String, doc='password')
    port = Column(String, doc='port')
    db_name = Column(String, doc='db_name')


def init(ds):
    engine = create_engine(ds.get_jdbc_url())
    Base.metadata.create_all(engine)
    with session_context() as session:
        session.commit()