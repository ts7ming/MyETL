from pyqueen import DataSource
from settings import SERVERS
from cheap.models import EtlDataCheck, get_session
from cheap.etl.utils import msg_robot

ds = DataSource(**SERVERS['main'])


def get_check_job(check_list):
    """
    添加逗号, 确保不会误匹配
    """
    check_list = [str(x) for x in check_list]
    session = get_session(ds)
    try:
        # 使用 in_ 操作符进行查询
        c_job = session.query(EtlDataCheck).filter(EtlDataCheck.id.in_(check_list)).all()
        return c_job
    finally:
        session.close()


def check(job):
    tmp_ds = DataSource(**SERVERS[str(job.server_id)])
    tmp_ds.set_db(job.db_name)
    v = ds.get_value(job.check_sql)
    if str(v) == '1':
        msg_robot(robot_id=job.robot_id, msg=job.warning_message)


def data_check(user_job_list):
    job_list = get_check_job(user_job_list)
    error_job = ''
    for job in job_list:
        try:
            check(job)
        except Exception as e:
            error_job += "check_id: " + str(job['id']) + str(e)[0:200]
    if error_job != '':
        raise Exception(error_job)
