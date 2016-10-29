# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import MySQLdb

from scrapy.exceptions import DropItem
from scrapy.http import Request

class MySQLStorePipeline(object):
    def __init__(self):
        self.conn = MySQLdb.connect(user='breezemedia', passwd='Breezemedia2014', db='yummy4u', host='54.193.16.72', charset="utf8", use_unicode=True)
        self.cursor = self.conn.cursor()

    def process_item(self, item, spider):    
        try:
            self.cursor.execute("""INSERT INTO merchants (name, alias, addr, tel) VALUES (%s, %s, %s, %s)""", 
                                 (item['name'], item['alias'], item['addr'], item['tel']))
            self.conn.commit()
        except MySQLdb.Error, e:
            print "Error %d: %s" % (e.args[0], e.args[1])

        return item

