# -*- coding: utf-8 -*-
import json
from scrapy import Spider,Request
from zhihu.items import ZhihuItem

class ZhihuspiderSpider(Spider):
    name = 'zhihuspider'
    allowed_domains = ['www.zhihu.com']
    start_urls = ['http://www.zhihu.com/']
    start_user = 'excited-vczh'

    user_url = 'https://www.zhihu.com/api/v4/members/{user}?include={include}'
    user_query = 'allow_message,is_followed,is_following,is_org,is_blocking,employments,answer_count,follower_count,articles_count,gender,badge[?(type=best_answerer)].topics'

    follows_url = 'https://www.zhihu.com/api/v4/members/{user}/followees?include={include}&offset={offset}&limit={limit}'
    follows_query = 'data[*].answer_count,articles_count,gender,follower_count,is_followed,is_following,badge[?(type=best_answerer)].topics'

    followers_url = 'https://www.zhihu.com/api/v4/members/{user}/followers?include={include}&offset={offset}&limit={limit}'
    followers_query = 'data[*].answer_count,articles_count,gender,follower_count,is_followed,is_following,badge[?(type=best_answerer)].topics'

    def start_requests(self):
        yield Request(url=self.user_url.format(user=self.start_user,include=self.user_query),callback=self.user_parse)
        yield Request(url=self.follows_url.format(user=self.start_user,include=self.follows_query,offset=0,limit=20),callback=self.follows_parse)
        yield Request(url=self.followers_url.format(user=self.start_user,include=self.followers_query,offset=0,limit=20),callback=self.followers_parse)

    def user_parse(self,response):
        results = json.loads(response.text)
        item = ZhihuItem()
        for field in item.fields:
            if field in results.keys():
                item[field] = results.get(field)
        yield item
        yield Request(url=self.follows_url.format(user=results.get('url_token'),include=self.follows_query,offset=0,limit=20),callback=self.follows_parse)
        yield Request(url=self.followers_url.format(user=results.get('url_token'),include=self.followers_query,offset=0,limit=20),callback=self.followers_parse)

    def follows_parse(self, response):
        results = json.loads(response.text)
        if 'data' in results.keys():
            for result in results.get('data'):
                 yield Request(url=self.user_url.format(user=result.get('url_token'),include=self.user_query),callback=self.user_parse)
        if 'paging' in results.keys() and results.get('paging').get('is_end') == False:
            next = results.get('paging').get('next')
            yield Request(url= next,callback=self.follows_parse)

    def followers_parse(self, response):
        results = json.loads(response.text)
        if 'data' in results.keys():
            for result in results.get('data'):
                 yield Request(url=self.user_url.format(user=result.get('url_token'),include=self.user_query),callback=self.user_parse)
        if 'paging' in results.keys() and results.get('paging').get('is_end') == False:
            next = results.get('paging').get('next')
            yield Request(url= next,callback=self.followers_parse)