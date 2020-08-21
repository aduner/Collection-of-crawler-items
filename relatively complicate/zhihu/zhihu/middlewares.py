# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html
import requests
import json
import random
from scrapy.downloadermiddlewares.useragent import UserAgentMiddleware
from twisted.internet.defer import DeferredLock
from .settings import USER_AGENT_LIST, PROXY
from .models import ProxyModel
from time import sleep


class RotateUserAgentMiddleware(UserAgentMiddleware):
    '''
    用户代理中间件（处于下载中间件位置）
    '''

    def process_request(self, request, spider):
        # proxy = random.choice(PROXY)
        # request.meta['proxy'] = proxy
        user_agent = random.choice(USER_AGENT_LIST)
        if user_agent:
            request.headers.setdefault('User-Agent', user_agent)


class IPProxyDownloadMiddleware(object):
    PROXY_URL = ''  # 代理接口

    def __init__(self):
        super(IPProxyDownloadMiddleware, self).__init__()
        self.current_proxy = None
        self.lock = DeferredLock()

    def process_request(self, request, spider):
        if ('proxy' not in request.meta) or self.current_proxy.is_expiring or self.current_proxy.is_blacked:
            self.updata_proxy()
        request.meta['proxy'] = self.current_proxy.proxy
    def process_response(self, request, response, spider):
        if response.status != 200:
            print("被拉黑")
            if not self.current_proxy.is_blacked:
                self.current_proxy.is_blacked = True
            self.updata_proxy()
            request.meta['proxy'] = self.current_proxy.proxy
            return request
        return response

    def updata_proxy(self):
        self.lock.acquire()
        if (not self.current_proxy) or self.current_proxy.is_expire or self.current_proxy.is_blacked:
            response = requests.get(self.PROXY_URL)
            text = response.text
            result = json.loads(text)
            if len(result['data']) > 0:
                data = result['data'][0]
                proxy_model = ProxyModel(data)
                self.current_proxy = proxy_model
                print("更新代理IP")
                print(data)
            else:
                print(text)
        self.lock.release()

    def process_exception(self, request, exception, spider):
        # 出现异常时（超时）使用代理
        print("超时重试")
        sleep(2.1)
        if not self.current_proxy.is_blacked == True:
            self.current_proxy.is_blacked = True
        self.updata_proxy()
        return request
