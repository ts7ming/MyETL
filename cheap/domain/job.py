from cheap.repo.base import DynamicRepo, Field
from cheap.domain.value_object import TableName




class JobAggregates(DynamicRepo):
    def __init__(self):
        super().__init__()
        self.__table_name__ = TableName.TABLE_ETL_JOB
        self.__table_comment__ = 'ETL-作业主表'

        self.id = Field(ft=int, cmt='', pk=True)

        self.name = Field(ft=str, cmt='作业名称')
        self.job_type = Field(ft=str, cmt='作业类型: workflow,datasync,datacheck,python')
        self.work_dir = Field(ft=str, cmt='工作目录')
        self.params = Field(ft=str, cmt='作业参数')
        self.status = Field(ft=int, cmt='作业状态(0:待执行,1:执行中,2:执行完成;3执行出错;99:立即执行)')
        self.enabled = Field(ft=int, cmt='作业启用(0:停用, 1:启用)')
        self.depend = Field(ft=str, cmt='作业依赖(job_id)')
        self.robot_id = Field(ft=int, cmt='通知机器人(robot_id)')
        self.schedule_minute = Field(ft=str, cmt='作业计划-分钟(0-59)')
        self.schedule_hour = Field(ft=str, cmt='作业计划-小时(0-23)')
        self.schedule_day = Field(ft=str, cmt='作业计划-日期(1-31)')
        self.schedule_week = Field(ft=str, cmt='作业计划-星期(1-7)')
        self.schedule_month = Field(ft=str, cmt='作业计划-月份(1-12)')
        self.xx = Field(ft=str, cmt='xxxx')

        self.task = []
        self.__job_log = 1
        self.__sub_job_log = 1

    def create_job(self):
        pass
