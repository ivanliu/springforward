# -*- coding: utf-8 -*-

# Scrapy settings for springforward project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'springforward'

SPIDER_MODULES = ['crawler.spiders']
# NEWSPIDER_MODULE = 'springforward.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'springforward (+http://www.yourdomain.com)'

ITEM_PIPELINES = {
    'crawler.pipelines.MultiCSVItemPipeline': 300,
}

# The amount of time (in secs) that the downloader should wait before downloading 
# consecutive pages from the same website. This can be used to throttle the crawling 
# speed to avoid hitting servers too hard. 
DOWNLOAD_DELAY = 0.025    # 25 ms of delay

