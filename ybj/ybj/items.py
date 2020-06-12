# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class YbjItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    name = scrapy.Field()
    code = scrapy.Field()
    area = scrapy.Field()
    type = scrapy.Field()
    level = scrapy.Field()
    address = scrapy.Field()
    postcode = scrapy.Field()
    brief_info = scrapy.Field()
    link = scrapy.Field()
    pass
