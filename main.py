from pyqueen import DataSource, TimeKit, Dingtalk
from settings import SERVERS, DINGTALK_DEV, WORK_DIR
from etl.workflow.data_sync import data_sync
from etl.workflow import get_dingtalk
import importlib
import sys, os
try:
    from settings import DEV
except:
    DEV = False


T_JOB = 'etl_job'
T_JOB_LOG = 'etl_job_log'


ds = DataSource(**SERVERS['10'])
ds.set_db('dw')



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


def get_job(user_job_list=None):
    """
    添加逗号, 确保不会误匹配
    """
    if user_job_list is None:
        tk = TimeKit()
        cur_month = str(int(str(tk.theday)[4:6])) + ','
        cur_week = str(tk.nday_of_week)+ ','
        cur_day = str(int(str(tk.theday)[6:8]))+ ','
        cur_hour = str(tk.hour)+ ','
        cur_minute = str(tk.minute)+ ','
        sql = f'''
            SELECT
                id, job_name, job_type, job_dir, job_params
            FROM
                dbo.{T_JOB}
            WHERE
                execution_status in (0, 99)
                and job_status = 1
                and (job_schedule_month='*' or concat(job_schedule_month,',') like '{cur_month}')
                and (job_schedule_week='*' or concat(job_schedule_week,',') like '{cur_week}')
                and (job_schedule_day='*' or concat(job_schedule_day,',') like '{cur_day}')
                and (job_schedule_hour='*' or concat(job_schedule_hour,',') like '{cur_hour}')
                and (job_schedule_minute='*' or concat(job_schedule_minute,',') like '{cur_minute}')
        '''
    else:
        job_list_str = ','.join([str(x) for x in user_job_list])
        sql = f'''
            SELECT
                id, job_name, job_type, job_dir, job_params, job_depend
            FROM
                dbo.{T_JOB}
            WHERE
                id in ({job_list_str})
        '''
    df = ds.read_sql(sql)
    return df.to_dict('records')

def get_follow_job(job_list):
    job_list_str = ','.join([str(x) for x in job_list])
    sql = f'''
        SELECT
            id, job_name, job_type, job_dir, job_params
        FROM
            dbo.{T_JOB}
        WHERE
            execution_status in (0, 99)
            and job_status = 1
            and job_depend = {job_list_str}
    '''
    df = ds.read_sql(sql)
    return df.to_dict('records')

def register_job(job_list):
    id_str = ','.join([str(x['id']) for x in job_list])
    sql1 = f'update {T_JOB} set execution_status=1 where id in ({id_str})'
    ds.exe_sql(sql1)


def start_job(job_id):
    sql1 = f'update {T_JOB} set execution_status=2 where id = {job_id}'
    sql2 = f'''
		insert into {T_JOB_LOG} (job_id, execution_status, start_time) 
		select id as job_id, 2 as execution_status, getdate() as start_time 
		from {T_JOB} 
		where id = {job_id}
	'''
    ds.exe_sql(sql1)
    ds.exe_sql(sql2)
    sql3= f'select max(id) as i from {T_JOB_LOG} where job_id = {job_id}'
    log_id = ds.get_value(sql3)
    return log_id


def end_job(job_id, log_id, status, msg):
    sql1 = f'update {T_JOB} set execution_status=0 where id ={job_id}'
    if msg is None:
        sql2 = f'update {T_JOB_LOG} set execution_status={status}, end_time = getdate() where id ={log_id}'
    else:
        msg = msg.replace("'",'"')
        sql2 = f'''update {T_JOB_LOG} set execution_status={status}, error_message='{msg}', end_time = getdate() where id ={log_id}'''
    ds.exe_sql(sql1)
    ds.exe_sql(sql2)


def run(job_type, job_params):
    try:
        if job_type == 'workflow':
            wf = import_from_absolute_path(os.path.join(WORK_DIR,job_params))
            wf.main()
        elif job_type == 'datasync':
            job_list = job_params.split(',')
            data_sync(job_list)
        else:
            raise Exception('无效作业类型')
        return 0,""
    except Exception as e:
        return -1,str(e)

def job(job_list):
    register_job(job_list)
    for job in job_list:
        log_id = start_job(job['id'])
        code, msg = run(job['job_type'], job['job_params'])
        if code == 0:
            end_job(job['id'], log_id, 2, None)
        else:
            end_job(job['id'], log_id, 3, msg)
            if DEV:
                print('[ludao]ETL任务 ' +str(job['job_name'])+ '\n执行出错\n\n'+str(msg)[0:100])
            else:
                ding_cfg = get_dingtalk(job['message_robot'])
                if ding_cfg is not None:
                    ding = Dingtalk(**get_dingtalk(job['']))
                    ding.send(content='ETL任务 ' +str(job['job_name'])+ '\n执行出错\n\n'+str(msg)[0:100])
    job_id_list = [str(x['id']) for x in job_list]
    follow_job_list = get_follow_job(job_id_list)
    if len(follow_job_list)==0:
        return None
    else:
        return follow_job_list

def main(user_job_list=None):
    job_list = get_job(user_job_list)
    
    # print(job_list)
    if len(job_list) == 0:
        print('没有任务')
        exit()
    do = True
    while do:
        if job_list is None:
            do = False
        else:
            job_list = job(job_list)




if __name__ == '__main__':
    user_job_list = sys.argv[1:]
    if len(user_job_list)==0:
        user_job_list = None
    try:
        main(user_job_list)
    except Exception as e:
        if DEV:
            print('调度出错\n\n'+str(e)[0:100])
        else:
            ding_ops = Dingtalk(**DINGTALK_DEV)
            ding_ops.send(content='调度出错\n\n'+str(e)[0:100])