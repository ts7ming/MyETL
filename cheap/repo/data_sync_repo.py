from pyqueen import TimeKit
from sqlalchemy import and_, or_, func
from cheap.models import EtlDataSync, EtlDataSyncLog
from cheap.utils import session_context
from cheap.repo.base import BaseJobRepo

class DataSyncRepo(BaseJobRepo):
    """
    作业管理
    """

    def __init__(self):
        super().__init__(job_main=EtlDataSync, job_log=EtlDataSyncLog)


