# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo
import pymysql
import scrapy
from scrapy.exceptions import DropItem
from scrapy.pipelines.images import ImagesPipeline
from zhihuCrawl.zhihuSpider.items import UserInfoItem


class ZhihucrawlPipeline:
    def __init__(self, localhost, user, passwd, mysqldb):
        print('调用cls()执行init')
        self.localhost = localhost
        self.user = user
        self.passwd = passwd
        self.mysqldb = mysqldb

    @classmethod
    def from_crawler(cls, crawler):
        print('调用from_crawler')
        zp = cls(
            localhost=crawler.settings.get('HOST'),
            user=crawler.settings.get('USER'),
            passwd=crawler.settings.get('PASSWORD'),
            mysqldb=crawler.settings.get('MYSQL_DATABASE', 'roleprod')
            )
        return zp

    def open_spider(self, spider):
        print('调用open_spider')
        self.conn = pymysql.connect(self.localhost, self.user,
                                      self.passwd, self.mysqldb)
        self.curr = self.conn.cursor()
        self.curr.execute('select * from py_table')
        res = self.curr.fetchall()
        for line in res:
            print(line)
            print()


    def close_spider(self, spider):
        print('调用close_spider')
        self.conn.close()

    def process_item(self, item, spider):
        print('调用process_item')
        if isinstance(item, UserInfoItem):
            self._process_user_item(item)
        else:
            self._process_relation_item(item)
        return item

    def _process_user_item(self, item):
        pass

    def _process_relation_item(self, item):
        pass


class ZhihuImagePipeline(ImagesPipeline):
    # 重写ImagesPipeline   get_media_requests方法
    def get_media_requests(self, item, info):
        '''
        :param item:
        :param info:
        :return:
        在工作流程中可以看到，
        管道会得到文件的URL并从项目中下载。
        为了这么做，你需要重写 get_media_requests() 方法，
        并对各个图片URL返回一个Request:
        '''
        print('调用get_media_requests')
        if isinstance(item, UserInfoItem):
            if item['user_image_url']:
                    yield scrapy.Request(item['user_image_url'])
            else:
                super(ZhihuImagePipeline, self).get_media_requests(item, info)

    def item_completed(self, results, item, info):
        '''
        :param results:
        :param item:
        :param info:
        :return:
        当一个单独项目中的所有图片请求完成时（要么完成下载，要么因为某种原因下载失败），
         item_completed() 方法将被调用。
        '''
        print('调用item_completed')
        if isinstance(item, UserInfoItem):
            image_paths = [x['path'] for ok, x in results if ok]
            if not image_paths:
                raise DropItem("Item contains no images")
        return item
