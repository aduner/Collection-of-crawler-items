# -*- coding: utf-8 -*-
from datetime import datetime, timedelta


class ProxyModel(object):
    def __init__(self, data):
        self.ip = data['ip']
        self.port = data['port']
        self.expire_str = data['expire_time']
        self.proxy = f'https://{self.ip}:{self.port}'
        self.is_blacked = False

        date_str, time_str = self.expire_str.split()
        year, month, day = list(map(int, date_str.split('-')))
        h, m, s = list(map(int, time_str.split(":")))
        self.expire_time = datetime(year=year, month=month, day=day, hour=h, minute=m, second=s)
    @property
    def is_expire(self):
        now = datetime.now()
        if (self.expire_time - now) < timedelta(seconds=10):
            return True
        else:
            return False
