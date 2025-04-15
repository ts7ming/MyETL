import sys
from cheap.etl.utils import msg_robot
from settings import IS_DEV
from cheap.repo.job_repo import JobRepo
from cheap.job_manager import JobManager


def main(job_list=None):
    jm = JobManager()
    job_repo = JobRepo()
    job_list = job_repo.pending_job(job_list)
    if len(job_list) == 0:
        print('没有任务')
        exit()

    while len(job_list) > 0:
        job_repo.collect_job(job_list)
        job = job_list.pop(0)
        if IS_DEV:
            print(job)
        follow_job = jm.run(job)
        job_list.extend(follow_job)


if __name__ == '__main__':
    user_job_list = sys.argv[1:]
    if len(user_job_list) == 0:
        user_job_list = None
    if IS_DEV:
        main(user_job_list)
    else:
        try:
            main(user_job_list)
        except Exception as e:
            msg_robot('1000', msg='调度出错\n\n' + str(e)[0:100])
