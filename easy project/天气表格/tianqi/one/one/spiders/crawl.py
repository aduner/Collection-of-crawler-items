# -*- coding: utf-8 -*-
import scrapy
import json
from openpyxl import Workbook


class CrawlSpider(scrapy.Spider):
    name = 'crawl'
    allowed_domains = ['xxfb.mwr.cn']
    start_urls = ['http://xxfb.mwr.cn/floodDroughtWarning/flood']

    def parse(self, response):
        a = response.text
        data = json.loads(a)["result"]
        data = [[i["stnm"].strip(),
                 i["addv"],
                 i["tm"],
                 round(float(i["zl"]) - float(i["wrz"]), 2)] for i in data]
        wb = Workbook()
        ws = wb.active
        ws.append(['站名', '站址', '时间', '汛情（米）'])
        for i in data:
            ws.append(i)
        wb.save('table.xlsx')
        print('over')
        return
