import requests
import json
import openpyxl


def get_china():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36',
    }
    url = 'https://api.inews.qq.com/newsqa/v1/query/inner/publish/modules/list?modules=chinaDayList,chinaDayAddList,cityStatis,nowConfirmStatis,provinceCompare'
    a = requests.get(url=url, headers=headers).text
    i = json.loads(a)["data"]["chinaDayList"][-1]
    data = ['中国',
            i["confirm"],
            i["heal"],
            round(i["heal"]/i["confirm"], 2),
            i["dead"],
            round(i["dead"]/i["confirm"], 4)]
    return data


headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36',
}
url = 'https://api.inews.qq.com/newsqa/v1/automation/foreign/country/ranklist'
a = requests.get(url=url, headers=headers).text
data = json.loads(a)["data"]
data = [[i["name"],
         i["confirm"],
         i["heal"],
         round(i["heal"]/i["confirm"], 2),  # 保留两位小数，如果不需要可以直接去掉round函数
         i["dead"],
         round(i["dead"]/i["confirm"], 4)]  # 保留四位小数，死亡率比较低，两位会有些直接归零
        for i in data]
wb = openpyxl.Workbook()
ws = wb.active
ws.append(['国家', '累计感染', '治愈', '治愈率', '死亡', '死亡率'])
ws.append(get_china())
for row in data:
    ws.append(row)
wb.save('country_data.xlsx')
print('over')
