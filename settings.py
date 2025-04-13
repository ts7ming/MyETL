import os

# 项目名称 - web页面展示
PROJECT_NAME = 'CheapETL'

# 工作目录 - 可自定义
WORK_DIR = os.path.dirname(os.path.abspath(__file__))

# 是否开发模式 (为False时用try...except记录报错信息 为True时直接抛出异常)
DEV = False

# 是否开启工作流日志
WF_LOG = True
T_ETL_WORKFLOW_LOG = 'etl_workflow_log'

# 表
T_ETL_JOB = 'etl_job'
T_ETL_JOB_LOG = 'etl_job_log'
T_ETL_SYNC = 'etl_data_sync'
T_ETL_SYNC_LOG = 'etl_data_sync_log'

T_ETL_CHECK = 'etl_data_check'

# 数据库和其他服务连接方式
# 必须配置一个`main` 数据库作为系统服务
# 业务数据库可以配置在 下面 `SERVERS` 中, 也可以配置在 `T_ETL_SERVER` 表中

T_ETL_SERVER = None  # 'etl_server'  # 如果为 None 则使用 `SERVERS` 配置

SERVERS = {
    # 配置数据库 - 可选 sqlite, SQL SERVER, MySQL
    'main': {
        'conn_type': 'sqlite',
        'host': str(os.path.join(WORK_DIR, 'cheap/cheap.db'))
    },
    # 新增其他业务数据库
    'dw01': {
        'conn_type': 'mssql'
    }
}

# 机器人配置表
# 建议配置一个 `devops` 运维通知群
T_ETL_ROBOT = 'etl_robot'  # 如果为 None 则使用 `ROBOTS` 配置

ROBOTS = {
    'devops': {
        'access_token': '',
        'secret': ''
    }
}
