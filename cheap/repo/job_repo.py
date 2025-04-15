from pyqueen import TimeKit
from sqlalchemy import and_, or_, func
from cheap.models import EtlJob, EtlJobLog
from cheap.repo.base import BaseJobRepo


class JobRepo(BaseJobRepo):
    """
    作业管理
    """

    def __init__(self):
        super().__init__(job_main=EtlJob, job_log=EtlJobLog)

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
                (self.job.job_status.in_([0, 99]), self.job.job_status == 1),
                or_(self.job.job_schedule_month == '*', func.concat(self.job.job_schedule_month, ',').like(f'{cur_month},%')),
                or_(self.job.job_schedule_week == '*', func.concat(self.job.job_schedule_week, ',').like(f'{cur_week},%')),
                or_(self.job.job_schedule_day == '*', func.concat(self.job.job_schedule_day, ',').like(f'{cur_day},%')),
                or_(self.job.job_schedule_hour == '*', func.concat(self.job.job_schedule_hour, ',').like(f'{cur_hour},%')),
                or_(self.job.job_schedule_minute == '*', func.concat(self.job.job_schedule_minute, ',').like(f'{cur_minute},%'))
            )
        else:
            job_list_str = [str(x) for x in job_list]
            job_filter = EtlJob.job_status.in_(job_list_str)
        pending_job_list = self.job_filter(job_filter)
        return pending_job_list

