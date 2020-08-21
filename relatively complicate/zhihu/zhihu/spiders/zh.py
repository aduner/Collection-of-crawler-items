# -*- coding: utf-8 -*-
import scrapy
import json
from ..items import ZhihuItem


class ZhSpider(scrapy.Spider):
    name = 'zh'
    allowed_domains = ['zhihu.com']
    start_urls = [
        'https://www.zhihu.com/api/v4/members/miji100/followers?include=data%5B*%5D.answer_count%2Carticles_count%2Cgender%2Cfollower_count%2Cis_followed%2Cis_following%2Cbadge%5B%3F(type%3Dbest_answerer)%5D.topics&offset=20&limit=20']
    user_num = 0
    amount = 0

    def parse(self, response):
        if self.user_num > 100:
            print('user crawl over')
            return
        user_list_json = json.loads(response.body.decode('utf-8'))
        try:
            user_list_url = user_list_json['paging']['next']
            print('爬取用户页：', self.user_num)
            self.user_num += 1
            for user in user_list_json['data']:
                user_url = user['url'].replace('api/v4/people', 'api/v3/feed/members') + '/activities'
                gender = user['gender']
                user_id = user['id']
                yield scrapy.Request(user_url, callback=self.parse_user,
                                     meta={'gender': gender, 'user_id': user_id, 'question_list': []})
            yield scrapy.Request(user_list_url, callback=self.parse)
        except:
            print('user crawl over')

    def parse_user(self, response):
        user_json = json.loads(response.body.decode('utf-8'))
        user_id = response.meta.get('user_id')  # 用户id号
        gender = response.meta.get('gender')  # 性别
        question_list = response.meta.get('question_list')
        for data in user_json['data']:
            action = data['action_text']  # 行为
            if action[-2:] != '问题':
                continue
            action = action[-5:-3]
            if 'question' in data['target'].keys():
                question_title = data['target']['question']['title']  # 问题标题
            else:
                question_title = data['target']['title']
            if question_title not in question_list:  # 去重
                question_list.append(question_title)
            else:
                continue
            # print('user_id:', user_id)
            # print('gender:', gender)
            # print('action', action)
            # print('question_title', question_title)
            self.amount += 1
            print('爬取：', self.amount)

            item = ZhihuItem(
                user_id=user_id,
                gender=gender,
                action=action,
                question_title=question_title
            )
            yield item
        try:
            next_url = user_json['paging']['next']
            yield scrapy.Request(next_url, callback=self.parse_user,
                                 meta={'gender': gender, 'user_id': user_id, 'question_list': question_list})
        except:
            return
