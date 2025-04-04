from pyqueen import DataSource
from settings import DATABASES
import pandas as pd

def dwlog(etl_log):
    try:
        etl_log = {k:[v] for k, v in etl_log.items()}
        df = pd.DataFrame(etl_log)
        ds_log = DataSource(**DATABASES['10'])
        ds_log.set_db('dw')
        ds_log.to_db(df, 'etl_workflow_log')
    except Exception as e:
        print(e)
