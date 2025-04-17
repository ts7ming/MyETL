from pyqueen import TimeKit
from sqlalchemy import and_, or_, func
from cheap.repo.models import EtlJob, get_sub_job_entity, get_job_log_entity
from cheap.repo.base import BaseRepo
from cheap.repo.models import JobStatus


class JobRepo(BaseRepo):
    """
    作业管理
    """

    def __init__(self, session):
        super().__init__(session)
        self.job_entity = EtlJob

    def get_job_list(self, job_id_list):
        return self.get_entity_list(entity=self.job_entity, entity_id_list=job_id_list)

    def pending_job_list(self):
        """
        待执行作业
        """
        tk = TimeKit()
        cur_month = str(int(str(tk.theday)[4:6])) + ','
        cur_week = str(tk.nday_of_week) + ','
        cur_day = str(int(str(tk.theday)[6:8])) + ','
        cur_hour = str(tk.hour) + ','
        cur_minute = str(tk.minute) + ','
        job_filter = and_(
            (self.job_entity.job_status.in_([0, 99]), self.job_entity.job_status == 1),
            or_(self.job_entity.job_schedule_month == '*', func.concat(self.job_entity.job_schedule_month, ',').like(f'{cur_month},%')),
            or_(self.job_entity.job_schedule_week == '*', func.concat(self.job_entity.job_schedule_week, ',').like(f'{cur_week},%')),
            or_(self.job_entity.job_schedule_day == '*', func.concat(self.job_entity.job_schedule_day, ',').like(f'{cur_day},%')),
            or_(self.job_entity.job_schedule_hour == '*', func.concat(self.job_entity.job_schedule_hour, ',').like(f'{cur_hour},%')),
            or_(self.job_entity.job_schedule_minute == '*', func.concat(self.job_entity.job_schedule_minute, ',').like(f'{cur_minute},%'))
        )
        return self.get_entity_list(entity=self.job_entity, entity_filter=job_filter)

    def follow_job_list(self, job):
        job_filter = and_(
            self.job_entity.job_status.in_([0, 99]),
            self.job_entity.job_status == 1,
            self.job_entity.job_depend == job.id
        )
        return self.get_entity_list(entity=self.job_entity, entity_filter=job_filter)


class Job(JobRepo):
    def __init__(self, session):
        super().__init__(session)

    def register_job_processing(self, job):
        job.job_status = JobStatus.processing
        self.session.commit()

    def register_job_start(self, job: EtlJob, job_log_info=None):
        job.status = JobStatus.running


        if job_log_info is None:
            job_log_info = {}
        log_id = self.generate_id()
        job_log_info['id'] = log_id
        if 'start_time' not in job_log_info:
            job_log_info['start_time'] = func.now
        self.entity_update(entity=get_sub_job_entity(job), update_info=job_log_info)
        return log_id

    def register_job_end(self, job, log_id=None, job_log_info=None):
        job_filter = self.job_entity.id == job.id
        update_info = {self.job_entity.job_status: JobStatus.pending}
        self.entity_update(entity=self.job_entity, entity_filter=job_filter, update_info=update_info)
        if log_id is not None:
            if 'end_time' not in job_log_info:
                job_log_info['end_time'] = func.now
            self.entity_update(entity=get_job_log_entity(job), entity_filter=job_filter, update_info=job_log_info)
