# -*- coding: utf-8 -*-
# @Time    : 2022/12/6 23:18
# @Author  : hxq
# @Software: PyCharm
# @File    : __init__.py
import contextlib
import re
import json
import datetime
import importlib
from typing import Union
from json import JSONEncoder
from decimal import Decimal
from dbutils.pooled_db import PooledDB, PooledDedicatedDBConnection

from hxq.utils.decorator import func_run_times


class DateTimeEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, (datetime.date, datetime.datetime)):
            return obj.isoformat(sep=" ")
        elif isinstance(obj, Decimal):
            return str(obj)
        return super().default(obj)


class DBHelper:
    """简单的数据库连接池助手"""
    sql_conns = {
        'mysql'  : 'pymysql',
        'mssql'  : 'pymssql',
        'sqlite3': 'sqlite3'
    }

    def __init__(self, config):
        """
        初始化连接池
        :param config:
        """
        self.config = self.import_config(config)
        self.pool = None
        self.dbtype = self.config.setdefault('SQL_CREATOR', 'mysql').lower()
        database = importlib.import_module(self.sql_conns.get(self.dbtype))
        if self.sql_conns.get(self.dbtype) == "sqlite3":
            self.pool = PooledDB(
                creator=database,
                maxconnections=self.config.setdefault('SQL_MAX_CONNECT', 16),
                mincached=self.config.setdefault('SQL_MIN_CACHED', 1),
                blocking=self.config.setdefault('SQL_BLOCKING', True),
                database=self.config.setdefault('SQL_DATABASE', None),
            )
        else:
            self.pool = PooledDB(
                creator=database,
                maxconnections=self.config.setdefault('SQL_MAX_CONNECT', 16),
                mincached=self.config.setdefault('SQL_MIN_CACHED', 1),
                blocking=self.config.setdefault('SQL_BLOCKING', True),
                ping=self.config.setdefault('SQL_PING', 0),
                host=self.config.setdefault('SQL_HOST', '127.0.0.1'),
                port=self.config.setdefault('SQL_PORT', 3306),
                user=self.config.setdefault('SQL_USER', 'root'),
                password=self.config.setdefault('SQL_PASSWORD', None),
                database=self.config.setdefault('SQL_DATABASE', None),
                charset=self.config.setdefault('SQL_CHARSET', 'utf8mb4')
            )

    """导入配置"""

    @staticmethod
    def import_config(obj) -> dict:
        """
        导入字典or类对象中的配置信息
        """
        config = dict()
        if isinstance(obj, dict):
            [config.update({k.upper(): v}) for k, v in obj.items()]
        elif hasattr(obj, '__dict__'):
            [config.update({k: getattr(obj, k)}) if k.isupper() else '' for k in dir(obj)]
        else:
            raise ValueError('请导入正确的config对象!')
        return config

    def get_placeholder(self, num=1):
        """
        根据数据库类型选择占位符
        :return:
        """
        if self.dbtype == "mysql":
            return ','.join(['%s'] * num)
        elif self.dbtype == "mssql":
            return ','.join(['%s'] * num)
        elif self.dbtype == "sqlite3":
            return ','.join(['?'] * num)
        raise ValueError("Unsupported database type")

    @staticmethod
    def _tuple2dict(results, cursor) -> list:
        """
        列表类型转字典
        :param results:
        :param cursor:
        :return:
        """
        desc = list(map(lambda x: x[0], cursor.description))
        result = [dict(zip(desc, item)) for item in results]
        #  json.dumps(result, cls=DateTimeEncoder)
        return json.loads(DateTimeEncoder().encode(result))

    @contextlib.contextmanager
    def auto_commit(self, begin: bool = False):
        """
        用于批量或多个sql执行的自动提交管理
        示例1:
        with self.auto_commit() as cursor:
            cursor.executemany(sql_statement, values)
        示例2:
        with db.auto_commit(True) as cursor:
            for i in range(1000000):
                cursor.execute(f"INSERT INTO hxq('NAME','AGE') values('{i}')")
        """
        with self.connect() as conn:
            if begin is True:
                conn.begin()
            cursor = conn.cursor()
            try:
                yield cursor
                conn.commit()
            except Exception as e:
                conn.rollback()
                raise e
            finally:
                if cursor:
                    cursor.close()

    def executemany(self, sql_statement, values: list):
        """
        批量执行sql
        :param sql_statement:
        :param values:
        :return:
        """
        with self.connect() as conn:
            cursor = conn.cursor()
            try:
                cursor.executemany(sql_statement, values)
                conn.commit()
            except Exception as e:
                conn.rollback()
                raise e
            finally:
                if cursor:
                    cursor.close()

    # @func_run_times()
    def execute(self, sql_statement: str) -> Union[list, dict, int]:
        """
        执行增删改查sql语句
        :param sql_statement:
        :return:
        """
        with self.connect() as conn:
            cursor = conn.cursor()
            row_count = cursor.execute(sql_statement)
            # 匹配对大小写不敏感 ,SELECT|SHOW开头
            if re.search(r"^(SELECT|SHOW)", sql_statement, re.I):
                result = cursor.fetchall()
                return self._tuple2dict(result, cursor)
            cursor.connection.commit()
            cursor.close()
            return row_count if row_count else 0

    # @func_run_times()
    def first(self, sql_statement) -> dict:
        """
        查询一条数据
        :param sql_statement:
        :return:
        """
        with self.connect() as conn:
            cursor = conn.cursor()
            cursor.execute(sql_statement)
            result = cursor.fetchone()
            cursor.close()
        if not result:
            return {}
        return self._tuple2dict([result], cursor)[0]

    # @func_run_times()
    def all(self, sql_statement) -> list:
        """
        查询所有数据
        :param sql_statement:
        :return:
        """
        with self.connect() as conn:
            cursor = conn.cursor()
            cursor.execute(sql_statement)
            result = cursor.fetchall()
            cursor.close()
        if not result:
            return []
        return self._tuple2dict(result, cursor)

    @contextlib.contextmanager
    def connect(self) -> PooledDedicatedDBConnection:
        """
        创建连接
        :return:
        """
        conn = self.pool.connection()
        try:
            yield conn
        finally:
            self.close(conn)

    @staticmethod
    def close(conn):
        """
        关闭连接
        :param conn:
        :return:
        """
        # conn.cursor().close()
        if conn:
            conn.close()

    # def __enter__(self):
    #     """
    #     # 实现with obj as f 主动从连接池中拿连接对象 并存放至线程堆中
    #     """
    #     conn, cursor = self.connect()
    #     return cursor
    #
    # def __exit__(self, exc_type, exc_val, exc_tb):
    #     """
    #     # 实现with 结束 从线程堆中获取链接对象，并回收连接至连接池
    #     """
    #     print(exc_type, exc_val, exc_tb)
