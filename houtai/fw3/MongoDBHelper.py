#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: 王靖宗 季宏涛
# Version: 1.0
# CreateTime: 2021/11/9 10:39
# Description: MongoDB数据库操作封装
import sys


class MongoDBHelper(object):
    def __init__(self, db='test'):
        '''初始化连接'''
        import pymongo
        self.connect_client = pymongo.MongoClient('mongodb://10.20.12.52:27017/')
        self.mydb = self.connect_client[db]  # 连接指定数据库

    def insert_collection(self, collection_name, value):  # 单个插入
        mycol = self.mydb[collection_name]
        mycol_id = mycol.insert_one(value)
        return mycol_id.inserted_id  # 返回insert_id，即插入文档的id值

    def insert_batch_collection(self, collection_name, value_list):  # 批量插入
        mycol = self.mydb[collection_name]
        mycol_id = mycol.insert_many(value_list)
        return mycol_id.inserted_ids  # 返回insert_id集合，即插入文档的id值

    def select_one_collection(self, collection_name, search_col=None):  # 获取一条数据
        '''search_col：只能是dict类型,key大于等于一个即可，也可为空
        可使用修饰符查询：{"name": {"$gt": "H"}}#读取 name 字段中第一个字母 ASCII 值大于 "H" 的数据
        使用正则表达式查询：{"$regex": "^R"}#读取 name 字段中第一个字母为 "R" 的数据'''
        my_col = self.mydb[collection_name]
        try:
            result = my_col.find_one(search_col)  # 这里只会返回一个对象，数据需要自己取
            return result
        except TypeError as e:
            print('查询条件只能是dict类型')
            return None

    def select_all_collection(self, collection_name, search_col=None, limit_num=sys.maxsize, sort_col='None_sort',
                              sort='asc'):
        '''search_col：只能是dict类型,key大于等于一个即可，也可为空
        可使用修饰符查询：{"name": {"$gt": "H"}}#读取 name 字段中第一个字母 ASCII 值大于 "H" 的数据
        使用正则表达式查询：{"$regex": "^R"}#读取 name 字段中第一个字母为 "R" 的数据
        limit_num:返回指定条数记录，该方法只接受一个数字参数(sys.maxsize:返回一个最大的整数值)'''
        my_col = self.mydb[collection_name]
        try:
            if sort_col == False or sort_col == 'None_sort':
                results = my_col.find(search_col).limit(limit_num)  # 这里只会返回一个对象，数据需要自己取
            else:
                sort_flag = 1
                if sort == 'desc':
                    sort_flag = -1
                results = my_col.find(search_col).sort(sort_col, sort_flag).limit(limit_num)  # 这里只会返回一个对象，数据需要自己取
            result_all = [i for i in results]  # 将获取到的数据添加至list
            return result_all
        except TypeError as e:
            print('查询条件只能是dict类型')
            return None

    def update_one_collecton(self, collection_name, search_col, update_col):
        '''该方法第一个参数为查询的条件，第二个参数为要修改的字段。
            如果查找到的匹配数据多余一条，则只会修改第一条。
            修改后字段的定义格式： { "$set": { "alexa": "12345" } }'''
        my_col = self.mydb[collection_name]
        try:
            relust = my_col.update_one(search_col, update_col)
            return relust
        except TypeError as e:
            print('查询条件与需要修改的字段只能是dict类型')
            return None

    def update_batch_collecton(self, collection_name, search_col, update_col):
        '''批量更新数据'''
        my_col = self.mydb[collection_name]
        try:
            relust = my_col.update_many(search_col, update_col)
            return relust
        except TypeError as e:
            print('查询条件与需要修改的字段只能是dict类型')
            return None

    def delete_one_collection(self, collection_name, search_col):  # 删除集合中的文档
        my_col = self.mydb[collection_name]
        try:
            relust = my_col.delete_one(search_col)
            return relust
        except TypeError as e:
            print('查询条件与需要修改的字段只能是dict类型')
            return None

    def delete_batch_collection(self, collection_name, search_col):  # 删除集合中的多个文档
        '''删除所有 name 字段中以 F 开头的文档:{ "name": {"$regex": "^F"} }
        删除所有文档：{}'''
        my_col = self.mydb[collection_name]
        try:
            relust = my_col.delete_many(search_col)
            return relust
        except TypeError as e:
            print('查询条件与需要修改的字段只能是dict类型')
            return None

    def drop_collection(self, collection_name):
        '''删除集合，如果删除成功 drop() 返回 true，如果删除失败(集合不存在)则返回 false'''
        my_col = self.mydb[collection_name]
        result = my_col.drop()
        return result

    def get_connections(self):  # 获取所有的connections
        return self.mydb.list_collection_names()

    def close_connect(self):
        self.connect_client.close()
        return 'mongo连接已关闭'
