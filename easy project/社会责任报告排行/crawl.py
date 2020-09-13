import demjson
import requests
from openpyxl import Workbook

headers = {
    'Accept': '*/*',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Connection': 'keep-alive',
    'Cookie': '__jsluid_h=9b0adc86e72ddd0b76e455e56aeee31e; HexunTrack=SID=20200617212928074eed72dee467f4f3ab0f8356db47efdd4&CITY=50&TOWN=0; ADHOC_MEMBERSHIP_CLIENT_ID1.0=d5c5f53b-7b93-be55-a543-9672482aad80',
    'Host': 'stockdata.stock.hexun.com',
    'Referer': 'http://stockdata.stock.hexun.com/zrbg/Plate.aspx?date=2019-12-31',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36'
}
for year in range(2010, 2020):
    s = 0
    page = 0
    wb = Workbook()
    ws = wb.active
    ws.append(['序号', '股票名称/代码', '总得分', '等级', '股东责任',
               '员工责任', '供应商、客户和消费者权益责任', '环境责任', '社会责任'])
    while True:
        page += 1
        url = f'http://stockdata.stock.hexun.com/zrbg/data/zrbList.aspx?date={year}-12-31&count=200&pname=20&titType=null&page={page}&callback=hxbase_json11592464536143'
        text = requests.get(url=url, headers=headers).text[13:-1]
        data = demjson.decode(text)
        sum_data = data['sum']
        ls = data['list']
        for i in ls:
            data = [
                i['Number'],
                i['industry'],
                i['industryrate'],
                i['Pricelimit'],
                i['stockNumber'],
                i['lootingchips'],
                i['Scramble'],
                i['rscramble'],
                i['Strongstock'],
            ]
            ws.append(data)
        s += 200
        if s > sum_data:
            print(f'{year}年   {(page-1)*200+sum_data//200}条')
            break
        print(f'{year}年   {page*200}条')
    wb.save(f'{year}年度社会责任报告排行.xlsx')
    print(f'{year}年数据完成')
