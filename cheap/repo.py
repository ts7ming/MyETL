from pyqueen import TimeKit
from sqlalchemy import and_, or_, func
from models import EtlJob, EtlJobLog,ETLJobExecutionStatus
from cheap.utils import session_context


class JobRepo(EtlJob):
    """
    作业管理
    """

    def __init__(self):
        self.status = ETLJobExecutionStatus

    def job_list(self, job_filter=None):
        """
        作业列表
        :param job_filter:
        :return:
        """
        with session_context() as session:
            job_list = session.query(self).filter(job_filter).all()
        return job_list

    def pending_job(self, job_list=None):
        """
        待执行作业
        """
        if job_list is None:
            tk = TimeKit()
            cur_month = str(int(str(tk.theday)[4:6])) + ','
            cur_week = str(tk.nday_of_week) + ','
            cur_day = str(int(str(tk.theday)[6:8])) + ','
            cur_hour = str(tk.hour) + ','
            cur_minute = str(tk.minute) + ','
            job_filter = and_(
                (self.execution_status.in_([0, 99]), self.job_status == 1),
                or_(self.job_schedule_month == '*', func.concat(self.job_schedule_month, ',').like(f'{cur_month},%')),
                or_(self.job_schedule_week == '*', func.concat(self.job_schedule_week, ',').like(f'{cur_week},%')),
                or_(self.job_schedule_day == '*', func.concat(self.job_schedule_day, ',').like(f'{cur_day},%')),
                or_(self.job_schedule_hour == '*', func.concat(self.job_schedule_hour, ',').like(f'{cur_hour},%')),
                or_(self.job_schedule_minute == '*', func.concat(self.job_schedule_minute, ',').like(f'{cur_minute},%'))
            )
        else:
            job_list_str = [str(x) for x in job_list]
            job_filter = EtlJob.execution_status.in_(job_list_str)
        pending_job_list = self.job_list(job_filter)
        return pending_job_list

    def collect_job(self, job_list):
        """
        领取任务, 标记任务执行中
        :param job_list:
        :return:
        """
        job_ids = [job['id'] for job in job_list]
        with session_context() as session:
            self.query(EtlJob).filter(EtlJob.id.in_(job_ids)).update({EtlJob.execution_status: self.status.collected}, synchronize_session=False)
            session.commit()

    def follow_job(self, job):
        """
        检查后序作业
        :return:
        """
        job_filter = and_(
            self.execution_status.in_([0, 99]),
            self.job_status == 1,
            EtlJob.job_depend == job.id
        )
        return self.job_list(job_filter)

    def register_job_start(self, job):
        with session_context() as session:
            self.query(EtlJob).filter(self.id == job.id).update({EtlJob.execution_status: self.status.running}, synchronize_session=False)
            new_log = EtlJobLog(id=job.id, start_time=func.now)
            session.add(new_log)
            session.commit()
            log_id = session.query(func.max(EtlJobLog.id)).filter(EtlJobLog.job_id == job_id).scalar()
        return log_id

    def register_job_success(self, job, job_log):
        with session_context() as session:
            self.query(EtlJob).filter(self.id == job.id).update({EtlJob.execution_status: self.status.pending}, synchronize_session=False)
            self.query(EtlJobLog).filter(self.id == job_log.id).update({EtlJob.execution_status: self.status.success}, synchronize_session=False)
            session.commit()

    def register_job_error(self, job, job_log, msg):
        with session_context() as session:
            self.query(EtlJob).filter(self.id == job.id).update({EtlJob.execution_status: self.status.pending}, synchronize_session=False)
            err = {
                EtlJobLog.execution_status: self.status.error,
                EtlJobLog.error_message: msg,
                EtlJobLog.end_time: func.now
            }
            self.query(EtlJobLog).filter(self.id == job_log.id).update(err, synchronize_session=False)
            session.commit()