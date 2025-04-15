from settings import (
    TABLE_ETL_CHECK,
    TABLE_ETL_SYNC,
    TABLE_ETL_SYNC_LOG,
    TABLE_ETL_WORKFLOW_LOG,
    TABLE_ETL_JOB,
    TABLE_ETL_JOB_LOG,
    TABLE_ETL_ROBOT,
    TABLE_ETL_SERVER
)

from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class ExecutionStatus:
    pending = 0
    collected = 1
    running = 2
    success = 3
    error = -1


class EtlJob(Base):
    __tablename__ = TABLE_ETL_JOB
    __table_args__ = {'comment': 'ETL-作业主表'}

    id = Column(Integer, primary_key=True)
    job_name = Column(String, doc='作业名称')
    job_type = Column(String, doc='作业类型: workflow,datasync,datacheck,python')
    job_dir = Column(String, doc='工作目录')
    job_params = Column(String, doc='作业参数')
    job_status = Column(Integer, doc='作业状态(0:待执行,1:执行中,2:执行完成;3执行出错;99:立即执行)')
    job_enabled = Column(Integer, doc='作业启用(0:停用, 1:启用)')
    job_depend = Column(String, doc='作业依赖(job_id)')
    job_robot = Column(Integer, doc='通知机器人(robot_id)')
    job_schedule_minute = Column(String, doc='作业计划-分钟(0-59)')
    job_schedule_hour = Column(String, doc='作业计划-小时(0-23)')
    job_schedule_day = Column(String, doc='作业计划-日期(1-31)')
    job_schedule_week = Column(String, doc='作业计划-星期(1-7)')
    job_schedule_month = Column(String, doc='作业计划-月份(1-12)')


class EtlJobLog(Base):
    __tablename__ = TABLE_ETL_JOB_LOG

    id = Column(Integer, primary_key=True)
    job_id = Column(Integer, nullable=False)
    start_time = Column(DateTime)
    end_time = Column(DateTime)
    execution_status = Column(Integer)
    error_message = Column(String)


class EtlDataSyncLog(Base):
    __tablename__ = TABLE_ETL_SYNC_LOG

    id = Column(Integer, primary_key=True)
    sync_id = Column(Integer, nullable=False)
    start_time = Column(DateTime)  # 使用 SQLAlchemy 的 DateTime 类型
    end_time = Column(DateTime)
    sync_status = Column(Integer)
    sync_rows = Column(Integer)


class EtlDevopsFrSql(Base):
    __tablename__ = 'etl_devops_fr_sql'
    id = Column(Integer, primary_key=True)
    fr_project = Column(String)
    fr_path = Column(String)
    server = Column(String)
    fr_dataset = Column(String)
    sql = Column(String)


class EtlDataCheck(Base):
    __tablename__ = TABLE_ETL_CHECK

    id = Column(Integer, primary_key=True)
    server_id = Column(Integer)
    db_name = Column(String)
    check_sql = Column(String)
    warning_message = Column(String)
    robot_id = Column(Integer)


class EtlDataSync(Base):
    __tablename__ = TABLE_ETL_SYNC

    id = Column(Integer, primary_key=True)
    from_server = Column(Integer, nullable=False)
    from_db = Column(String)
    from_sql = Column(String)
    to_server = Column(Integer, nullable=False)
    to_db = Column(String)
    to_table = Column(String)
    before_write = Column(String)


class EtlWorkflowLog(Base):
    __tablename__ = TABLE_ETL_WORKFLOW_LOG

    id = Column(Integer, primary_key=True)
    py_path = Column(String)
    func_name = Column(String)
    start_time = Column(DateTime)
    end_time = Column(DateTime)
    duration = Column(Integer)
    file_path = Column(String)
    sql_String = Column(String)
    server_id = Column(String)
    db_name = Column(String)
    table_name = Column(String)


class EtlRobot(Base):
    __tablename__ = TABLE_ETL_ROBOT

    id = Column(Integer, primary_key=True)
    access_token = Column(String)
    secret = Column(String)
    name = Column(String)


class EtlServer(Base):
    __tablename__ = TABLE_ETL_SERVER

    server_id = Column(Integer, primary_key=True)
    server_name = Column(String)
