import requests
import re
import base64
from lxml import etree
from fontTools.ttLib import TTFont
from io import BytesIO


data_map = {(0, 1549): 'B', (1588, 0): '男', (868, 0): '王', (825, 367): '大', (265, -118): '专', (0, 1026): 'M',
            (-110, -150): '女', (1460, 0): '吴', (230, 390): '硕', (156, 262): '赵', (660, 0): '黄', (924, 0): '李',
            (0, 1325): '1', (0, 134): '8', (0, 144): '经', (0, 125): '2', (1944, 0): '下', (-52, -52): '本', (582, 0): '届',
            (0, -227): '5', (146, 78): '应', (228, 306): '科', (-244, -426): '7', (770, 0): '中', (928, 0): '生',
            (-121, 62): '6', (-833, 0): 'E', (299, 0): '陈', (159, -123): '3', (164, 0): '以', (-764, 0): '杨',
            (-221, 0): 'A', (238, 0): '张', (0, -1023): '4', (784, 0): '无', (0, 410): '0', (128, -74): '9',
            (-46, -550): '验', (0, 110): '博', (0, 132): '技', (746, 0): '士', (210, 358): '校', (1298, 0): '高',
            (-74, -366): '刘', (0, -508): '周'}


def get_font_map(content):
    font_map = {}
    result = re.search(r"base64,(.*?)\)", content, flags=re.S).group(1)
    b = base64.b64decode(result)
    tf = TTFont(BytesIO(b))
    # print(tf.getGlyphNames())
    # 运行三遍分别保存字体库01、02、03用来做分析
    with open("ztku01.woff", "wb")as f:
        f.write(b)

    fonts = TTFont("ztku01.woff")
    fonts.saveXML("ztku01.xml")
    for index, i in enumerate(tf.getGlyphNames()[1:-1]):
        temp = tf["glyf"][i].coordinates
        # print(temp)
        x1, y1 = temp[0]
        x2, y2 = temp[1]
        new = (x2 - x1, y2 - y1)
        key = i.replace("uni", "&#x").lower()
        # key = key.encode('utf-8').decode('unicode_escape')
        font_map[key] = data_map[new]
    # print(font_map)
    return font_map

def parse_html():
    url = "https://sz.58.com/searchjob/"
    header = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.75 Safari/537.36',
        'cookie':'f=n; commontopbar_new_city_info=4%7C%E6%B7%B1%E5%9C%B3%7Csz; commontopbar_ipcity=nj%7C%E5%8D%97%E4%BA%AC%7C0; id58=c5/nfF+Sknm6SD4eCO3jAg==; 58tj_uuid=d211bd8b-12df-4c1d-8f7d-028f7008e47b; wmda_uuid=bdddb32235cec15c7b11cdf0ffeea515; wmda_new_uuid=1; als=0; param8616=1; param8716kop=1; xxzl_deviceid=OXcYq9MHR9sSfFcdBEf15sbGB%2BfuNGErOB8zF9mYTIwaUcL1GOftnMpODytvWsXY; 58home=nj; city=nj; wmda_visited_projects=%3B1732038237441%3B10104579731767%3B1731916484865%3B11187958619315; xxzl_smartid=86250991fae8f3f8d840220570a4a9c2; gr_user_id=67da4a1f-6df3-471d-8535-ed50d2169f46; xxzl_sid="5gUA96-Q2s-M14-TZW-1dUWAMwQB"; xxzl_cid=5b90dd2f7629460e847135078a677d3a; xzuid=ac7d7762-2fee-408d-a15b-5af8089c5bc9; ppStore_fingerprint=1CE10EF5EFE674BEA245325E11F400B3CDAB51EB558C7B95%EF%BC%BF1603676316187; xxzl_token="ChvKzVGngqKKZd6ehpAcKOYjKdnVedj9GJ7PvVQJeNLMpGlF/AREgI4hI4flxA+Iin35brBb//eSODvMgkQULA=="; sessionid=14eddd9e-8ed2-44a6-8046-279a8bfa6fb1; wmda_session_id_10104579731767=1604538949095-711f512a-8dbf-6890; PPU="UID=66348500812560&UN=iykm2xg5x&TT=9644c6dd8657b40faf1233b6cadb8a29&PBODY=JDK8GoWtz5PeW8yy-kwpIaesOoL-qsDXUI9OdXQEGgdESQQ508ahoHA7_2WXsTYuSMyfM6BvNg6oaXr9fBPmbwJS5qyic-SKrLL712M0tTX3Xv5lpTJ1TW8S_WT6BdKfWPNSZf6wZygvi6Krveg4pAgdJPZ_oqBgoM7-U88y5mI&VER=1"; www58com="UserID=66348500812560&UserName=iykm2xg5x"; 58cooper="userid=66348500812560&username=iykm2xg5x"; 58uname=iykm2xg5x; JSESSIONID=F4DA7E33832CFE075B8394F0F5BE72E5; new_session=1; new_uv=7; utm_source=; spm=; init_refer=https%253A%252F%252Fpassport.58.com%252F; jl_list_left_banner=1; Hm_lvt_a3013634de7e7a5d307653e15a0584cf=1603633938,1604538997; Hm_lpvt_a3013634de7e7a5d307653e15a0584cf=1604538997; wmda_session_id_1731916484865=1604538996895-30c87e59-c192-b18b; f=n',
    }
    response = requests.get(url, headers=header)
    html = response.text
    font_map = get_font_map(html)
    for i in font_map:
        # print(i+";")2
        html = html.replace(i + ";", font_map[i])
    data = etree.HTML(html)
    print(html)#此处已经是解密后的网页源代码 正常解析就行
    exit()
    personal_information = data.xpath('//div[@id="infolist"]/ul/li//dl[@class="infocardMessage clearfix"]')
    for info in personal_information:
        # 姓名
        name = info.xpath('./dd//span[@class="infocardName fl stonefont resumeName"]/text()')[0]
        # 性别
        gender = info.xpath('./dd//div[@ class="infocardBasic fl"]/div/em[1]/text()')[0]
        # 年龄
        age = info.xpath('./dd//div[@ class="infocardBasic fl"]/div/em[2]/text()')[0]
        # 工作经验
        work_experience = info.xpath('./dd//div[@ class="infocardBasic fl"]/div/em[3]/text()')[0]
        # 学历
        education = info.xpath('./dd//div[@ class="infocardBasic fl"]/div/em[4]/text()')[0]
        print("===============================")
        print(name, gender, age, work_experience, education)

if __name__ == "__main__":
    parse_html()