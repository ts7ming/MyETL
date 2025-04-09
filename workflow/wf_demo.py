import pandas as pd
from cheap import get_ds

ds = get_ds('main')


def init_demo():
    sql = '''create table if not exists demo (
        id integer primary key autoincrement,
        a int,
        b int,
        c int
    )'''
    ds.exe_sql(sql)


def write_demo():
    df = pd.DataFrame([[1, 2, 3], [4, 5, 6]], columns=['a', 'b', 'c'])
    ds.to_db(df, 'demo')


def update_demo():
    sql = 'update demo set a=100 where b=2'
    ds.exe_sql(sql)


def main():
    init_demo()
    write_demo()
    update_demo()
