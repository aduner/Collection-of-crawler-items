import requests
import json
import csv
# 设置请求头
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
}
# url为数据接口，返回的是json数据
url = 'http://data.stats.gov.cn/easyquery.htm?m=QueryData&dbcode=fsyd&rowcode=reg&colcode=sj&wds=%5B%7B%22wdcode%22%3A%22zb%22%2C%22valuecode%22%3A%22A140101%22%7D%5D&dfwds=%5B%7B%22wdcode%22%3A%22sj%22%2C%22valuecode%22%3A%22LAST24%22%7D%5D&k1=1594712087459'
# 请求获取数据
data = requests.get(url=url, headers=headers).text
# 加载成json格式，不懂的话查一下就懂了，不难
data = json.loads(data)["returndata"]["datanodes"]  # 这里直接取到表格数据项
# 数据项数量
length = len(data)
table_data = []  # 定义一个列表存储我们需要的数据
# json中没有给地名，我们自己定义一个地名，反正他不会变
region = ['北京市',
          '天津市',
          '河北省',
          '山西省',
          '内蒙古自治区',
          '辽宁省',
          '吉林省',
          '黑龙江省',
          '上海市',
          '江苏省',
          '浙江省',
          '安徽省',
          '福建省',
          '江西省',
          '山东省',
          '河南省',
          '湖北省',
          '湖南省',
          '广东省',
          '广西壮族自治区',
          '海南省',
          '重庆市',
          '四川省',
          '贵州省',
          '云南省',
          '西藏自治区',
          '陕西省',
          '甘肃省',
          '青海省',
          '宁夏回族自治区',
          '新疆维吾尔自治区', ]
num = 0
while True:
    # 通过这两个索引，我们可以拿到2020年05月和2019年05月的数据，每个地区给出24月的数据，所以每次加24就是下个地区的
    one_index = 1+24*num
    two_index = 13+24*num
    if one_index > length:  # 一旦超过长度说明到头了，跳出循环即可
        break
    temp = [region[num]]  # 这里是为了把地区名加入列表
    # 循环加入数据即可
    for i in range(4):
        temp.append(data[one_index+i]['data']["strdata"])
    for i in range(4):
        temp.append(data[two_index+i]['data']["strdata"])
    table_data.append(temp)
    num += 1
# 定义表头
title = ['地区', '2020年05月', '2020年04月', '2020年03月', '2020年02月',
         '2019年05月', '2019年04月', '2019年03月', '2019年02月']
# 写入表格即可
with open('table.csv', 'w', encoding='gbk', newline='') as f:
    f_csv = csv.writer(f)
    f_csv.writerow(title)
    f_csv.writerows(table_data)
