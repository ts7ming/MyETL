import os
from pyqueen import DataSource

# 项目名称 - web页面展示
PROJECT_NAME = 'CheapETL'

# 工作目录 - 可自定义
WORK_DIR = os.path.dirname(os.path.abspath(__file__))

# 是否开发模式 (为False时用try...except记录报错信息 为True时直接抛出异常)
IS_DEV = False

# 是否开启工作流日志
IS_LOG = True

# 是否开启通知
IS_MESSAGE = False

# 各类配置和日志
DS_MAIN = DataSource(conn_type='sqlite', host=str(os.path.join(WORK_DIR, 'cheap/cheap.db')))

TABLE_ETL_SERVER = 'etl_server'  # 如果为 None 则使用 `SERVERS` 配置
TABLE_ETL_ROBOT = 'etl_robot'  # 如果为 None 则使用 `ROBOTS` 配置

TABLE_ETL_JOB = 'etl_job'
TABLE_ETL_JOB_LOG = 'etl_job_log'

TABLE_ETL_WORKFLOW = 'etl_workflow'
TABLE_ETL_WORKFLOW_LOG = 'etl_workflow_log'

TABLE_ETL_SYNC = 'etl_data_sync'
TABLE_ETL_SYNC_LOG = 'etl_data_sync_log'

TABLE_ETL_CHECK = 'etl_data_check'


# TABLE_ETL_SERVER 或 DS_MAIN 为 None 时生效
SERVERS = {
    # 业务数据库
    'dw01': {
        'conn_type': 'mssql'
    }
}

# 机器人配置表
# 建议配置一个 `devops` 运维通知群
# TABLE_ETL_ROBOT 为 None 时生效

ROBOTS = {
    'devops': {
        'access_token': '',
        'secret': ''
    }
}
