# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ZhihuItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    user_id = scrapy.Field()
    gender = scrapy.Field()
    action = scrapy.Field()
    question_title = scrapy.Field()

