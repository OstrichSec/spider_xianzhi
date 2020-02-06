# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class XianzhiItem(scrapy.Item):
    # define the fields for your item here like:
    art_name = scrapy.Field()
    art_url = scrapy.Field()
    author = scrapy.Field()
    category = scrapy.Field()
    post_time = scrapy.Field()
    detail = scrapy.Field()
