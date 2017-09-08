# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
from fake_useragent import UserAgent
import time,os



class meizitu(object):
    ua=UserAgent()

    def process_request(self, request, spider):
        '''设置headers和切换请求头
        :param request: 请求体
        :param spider: spider对象
        :return: None
        '''
        request.headers["User-Agent"]=self.ua.chrome
        referer = request.meta.get('referer', None)
        if referer:
            request.headers['referer'] = referer

    def process_response(self, request, response, spider):
        if response.status in [403,414]:
            print(response.status,'pause')
            os.system('pause')
        elif response.status in [514]:
            pass
        return response


