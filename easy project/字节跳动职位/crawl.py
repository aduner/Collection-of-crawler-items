import requests
import json
import openpyxl


def get_data(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36'
    }
    html = requests.get(url=url, headers=headers).text
    data = json.loads(html)['data']["job_post_detail"]
    title = data["title"]
    city = data["city_info"]["name"]
    job_category_name = data["job_category"]['name']
    parent = data["recruit_type"]["parent"]["name"]
    description = data["description"]
    requirement = data["requirement"]
    return [title, city, job_category_name, parent, description, requirement]


wb = openpyxl.Workbook()
ws = wb.active
ws.append(['岗位名词', '工作地点', '岗位类型', '招聘方式', '职位描述', '职位要求'])
with open('urls.txt', 'r') as f:
    url_id = f.read().split('\n')
num = 0
for i in url_id:
    url = f'https://job.bytedance.com/api/v1/job/posts/{i}?portal_type=2&_signature=ZEFZKwAAAACIfSIZCdSXW2RBWTAADq.&portal_type=2'
    ws.append(get_data(url))
    num += 1
    print(num)
wb.save('字节跳动电商岗位信息.xlsx')

