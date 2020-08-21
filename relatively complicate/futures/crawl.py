import openpyxl
import requests
from lxml import etree
from datetime import date, timedelta
from time import time

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
}


def get_fivedate():
    return [str(date.today() + timedelta(i)) for i in range(0, -5, -1)]


def get_jys(date_time):
    # 交易所信息
    millis = int(round(time() * 1000))
    url = f'http://service.99qh.com/hold2/AgreementHold/GetExchInfo.aspx?date={date_time}&_={millis}'
    a = requests.get(url=url, headers=headers).text
    e = etree.HTML(a)
    num = e.xpath('//exchid/text()')
    name = e.xpath('//exchname/text()')
    return [[name[i], num[i]] for i in range(len(name))]


def get_qh(date_time, jys_num):
    # 期货信息
    millis = int(round(time() * 1000))
    url = f'http://service.99qh.com/hold2/AgreementHold/GetGoodsInfo.aspx?date={date_time}&exch={jys_num}&_={millis}'
    a = requests.get(url=url, headers=headers).text
    e = etree.HTML(a)
    num = e.xpath('//goodsid/text()')
    name = e.xpath('//goodsname/text()')
    return [[name[i], num[i]] for i in range(len(name))]


def get_data(date_time, qh_num):
    # 单个期货的数据
    millis = int(round(time() * 1000))
    url = f'http://service.99qh.com/hold2/MemberHold/GetTableHtml.aspx?date={date_time}&user=99qh&goods={qh_num}&agreement=ALL&count=20&_={millis}'
    a = requests.get(url=url, headers=headers).text
    e = etree.HTML(a)
    return e.xpath('//table[1]//tr[last()]/td//text()')[2:]


def crawl_day(date_time):
    # 爬取单天的数据
    print(f'---------- 爬取 {date_time} 数据 ----------')
    jys_data = get_jys(date_time)
    data = []
    for jys in jys_data:
        jys_name, jys_num = jys
        qh_data = get_qh(date_time, jys_num)
        for qh in qh_data:
            qh_name, qh_num = qh
            data += [[jys_name, qh_name] + get_data(date_time, qh_num)]
            print(jys_name, "---", qh_name)
    print('-'*20)
    return data


fivedate = get_fivedate()
wb = openpyxl.Workbook()
ws = wb.active
ws.title = str(fivedate[0])
a = crawl_day(fivedate[0])
ws.append(['交易所', '品类',
           ' ', ' ', '成交量', '增减',
           ' ', ' ', '多仓', '增减',
           ' ', ' ', '空仓', '增减'
           ])
for i in a:
    ws.append(i)

for date_time in fivedate[1:]:
    ws = wb.create_sheet()
    ws.title = str(date_time)
    a = crawl_day(date_time)
    ws.append(['交易所', '品类',
               ' ', ' ', '成交量', '增减',
               ' ', ' ', '多仓', '增减',
               ' ', ' ', '空仓', '增减'
               ])
    for i in a:
        ws.append(i)
wb.save('data.xlsx')
