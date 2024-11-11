# -*- coding: utf-8 -*-
# @Time    : 2023/4/6 23:38
# @Author  : hxq
# @Software: PyCharm
# @File    : db.py
import time
from hxq.libs.db import DBHelper

__all__ = [
    "DBHelper",
]

if __name__ == '__main__':
    CONFIG = {
        'SQL_CREATOR' : 'sqlite3',
        'SQL_DATABASE': r'blog.sqlite3'
    }
    db = DBHelper(config=CONFIG)

    # input(db.get_placeholder(2))
    create_table = '''
    CREATE TABLE IF NOT EXISTS hxq(
       ID INTEGER PRIMARY KEY AUTOINCREMENT,
       NAME           TEXT    NOT NULL,
       AGE            INT     NOT NULL,
       ADDRESS        CHAR(50),
       SALARY         REAL
    );
    '''
    db.execute(create_table)

    data_list = []
    for i in range(10):
        data_list.append(('test', f'{i}'))
    print(db.get_placeholder())
    sql = f"INSERT INTO hxq('NAME','AGE') VALUES ({db.get_placeholder(2)})"
    print(sql)
    db.executemany(sql, data_list)

    r = db.all("select * from hxq")
    print(r)
    if isinstance(r, list):
        for i in r:
            print(i)
    else:
        print(r)

    print(len(r))
