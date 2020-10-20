import pymongo
import requests
from lxml import etree
import json
headers = {
    'Host': 'fuwu.rsj.beijing.gov.cn',
    'Origin': 'http://fuwu.rsj.beijing.gov.cn',
    'Referer': 'http://fuwu.rsj.beijing.gov.cn/nwesqintegralpublic/settleperson/settlePersonTable',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36'
}
url = 'http://fuwu.rsj.beijing.gov.cn/nwesqintegralpublic/settlePerson/settlePersonDetails'
data_all = []


def get_data(data_id):
    form_data = {'id': f'{data_id}'}
    html = requests.post(url=url, headers=headers, data=form_data).text
    e = etree.HTML(html)

    integral = e.xpath('/html/body/p[1]//text()')
    address, name = ''.join(e.xpath('/html/body/p[2]/text()')).split()
    row = ['序号', '积分项目明细', '分值']
    trs = e.xpath('/html/body/table[1]//tr')
    tables = [tr.xpath('./td/text()') for tr in trs][1:]
    return [integral, [address, ], [name, ], row]+tables


for data_id in range(2, 6034):
    while True:
        try:
            data_all.append(get_data(data_id))
            break
        except requests.exceptions.RequestException:
            if input("----:")=='y':
                continue
            else:
                with open('data.json', 'w', encoding='utf-8') as f:
                    json.dump(data_all, f, indent=4, ensure_ascii=False)
    print(data_id)

with open('data.json', 'w', encoding='utf-8') as f:
    json.dump(data_all, f, indent=4, ensure_ascii=False)

