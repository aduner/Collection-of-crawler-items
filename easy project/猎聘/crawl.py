import requests
from lxml import etree
import copy
from openpyxl import Workbook
# 请求头
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36'
}
# 建立表格
wb = Workbook()
ws = wb.active
ws.append(['标题', '薪酬', '地区', '学历', '工作经验', '公司名称', '行业', '福利'])

# 循环访问
for page in range(10):
    url = f'https://www.liepin.com/zhaopin/?compkind=&dqs=&pubTime=&pageSize=40&salary=&compTag=&sortFlag=&degradeFlag=0&compIds=&subIndustry=&jobKind=&industries=&compscale=&key=%E6%96%B0%E5%AA%92%E4%BD%93&siTag=rmq2QhgMEpRoDbxhhbxJDw%7EfA9rXquZc5IkJpXC-Ycixw&d_sfrom=search_fp&d_ckId=b41078a3e1db7fd63ba81e171748d231&d_curPage=0&d_pageSize=40&d_headId=b41078a3e1db7fd63ba81e171748d231&curPage={page}'
    html = requests.get(url=url, headers=headers).text
    # 解析xpath
    e = etree.HTML(html)
    # 分开加入列表
    for i in range(1, 41):
        title = e.xpath(f'//ul[@class="sojob-list"]/li[{i}]//h3/@title')
        salary = e.xpath(
            f'//ul[@class="sojob-list"]/li[{i}]//p[1]/span[1]/text()')
        city = e.xpath(
            f'//ul[@class="sojob-list"]/li[{i}]//p[1]/a[@class="area"]/text()')
        education = e.xpath(
            f'//ul[@class="sojob-list"]/li[{i}]//p[1]/span[2]/text()')
        year = e.xpath(
            f'//ul[@class="sojob-list"]/li[{i}]//p[1]/span[3]/text()')
        company = e.xpath(
            f'//ul[@class="sojob-list"]/li[{i}]//*[@class="company-info nohover"]//a/@title')
        company = [i[2:] for i in company]  # 去除无用字
        industry = e.xpath(
            f'//ul[@class="sojob-list"]/li[{i}]//p[@class="field-financing"]//text()')
        industry = [i.strip() for i in industry]  # 去除无用字
        welfare = e.xpath(
            f'//ul/li[{i}]/div/div[2]/p[3]/span/text()')
        # 网页有时候会溜掉信息，预处理一下，出错了就跳过
        try:
            industry = ''.join(industry)
            welfare = ',\n'.join(welfare)
            ws.append([title[0],
                        salary[0],
                        city[0],
                        education[0],
                        year[0],
                        company[0],
                        industry,
                        welfare])
        except:
            continue
    print(page)  # 打印页数
wb.save('猎聘.xlsx')
