from pyqueen import DataSource
from settings import SERVERS
from cheap.models import EtlDataSync, EtlDataSyncLog, get_session
from sqlalchemy import func

ds = DataSource(**SERVERS['main'])


def get_job(user_job_list):
    """
    添加逗号, 确保不会误匹配
    """
    session = get_session(ds)
    user_job_list = [str(x) for x in user_job_list]
    try:
        d_job = session.query(EtlDataSync).filter(EtlDataSync.id.in_(user_job_list)).all()
        return d_job
    finally:
        session.close()


def start_job(job):
    session = get_session(ds)
    try:
        new_log = EtlDataSyncLog(sync_id=job.sync_id, start_time=func.now)
        session.add(new_log)
        session.commit()
        log_id = session.query(func.max(EtlDataSyncLog.id)).filter(EtlDataSyncLog.sync_id == job.sync_id).scalar()
        return log_id
    finally:
        session.close()


def end_job(log_id, status, rows, msg):
    session = get_session(ds)
    try:
        job_log = session.query(EtlDataSyncLog).filter(EtlDataSyncLog.id == log_id).first()
        job_log.sync_status = status
        job_log.sync_rows = rows
        job_log.end_time = func.now
        if msg is not None:
            job_log.error_message = msg.replace("'", '"')
        session.commit()
    finally:
        session.close()


def read_data(job):
    if job.from_sql is None:
        return None
    from_server = str(job.from_server)
    from_db = job.from_db
    from_sql = job.from_sql
    ds_source = DataSource(**SERVERS[from_server])
    ds_source.set_db(from_db)
    df = ds_source.read_sql(from_sql)
    return df


def write_data(job, df):
    to_server = str(job.to_server)
    to_db = job.to_db
    to_table = job.to_table
    before_write = job.before_write
    ds_target = DataSource(**SERVERS[to_server])
    ds_target.set_db(to_db)
    if before_write != '':
        ds_target.exe_sql(before_write)
    if df is not None:
        ds_target.to_db(df, to_table)


def data_sync(user_job_list):
    job_list = get_job(user_job_list)
    error_job = ''
    for job in job_list:
        try:
            log_id = start_job(job)
            df = read_data(job)
            write_data(job, df)
            if df is None:
                row_num = 0
            else:
                row_num = len(df)
            end_job(log_id, 3, row_num, None)
        except Exception as e:
            error_job += "sync_id: " + str(job.id) + str(e)[0:200]
    if error_job != '':
        raise Exception(error_job)
