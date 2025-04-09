from pyqueen import DataSource
from settings import SERVERS, T_CHECK
from cheap.etl.utils import msg_robot

ds = DataSource(**SERVERS['main'])


def get_check_job(check_list):
    """
    添加逗号, 确保不会误匹配
    """
    check_list_str = ','.join([str(x) for x in check_list])
    sql = f'''
        SELECT id,server_id,db_name,check_sql,warning_message,robot_id
        FROM {T_CHECK}
        WHERE id in ({check_list_str})
    '''
    df = ds.read_sql(sql)
    return df.to_dict('records')


def check(job):
    ds = DataSource(**SERVERS[str(job['server_id'])])
    ds.set_db(job['db_name'])
    v = ds.get_value(job['check_sql'])
    if str(v) == '1':
        msg_robot(robot_id=job['robot_id'], msg=job['warning_message'])


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
