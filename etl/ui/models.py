from etl.ui import db


class EtlDataCheck(db.Model):
    __tablename__ = 'etl_data_check'

    id = db.Column(db.Integer, primary_key=True)
    server_id = db.Column(db.Integer)
    db_name = db.Column(db.Text)
    check_sql = db.Column(db.Text)
    check_value = db.Column(db.Text)
    warning_message = db.Column(db.Text)
    robot_id = db.Column(db.Integer)

    def __repr__(self):
        return f'<EtlDataCheck {self.id}>'


class EtlDataSync(db.Model):
    __tablename__ = 'etl_data_sync'

    id = db.Column(db.Integer, primary_key=True)
    from_server = db.Column(db.Integer, nullable=False)
    from_db = db.Column(db.Text)
    from_sql = db.Column(db.Text)
    to_server = db.Column(db.Integer, nullable=False)
    to_db = db.Column(db.Text)
    to_table = db.Column(db.Text)
    before_write = db.Column(db.Text)

    def __repr__(self):
        return f'<EtlDataSync {self.id}>'


class EtlDataSyncLog(db.Model):
    __tablename__ = 'etl_data_sync_log'

    id = db.Column(db.Integer, primary_key=True)
    sync_id = db.Column(db.Integer, nullable=False)
    start_time = db.Column(db.DateTime)  # 使用 SQLAlchemy 的 DateTime 类型
    end_time = db.Column(db.DateTime)
    sync_status = db.Column(db.Integer)
    sync_rows = db.Column(db.Integer)

    def __repr__(self):
        return f'<EtlDataSyncLog {self.id}>'


class EtlDevopsFrSql(db.Model):
    __tablename__ = 'etl_devops_fr_sql'
    id = db.Column(db.Integer, primary_key=True)
    fr_project = db.Column(db.Text)
    fr_path = db.Column(db.Text)
    server = db.Column(db.Text)
    fr_dataset = db.Column(db.Text)
    sql = db.Column(db.Text)

    def __repr__(self):
        return f'<EtlDevopsFrSql {self.id}>'


class EtlJob(db.Model):
    __tablename__ = 'etl_job'

    id = db.Column(db.Integer, primary_key=True)
    job_name = db.Column(db.Text)
    job_type = db.Column(db.Text)
    job_dir = db.Column(db.Text)
    job_params = db.Column(db.Text)
    execution_status = db.Column(db.Integer)
    job_schedule_minute = db.Column(db.Text)
    job_schedule_hour = db.Column(db.Text)
    job_schedule_day = db.Column(db.Text)
    job_schedule_week = db.Column(db.Text)
    job_schedule_month = db.Column(db.Text)
    job_status = db.Column(db.Integer)
    job_depend = db.Column(db.Text)
    message_robot = db.Column(db.Integer)

    def __repr__(self):
        return f'<EtlJob {self.job_name}>'


class EtlJobLog(db.Model):
    __tablename__ = 'etl_job_log'

    id = db.Column(db.Integer, primary_key=True)
    job_id = db.Column(db.Integer, nullable=False)
    start_time = db.Column(db.DateTime)
    end_time = db.Column(db.DateTime)
    execution_status = db.Column(db.Integer)
    error_message = db.Column(db.Text)

    def __repr__(self):
        return f'<EtlJobLog {self.id}>'


class EtlRobot(db.Model):
    __tablename__ = 'etl_robot'

    id = db.Column(db.Integer, primary_key=True)
    access_token = db.Column(db.Text)
    secret = db.Column(db.Text)
    name = db.Column(db.Text)

    def __repr__(self):
        return f'<EtlRobot {self.name}>'


class EtlServer(db.Model):
    __tablename__ = 'etl_server'

    server_id = db.Column(db.Integer, primary_key=True)
    server_name = db.Column(db.Text)

    def __repr__(self):
        return f'<EtlServer {self.server_name}>'


class EtlWorkflowLog(db.Model):
    __tablename__ = 'etl_workflow_log'

    id = db.Column(db.Integer, primary_key=True)
    py_path = db.Column(db.Text)
    func_name = db.Column(db.Text)
    start_time = db.Column(db.DateTime)
    end_time = db.Column(db.DateTime)
    duration = db.Column(db.Integer)
    file_path = db.Column(db.Text)
    sql_text = db.Column(db.Text)
    server_id = db.Column(db.Text)
    db_name = db.Column(db.Text)
    table_name = db.Column(db.Text)

    def __repr__(self):
        return f'<EtlWorkflowLog {self.id}>'
