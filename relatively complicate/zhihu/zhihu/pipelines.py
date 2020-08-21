# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql
from twisted.enterprise import adbapi
from .items import ZhihuItem


class ZhihuPipeline:
    def __init__(self):
        # 连接本地mysql
        dbparams = {
            'host': '127.0.0.1',
            'port': 3306,
            'user': 'debian-sys-maint',
            'password': 'lD3wteQ2BEPs5i2u',
            'database': 'zhihu',
            'charset': 'utf8mb4',
            'cursorclass': pymysql.cursors.DictCursor
        }
        self.dbpool = adbapi.ConnectionPool('pymysql', **dbparams)
        self._sql_zhihu_user = None


    @property
    def sql_zhihu(self):
        # 初始化sql语句
        if not self._sql_zhihu_user:
            self._sql_zhihu_user = '''
                     insert into zhihu_user(id,user_id,gender,question_title,action)\
                     values(null,%s,%s,%s,%s)'''
        return self._sql_zhihu_user

    def process_item(self, item, spider):
        if isinstance(item, ZhihuItem):
            # 提交
            defer_zhihu = self.dbpool.runInteraction(self.insert_zhihu_item, item)
            # 错误处理
            defer_zhihu.addErrback(self.handle_error)

    def insert_zhihu_item(self, cursor, item):
        cursor.execute(self.sql_zhihu, (item['user_id'],
                                        item['gender'],
                                        item['question_title'],
                                        item['action'],))

    def handle_error(self, error):
        print()
        print(error, end='\n\n')
