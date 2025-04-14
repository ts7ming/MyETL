from settings import (
    T_ETL_CHECK,
    T_ETL_SYNC,
    T_ETL_SYNC_LOG,
    T_ETL_WORKFLOW_LOG,
    T_ETL_JOB,
    T_ETL_JOB_LOG,
    T_ETL_ROBOT,
    T_ETL_SERVER,
    SERVERS
)

from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy import and_, or_, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from contextlib import contextmanager
from pyqueen import DataSource, TimeKit

main_jdbc_url = DataSource(**SERVERS['main']).get_jdbc_url()

Base = declarative_base()


class EtlDataCheck(Base):
    __tablename__ = T_ETL_CHECK

    id = Column(Integer, primary_key=True)
    server_id = Column(Integer)
    db_name = Column(String)
    check_sql = Column(String)
    warning_message = Column(String)
    robot_id = Column(Integer)


class EtlDataSync(Base):
    __tablename__ = T_ETL_SYNC

    id = Column(Integer, primary_key=True)
    from_server = Column(Integer, nullable=False)
    from_db = Column(String)
    from_sql = Column(String)
    to_server = Column(Integer, nullable=False)
    to_db = Column(String)
    to_table = Column(String)
    before_write = Column(String)


class EtlDataSyncLog(Base):
    __tablename__ = T_ETL_SYNC_LOG

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


class EtlJob(Base):
    __tablename__ = T_ETL_JOB

    id = Column(Integer, primary_key=True)
    job_name = Column(String)
    job_type = Column(String)
    job_dir = Column(String)
    job_params = Column(String)
    execution_status = Column(Integer)
    job_schedule_minute = Column(String)
    job_schedule_hour = Column(String)
    job_schedule_day = Column(String)
    job_schedule_week = Column(String)
    job_schedule_month = Column(String)
    job_status = Column(Integer)
    job_depend = Column(String)
    message_robot = Column(Integer)

    def get_job(self, job_list=None):
        """
        添加逗号, 确保不会误匹配
        """
        if job_list is None:
            tk = TimeKit()
            cur_month = str(int(str(tk.theday)[4:6])) + ','
            cur_week = str(tk.nday_of_week) + ','
            cur_day = str(int(str(tk.theday)[6:8])) + ','
            cur_hour = str(tk.hour) + ','
            cur_minute = str(tk.minute) + ','

            with session_context() as session:
                job = session.query(self).filter(and_(
                    or_(self.execution_status.in_([0, 99]), self.job_status == 1),
                    or_(self.job_schedule_month == '*', func.concat(self.job_schedule_month, ',').like(f'{cur_month},%')),
                    or_(self.job_schedule_week == '*', func.concat(self.job_schedule_week, ',').like(f'{cur_week},%')),
                    or_(self.job_schedule_day == '*', func.concat(self.job_schedule_day, ',').like(f'{cur_day},%')),
                    or_(self.job_schedule_hour == '*', func.concat(self.job_schedule_hour, ',').like(f'{cur_hour},%')),
                    or_(self.job_schedule_minute == '*', func.concat(self.job_schedule_minute, ',').like(f'{cur_minute},%'))
                )).all()
        else:
            job_list_str = [str(x) for x in job_list]
            with session_context() as session:
                job = session.query(EtlJob).filter(EtlJob.execution_status.in_(job_list_str)).all()
        return job


class EtlJobLog(Base):
    __tablename__ = T_ETL_JOB_LOG

    id = Column(Integer, primary_key=True)
    job_id = Column(Integer, nullable=False)
    start_time = Column(DateTime)
    end_time = Column(DateTime)
    execution_status = Column(Integer)
    error_message = Column(String)


class EtlRobot(Base):
    __tablename__ = T_ETL_ROBOT

    id = Column(Integer, primary_key=True)
    access_token = Column(String)
    secret = Column(String)
    name = Column(String)


class EtlServer(Base):
    __tablename__ = T_ETL_SERVER

    server_id = Column(Integer, primary_key=True)
    server_name = Column(String)


class EtlWorkflowLog(Base):
    __tablename__ = T_ETL_WORKFLOW_LOG

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


@contextmanager
def session_context(jdbc_url=None):
    if jdbc_url is None:
        jdbc_url = main_jdbc_url
    engine = create_engine(jdbc_url, echo=True)
    session_obj = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    session = session_obj()
    try:
        yield session
    except Exception as e:
        raise Exception(e)
    finally:
        session.close()
