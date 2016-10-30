# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class InvestorItem(scrapy.Item):
    investor_code = scrapy.Field()
    investor_name = scrapy.Field()
    value = scrapy.Field()
    count = scrapy.Field()

class StockItem(scrapy.Item):
    stock_code = scrapy.Field()
    stock_name = scrapy.Field()
    sector = scrapy.Field()

class ActivityItem(scrapy.Item):
    investor_code = scrapy.Field()
    stock_code = scrapy.Field()
    period = scrapy.Field()
    shares = scrapy.Field()
    portfolio_percent = scrapy.Field()
    activity = scrapy.Field()
    change_to_portfolio_percent = scrapy.Field()
    price = scrapy.Field()

