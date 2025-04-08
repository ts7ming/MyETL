from pyqueen import DataSource
from settings import SERVERS

try:
    from settings import DEV
except:
    DEV = True

T_CHECK = 'etl_data_check'


ds = DataSource(**SERVERS['main'])


def get_check_job(check_list):
    """
    添加逗号, 确保不会误匹配
    """
    check_list_str = ','.join([str(x) for x in check_list])
    sql = f'''
        SELECT
            server_id,
            db_name,
            check_sql,
            check_value,
            warning_message,
            robot_id
        FROM
            dbo.{T_CHECK}
        WHERE
            id in ({check_list_str})
    '''
    df = ds.read_sql(sql)
    return df.to_dict('records')
