# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
from scrapy.spiders import CrawlSpider, Rule
from zhihuSpider.items import UserInfoItem, HouseInfoItem, CommunityInfoItem


class Ly58ComSpider(CrawlSpider):
    name = 'ly.58.com'
    allowed_domains = ['ly.58.com']
    start_urls = ['https://ly.58.com/']

    # rules = (
    #     Rule(LinkExtractor(allow=r'Items/'), callback='parse_item', follow=True),
    # )

    def __init__(self):
        pass

    def start_requests(self):
        # 进入58龙岩新罗二手房页面
        return [Request('https://ly.58.com/xinluoqu/ershoufang',
                        callback=self.parse_summary_page)]

    def parse_summary_page(self, response):
        # 抽取总价、单价、详情url列表、下一页url
        totalPrice_list = response.xpath("//ul[@class='house-list-wrap']/li/descendant::p[@class='sum']/b/text()").extract()
        unitPrice_list = response.xpath("//ul[@class='house-list-wrap']/li/descendant::p[@class='unit']/text()").extract()
        next_page = response.xpath("//div[@class='pager']/descendant::a[1]/@href").extract_first()
        next_url = ''.join([Ly58ComSpider.start_urls[0], next_page])
        houseinfo_urls = response.xpath("//ul[@class='house-list-wrap']/li/div[@class='list-info']/h2[@class='title']/a/@href").extract()
        limit_number = 0
        # 获取下一页的页码
        _start = next_url.find("pn")
        next_page_no = next_url[_start+2:_start+3]
        for url, totalPrice, unitPrice in zip(houseinfo_urls, totalPrice_list, unitPrice_list):
            # 每页抽取20条
            if limit_number == 20:
                print("第一页封装20条连接请求完成")
                break
            limit_number += 1
            # //short.58.com/zd_p/7c6fef24-2447-4a09-b88b-f67c305edc58/?target=na-16-xgk_psfegvimob_80588994492248q-feykn&end=end
            if "short" in url:
                url = "".join(["https:", url])
            yield Request(url=url, meta={'totalPrice': totalPrice, 'unitPrice': unitPrice},
                          callback=self.parse_detail_page,
                          errback=self.parse_err)
        if next_page_no == 6:
            print("前5页数据爬取完毕")
        yield Request(url=next_url, callback=self.parse_summary_page, errback=self.parse_err)

    def parse_detail_page(self, response):
        # 抽取房屋详情和小区详情信息
        community_name = response.xpath("//div[@id='xiaoWrap']/descendant::div[@class='xiaoqu-info']/h3/a/text()").extract_first()
        if not community_name:
            print("链接：%s 未抽取到community_name" % response.request.url)
        street_block = response.xpath("//div[@id='xiaoWrap']/descendant::div[@class='xiaoqu-info']/ul/li[2]/span[@class='c_333']/a[2]/text()").extract_first()
        average_price = response.xpath("//div[@id='xiaoWrap']/descendant::div[@class='xiaoqu-info']/ul/li[1]/span[2]/text()").extract_first()
        property_fee = response.xpath("//div[@id='xiaoWrap']/descendant::div[@class='xiaoqu-info']/ul/li[3]/span[2]/text()").extract_first()
        plot_rate = response.xpath("//div[@id='xiaoWrap']/descendant::div[@class='xiaoqu-info']/ul/li[4]/span[2]/text()").extract_first()
        greening_rate = response.xpath("//div[@id='xiaoWrap']/descendant::div[@class='xiaoqu-info']/ul/li[5]/span[2]/text()").extract_first()
        city = "龙岩市"
        distrit = "新罗区"
        # 房屋详情
        title = response.xpath("//div[@class='house-title']/h1[1]/text()").extract_first().strip()
        total_price = response.request.meta['totalPrice']
        unit_price = response.request.meta['unitPrice']
        house_type = response.xpath("//p[@class='room']/span[1]/text()").extract_first().strip()
        decorate = response.xpath("//p[@class='area']/span[2]/text()").extract_first().strip()
        legal_area = response.xpath("//div[@id='generalSituation']/descendant::ul[@class='general-item-left']/descendant::span[last()-2]/text()").extract_first()
        use_area = response.xpath("//p[@class='area']/span[1]/text()").extract_first().strip().strip()
        built_age = response.xpath("//div[@id='generalSituation']/ descendant::ul[@class='general-item-right']/descendant::span[last()]/text()").extract_first()
        floor = response.xpath("//p[@class='room']/span[2]/text()").extract_first().strip()
        right_limit = response.xpath("//div[@id='generalSituation']/ descendant::ul[@class='general-item-right']/descendant::span[last()-2]/text()").extract_first()
        publish_date = response.xpath("//p[@class='house-update-info']/span[@class='up'][1]/text()").extract_first()
        pic_urls = response.xpath("//div[@class='basic-pic-list pr']/descendant::li/@data-value").extract()

        communityInfoItem = CommunityInfoItem(community_name=community_name, street_block=street_block, average_price=average_price,
                                              property_fee=property_fee, plot_rate=plot_rate, greening_rate=greening_rate,
                                              city=city, district=distrit)
        yield communityInfoItem

        houseInfoItem = HouseInfoItem(title=title, community_name=community_name, total_price=total_price,
                                      unit_price=unit_price,house_type=house_type, decorate=decorate,
                                      legal_area=legal_area, use_area=use_area, built_age=built_age, floor=floor,
                                      right_limit=right_limit, publish_date=publish_date, pic_urls=pic_urls)
        yield houseInfoItem

    def parse_err(self, response):
        pass
