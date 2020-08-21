import json
import requests
from lxml import etree
from os.path import exists
from os import makedirs
from openpyxl import Workbook
from datetime import datetime
from time import time, sleep


class CrawlData(object):
    def __init__(self):
        self.proxise = False

    def run(self):
        username = '1'  # input('请输入微博账号：')
        password = 's'  # input('请输入密码：')
        s = self.login(username, password)
        print('\n获取目标用户id，具体方法参见说明文档')
        uid = input('填入用户id(一次填对，填错有不可预料的错误)：').strip()
        self.crawl_weibo(uid, s)

    def get_proxise(self):
        print('更新ip')
        # 芝麻代理接口，其他代理请根据实际情况重写本函数
        url = ''
        p = requests.get(url).text.strip()
        proxies = {
            "https": p,
        }
        self.proxise = proxies
        print('更新成功!', p)
        sleep(1)

    def login(self, username, password):
        form_data = {'username': username,
                     'password': password,
                     'savestate': '1',
                     'r': 'https://m.weibo.cn/profile/1752502537',
                     'ec': '0',
                     'pagerefer': 'https://m.weibo.cn/login?backURL=https%3A%2F%2Fm.weibo.cn%2Fprofile%2F1752502537',
                     'entry': 'mweibo',
                     'wentry': '',
                     'loginfrom': '',
                     'client_id': '',
                     'code': '',
                     'qq': '',
                     'mainpageflag': '1',
                     'hff': '',
                     'hfp': ''}
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36',
        }
        s = requests.Session()
        s.post(url='https://passport.weibo.cn/sso/login',
               headers=headers, data=form_data)
        return s

    def mkdir(self, path, flag=True):
        folder = exists(path)
        if not folder:  # 判断是否存在文件夹如果不存在则创建为文件夹
            makedirs(path)  # makedirs 创建文件时如果路径不存在会创建这个路径
            return path
        else:
            if flag:
                print("已存在同名文件文件夹！！！")
                return False
            return path

    def download_img(self, urls, img_id, user_id, s):
        num = 0
        for url in urls:
            num += 1
            houzui = url.split('.')[-1]
            name = f'{num}.{houzui}'
            self.mkdir(f'.\\爬取结果\\{user_id}\\img\\{img_id}', flag=False)
            with open(f'.\\爬取结果\\{user_id}\\img\\{img_id}\\{name}', 'wb') as f:
                ttt = 0
                while True:
                    if ttt > 10:
                        print('ip可能被封禁,稍后重试')
                        return
                    try:
                        f.write(s.get(url).content)
                        break
                    except:
                        ttt += 1
                        print('超时!重试中')
                        continue
        print(f'第 {img_id} 条微博的图片下载完毕')

    def parse_time(self, put_time):
        if '-' not in put_time:
            return str(datetime.today()).split()[0]
        else:
            if '-' in put_time[:4]:
                return str(datetime.today()).split('-')[0]+'-'+put_time
            return put_time

    def save_excel(self, data, save_path):
        wb = Workbook()
        ws = wb.active
        ws.append(['id', '发布时间', '博文内容'])
        for i in data:
            ws.append(i)
        wb.save(f'.\\爬取结果\\{save_path}\\微博博文.xlsx')

    def crawl_weibo(self, user_id, s):
        data = []
        headers = {
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36'}
        print(f'创建文件夹 {user_id}')
        if self.mkdir(f'.\\爬取结果\\{user_id}'):
            print('创建成功！')
        else:
            print('下面可能会覆盖源文件内容，是否继续(y/n)?')
            if input('退出输入 no，如果继续输入 yes : ') == 'no':
                print('程序结束')
                return
        print('开始爬取文本数据……')
        tt = 0
        for page in range(1, 9999999):
            url = f'https://m.weibo.cn/api/container/getIndex?containerid={user_id}_-_WEIBO_SECOND_PROFILE_WEIBO&page_type=03&page={page}'
            ttt = 0
            while True:
                if ttt > 3:
                    self.get_proxise()
                    # return
                if ttt > 5:
                    print('未知错误')
                    break
                try:
                    if not self.proxise:
                        string = s.get(url=url, timeout=5,
                                       headers=headers).text
                        temp = json.loads(string, strict=False)[
                            "data"]["cards"]
                    else:
                        string = s.get(
                            url=url, timeout=5, headers=headers, proxies=self.proxise).text
                        temp = json.loads(string, strict=False)[
                            "data"]["cards"]
                    # sleep(1)
                    break
                except TimeoutError:
                    ttt += 1
                    print('超时!重试中')
                    continue
                except json.JSONDecodeError:
                    self.get_proxise()
                    continue

            if temp[0].get("name") == "暂无微博":
                tt += 1
                if tt > 2:
                    break
                continue

            data += temp
            print(f'爬取第 {page} 页……')
        for i in data:
            if i.get("mblog") != None:
                data = [i["mblog"] for i in data[data.index(i):]]
                break
        weibo_data = []
        num = 0
        print('开始处理数据并下载图片!\n……')
        for i in data:
            num += 1
            weibo_data.append(
                [num, self.parse_time(i["created_at"]), i["raw_text"]])
        self.save_excel(weibo_data, f'.\\{user_id}')
        num = 0
        for i in data:
            num += 1
            pics = i.get("pics")
            if pics != None and len(pics) > 0:
                self.download_img([pic["url"]
                                   for pic in i["pics"]], num, user_id, s)


c = CrawlData()
c.run()
