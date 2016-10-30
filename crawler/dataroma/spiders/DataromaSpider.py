import re
import scrapy
import urlparse

from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor

class DataromaSpider(CrawlSpider):
    '''
    A spider to crawl dataroma.com
    '''
    name = 'dataroma'
    allowed_domains = ['dataroma.com']
    start_urls = [
            'http://www.dataroma.com/m/managers.php',
    ]

    # follow link of http://www.ccyp.com/NCCYP/ListingDetail.asp?PIndex=[A-Z]\d+
    #    rules = [ Rule(SgmlLinkExtractor(allow=('ListingDetail.asp?PIndex=[A-Z]\d+',)), follow=True), 
    #              Rule(SgmlLinkExtractor(allow=('ListingDetail.asp?PageNo=\d+\&PIndex=[A-Z]\d+',)), callback='parse_item', follow=True)
    #            ]

    # rules = (Rule(LinkExtractor(allow=(r'NCCYP\/ListingDetail.asp\?PIndex=[A-Z]\d+', )), callback='parse_item'), )
   
    def parse(self, response):
        '''
        Extract following info from http://www.dataroma.com/m/managers.php
          - investor code
          - investor name
          - portfolio value
          - no of stocks
        '''
        for row in response.xpath('/html/body/div/div[@id="main"]/div/table/tbody/tr'):
            name = row.xpath('td[@class="man"]/a/text()').extract_first().strip()
            link = row.xpath('td[@class="man"]/a/@href').extract_first().strip()
            val = row.xpath('td[@class="val"]/text()').extract_first().strip()
            cnt = row.xpath('td[@class="cnt"]/text()').extract_first().strip()
            code = link.split('=')[1].strip()
            yield {
                    'investor_code': code,
                    'investor': name,
                    'value': val,
                    'count': cnt
            }

            if link:
                link = response.urljoin(link)
                yield scrapy.Request(link, callback=self.parse_holdings)

    def parse_holdings(self, response):
        '''
        Extract following info from http://www.dataroma.com/m/holdings.php?m=AV
          - the links to activity history of all holdings
        '''
        for row in response.xpath('/html/body/div/div[@id="main"]/div[@id="wrap"]/table/tbody/tr'):
            link = row.xpath('td[@class="hist"]/a/@href').extract_first().strip()
            if link:
                link = response.urljoin(link)
                yield scrapy.Request(link, callback=self.parse_activities)

    def parse_stock(self, response):
        '''
        Extract following info from http://www.dataroma.com/m/stock.php?sym=BRK.B
          - stock code
          - stock name
          - sector
        '''
        # parse response url to get codes for investor and stock
        parsed = urlparse.urlparse(response.url)
        kvs = urlparse.parse_qs(parsed.query)
        stock_code = kvs['sym'][0]

        # get stock name and sector from the page
        name = response.xpath('/html/body/div/div[@id="main"]/div[@id="b1"]/p[@id="st_name"]/text()').extract_first().strip()
        sector = response.xpath('/html/body/div/div[@id="main"]/div[@id="b1"]/table/tr[1]/td[2]/b/text()').extract_first().strip()
        yield {
                'stock_code': stock_code,
                'name': name,
                'sector': sector
        }

    def parse_activities(self, response):
        '''
        Extract following info from http://www.dataroma.com/m/hist/hist.php?f=AV&s=BRK.B 
          - investor code
          - period
          - shares
          - % of portfolio
          - activity
          - % change to portfolio
          - reported price
        '''
        # parse response url to get codes for investor and stock
        parsed = urlparse.urlparse(response.url)
        kvs = urlparse.parse_qs(parsed.query)
        investor_code = kvs['f'][0] 
        stock_code = kvs['s'][0]

        # extract the link to stock page
        link = response.xpath('/html/body/div/div[@id="main"]/p[@id="p2"]/b/a/@href').extract_first().strip() 
        if link:
            link = response.urljoin(link)
            yield scrapy.Request(link, callback=self.parse_stock)

        for row in response.xpath('/html/body/div/div[@id="main"]/div[@id="wrap"]/table/tbody/tr'):
            cells = row.xpath('td')
            period = cells[0].css('td::text').extract_first()
            shares = cells[1].css('td::text').extract_first()
            portfolio_percent = cells[2].css('td::text').extract_first()
            activity = cells[3].css('td::text').extract_first()
            change_to_portfolio_percent = cells[4].css('td::text').extract_first()
            price = cells[5].css('td::text').extract_first()

            yield {
                    'investor_code': investor_code,
                    'stock_code': stock_code,
                    'period': re.sub(r"\s+&nbsp\s+", " ", period),
                    'share': shares.strip() if shares else "",
                    'portfolio_percent': portfolio_percent.strip() if portfolio_percent else "",
                    'activity': activity.strip() if activity else "",
                    'change_to_portfolio_percent': change_to_portfolio_percent.strip() if change_to_portfolio_percent else "",
                    'price': price.strip() if price else ""
            }

