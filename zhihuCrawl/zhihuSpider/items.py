# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class UserInfoItem(scrapy.Item):
    # define the fields for your item here like:
    # id
    user_id = scrapy.Field()
    # 头像img
    user_image_url = scrapy.Field()
    # 姓名
    name = scrapy.Field()
    # 居住地
    location = scrapy.Field()
    # 技术领域
    business = scrapy.Field()
    # 性别
    gender = scrapy.Field()
    # 公司
    employment = scrapy.Field()
    # 职位
    position = scrapy.Field()
    # 教育经历
    education = scrapy.Field()
    # 我关注的人数
    followees_num = scrapy.Field()
    # 关注我的人数
    followers_num = scrapy.Field()


class RelationItem(scrapy.Item):
    # 用户id
    user_id = scrapy.Field()
    # relation 类型
    relation_type = scrapy.Field()
    # 和我有关系人的id列表
    relations_id = scrapy.Field()


class HouseInfoItem(scrapy.Item):
    # 总价
    title = scrapy.Field()
    community_name = scrapy.Field()
    total_price = scrapy.Field()
    unit_price = scrapy.Field()
    house_type = scrapy.Field()
    decorate = scrapy.Field()
    legal_area = scrapy.Field()
    use_area = scrapy.Field()
    # cx = scrapy.Field()
    floor = scrapy.Field()
    right_limit = scrapy.Field()
    built_age = scrapy.Field()
    pic_urls = scrapy.Field()
    publish_date = scrapy.Field()


class CommunityInfoItem(scrapy.Item):
    community_name = scrapy.Field()
    street_block = scrapy.Field()
    average_price = scrapy.Field()
    property_fee = scrapy.Field()
    plot_rate = scrapy.Field()
    greening_rate = scrapy.Field()
    city = scrapy.Field()
    district = scrapy.Field()
