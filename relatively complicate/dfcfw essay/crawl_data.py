import requests
import time
import threading
import queue
from lxml import etree
import json
import multiprocessing
import pymysql


class CrawlDate(multiprocessing.Process):
    def __init__(self, m_name, queue, lock):
        super(CrawlDate, self).__init__()
        self.queue = queue
        self.name = m_name
        self.lock = lock

    def run(self):
        while True:
            self.lock.acquire()
            try:
                code = self.queue.get(timeout=5)
            except:
                print('全部code已经爬完')
                self.lock.release()
                return
            self.lock.release()
            urls_queue = self.read_urls(code)
            t1 = CrawlPage(urls_queue, code, self.name)
            t2 = CrawlPage(urls_queue, code, self.name)
            t3 = CrawlPage(urls_queue, code, self.name)
            t4 = CrawlPage(urls_queue, code, self.name)
            t1.start()
            t2.start()
            t3.start()
            t4.start()
            t1.join()
            t2.join()
            t3.join()
            t4.join()
            with open(f'{code}_data.json', 'w', encoding='utf-8') as f:
                f.write('x')
            print(code, '数据已保存')

    def read_urls(self, code):
        with open(f'{code}.json', 'r', encoding='utf-8') as f:
            urls = json.load(f)
        q = queue.Queue()
        for i in urls:
            q.put(i)
        return q


class CrawlPage(threading.Thread):
    def __init__(self, queue, code, m_name):
        super(CrawlPage, self).__init__()
        self.queue = queue
        self.code = code
        self.m_name = m_name
        self.lock = threading.Lock()
        self.conn = pymysql.connect(host='127.0.0.1',
                                    port=3306,
                                    user='root',
                                    passwd='root',
                                    db='dfcfw',
                                    charset='utf8mb4')

    def run(self):
        cursor = self.conn.cursor()
        while True:
            self.lock.acquire()
            try:
                url = self.queue.get(timeout=3)
            except:
                self.conn.commit()
                cursor.close()
                self.conn.close()
                print(f'全部该{self.code}已经爬完')
                self.lock.release()
                return
            self.lock.release()
            data = self.get_data(url)
            if data != None:
                title, put_time, contend = data
                try:
                    cursor.execute(
                        f"insert into wenzhang values('{self.code}','{title}','{put_time}','{contend}')")
                except:
                    continue

    def get_data(self, url):
        host = url.split('/')[2]
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36',
            'Host': host,
            'Upgrade-Insecure-Requests': '1'
        }
        for i in range(2):

            try:
                a = requests.get(url=url, headers=headers)
                a.encoding = 'utf-8'
                a = a.text
                e = etree.HTML(a)
                title = e.xpath('//h1/text()')[0]
                put_time = e.xpath('//div[@class="time"]/text()')[0]
                text = '\n'.join(e.xpath('//*[@id="ContentBody"]//p/text()'))
                break
            except:
                time.sleep(1)
                print('重试')
        else:
            print('抛弃')
            return None
        print(f'{self.m_name}: {self.code}--->{put_time}')
        return [title, put_time, text]


if __name__ == "__main__":
    codes = [
        # '600030',
        # '600050',
        # '600104',
        # '600196',
        # '600276',
        # '600309',
        # '600519',
        # '600547',
        # '600585',
        # '600588',
        # '600690',
        '600703',
        '600745',
        '600837',
        '600887',
        '601012',
        '601066',
        '601088',
        '601138',
        '601166',
        '601186',
        '601211',
        '601236',
        '601288',
        '601318',
        '601319',
        '601328',
        '601336',
        '601398',
        '601601',
        '601628',
        '601658',
        '601668',
        '601688',
        '601816',
        '601818',
        '601857',
        '601888',
        '601988',
        '601989',
        '603160',
        '603259',
        '603993']
    q = multiprocessing.JoinableQueue()
    for i in codes:
        q.put(i)
    lock = multiprocessing.Lock()
    t1 = CrawlDate('t1', q, lock)
    t2 = CrawlDate('t2', q, lock)
    t3 = CrawlDate('t3', q, lock)
    t4 = CrawlDate('t4', q, lock)
    t1.start()
    t2.start()
    t3.start()
    t4.start()
    t3.join()
    t4.join()
    t1.join()
    t2.join()
    print('over')
