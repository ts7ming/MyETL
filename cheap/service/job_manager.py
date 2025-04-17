from cheap.domain.job import JobAggregates


class JobManager:
    def __init__(self):
        self.ja = JobAggregates()

    def execute_job(self, job_id_list):
        pass

    def execute_schedule(self):
        pass

    def create_job(self):
        pass

    def create_task(self):
        pass


