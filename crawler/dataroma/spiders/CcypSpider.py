import re
import urlparse
import scrapy

from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor

from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.linkextractors.lxmlhtml import LxmlLinkExtractor

from breezemedia.items import MerchantItem

class CcypSpider(CrawlSpider):
    '''
    A spider to crawl ccyp.com
    '''
    name = 'ccyp'
    allowed_domains = ['ccyp.com']
    start_urls = [
            'http://www.ccyp.com/NCCYP/Default.asp?PIndex=J'
            ]

    # follow link of http://www.ccyp.com/NCCYP/ListingDetail.asp?PIndex=[A-Z]\d+
#    rules = [ Rule(SgmlLinkExtractor(allow=('ListingDetail.asp?PIndex=[A-Z]\d+',)), follow=True), 
#              Rule(SgmlLinkExtractor(allow=('ListingDetail.asp?PageNo=\d+\&PIndex=[A-Z]\d+',)), callback='parse_item', follow=True)
#            ]

    rules = (Rule(LinkExtractor(allow=(r'NCCYP\/ListingDetail.asp\?PIndex=[A-Z]\d+', )), callback='parse_item'), )

    tel_pattern = re.compile('((\(\d{3}\) ?)|(\d{3}-))?\d{3}-\d{4}')

    def extract_tel(self, stuff):
        '''
        use a pattern to extract tel from a random string
        '''
        m = self.tel_pattern.search(stuff)
        if m:
            return stuff[m.start() : m.end()]
        else:
            return ''

    def parse_item(self, response):
        prev_name = ''
        for cell in response.xpath('/html/body/table[@class="border"]/tr/td[@width>10]/table/tr/td'):   
            merchant = MerchantItem()
            u_names = cell.xpath("(span[@class='listing_link'])/text() | (a[@class='listing_link'])/text()").extract()
            u_alias_addr_tel = cell.xpath("text()").extract()

            # name
            if len(u_names) > 0:
                merchant['name'] = u_names[0].encode('utf-8').strip()
                prev_name = merchant['name']
            else:
                merchant['name'] = prev_name

            # alias, address, tel
            if len(u_alias_addr_tel) > 0:
                alias_addr_tel = '\t'.join(u_alias_addr_tel).encode('utf-8')
                merchant['tel'] = self.extract_tel(alias_addr_tel).strip()
                if merchant['tel']:
                    alias_addr = alias_addr_tel[:alias_addr_tel.find(merchant['tel'])].strip()
                else:
                    alias_addr = alias_addr_tel.strip()

                parts = alias_addr.split('\n')
                merchant['alias'] = ''
                merchant['addr'] = ''
                if len(parts) == 2:
                    merchant['alias'] = parts[0].strip()
                    merchant['addr'] = parts[1].strip()
                elif len(parts) == 1:
                    merchant['addr'] = parts[0].strip()
            else:
                merchant['alias'] = ''
                merchant['addr'] = ''
                merchant['tel'] = ''

            #print "name: ", merchant['name']
            #print "alias: ", merchant['alias']
            #print "addr: ", merchant['addr']
            #print "tel: ", merchant['tel']
            yield merchant

        for url in response.xpath('/html/body/table[@class="border"]/tr/td[@class="listingPageNo"]/a/@href').extract():   
            yield scrapy.Request(urlparse.urljoin(response.url, url), callback=self.parse_item)

