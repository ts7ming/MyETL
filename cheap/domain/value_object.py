from sqlalchemy import Column, Integer, String, DateTime, create_engine


class Schedule:
    def __init__(self, second, minute, hour, day, week, month):
        pass


class Field:
    def __init__(self, ft, cmt, pk=False):
        self.value = ''
        self.type = ''
        self.cmt = cmt
        self.pk = pk
        self.orm_type = Integer


class TableName:
    from settings import (
        TABLE_ETL_CHECK,
        TABLE_ETL_SYNC,
        TABLE_ETL_SYNC_LOG,
        TABLE_ETL_WORKFLOW_LOG,
        TABLE_ETL_JOB,
        TABLE_ETL_ROBOT,
        TABLE_ETL_SERVER
    )