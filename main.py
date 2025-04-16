import sys
from cheap.etl.utils import msg_robot
from settings import IS_DEV
from cheap.repo.job_repo import JobRepo
from cheap.job_manager import JobManager


def main(job_id_list=None):
    jm = JobManager()
    jm.main(job_id_list)



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
