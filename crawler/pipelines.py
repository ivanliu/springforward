# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from pydispatch import dispatcher

from scrapy import signals
from scrapy.exporters import CsvItemExporter

CSVDir = 'crawler/data/'

def item_type(item):
    return type(item).__name__.replace('Item','').lower()  # InvestorItem => team

class MultiCSVItemPipeline(object):
    SaveTypes = ['investor', 'stock', 'activity']

    def __init__(self):
        dispatcher.connect(self.spider_opened, signal=signals.spider_opened)
        dispatcher.connect(self.spider_closed, signal=signals.spider_closed)

    def spider_opened(self, spider):
        self.files = dict([ (name, open(CSVDir + name +'.csv', 'w')) for name in self.SaveTypes ])
        self.exporters = dict([ (name, CsvItemExporter(self.files[name])) for name in self.SaveTypes])
        [e.start_exporting() for e in self.exporters.values()]

    def spider_closed(self, spider):
        [e.finish_exporting() for e in self.exporters.values()]
        [f.close() for f in self.files.values()]

    def process_item(self, item, spider):
        what = item_type(item)
        if what in set(self.SaveTypes):
            self.exporters[what].export_item(item)
        return item

