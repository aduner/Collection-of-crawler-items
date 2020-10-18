import requests
import re
import jieba
import time
import sys
from bs4 import BeautifulSoup
from matplotlib import pyplot as plt
from wordcloud import WordCloud
from PIL import Image
import numpy as np
from jieba import posseg
from openpyxl import Workbook
from collections import Counter


class Bilibili:
    def __init__(self, videourl, page, img_path):

        self.page = str(page)
        self.img_path = img_path
        self.baseurl = videourl.split('?')[0]
        self.fenci = None

    def getAidAndCid(self):
        cidurl = self.baseurl+"?p="+self.page
        cidRegx = '{"cid":([\d]+),"page":%s,' % (self.page)
        r = requests.get(cidurl)
        r.encoding = 'utf-8'
        try:
            self.cid = re.findall(cidRegx, r.text)[0]
        except:
            time.sleep(3)
            sys.exit()

    def getBarrage(self):
        print('正在获取弹幕......')

        commentUrl = 'https://comment.bilibili.com/'+self.cid+'.xml'
        print(commentUrl)
        # 获取并提取弹幕 #
        r = requests.get(commentUrl)
        r.encoding = 'utf-8'
        content = r.text
        # 正则表达式匹配字幕文本
        comment_list = re.findall('>(.*?)</d><d ', content)

        # jieba分词
        self.barrage = "".join(comment_list)

    def create_wordcloud(self, img_path, put_path):
        # 生成词云，具体wordcloud包的使用方法网上一搜一大把
        string = self.fenci_tiqu(self.barrage)
        img = Image.open(img_path)
        img_array = np.array(img)  # 遮罩图片栅格数组化
        wc = WordCloud(
            collocations=False,
            background_color='white',
            mask=img_array,
            font_path='站酷快乐体2016修订版.ttf',
            width=200,
            height=500
        )
        wc.generate_from_text(string)
        fig = plt.figure(1)
        plt.imshow(wc)
        plt.axis("off")
        plt.savefig(put_path, dpi=300)

    def fenci_tiqu(self, text):
        # 分词
        word_nan = posseg.cut(text)  # 此方法可以分辨词性
        wl = []
        for w in word_nan:
            # if w.flag == "n":
            #     word_list.append(w.word)
            wl.append(w.word)
        word_list = []
        n = 0
        for i in wl:
            if '哈' in i:
                n += 1
                continue
            word_list.append(i)
        word_list += ['哈哈哈']*n
        string = ' '.join(word_list)
        self.fenci = word_list
        return string

    def bubbleSort(self, array):
        # 冒泡排序，后面好看些，如果你数据量比较大，建议你就导入excel之后自行排序吧
        for i in range(len(array) - 1):
            for j in range(len(array) - i - 1):
                if array[j][1] < array[j + 1][1]:
                    array[j], array[j + 1] = array[j + 1], array[j]
        return array

    def get_words(self):
        c = Counter()
        for x in self.fenci:
            if len(x) > 1 and x != '\r\n':
                c[x] += 1
        return [[k, v] for k, v in c.most_common() if v > 3]

    def put_excel(self, path):
        # 输出excel
        output = self.get_words()
        output = self.bubbleSort(output)
        wb = Workbook()
        ws = wb.active
        ws.append(['关键词', '词频'])
        for i in output[:20]:
            if i[0] == '-':
                continue
            ws.append(i)
        wb.save(path)


def checkUrl(url):
    try:
        r = requests.get(url)
    except:
        return 0
    r.encoding = 'utf-8'
    # 视频名称正则表达式
    regx = '"part":"(.*?)"'
    result = re.findall(regx, r.text)
    count = 0
    if len(result) > 0:
        print('------视频列表------')
        for i in result:
            count += 1
            print("视频"+str(count)+" : "+i)
        return 1
    return 0


def run(videourl, img_path, excel_path):
    # videourl = 'https://www.bilibili.com/video/BV1FJ41147G5'
    if checkUrl(videourl):
        # 第n个视频
        page = 1

        # 计时
        start_time = time.time()

        # 实例化类
        b = Bilibili(videourl, page, img_path)

        # 获取aid和cid
        b.getAidAndCid()

        # 获取弹幕
        b.getBarrage()

        # 生成词云
        b.create_wordcloud('chinaboy.jpg', img_path)

        # 输出excel
        b.put_excel(excel_path)

        print('耗时:{:.2f}s'.format(time.time()-start_time))
    else:
        print('视频地址无效')


if __name__ == '__main__':
    run('https://www.bilibili.com/video/BV1wi4y187bu',
        'BV1wi4y187bu词云.png', 'BV1wi4y187bu.xlsx')

    # https://www.bilibili.com/video/BV1FJ41147G5?from=search&seid=1392824669673707255
    # 这里只要基础url
    run('https://www.bilibili.com/video/BV1FJ41147G5',
        'BV1FJ41147G5词云.png', 'BV1FJ41147G5.xlsx')
