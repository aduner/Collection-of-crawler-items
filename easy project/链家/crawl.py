import requests
from lxml import etree
import time
import json
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36',
}

url = f'https://cq.lianjia.com/ershoufang/rs%E5%8C%97%E4%BA%AC/'
a = requests.get(url=url, headers=headers).text
e = etree.HTML(a)
name = e.xpath('//*[@id="content"]/div[1]/ul/li/div[1]/div[1]/a/text()')
ar = e.xpath('//*[@id="content"]/div[1]/ul/li/div[1]/div[2]/div')
address = [''.join(i.xpath('.//text()')) for i in ar]
p = e.xpath('//*[@id="content"]/div[1]/ul/li/div[1]/div[6]/div[1]')
price = [''.join(i.xpath('.//text()')) for i in p]
unit_price = e.xpath(
    '//*[@id="content"]/div[1]/ul/li/div[1]/div[6]/div[2]/span/text()')
unit_price = [i[2:] for i in unit_price]

for page in range(2, 6):
    url = f'https://cq.lianjia.com/ershoufang/pg{page}rs%E5%8C%97%E4%BA%AC/'

    a = requests.get(url=url, headers=headers).text
    e = etree.HTML(a)
    name += e.xpath('//*[@id="content"]/div[1]/ul/li/div[1]/div[1]/a/text()')
    ar = e.xpath('//*[@id="content"]/div[1]/ul/li/div[1]/div[2]/div')
    address += [''.join(i.xpath('.//text()')) for i in ar]
    p = e.xpath('//*[@id="content"]/div[1]/ul/li/div[1]/div[6]/div[1]')
    price += [''.join(i.xpath('.//text()')) for i in p]
    up = e.xpath(
        '//*[@id="content"]/div[1]/ul/li/div[1]/div[6]/div[2]/span/text()')
    unit_price += [i[2:] for i in up]
with open('data.json', 'w', encoding='utf-8') as f:

    json.dump([name, address, price, unit_price], f)
with open('data.json', 'r', encoding='utf-8') as f:

    data=json.load(f)

import openpyxl
wb=openpyxl.Workbook()
ws=wb.active
ws.append(['name','address','price','unit_price'])
for i in range(len(data[0])):
    ws.append([data[0][i],data[1][i],data[2][i],data[3][i]])
wb.save('data.xlsx')