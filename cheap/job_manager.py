from cheap.utils import load_workflow
from settings import DEV
from cheap.repo.job_repo import JobRepo
from cheap.repo.data_sync_repo import DataSyncRepo
from cheap.etl.utils import msg_robot


class JobManager:
    def __init__(self):
        self.job_repo = JobRepo()
        self.data_sync_repo = DataSyncRepo()

    def __data_sync(self, job_list):
        data_sync_job_list = self.data_sync_repo.job_list(job_filter=None)


    def __data_check(self, job_list):
        pass

    def __exe(self, job):
        if job.job_type == 'workflow':
            wf = load_workflow(job.job_dir)
            wf.main()
        elif job.job_type == 'datasync':
            job_list = job.job_params.split(',')
            self.__data_sync(job_list)
        elif job.job_type == 'datacheck':
            job_list = job.job_params.split(',')
            self.__data_check(job_list)
        else:
            raise Exception('无效作业类型')
        return 0, ""

    def run(self, job):
        job_log = self.job_repo.register_job_start(job)
        if DEV:
            code, msg = self.__exe(job)
        else:
            try:
                code, msg = self.__exe(job)
            except Exception as err:
                code, msg = -1, str(err)
        if code == 0:
            self.job_repo.register_job_success(job=job, job_log=job_log)
        else:
            self.job_repo.register_job_error(job=job, job_log=job_log, msg=msg)
            msg_robot(robot_id=job['message_robot'], msg='ETL任务 ' + str(job['job_name']) + '\n执行出错\n\n' + str(msg)[0:100])

        follow_job_list = self.job_repo.follow_job(job)
        if len(follow_job_list) == 0:
            return []
        else:
            return follow_job_list
