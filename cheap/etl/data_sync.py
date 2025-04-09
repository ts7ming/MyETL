from pyqueen import DataSource
from settings import SERVERS, T_SYNC, T_SYNC_LOG


ds = DataSource(**SERVERS['main'])


def get_job(user_job_list):
    """
    添加逗号, 确保不会误匹配
    """
    job_list_str = ','.join([str(x) for x in user_job_list])
    sql = f'''
        SELECT
            id,
            from_server,
            from_db,
            from_sql,
            to_server,
            to_db,
            to_table,
            before_write
        FROM
            {T_SYNC}
        WHERE
            id in ({job_list_str})
    '''
    df = ds.read_sql(sql)
    return df.to_dict('records')


def start_job(sync_id):
    sql = f'''
		insert into {T_SYNC_LOG} (sync_id, start_time) 
		select id as sync_id, getdate() as start_time 
		from {T_SYNC} 
		where id = {sync_id}
	'''
    ds.exe_sql(sql)
    sql3 = f'select max(id) as i from {T_SYNC_LOG} where sync_id = {sync_id}'
    log_id = ds.get_value(sql3)
    return log_id


def end_job(log_id, status, rows, msg):
    if msg is None:
        sql = f'update {T_SYNC_LOG} set sync_status={status},sync_rows={rows}, end_time = getdate() where id ={log_id}'
    else:
        msg = msg.replace("'", '"')
        sql = f'''update {T_SYNC_LOG} set sync_status={status},sync_rows={rows}, error_message='{msg}', end_time = getdate() where id ={log_id}'''
    ds.exe_sql(sql)


def read_data(job):
    if job['from_sql'] is None:
        return None
    from_server = str(job["from_server"])
    from_db = job["from_db"]
    from_sql = job["from_sql"]
    ds_source = DataSource(**SERVERS[from_server])
    ds_source.set_db(from_db)
    df = ds_source.read_sql(from_sql)
    return df


def write_data(job, df):
    to_server = str(job["to_server"])
    to_db = job["to_db"]
    to_table = job["to_table"]
    before_write = job["before_write"]
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
            log_id = start_job(job['id'])
            df = read_data(job)
            write_data(job, df)
            if df is None:
                row_num = 0
            else:
                row_num = len(df)
            end_job(log_id, 3, row_num, None)
        except Exception as e:
            error_job += "sync_id: " + str(job['id']) + str(e)[0:200]
    if error_job != '':
        raise Exception(error_job)
