import importlib
import os
import sys
from pyqueen import DataSource, TimeKit
from sqlalchemy import and_, or_, func

from cheap.etl.data_check import data_check
from cheap.etl.data_sync import data_sync
from cheap.etl.utils import msg_robot
from settings import SERVERS, WORK_DIR, DEV
from cheap.models import session_context, EtlJob, EtlJobLog

ds = DataSource(**SERVERS['main'])


def import_from_absolute_path(file_path, module_name=None):
    # 确保路径存在
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"文件不存在: {file_path}")

    # 自动生成模块名（如果未提供）
    if module_name is None:
        module_name = os.path.basename(file_path).split(".")[0]

    # 创建模块规范
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    if spec is None:
        raise ImportError(f"无法为文件 {file_path} 创建模块规范")

    # 加载模块
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)  # 执行模块代码
    return module



def get_follow_job(job_str):
    sql = f'''
        SELECT
            id, job_name, job_type, job_dir, job_params, message_robot
        FROM
            {T_JOB}
        WHERE
            execution_status in (0, 99)
            and job_status = 1
            and job_depend in ({job_str})
    '''
    df = ds.read_sql(sql)
    return df.to_dict('records')


def register_job(job_list):
    id_str = ','.join([str(x['id']) for x in job_list])
    sql1 = f'update {T_JOB} set execution_status=1 where id in ({id_str})'
    ds.exe_sql(sql1)


def start_job(job_id):
    tk = TimeKit()
    t_now = tk.int2str(tk.now)
    sql1 = f'update {T_JOB} set execution_status=2 where id = {job_id}'
    sql2 = f'''
        insert into {T_JOB_LOG} (job_id, execution_status, start_time) 
        select id as job_id, 2 as execution_status, '{t_now}' as start_time 
        from {T_JOB} 
        where id = {job_id}
    '''
    ds.exe_sql(sql1)
    ds.exe_sql(sql2)
    sql3 = f'select max(id) as i from {T_JOB_LOG} where job_id = {job_id}'
    log_id = ds.get_value(sql3)
    return log_id


def end_job(job_id, log_id, status, msg):
    tk = TimeKit()
    t_now = tk.int2str(tk.now)
    sql1 = f'update {T_JOB} set execution_status=0 where id ={job_id}'
    if msg is None:
        sql2 = f"update {T_JOB_LOG} set execution_status={status}, end_time = '{t_now}' where id ={log_id}"
    else:
        msg = msg.replace("'", '"')
        sql2 = f'''update {T_JOB_LOG} set execution_status={status}, error_message='{msg}', end_time = {t_now} where id ={log_id}'''
    ds.exe_sql(sql1)
    ds.exe_sql(sql2)


def exe(job_type, job_params):
    if job_type == 'workflow':
        wf = import_from_absolute_path(os.path.join(WORK_DIR, job_params))
        wf.main()
    elif job_type == 'datasync':
        job_list = job_params.split(',')
        data_sync(job_list)
    elif job_type == 'datacheck':
        job_list = job_params.split(',')
        data_check(job_list)
    else:
        raise Exception('无效作业类型')
    return 0, ""


def run(job):
    log_id = start_job(job['id'])
    if DEV:
        code, msg = exe(job['job_type'], job['job_params'])
    else:
        try:
            code, msg = exe(job['job_type'], job['job_params'])
        except Exception as e:
            code, msg = -1, str(e)
    if code == 0:
        end_job(job['id'], log_id, 2, None)
    else:
        end_job(job['id'], log_id, 3, msg)
        msg_robot(robot_id=job['message_robot'], msg='ETL任务 ' + str(job['job_name']) + '\n执行出错\n\n' + str(msg)[0:100])

    follow_job_list = get_follow_job(str(job['id']))
    if len(follow_job_list) == 0:
        return []
    else:
        return follow_job_list


def main(job_list=None):
    job_list = EtlJob().get_job(job_list)
    if len(job_list) == 0:
        print('没有任务')
        exit()

    while len(job_list) > 0:
        register_job(job_list)
        job = job_list.pop(0)
        if DEV:
            print(job)
        re = run(job)
        job_list.extend(re)


if __name__ == '__main__':
    user_job_list = sys.argv[1:]
    if len(user_job_list) == 0:
        user_job_list = None
    if DEV:
        main(user_job_list)
    else:
        try:
            main(user_job_list)
        except Exception as e:
            msg_robot('1000', msg='调度出错\n\n' + str(e)[0:100])
