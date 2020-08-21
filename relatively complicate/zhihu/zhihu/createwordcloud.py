# -*- coding: utf-8 -*-
import jieba
from matplotlib import pyplot as plt
from wordcloud import WordCloud
from PIL import Image
import numpy as np
import pymysql
from jieba import posseg


def pinjie(images):
    # 获取当前文件夹中所有JPG图像
    # imges = ['./image/output1.jpg', './image/output2.jpg']
    im_list = [Image.open(fn) for fn in images]

    # 单幅图像尺寸
    width, height = im_list[0].size

    # 创建空白长图
    result = Image.new(im_list[0].mode, (width * len(im_list), height))

    # 拼接图片
    for i, im in enumerate(im_list):
        result.paste(im, box=(i * width, 0))

    # 保存图片
    result.save('./image/wordcloud.jpg')


def fenci_tiqu(text):
    word_nan = posseg.cut(text)
    word_list = []
    for w in word_nan:
        if w.flag == "n" and w.word not in ['评价', '体验', '感觉', '问题', '时候', '事件']:
            word_list.append(w.word)
    string = ' '.join(word_list)
    return string


def create_wordcloud(img_path, put_path, string):
    img = Image.open(img_path)
    img_array = np.array(img)
    wc = WordCloud(
        background_color='white',
        mask=img_array,
        font_path='../站酷快乐体2016修订版.ttf',
        width=200,
        height=500
    )
    wc.generate_from_text(string)

    fig = plt.figure(1)
    plt.imshow(wc)
    plt.axis("off")
    plt.savefig(put_path, dpi=100)


db = pymysql.connect('127.0.0.1', "debian-sys-maint", "lD3wteQ2BEPs5i2u", "zhihu")
text_nan = ''
text_nv = ''
cursor = db.cursor()

select_nan = '''
select question_title from zhihu_user where gender=1
'''
select_nv = '''
select question_title from zhihu_user where gender=0
'''
cursor.execute(select_nv)
data_nv = cursor.fetchall()
cursor.execute(select_nan)
data_nan = cursor.fetchall()


for i in data_nan:
    text_nan += i[0]

for i in data_nv:
    text_nv += i[0]

cursor.close()
db.close()

string_nan = fenci_tiqu(text_nan)
string_nv = fenci_tiqu(text_nv)

create_wordcloud('./image/nan.jpg', './image/output1.jpg', string_nan)
create_wordcloud('./image/nv.jpg', './image/output2.jpg', string_nv)
pinjie(['./image/output1.jpg', './image/output2.jpg'])
