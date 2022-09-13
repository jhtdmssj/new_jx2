#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Version: 1.0
# CreateTime: 2021/11/9 14:24
import pymysql

class pymysql_tool():
    # 数据库连接参数
    __db_host = "10.20.12.52"
    __db_port = 3306
    __db_username = "produce"
    __db_password = "root"
    __db_database = "produce_db"
    __db_charset = 'utf8'

    def __init__(self, host=__db_host, port=__db_port, user=__db_username,
                 password=__db_password, database=__db_database, charset=__db_charset):
        """ 初始化数据库连接参数

        :param host: 主机地址
        :param port: 端口
        :param user: 用户名
        :param password: 密码
        :param database: 数据库
        :param charset: 编码
        """
        try:
            self.conn = pymysql.connect(host=host, user=user, password=password, database=database,
                                        port=port,
                                        charset=charset)
        except pymysql.Error as e:
            print("Connect Database Failed.", str(e))
        self.cursor = self.conn.cursor()

    # 查询所有
    def fetchAll(self, sql):
        """ 查询所有

        :param sql: sql
        :return: 结果集
        """
        try:
            self.__execute(sql)
            return self.cursor.fetchall()
        except Exception as e:
            print(e)

    # 查询多条数据
    def fetchMany(self, sql, size=1):
        """ 查询多条数据

        :param sql: sql
        :param size: 要查几条
        :return: 结果集
        """
        try:
            self.__execute(sql)
            return self.cursor.fetchmany(size)
        except Exception as e:
            print(e)

    # 查询一条数据
    def fetchOne(self, sql):
        """ 查询一条数据

        :param sql: sql
        :return: 数据结果
        """
        try:
            self.__execute(sql)
            return self.cursor.fetchone()
        except Exception as e:
            print(e)

    # 增删改
    def change(self, sql):
        """ 增删改

        :param sql: sql
        :return: 受影响行数
        """
        try:
            self.__execute(sql)
            self.conn.commit()
            return self.cursor.rowcount
        except Exception as e:
            print(e)

    # 执行私有方法
    def __execute(self, sql):
        self.cursor.execute(sql)

    # 关闭游标和连接
    def __del__(self):
        self.cursor.close()
        self.conn.close()
