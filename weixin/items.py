# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class WeixinItem(scrapy.Item):
    # define the fields for your item here like:
    title = scrapy.Field()
    create_time = scrapy.Field()
    source = scrapy.Field()
    body = scrapy.Field()
    content = scrapy.Field()
