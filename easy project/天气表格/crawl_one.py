import requests
import json


headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
}
url = f'http://xxfb.mwr.cn/floodDroughtWarning/flood'
a = requests.get(url=url, headers=headers).text
data = json.loads(a)["result"]
data = [[i["stnm"].strip(), i["addv"], i["tm"], round(
    float(i["zl"])-float(i["wrz"]), 2)] for i in data]
pass