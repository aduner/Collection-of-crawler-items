import requests
import json


headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
}
def get_greatRiver():
    url = f'http://xxfb.mwr.cn/hydroSearch/greatRiver'
    a = requests.get(url=url, headers=headers).text
    data = json.loads(a)["result"]["data"]
    data = [[i["poiBsnm"].strip(),
            i["poiAddv"].strip(),
            i["rvnm"].strip(),
            i["stnm"].strip(),
            i["dateTime"],
            i["zl"],
            i["ql"],
            i["wrz"]] for i in data]
    return data

def get_greatRsvr():
    url = f'http://xxfb.mwr.cn/hydroSearch/greatRsvr'
    a = requests.get(url=url, headers=headers).text
    data = json.loads(a)["result"]["data"]
    data = [[i["poiBsnm"].strip(),
            i["poiAddv"].strip(),
            i["rvnm"].strip(),
            i["stnm"].strip(),
            i["rz"],
            i["wl"],
            i["inq"],
            i["damel"]] for i in data]
    return data

def get_pointHydroInfo():
    url = f'http://xxfb.mwr.cn/hydroSearch/pointHydroInfo'
    a = requests.get(url=url, headers=headers).text
    data = json.loads(a)["result"]["data"]
    data = [[i["poiBsnm"].strip(),
            i["poiAddv"].strip(),
            i["rvnm"].strip(),
            i["stnm"].strip(),
            i["dateTime"],
            i["dyp"],
            i["wth"],] for i in data]
    return data
a=get_greatRsvr()
pass 