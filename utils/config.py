from pyqueen import DataSource
from settings import DATABASES


def get_dingtalk(id):
    id =str(id)
    ds = DataSource(**DATABASES['10'])
    ds.set_db('dw')
    sql = f'''
    select access_token,secret
    from etl_robot
    where id = {id}
    '''
    df= ds.read_sql(sql)
    cfg = {
        'access_token':df['access_token'].to_list()[0],
        'secret':df['secret'].to_list()[0]
    }
    return cfg