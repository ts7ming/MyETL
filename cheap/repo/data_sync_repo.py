from cheap.repo.models import EtlDataSync, EtlDataSyncLog
from cheap.repo.base import BaseRepo


class DataSyncRepo(BaseRepo):
    """
    作业管理
    """

    def __init__(self):
        super().__init__()
