-- ----------------------------
-- Table structure for etl_data_check
-- ----------------------------
IF EXISTS (SELECT * FROM sys.all_objects WHERE object_id = OBJECT_ID(N'[dbo].[etl_data_check]') AND type IN ('U'))
	DROP TABLE [dbo].[etl_data_check]
GO

CREATE TABLE [dbo].[etl_data_check] (
  [id] int  NOT NULL,
  [server_id] int  NULL,
  [db_name] varchar(255) COLLATE Chinese_PRC_CI_AS  NULL,
  [check_sql] nvarchar(max) COLLATE Chinese_PRC_CI_AS  NULL,
  [check_value] nvarchar(50) COLLATE Chinese_PRC_CI_AS  NULL,
  [warning_message] nvarchar(max) COLLATE Chinese_PRC_CI_AS  NULL,
  [robot_id] int  NULL
)
GO

ALTER TABLE [dbo].[etl_data_check] SET (LOCK_ESCALATION = TABLE)
GO

EXEC sp_addextendedproperty
'MS_Description', N'目标服务器',
'SCHEMA', N'dbo',
'TABLE', N'etl_data_check',
'COLUMN', N'server_id'
GO

EXEC sp_addextendedproperty
'MS_Description', N'目标数据库',
'SCHEMA', N'dbo',
'TABLE', N'etl_data_check',
'COLUMN', N'db_name'
GO

EXEC sp_addextendedproperty
'MS_Description', N'校验SQL(只取第一行第一列的值)',
'SCHEMA', N'dbo',
'TABLE', N'etl_data_check',
'COLUMN', N'check_sql'
GO

EXEC sp_addextendedproperty
'MS_Description', N'检查SQL结果',
'SCHEMA', N'dbo',
'TABLE', N'etl_data_check',
'COLUMN', N'check_value'
GO

EXEC sp_addextendedproperty
'MS_Description', N'和check_value不一致时发送通知',
'SCHEMA', N'dbo',
'TABLE', N'etl_data_check',
'COLUMN', N'warning_message'
GO

EXEC sp_addextendedproperty
'MS_Description', N'通知机器人id',
'SCHEMA', N'dbo',
'TABLE', N'etl_data_check',
'COLUMN', N'robot_id'
GO

EXEC sp_addextendedproperty
'MS_Description', N'ETL-数据校验',
'SCHEMA', N'dbo',
'TABLE', N'etl_data_check'
GO


-- ----------------------------
-- Table structure for etl_data_sync
-- ----------------------------
IF EXISTS (SELECT * FROM sys.all_objects WHERE object_id = OBJECT_ID(N'[dbo].[etl_data_sync]') AND type IN ('U'))
	DROP TABLE [dbo].[etl_data_sync]
GO

CREATE TABLE [dbo].[etl_data_sync] (
  [id] int  IDENTITY(1,1) NOT NULL,
  [from_server] int  NOT NULL,
  [from_db] nvarchar(50) COLLATE Chinese_PRC_CI_AS  NULL,
  [from_sql] nvarchar(max) COLLATE Chinese_PRC_CI_AS  NULL,
  [to_server] int  NOT NULL,
  [to_db] nvarchar(50) COLLATE Chinese_PRC_CI_AS  NULL,
  [to_table] nvarchar(100) COLLATE Chinese_PRC_CI_AS  NULL,
  [before_write] nvarchar(max) COLLATE Chinese_PRC_CI_AS  NULL
)
GO

ALTER TABLE [dbo].[etl_data_sync] SET (LOCK_ESCALATION = TABLE)
GO

EXEC sp_addextendedproperty
'MS_Description', N'来源服务器',
'SCHEMA', N'dbo',
'TABLE', N'etl_data_sync',
'COLUMN', N'from_server'
GO

EXEC sp_addextendedproperty
'MS_Description', N'来源数据库',
'SCHEMA', N'dbo',
'TABLE', N'etl_data_sync',
'COLUMN', N'from_db'
GO

EXEC sp_addextendedproperty
'MS_Description', N'取数SQL',
'SCHEMA', N'dbo',
'TABLE', N'etl_data_sync',
'COLUMN', N'from_sql'
GO

EXEC sp_addextendedproperty
'MS_Description', N'目标服务器',
'SCHEMA', N'dbo',
'TABLE', N'etl_data_sync',
'COLUMN', N'to_server'
GO

EXEC sp_addextendedproperty
'MS_Description', N'目标数据库',
'SCHEMA', N'dbo',
'TABLE', N'etl_data_sync',
'COLUMN', N'to_db'
GO

EXEC sp_addextendedproperty
'MS_Description', N'目标表名',
'SCHEMA', N'dbo',
'TABLE', N'etl_data_sync',
'COLUMN', N'to_table'
GO

EXEC sp_addextendedproperty
'MS_Description', N'写入前执行',
'SCHEMA', N'dbo',
'TABLE', N'etl_data_sync',
'COLUMN', N'before_write'
GO

EXEC sp_addextendedproperty
'MS_Description', N'ETL-数据同步作业',
'SCHEMA', N'dbo',
'TABLE', N'etl_data_sync'
GO


-- ----------------------------
-- Table structure for etl_data_sync_log
-- ----------------------------
IF EXISTS (SELECT * FROM sys.all_objects WHERE object_id = OBJECT_ID(N'[dbo].[etl_data_sync_log]') AND type IN ('U'))
	DROP TABLE [dbo].[etl_data_sync_log]
GO

CREATE TABLE [dbo].[etl_data_sync_log] (
  [id] int  IDENTITY(1,1) NOT NULL,
  [sync_id] int  NOT NULL,
  [start_time] datetime  NULL,
  [end_time] datetime  NULL,
  [sync_status] int  NULL,
  [sync_rows] int  NULL
)
GO

ALTER TABLE [dbo].[etl_data_sync_log] SET (LOCK_ESCALATION = TABLE)
GO

EXEC sp_addextendedproperty
'MS_Description', N'etl_data_sync.id',
'SCHEMA', N'dbo',
'TABLE', N'etl_data_sync_log',
'COLUMN', N'sync_id'
GO

EXEC sp_addextendedproperty
'MS_Description', N'开始时间',
'SCHEMA', N'dbo',
'TABLE', N'etl_data_sync_log',
'COLUMN', N'start_time'
GO

EXEC sp_addextendedproperty
'MS_Description', N'完成时间',
'SCHEMA', N'dbo',
'TABLE', N'etl_data_sync_log',
'COLUMN', N'end_time'
GO

EXEC sp_addextendedproperty
'MS_Description', N'同步状态',
'SCHEMA', N'dbo',
'TABLE', N'etl_data_sync_log',
'COLUMN', N'sync_status'
GO

EXEC sp_addextendedproperty
'MS_Description', N'同步行数',
'SCHEMA', N'dbo',
'TABLE', N'etl_data_sync_log',
'COLUMN', N'sync_rows'
GO

EXEC sp_addextendedproperty
'MS_Description', N'ETL-数据同步作业详情',
'SCHEMA', N'dbo',
'TABLE', N'etl_data_sync_log'
GO


-- ----------------------------
-- Table structure for etl_devops_fr_sql
-- ----------------------------
IF EXISTS (SELECT * FROM sys.all_objects WHERE object_id = OBJECT_ID(N'[dbo].[etl_devops_fr_sql]') AND type IN ('U'))
	DROP TABLE [dbo].[etl_devops_fr_sql]
GO

CREATE TABLE [dbo].[etl_devops_fr_sql] (
  [fr_project] nvarchar(50) COLLATE Chinese_PRC_CI_AS  NULL,
  [fr_path] nvarchar(max) COLLATE Chinese_PRC_CI_AS  NULL,
  [server] nvarchar(50) COLLATE Chinese_PRC_CI_AS  NULL,
  [fr_dataset] varchar(50) COLLATE Chinese_PRC_CI_AS  NULL,
  [sql] nvarchar(max) COLLATE Chinese_PRC_CI_AS  NULL
)
GO

ALTER TABLE [dbo].[etl_devops_fr_sql] SET (LOCK_ESCALATION = TABLE)
GO

EXEC sp_addextendedproperty
'MS_Description', N'ETL-帆软查询SQL',
'SCHEMA', N'dbo',
'TABLE', N'etl_devops_fr_sql'
GO


-- ----------------------------
-- Table structure for etl_job
-- ----------------------------
IF EXISTS (SELECT * FROM sys.all_objects WHERE object_id = OBJECT_ID(N'[dbo].[etl_job]') AND type IN ('U'))
	DROP TABLE [dbo].[etl_job]
GO

CREATE TABLE [dbo].[etl_job] (
  [id] int  IDENTITY(1,1) NOT NULL,
  [job_name] nvarchar(100) COLLATE Chinese_PRC_CI_AS  NULL,
  [job_type] nvarchar(50) COLLATE Chinese_PRC_CI_AS  NULL,
  [job_dir] nvarchar(50) COLLATE Chinese_PRC_CI_AS  NULL,
  [job_params] nvarchar(max) COLLATE Chinese_PRC_CI_AS  NULL,
  [execution_status] int  NULL,
  [job_schedule_minute] varchar(120) COLLATE Chinese_PRC_CI_AS  NULL,
  [job_schedule_hour] varchar(100) COLLATE Chinese_PRC_CI_AS  NULL,
  [job_schedule_day] varchar(100) COLLATE Chinese_PRC_CI_AS  NULL,
  [job_schedule_week] varchar(20) COLLATE Chinese_PRC_CI_AS  NULL,
  [job_schedule_month] varchar(50) COLLATE Chinese_PRC_CI_AS  NULL,
  [job_status] int  NULL,
  [job_depend] nvarchar(100) COLLATE Chinese_PRC_CI_AS  NULL,
  [message_robot] int  NULL
)
GO

ALTER TABLE [dbo].[etl_job] SET (LOCK_ESCALATION = TABLE)
GO

EXEC sp_addextendedproperty
'MS_Description', N'job_id',
'SCHEMA', N'dbo',
'TABLE', N'etl_job',
'COLUMN', N'id'
GO

EXEC sp_addextendedproperty
'MS_Description', N'名称',
'SCHEMA', N'dbo',
'TABLE', N'etl_job',
'COLUMN', N'job_name'
GO

EXEC sp_addextendedproperty
'MS_Description', N'类型: workflow,datasync,workflow_dev,datasync_dev',
'SCHEMA', N'dbo',
'TABLE', N'etl_job',
'COLUMN', N'job_type'
GO

EXEC sp_addextendedproperty
'MS_Description', N'datasync不填',
'SCHEMA', N'dbo',
'TABLE', N'etl_job',
'COLUMN', N'job_dir'
GO

EXEC sp_addextendedproperty
'MS_Description', N'参数. workflow填脚本路径; datasync填任务id(多个任务逗号分隔)',
'SCHEMA', N'dbo',
'TABLE', N'etl_job',
'COLUMN', N'job_params'
GO

EXEC sp_addextendedproperty
'MS_Description', N'执行状态. 0:待执行,1:执行中,2:执行完成;3执行出错;99:立即执行',
'SCHEMA', N'dbo',
'TABLE', N'etl_job',
'COLUMN', N'execution_status'
GO

EXEC sp_addextendedproperty
'MS_Description', N'作业计划-分钟',
'SCHEMA', N'dbo',
'TABLE', N'etl_job',
'COLUMN', N'job_schedule_minute'
GO

EXEC sp_addextendedproperty
'MS_Description', N'作业计划-小时',
'SCHEMA', N'dbo',
'TABLE', N'etl_job',
'COLUMN', N'job_schedule_hour'
GO

EXEC sp_addextendedproperty
'MS_Description', N'作业计划-日期',
'SCHEMA', N'dbo',
'TABLE', N'etl_job',
'COLUMN', N'job_schedule_day'
GO

EXEC sp_addextendedproperty
'MS_Description', N'作业计划-星期',
'SCHEMA', N'dbo',
'TABLE', N'etl_job',
'COLUMN', N'job_schedule_week'
GO

EXEC sp_addextendedproperty
'MS_Description', N'作业计划-月份',
'SCHEMA', N'dbo',
'TABLE', N'etl_job',
'COLUMN', N'job_schedule_month'
GO

EXEC sp_addextendedproperty
'MS_Description', N'作业状态: 0:停用, 1:启用',
'SCHEMA', N'dbo',
'TABLE', N'etl_job',
'COLUMN', N'job_status'
GO

EXEC sp_addextendedproperty
'MS_Description', N'作业依赖, 前序job_id',
'SCHEMA', N'dbo',
'TABLE', N'etl_job',
'COLUMN', N'job_depend'
GO

EXEC sp_addextendedproperty
'MS_Description', N'报错机器人(为空不通知)',
'SCHEMA', N'dbo',
'TABLE', N'etl_job',
'COLUMN', N'message_robot'
GO

EXEC sp_addextendedproperty
'MS_Description', N'ETL-作业',
'SCHEMA', N'dbo',
'TABLE', N'etl_job'
GO


-- ----------------------------
-- Table structure for etl_job_log
-- ----------------------------
IF EXISTS (SELECT * FROM sys.all_objects WHERE object_id = OBJECT_ID(N'[dbo].[etl_job_log]') AND type IN ('U'))
	DROP TABLE [dbo].[etl_job_log]
GO

CREATE TABLE [dbo].[etl_job_log] (
  [id] int  IDENTITY(1,1) NOT NULL,
  [job_id] int  NOT NULL,
  [start_time] datetime  NULL,
  [end_time] datetime  NULL,
  [execution_status] int  NULL,
  [error_message] nvarchar(max) COLLATE Chinese_PRC_CI_AS  NULL
)
GO

ALTER TABLE [dbo].[etl_job_log] SET (LOCK_ESCALATION = TABLE)
GO

EXEC sp_addextendedproperty
'MS_Description', N'etl_job.id',
'SCHEMA', N'dbo',
'TABLE', N'etl_job_log',
'COLUMN', N'job_id'
GO

EXEC sp_addextendedproperty
'MS_Description', N'开始时间',
'SCHEMA', N'dbo',
'TABLE', N'etl_job_log',
'COLUMN', N'start_time'
GO

EXEC sp_addextendedproperty
'MS_Description', N'完成时间',
'SCHEMA', N'dbo',
'TABLE', N'etl_job_log',
'COLUMN', N'end_time'
GO

EXEC sp_addextendedproperty
'MS_Description', N'执行状态',
'SCHEMA', N'dbo',
'TABLE', N'etl_job_log',
'COLUMN', N'execution_status'
GO

EXEC sp_addextendedproperty
'MS_Description', N'报错信息',
'SCHEMA', N'dbo',
'TABLE', N'etl_job_log',
'COLUMN', N'error_message'
GO

EXEC sp_addextendedproperty
'MS_Description', N'ETL-作业日志',
'SCHEMA', N'dbo',
'TABLE', N'etl_job_log'
GO


-- ----------------------------
-- Table structure for etl_robot
-- ----------------------------
IF EXISTS (SELECT * FROM sys.all_objects WHERE object_id = OBJECT_ID(N'[dbo].[etl_robot]') AND type IN ('U'))
	DROP TABLE [dbo].[etl_robot]
GO

CREATE TABLE [dbo].[etl_robot] (
  [id] int  NOT NULL,
  [access_token] varchar(100) COLLATE Chinese_PRC_CI_AS  NULL,
  [secret] varchar(100) COLLATE Chinese_PRC_CI_AS  NULL,
  [name] nvarchar(50) COLLATE Chinese_PRC_CI_AS  NULL
)
GO

ALTER TABLE [dbo].[etl_robot] SET (LOCK_ESCALATION = TABLE)
GO

EXEC sp_addextendedproperty
'MS_Description', N'ETL-钉钉机器人',
'SCHEMA', N'dbo',
'TABLE', N'etl_robot'
GO


-- ----------------------------
-- Table structure for etl_server
-- ----------------------------
IF EXISTS (SELECT * FROM sys.all_objects WHERE object_id = OBJECT_ID(N'[dbo].[etl_server]') AND type IN ('U'))
	DROP TABLE [dbo].[etl_server]
GO

CREATE TABLE [dbo].[etl_server] (
  [server_id] int  NOT NULL,
  [server_name] nvarchar(100) COLLATE Chinese_PRC_CI_AS  NULL
)
GO

ALTER TABLE [dbo].[etl_server] SET (LOCK_ESCALATION = TABLE)
GO

EXEC sp_addextendedproperty
'MS_Description', N'ETL-服务器列表',
'SCHEMA', N'dbo',
'TABLE', N'etl_server'
GO


-- ----------------------------
-- Table structure for etl_workflow_log
-- ----------------------------
IF EXISTS (SELECT * FROM sys.all_objects WHERE object_id = OBJECT_ID(N'[dbo].[etl_workflow_log]') AND type IN ('U'))
	DROP TABLE [dbo].[etl_workflow_log]
GO

CREATE TABLE [dbo].[etl_workflow_log] (
  [id] int  IDENTITY(1,1) NOT NULL,
  [py_path] nvarchar(200) COLLATE Chinese_PRC_CI_AS  NULL,
  [func_name] nvarchar(100) COLLATE Chinese_PRC_CI_AS  NULL,
  [start_time] datetime  NULL,
  [end_time] datetime  NULL,
  [duration] int  NULL,
  [file_path] nvarchar(max) COLLATE Chinese_PRC_CI_AS  NULL,
  [sql_text] nvarchar(max) COLLATE Chinese_PRC_CI_AS  NULL,
  [server_id] varchar(100) COLLATE Chinese_PRC_CI_AS  NULL,
  [db_name] varchar(100) COLLATE Chinese_PRC_CI_AS  NULL,
  [table_name] varchar(100) COLLATE Chinese_PRC_CI_AS  NULL
)
GO

ALTER TABLE [dbo].[etl_workflow_log] SET (LOCK_ESCALATION = TABLE)
GO

EXEC sp_addextendedproperty
'MS_Description', N'py脚本',
'SCHEMA', N'dbo',
'TABLE', N'etl_workflow_log',
'COLUMN', N'py_path'
GO

EXEC sp_addextendedproperty
'MS_Description', N'函数',
'SCHEMA', N'dbo',
'TABLE', N'etl_workflow_log',
'COLUMN', N'func_name'
GO

EXEC sp_addextendedproperty
'MS_Description', N'开始时间',
'SCHEMA', N'dbo',
'TABLE', N'etl_workflow_log',
'COLUMN', N'start_time'
GO

EXEC sp_addextendedproperty
'MS_Description', N'结束时间',
'SCHEMA', N'dbo',
'TABLE', N'etl_workflow_log',
'COLUMN', N'end_time'
GO

EXEC sp_addextendedproperty
'MS_Description', N'用时',
'SCHEMA', N'dbo',
'TABLE', N'etl_workflow_log',
'COLUMN', N'duration'
GO

EXEC sp_addextendedproperty
'MS_Description', N'文件路径',
'SCHEMA', N'dbo',
'TABLE', N'etl_workflow_log',
'COLUMN', N'file_path'
GO

EXEC sp_addextendedproperty
'MS_Description', N'执行sql',
'SCHEMA', N'dbo',
'TABLE', N'etl_workflow_log',
'COLUMN', N'sql_text'
GO

EXEC sp_addextendedproperty
'MS_Description', N'目标服务器',
'SCHEMA', N'dbo',
'TABLE', N'etl_workflow_log',
'COLUMN', N'server_id'
GO

EXEC sp_addextendedproperty
'MS_Description', N'目标数据库',
'SCHEMA', N'dbo',
'TABLE', N'etl_workflow_log',
'COLUMN', N'db_name'
GO

EXEC sp_addextendedproperty
'MS_Description', N'目标表',
'SCHEMA', N'dbo',
'TABLE', N'etl_workflow_log',
'COLUMN', N'table_name'
GO

EXEC sp_addextendedproperty
'MS_Description', N'ETL-工作流日志',
'SCHEMA', N'dbo',
'TABLE', N'etl_workflow_log'
GO
