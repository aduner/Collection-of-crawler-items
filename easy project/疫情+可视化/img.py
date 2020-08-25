import matplotlib.pyplot as plt
import numpy as np
import requests
import json
from matplotlib.ticker import FuncFormatter


def get_data():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36',
    }
    data = []
    url = 'https://api.inews.qq.com/newsqa/v1/query/inner/publish/modules/list?modules=chinaDayList,chinaDayAddList,cityStatis,nowConfirmStatis,provinceCompare'
    a = requests.get(url=url, headers=headers).text
    i = json.loads(a)["data"]["chinaDayList"]
    data.append(i)
    country = ['意大利',
               '巴西',
               '西班牙',
               '德国',
               '英国',
               '法国',
               '美国',
               '俄罗斯']
    for c in country:
        url = f'https://api.inews.qq.com/newsqa/v1/automation/foreign/daily/list?country={c}&'
        a = requests.get(url=url, headers=headers).text
        data.append(json.loads(a)["data"])
    return data


def img_confirm(data):
    country = ['中国',
               '意大利',
               '巴西',
               '西班牙',
               '德国',
               '英国',
               '法国',
               '美国',
               '俄罗斯']
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.figure(figsize=(15, 8))
    index = 0
    for c in country:
        x = [i['date'] for i in data[index]]
        y = [i['confirm'] for i in data[index]]
        if len(x) > 206:
            if c == '中国':
                x = x[len(x)-207:]
                y = y[len(y)-207:]
            else:
                x = x[len(x)-206:]
                y = y[len(y)-206:]
        plt.plot(x, y, label=c)
        index += 1
    plt.legend()
    x = [i['date'] for i in data[1]]
    my_x_ticks = [x[i] for i in range(0, len(x), 14)]+[x[-1]]
    my_y_ticks = [i for i in range(0, 6000001, 1000000)]
    plt.xticks(my_x_ticks)
    plt.yticks(my_y_ticks)
    plt.xticks(rotation=45)
    plt.xlabel("日期")
    plt.ylabel(f"人数(百万)")
    plt.title(f"感染趋势")
    plt.savefig(f'感染趋势.jpg')
    plt.show()


def img_heal(data):
    country = ['中国',
               '意大利',
               '巴西',
               '西班牙',
               '德国',
               '英国',
               '法国',
               '美国',
               '俄罗斯']
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.figure(figsize=(15, 8))
    index = 0
    for c in country:
        x = [i['date'] for i in data[index]]
        y = [i["heal"] for i in data[index]]
        if len(x) > 206:
            if c == '中国':
                x = x[len(x)-207:]
                y = y[len(y)-207:]
            else:
                x = x[len(x)-206:]
                y = y[len(y)-206:]
        plt.plot(x, y, label=c)
        index += 1
    plt.legend()
    x = [i['date'] for i in data[1]]
    my_x_ticks = [x[i] for i in range(0, len(x), 14)]+[x[-1]]
    my_y_ticks = [i for i in range(0, 4000001, 1000000)]
    plt.xticks(my_x_ticks)
    plt.yticks(my_y_ticks)

    plt.xlabel("日期")
    plt.ylabel(f"人数(百万)")
    plt.title(f"治愈趋势")
    plt.savefig(f'治愈趋势.jpg')
    plt.show()


def img_dead(data):
    country = ['中国',
               '意大利',
               '巴西',
               '西班牙',
               '德国',
               '英国',
               '法国',
               '美国',
               '俄罗斯']
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.figure(figsize=(15, 8))
    index = 0
    for c in country:
        x = [i['date'] for i in data[index]]
        y = [i["dead"] for i in data[index]]
        if len(x) > 206:
            if c == '中国':
                x = x[len(x)-207:]
                y = y[len(y)-207:]
            else:
                x = x[len(x)-206:]
                y = y[len(y)-206:]
        plt.plot(x, y, label=c)
        index += 1
    plt.legend()
    x = [i['date'] for i in data[1]]
    my_x_ticks = [x[i] for i in range(0, len(x), 14)]+[x[-1]]
    my_y_ticks = [i for i in range(0, 200001, 20000)]
    plt.xticks(my_x_ticks)
    plt.yticks(my_y_ticks)

    plt.xlabel("日期")
    plt.ylabel(f"人数")
    plt.title(f"死亡趋势")
    plt.savefig(f'死亡趋势.jpg')
    plt.show()


def img_heal_ratio(data):
    country = ['中国',
               '意大利',
               '巴西',
               '西班牙',
               '德国',
               '英国',
               '法国',
               '美国',
               '俄罗斯']
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.figure(figsize=(15, 8))
    index = 0
    for c in country:
        x = [i['date'] for i in data[index]]
        y = [i['heal']/i['confirm'] for i in data[index]]
        if len(x) > 206:
            if c == '中国':
                x = x[len(x)-207:]
                y = y[len(y)-207:]
            else:
                x = x[len(x)-206:]
                y = y[len(y)-206:]
        plt.plot(x, y, label=c)
        index += 1
    plt.legend()
    x = [i['date'] for i in data[1]]
    my_x_ticks = [x[i] for i in range(0, len(x), 14)]+[x[-1]]
    plt.xticks(my_x_ticks)

    def to_percent(temp, position):
        return '%1.0f' % (10*temp) + '%'
    plt.gca().yaxis.set_major_formatter(FuncFormatter(to_percent))

    plt.xlabel("日期")
    plt.ylabel(f"治愈率")
    plt.title(f"治愈率趋势")
    plt.savefig(f'治愈率趋势.jpg')
    plt.show()


def img_dead_ratio(data):
    country = ['中国',
               '意大利',
               '巴西',
               '西班牙',
               '德国',
               '英国',
               '法国',
               '美国',
               '俄罗斯']
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.figure(figsize=(15, 8))
    index = 0
    for c in country:
        x = [i['date'] for i in data[index]]
        y = [i['dead']/i['confirm'] for i in data[index]]
        if len(x) > 206:
            if c == '中国':
                x = x[len(x)-207:]
                y = y[len(y)-207:]
            else:
                x = x[len(x)-206:]
                y = y[len(y)-206:]
        plt.plot(x, y, label=c)
        index += 1
    plt.legend()
    x = [i['date'] for i in data[1]]
    my_x_ticks = [x[i] for i in range(0, len(x), 14)]+[x[-1]]
    plt.xticks(my_x_ticks)

    def to_percent(temp, position):
        return '%1.1f' % (10*temp) + '%'
    plt.gca().yaxis.set_major_formatter(FuncFormatter(to_percent))

    plt.xlabel("日期")
    plt.ylabel(f"死亡率")
    plt.title(f"死亡率趋势")
    plt.savefig(f'死亡率趋势.jpg')
    plt.show()


if __name__ == "__main__":
    data = get_data()
    img_confirm(data)
    img_heal(data)
    img_dead(data)
    img_heal_ratio(data)
    img_dead_ratio(data)
