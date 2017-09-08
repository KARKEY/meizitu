from scrapy import Request,Spider,Selector
from meizitu.items import MeizituItem
import re
import redis,json,time
from scrapy.utils.reqser import request_to_dict, request_from_dict

class mztspider(Spider):
    name='meizitu'
    allowed_domains = ['mzitu.com']

    def start_requests(self):
        url='http://www.mzitu.com/all/'
        yield Request(url,callback=self.parse_index)

    def parse_index(self, response):
        selector=Selector(response)
        index_urls=selector.xpath('//a[@href and @target="_blank"]')
        for index in index_urls[:-1]:
            url=index.xpath('./@href').extract_first()
            title=index.xpath('./text()').extract_first()
            yield Request(url,callback=self.parse_detail,meta={'title':title})

    def parse_detail(self, response):
        match=re.search(r'\/\d{1,6}\/(\d{1,6})', response.url)
        if match==None:
            page=1
            item=MeizituItem()
            item['url']=response.url
            item['title']=response.meta.get('title', '')
            item['image_urls']=[]
        else:
            item=response.meta.get('item')
            page=match.group(1)
        selecotr=Selector(response)
        imgae_urls=selecotr.xpath('//div[@class="main-image"]//img/@src').extract()
        for url in imgae_urls:
            item['image_urls'].append(url)
        next_page = selecotr.xpath('//span[contains(text(), "下一页")]/parent::a/@href').extract_first(default=None)
        if next_page:
            yield Request(next_page,callback=self.parse_detail,meta={'item':item,'referer':response.url},priority=int(page))
        else:
            yield item



class mztspider(Spider):
    name='meizitu1.0'
    allowed_domains = ['mzitu.com']
    urls=[]

    def start_requests(self):
        url='http://www.mzitu.com/all/'
        yield Request(url,callback=self.parse_index)

    def parse_index(self, response):
        selector=Selector(response)
        index_urls=selector.xpath('//a[@href and @target="_blank"]')
        for i,index in enumerate(index_urls[:-1]):
            url=index.xpath('./@href').extract_first()
            title=index.xpath('./text()').extract_first()
            self.urls.append(Request(url,callback=self.parse_detail,meta={'title':title}))
        for i in range(8):
            yield self.urls.pop(0)



    def parse_detail(self, response):
        match=re.search(r'\/\d{1,6}\/(\d{1,6})', response.url)
        if match==None:
            page=1
            item=MeizituItem()
            item['url']=response.url
            item['title']=response.meta.get('title', '')
            item['image_urls']=[]
        else:
            item=response.meta.get('item')
            page=match.group(1)
        selecotr=Selector(response)
        imgae_urls=selecotr.xpath('//div[@class="main-image"]//img/@src').extract()
        for url in imgae_urls:
            item['image_urls'].append(url)
        next_page = selecotr.xpath('//span[contains(text(), "下一页")]/parent::a/@href').extract_first(default=None)
        if next_page:
            yield Request(next_page,callback=self.parse_detail,meta={'item':item,'referer':response.url},priority=int(page))
        else:
            yield item
            yield self.urls.pop(0)

