from pyqueen import TimeKit
from sqlalchemy import and_, or_, func
from cheap.models import ExecutionStatus
from cheap.utils import session_context


class BaseJobRepo:
    """
    作业管理
    """

    def __init__(self, job_main, job_log):
        self.job = job_main
        self.log = job_log
        self.status = ExecutionStatus

    def job_filter(self, job_filter=None):
        """
        作业列表
        :param job_filter:
        :return:
        """
        with session_context() as session:
            job_list = session.query(self.job).filter(job_filter).all()
        return job_list


    def job_list(self, customer_list):
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
            session.query(self.job).filter(self.job.id.in_(job_ids)).update({self.job.execution_status: self.status.collected},
                                                                            synchronize_session=False)
            session.commit()

    def follow_job(self, job):
        """
        检查后序作业
        :return:
        """
        job_filter = and_(
            self.job.execution_status.in_([0, 99]),
            self.job.job_status == 1,
            self.job.job_depend == job.id
        )
        return self.job_list(job_filter)

    def register_job_start(self, job):
        with session_context() as session:
            session.query(self.job).filter(self.job.id == job.id).update({self.job.execution_status: self.status.running}, synchronize_session=False)
            new_log = self.log(id=job.id, start_time=func.now)
            session.add(new_log)
            session.commit()
            log_id = session.query(func.max(self.log.id)).filter(self.log.job_id == job.id).scalar()
        return log_id

    def register_job_success(self, job, job_log):
        with session_context() as session:
            session.query(self.job).filter(self.job.id == job.id).update({self.job.execution_status: self.status.pending}, synchronize_session=False)
            session.query(self.log).filter(self.log.id == job_log.id).update({self.job.execution_status: self.status.success},
                                                                             synchronize_session=False)
            session.commit()

    def register_job_error(self, job, job_log, msg):
        with session_context() as session:
            session.query(self.job).filter(self.job.id == job.id).update({self.job.execution_status: self.status.pending}, synchronize_session=False)
            err = {
                self.log.execution_status: self.status.error,
                self.log.error_message: msg,
                self.log.end_time: func.now
            }
            session.query(self.log).filter(self.log.id == job_log.id).update(err, synchronize_session=False)
            session.commit()
