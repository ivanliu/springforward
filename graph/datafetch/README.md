0) Scrapy: An open source and collaborative framework for extracting the data you need from websites
https://scrapy.org/

1) Installation
```bash
$ pip install Scrapy
```

2) Scrapy at a glance
```bash
$ cd example
$ scrapy runspider quotes_spider.py -o quotes.json
```

3) How to get entire page using Scrapy
In items.py
```python
from scrapy.item import Item, Field

class Listing(Item):
    url = Field()
    html = Field()
```

and you've been saving your scraped data to those items in your spider like so:
```python
item['url'] = response.url
item['html'] = response.body
```

your pipelines.py would just be:
```python
import hashlib
class HtmlFilePipeline(object):
    def process_item(self, item, spider):
        file_name = hashlib.sha224(item['url']).hexdigest() #chose whatever hashing func works for you
        with open('files/%s.html' % file_name, 'w+b') as f:
            f.write(item['html'])
```

