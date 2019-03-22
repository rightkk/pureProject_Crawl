import os
import re
import datetime
import pymysql
import scrapy
from scrapy.exceptions import DropItem
from scrapy.pipelines.images import ImagesPipeline
from scrapy.utils.project import get_project_settings
from zhihuSpider.items import HouseInfoItem, CommunityInfoItem


class Ly58ershoufangPipeline:
    def __init__(self, host, user, passwd, mysqldb):
        self.host = host
        self.user = user
        self.passwd = passwd
        self.mysqldb = mysqldb
        self.conn = None
        self.curr = None

    @classmethod
    def from_crawler(cls, crawler):
        return cls(host=crawler.settings.get('HOST'),
                   user=crawler.settings.get('USER'),
                   passwd=crawler.settings.get('PASSWORD'),
                   mysqldb=crawler.settings.get('MYSQL_DATABASE', 'roleprod'))

    def open_spider(self, spider):
        self.conn = pymysql.connect(self.host, self.user, self.passwd, self.mysqldb)
        self.curr = self.conn.cursor()
        self.curr.execute('select * from py_table')
        res = self.curr.fetchall()
        for line in res:
            print(line)

    def close_spider(self, spider):
        self.conn.close()

    def process_item(self, item, spider):
        if isinstance(item, CommunityInfoItem):
            self._process_community_info(item)
        elif isinstance(item, HouseInfoItem):
            self._process_house_info(item)
        return item

    def _process_community_info(self, item):
        sql = "insert into crawl_communityinfo value(null,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        find_sql = "select count(*) from crawl_communityinfo where communityName='%s'" % item['community_name'].strip()
        self.curr.execute(find_sql)
        res = self.curr.fetchone()
        if res[0] > 0:
            return
        try:
            average_price = re.findall("\d+", item['average_price'])[0]
        except Exception as e:
            average_price = 0
        try:
            property_fee = re.findall("\d+", item['property_fee'])[0]
        except Exception as e:
            property_fee = 0
        create_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        try:
            plot_rate = re.findall("\d+", item['plot_rate'])[0]
        except Exception as e:
            plot_rate = 0
        try:
            greening_rate = re.findall("\d+", item['greening_rate'])[0]
        except Exception as e:
            greening_rate = 0

        data = (item['community_name'].strip(), item['street_block'].strip(), average_price,
                property_fee, plot_rate, greening_rate,
                item['city'], item['district'], create_time)
        self.curr.execute(sql, data)
        self.conn.commit()

    def _process_house_info(self, item):
        sql = "insert into crawl_houseinfo value(null,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        find_sql = "select id from crawl_communityinfo where communityName='%s'" % item['community_name'].strip()
        self.curr.execute(find_sql)
        res = self.curr.fetchone()
        if not res[0]:
            raise RuntimeError("community_id 没有获取到")
        else:
            community_id = res[0]
        if not item['community_name']:
            print("item里的community_name字段为None")
            item['community_name'] = ""
        unit_price = item['unit_price'].split('元')[0]
        legal_area = item['legal_area'].split('㎡')[0]
        use_area = item['use_area'].split("平")[0]
        built_age = item['built_age'].split("年")[0]
        right_limit = item['right_limit'].split("年")[0]
        # 处理发布日期:24小时内时写作：xx小时前；超过24小时但在48小时内写作：1天前；其它时间写日期
        str = item['publish_date']
        publish_date = None
        if "-" not in str:
            str2 = re.findall("\d+", str)[0]
            if "小时" in str:
                publish_date = (datetime.datetime.now() - datetime.timedelta(hours=int(str2))).strftime("%Y-%m-%d")
            elif "天" in str:
                publish_date = (datetime.datetime.now() - datetime.timedelta(days=int(str2))).strftime("%Y-%m-%d")
        else:
            year = datetime.datetime.now().strftime("%Y")
            publish_date = "-".join([year, str])
        pic_urls = ",".join(item['pic_urls'])
        create_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        data = (community_id, item['title'], item['total_price'], unit_price,
                item['house_type'], item['decorate'], legal_area,
                use_area, built_age, item['floor'],
                right_limit, publish_date, pic_urls,
                create_time)
        self.curr.execute(sql, data)
        self.conn.commit()


class HouseImagesPipeline(ImagesPipeline):

    # 从settings获取图片存储路径
    # IMAGES_STORE = get_project_settings().get('IMAGES_STORE')

    def get_media_requests(self, item, info):
        """
        :作用：默认是从item获取图片的urls并封装为Request对象返回给scrapy
        此处要改写，遍历item里的pic_urls，将每个url封装为Request对象提交给scrapy处理
        图片下载完后，下载结果会以元祖列表的形式返回给item_completed()处理
        :param item:
        :param info:
        :return:
        """
        if isinstance(item, HouseInfoItem):
            for pic_url in item['pic_urls']:
                yield scrapy.Request(url=pic_url)
        else:
            super(HouseImagesPipeline, self).get_media_requests(item, info)

    def item_completed(self, results, item, info):
        """
        :param :下载结果，二元组定义如下：(success, image_info_or_failure)。
            第一个元素表示图片是否下载成功；第二个元素是一个字典
            如果success=true，image_info_or_error词典包含以下键值对。失败则包含一些出错信息。
         字典内包含* url：原始URL * path：本地存储路径 * checksum：校验码
            results:[(True,
              {'checksum': '2b00042f7481c7b056c4b410d28f33cf',
               'path': 'full/0a79c461a4062ac383dc4fade7bc09f1384a3910.jpg',
               'url': 'http://www.example.com/files/product1.pdf'}),
             (False,
              Failure(...))]
        :param item:
        :param info:
        :return:
        """
        # if isinstance(item, HouseInfoItem):
        #     image_paths = [x['path'] for ok, x in results if ok]
        #     if not image_paths:
        #         raise DropItem("Item does not contain images")
        #     # 修改图片保存名
        #     # ...
        #     return item
        super(HouseImagesPipeline, self).item_completed(results, item, info)

    def file_path(self, request, response=None, info=None):
        """
        这个方法是scrapy用来获取图片路径（文件名）的，默认的图片名是以校验码来命名的
        可以重写这个方法把将自己想要的文件名返回给scrapy
        此方法要应该是在每张图片保存时都会调用
        :param request:
        :param response:
        :param info:
        :return:
        """
        return super(HouseImagesPipeline, self).file_path(request)


if __name__ == '__main__':
    print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    print(datetime.datetime.now().strftime("%Y"))
