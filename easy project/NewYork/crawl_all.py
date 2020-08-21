import requests
from lxml import etree
from openpyxl import Workbook
from time import sleep


def get_data():
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'zh-CN,zh;q=0.9',
        'cache-control': 'max-age=0',
        'cookie': 'nyt-a=yS2aioybNwT2g724ZzQI1w; nyt-gdpr=0; nyt-purr=cfhhcfhhhu; walley=GA1.2.436964788.1592100275; walley_gid=GA1.2.699461500.1592100275; purr-cache=<K0<r<C_<G_<S0; b2b_cig_opt=%7B%22isCorpUser%22%3Afalse%7D; edu_cig_opt=%7B%22isEduUser%22%3Afalse%7D; _gcl_au=1.1.138905513.1592100275; _cb_ls=1; _cb=CrBy1KDGfOaT-fefP; __gads=ID=71010f9495bc8b69:T=1592100280:S=ALNI_MYHugTgmSttAwEsAQCSnqS28c_MFg; nyt-us=0; nyt-geo=HK; g_state={"i_p":1592108519377,"i_l":1}; iter_id=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhaWQiOiI1ZWU1ODljODdiZDkwYTAwMDE0NDY4ZDUiLCJjb21wYW55X2lkIjoiNWMwOThiM2QxNjU0YzEwMDAxMmM2OGY5IiwiaWF0IjoxNTkyMTAxMzIwfQ.rrw7Dja6RqXZyArx-TEmpwvB-Hq-XmrTj9jnOSbZaTk; NYT-S=1wNOvK1OczMppaShiKmeg0BQHv3OXyLZK1JUob/NLbPE0Z83hMdCwunLO5ucXru.wgjOoea6bgYnRezKaidtUysVnZ5Iwnt9hhXfENw/21PcCv523CBFP173xDTQO38FS1; nyt-auth-method=sso; optimizelyEndUserId=oeu1592102659758r0.22104608887055543; FPC=id=72f1bdb5-3f96-4f76-a8ff-60039042df18; WTPERSIST=regi_id=135495355; _derived_epik=dj0yJnU9MWRucGh6dE8tWDIzckxNN3o3NzY1UlY0a1JqN1ZPUWsmbj1PR2F3cGNCc0NKdkRZb0NfWXdlYUxRJm09NyZ0PUFBQUFBRjdsandV; _pin_unauth=dWlkPVl6UTJOelZqTTJNdFpqRmlPUzAwT0dRNExXRTVaakF0TURKak5UTmlaVEl3WkdVMA; _fbp=fb.1.1592102665796.898335839; LPVID=NlZGYzZTdhMmQ3MGU2OWU3; _ga=GA1.2.1585306910.1592108598; _gid=GA1.2.1963825333.1592108598; _cb_svref=null; _gat_UA-58630905-2=1; datadome=FO35imXN~Xk5bo2_hS20T6Cg22oNEpvYyR0_tRZqNDT5mHOxmHZx_KqF_EXESw_lBM~_A8oqyefimj.wgSkrUSkuOrYp88M5bJYVphd.R8; mnet_session_depth=3%7C1592118313032; nyt-m=51BCCB6F86AA2A0D894A13AF429C4105&er=i.1592118341&l=l.3.2105973487.2885420359.1710048711&t=i.7&igu=i.1&iru=i.0&ira=i.0&vp=i.0&fv=i.0&cav=i.0&iue=i.0&ier=i.0&ft=i.0&iir=i.0&s=s.core&rc=i.0&ifv=i.0&igd=i.0&igf=i.0&vr=l.4.0.0.0.0&ica=i.0&uuid=s.ff6c669d-e1da-4829-9d90-9b257876d71a&imu=i.1&ird=i.0&g=i.0&pr=l.4.0.0.0.0&prt=i.0&e=i.1593561600&v=i.3&n=i.2&iub=i.0&iga=i.0&imv=i.0; nyt-jkidd=uid=135495355&lastRequest=1592118342247&activeDays=%5B0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C0%2C1%5D&adv=1&a7dv=1&a14dv=1&a21dv=1&lastKnownType=regi; _chartbeat2=.1592100275551.1592118343293.1.NbtBCBfdxJlCLoNLuD6xxBUofhKR.22',
        'if-modified-since': 'Sun, 14 Jun 2020 07:05:12 GMT',
        'referer': 'https://www.nytimes.com/search?dropmab=false&query=Coronavirus&sections=U.S.%7Cnyt%3A%2F%2Fsection%2Fa34d3d6c-c77f-5931-b951-241b4e28681c&sort=best&types=article',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36'
    }
    with open('newyork_url.txt', 'r', encoding='utf-8') as f:
        urls = f.read().split('\n')
    data = []
    num = 0
    for url in urls:
        date = url[25:35]
        while True:
            try:
                html = requests.get(url=url, headers=headers, timeout=1).text
            except:
                print('超时')
                continue
            if html == '':
                print('被检测到了，等 1s')
                sleep(1)
            else:
                break
        title, text = parse_web(html)
        data.append([title, date, text])
        num += 1
        print(num, '  ', url)

    return data


def parse_web(html):
    e = etree.HTML(html)
    title = ''.join(e.xpath(
        '/html/body/div[1]/div/div/div[2]/main/div/article/div[3]/header/div[3]/h1//text()'))
    p = e.xpath('//*[@class="css-158dogj evys1bk0"]')
    t = ''
    for i in p:
        text = i.xpath('.//text()')
        text = ''.join([i.strip() for i in text])
        text = text.replace("\n                                        ", '')
        text = text.replace('                                        ', '')
        t = t+text
    return [title, t]
    
def save_data():
    data = get_data()
    wb = Workbook()
    ws = wb.active
    ws.append(['题目', '日期', '文章'])
    for i in data:
        ws.append(i)
    wb.save('newyork.xlsx')


save_data()
