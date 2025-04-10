# CheapETL
>基于 [PyQueen](https://pyqueen.readthedocs.io/zh-cn/latest/) 超轻量ETL工作流调度框架



![GitHub License](https://img.shields.io/github/license/ts7ming/CheapETL)
[![LICENSE](https://img.shields.io/badge/license-Anti%20996-blue.svg)](https://github.com/996icu/996.ICU/blob/master/LICENSE)
![Language](https://img.shields.io/badge/language-Python-brightgreen)

# Doc
[CheapETL](https://cheapetl.readthedocs.io/zh-cn/latest/)


# 1. 主要功能
###  CheapETL 作业类型
- datasync: 根据自定义数据连接, SQL和库表信息跨库同步数据
- datacheck: 根据自定义数据连接, SQL检查数据计算/同步结果, 发送异常通知
- workflow: 调用自定义脚本实现复杂数据处理, 内置数据读写函数

### CheapETL 框架功能
- 统一调度作业执行, 记录报错信息, 发送报错通知
- 支持CronJob风格(分/时/日/月/周)配置执行规则
- 支持设置任务依赖关系, 链式执行

# 2. 组件
### 配置信息: 
- SQLite
- MySQL
- SQL Server
- PgSQL
- Oracle

### 调度 
>每分钟执行 start.sh/start.bat 或根据实际情况降低频率
- Windows计划任务
- Linux Crontab

### 界面
- 无需界面直接修改数据库
- 本地启动web
- 服务器部署web

# 3. 配置
- 基础配置 `settings.py`

# 4. ToDo
- 根据作业日志自动生成数据血缘
- Web-UI界面
- 试试内置7b级的大模型来解析SQL, 应该比正则效果好