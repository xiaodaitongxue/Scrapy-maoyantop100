# -*- coding: utf-8 -*-
import re

import scrapy

from maoyan100.items import Maoyan100Item


class MaoyanSpider(scrapy.Spider):
    name = 'maoyan'
    allowed_domains = ['maoyan.com']
    start_urls = ['http://maoyan.com/board/4/']

    def parse(self, response):
        # pass，
        pattern = re.compile(
            r'p class="name".*?<a href=.*?>(.*?)</a>.*?p class="star">(.*?)</p>.*?p class="releasetime">(.*?)</p>.*?p class="score">.*?"integer">(.*?)</i>.*?"fraction">(.*?)</i>',
            re.S)
        results = re.findall(pattern, response.text)
        for result in results:
            item = Maoyan100Item()
            name=result[0]
            star=result[1].strip()[3:]
            releasetime=result[2][5:]
            score=result[3]+result[4]
            item['name']=name
            item['star']=star
            item['releasetime']=releasetime
            item['score']=score
            yield item

        next=response.css('.wrapper .pager-main .list-pager a::attr(href)').extract()[-1]  #//*[@id="app"]/div/div/div[2]/ul/li[9]/a
        print(next)
        url = response.urljoin(next) #'?offset=30'
        yield scrapy.Request(url=url, callback=self.parse)


        # print(response.text)