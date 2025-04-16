from cheap.utils import load_workflow
from settings import IS_DEV
from cheap.repo.job_repo import JobRepo
from cheap.repo.data_sync_repo import DataSyncRepo
from cheap.etl.utils import msg_robot


class JobAggregates:
    def __init__(self, job_inst):
        self.inst = job_inst

    def register_processing(self):
        pass

    def exe(self):
        pass


class JobManager:
    def __init__(self):
        self.job_repo = JobRepo()
        self.data_sync_repo = DataSyncRepo()

    def __entity2inst(self, entity=None, entity_list=None):
        if entity is not None:
            inst = Job()
        elif entity_list is not None:
            inst = [Job() for j in entity_list]
        else:
            raise Exception('')
        return inst

    def get_job_list(self, job_id_list=None):
        return self.__entity2inst(entity_list=self.job_repo.get_job_list(job_id_list))

    def get_follow_job_list(self, job):
        return self.__entity2inst(entity_list=self.job_repo.follow_job_list(job))


    def __exe(self, job):
        if job.job_type == 'workflow':
            wf = load_workflow(job.work_dir)
            wf.main()
        elif job.job_type == 'datasync':
            job_list = job.params.split(',')
            self.__data_sync(job_list)
        elif job.job_type == 'datacheck':
            job_list = job.params.split(',')
            self.__data_check(job_list)
        else:
            raise Exception('无效作业类型')
        return 0, ""

    def run(self, job):
        log_id = self.job_repo.register_job_start(job)
        if IS_DEV:
            code, msg = self.__exe(job)
        else:
            try:
                code, msg = self.__exe(job)
            except Exception as err:
                code, msg = -1, str(err)
        if code == 0:
            self.job_repo.register_job_end(job=job, log_id=log_id)
        else:
            self.job_repo.register_job_end(job=job, log_id=log_id, job_log_info={'message': msg})
            msg_robot(robot_id=job.message_robot, msg='ETL任务 ' + str(job.name) + '\n执行出错\n\n' + str(msg)[0:100])

        follow_job_list = self.job_repo.follow_job(job)
        if len(follow_job_list) == 0:
            return []
        else:
            return follow_job_list

    def main(self, job_id_list):
        if len(job_id_list) == 0:
            print('没有任务')
            return None

        job_list = self.get_job_list(job_id_list)
        for job in job_list:
            job.register_processing()

        while len(job_list) > 0:
            job = job_list.pop(0)
            if IS_DEV:
                print(job)
            job.exe()
            follow_job = self.get_follow_job_list(job.repo)
            job_list.extend(follow_job)
