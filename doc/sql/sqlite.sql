-- ----------------------------
-- Table structure for etl_data_check
-- ----------------------------
DROP TABLE IF EXISTS "etl_data_check";
CREATE TABLE "etl_data_check" (
  "id" integer NOT NULL,
  "server_id" integer,
  "db_name" text,
  "check_sql" text,
  "check_value" text,
  "warning_message" text,
  "robot_id" integer
);

-- ----------------------------
-- Table structure for etl_data_sync
-- ----------------------------
DROP TABLE IF EXISTS "etl_data_sync";
CREATE TABLE "etl_data_sync" (
  "id" INTEGER NOT NULL,
  "from_server" integer NOT NULL,
  "from_db" text,
  "from_sql" text,
  "to_server" integer NOT NULL,
  "to_db" text,
  "to_table" text,
  "before_write" text,
  PRIMARY KEY ("id")
);

-- ----------------------------
-- Table structure for etl_data_sync_log
-- ----------------------------
DROP TABLE IF EXISTS "etl_data_sync_log";
CREATE TABLE "etl_data_sync_log" (
  "id" INTEGER NOT NULL,
  "sync_id" integer NOT NULL,
  "start_time" DATETIME,
  "end_time" DATETIME,
  "sync_status" integer,
  "sync_rows" integer,
  PRIMARY KEY ("id")
);

-- ----------------------------
-- Table structure for etl_devops_fr_sql
-- ----------------------------
DROP TABLE IF EXISTS "etl_devops_fr_sql";
CREATE TABLE "etl_devops_fr_sql" (
  "fr_project" text,
  "fr_path" text,
  "server" text,
  "fr_dataset" text,
  "sql" text
);

-- ----------------------------
-- Table structure for etl_job
-- ----------------------------
DROP TABLE IF EXISTS "etl_job";
CREATE TABLE "etl_job" (
  "id" INTEGER,
  "job_name" text,
  "job_type" text,
  "job_dir" text,
  "job_params" text,
  "execution_status" integer,
  "job_schedule_minute" text,
  "job_schedule_hour" text,
  "job_schedule_day" text,
  "job_schedule_week" text,
  "job_schedule_month" text,
  "job_status" integer,
  "job_depend" text,
  "message_robot" integer,
  PRIMARY KEY ("id")
);

-- ----------------------------
-- Table structure for etl_job_log
-- ----------------------------
DROP TABLE IF EXISTS "etl_job_log";
CREATE TABLE "etl_job_log" (
  "id" INTEGER,
  "job_id" integer NOT NULL,
  "start_time" DATETIME,
  "end_time" DATETIME,
  "execution_status" integer,
  "error_message" text,
  PRIMARY KEY ("id")
);

-- ----------------------------
-- Table structure for etl_robot
-- ----------------------------
DROP TABLE IF EXISTS "etl_robot";
CREATE TABLE "etl_robot" (
  "id" integer NOT NULL,
  "access_token" text,
  "secret" text,
  "name" text
);

-- ----------------------------
-- Table structure for etl_server
-- ----------------------------
DROP TABLE IF EXISTS "etl_server";
CREATE TABLE "etl_server" (
  "server_id" integer NOT NULL,
  "server_name" text
);

-- ----------------------------
-- Table structure for etl_workflow_log
-- ----------------------------
DROP TABLE IF EXISTS "etl_workflow_log";
CREATE TABLE "etl_workflow_log" (
  "id" INTEGER,
  "py_path" text,
  "func_name" text,
  "start_time" DATETIME,
  "end_time" DATETIME,
  "duration" integer,
  "file_path" text,
  "sql_text" text,
  "server_id" text,
  "db_name" text,
  "table_name" text,
  PRIMARY KEY ("id")
);
