# -*- coding: utf-8 -*-

import scrapy
from scrapy.http import FormRequest
import logging
from ptt_crawler.items import PttCrawlerItem

class PTTSpider(scrapy.Spider):
    name = 'ptt'
    allowed_domains = ['ptt.cc']
    start_urls = ['https://www.ptt.cc/bbs/Gossiping/index.html']
    _retries = 0
    MAX_RETRY = 1

    def parse(self, response):
        if len(response.xpath('//div[@class="over18-button-container"]')) > 0:
            if self._retries < PTTSpider.MAX_RETRY:
                self._retries += 1
                logging.warning('retry {} times...'.format(self._retries))
                yield FormRequest.from_response(response,
                                                formdata={'yes': 'yes'},
                                                callback=self.parse)
            else:
                logging.warning('you cannot pass')
        else:
            item = PttCrawlerItem()

            item['title'] = response.xpath("//*[@id=\"main-container\"]/div[2]/div[1]/div[3]/a")[0].extract()

            print 'xxxxxx' + item['title']

            filename = response.url.split('/')[-2] + '.html'
            with open(filename, 'wb') as f:
                f.write(response.body)