import os

# 项目名称 - web页面展示
PROJECT_NAME = 'CheapETL'

# 是否开发模式 (为False时用try...except记录报错信息 为True时直接抛出异常)
DEV = False

# 工作目录 - 可自定义
WORK_DIR = os.path.dirname(os.path.abspath(__file__))

# 数据库和其他服务连接方式
SERVERS = {
    # 配置数据库 - 可选 sqlte, SQL SERVER, MySQL
    'main': {
        'conn_type': 'sqlite',
        'host': os.path.join(WORK_DIR, 'etl/main.db')
    },
    # 新增其他业务数据库
    'dw01': {
        'conn_type': 'mssql'
    }
}
