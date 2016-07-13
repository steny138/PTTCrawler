# -*- coding: utf-8 -*-

import re
import scrapy
import logging
from ptt_crawler.items import PttCrawlerItem, PTTGroupItem, PttBoardItem, PttArticleItem


class PttBoard(scrapy.Spider):

    name = 'board'
    allowed_domains = ['ptt.cc']
    domain = 'https://www.ptt.cc'
    start_urls = ['https://www.ptt.cc/bbs/index.html']
    _retries = 0
    MAX_RETRY = 1

    def parse(self, response):

        if self.__isOver18(response):
             # 抓所有群組
            if len(response.css('div#prodlist>dl>dd')) > 0:
                for prod in response.css("div#prodlist>dl>dd>p"):

                    url = self.domain + prod.css("a::attr(href)").extract()[0]
                    typeSrc = prod.css("img::attr(src)").extract()[0]

                    if not re.search(ur'f\.gif', typeSrc) is None:
                        # 抓所有看版
                        print "看板"
                        board = PttBoardItem()
                        board['name'] = prod.css("a::attr(href)").extract()[0].split('/')[-2]
                        board['title'] = prod.css("a::text").extract()[0]
                        board['description'] = prod.css("::text").extract()[0]
                        board['url'] = prod.css("a::attr(href)").extract()[0]
                        board['front'] = response.url.split(
                            '/')[-1].replace('.html', '')
                        board['articles'] = []

                        # board['articles'].append(scrapy.Request(url, callback=self.parse_board))

                        # yield scrapy.Request(url, callback=self.parse_board)

                        yield board

                    elif not re.search(ur'folder\.gif', typeSrc) is None:
                        # 抓所有群組
                        print "群組"
                        group=PTTGroupItem()
                        group['name']=prod.css("a::attr(href)").extract()[
                                               0].split('/')[-2]
                        group['title']=prod.css("a::text").extract()[0]
                        group['description']=prod.css("::text").extract()[0]
                        group['url']=prod.css("a::attr(href)").extract()[0]
                        group['front']=response.url.split(
                            '/')[-1].replace('.html', '')
                        group['boards']=[]

                        yield group
                        yield scrapy.Request(url, callback=self.parse_group)

                    else:
                        logging.warning(
                            'There are no group or board can be found1.')
            else:
                logging.warning('There are no group or board can be found2.')
        else:
            pass

    def parse_group(self, response):
        if self.__isOver18(response):
            if len(response.css('div#prodlist>dl>dd')) > 0:
                for prod in response.css("div#prodlist>dl>dd>p"):

                    url=self.domain + prod.css("a::attr(href)").extract()[0];
                    typeSrc=prod.css("img::attr(src)").extract()[0];
                    if not re.search(ur'f\.gif', typeSrc) is None:
                        # 抓所有群組
                        print "看板"
                        board=PttBoardItem()
                        board['name']=prod.css("a::attr(href)").extract()[0].split('/')[-2]
                        board['title']=prod.css("a::text").extract()[0]
                        board['description']=prod.css("::text").extract()[0]
                        board['url']=prod.css("a::attr(href)").extract()[0]
                        board['front']=response.url.split(
                            '/')[-1].replace('.html', '')
                        board['articles']=[]
                        # board['articles'].append(scrapy.Request(url, callback=self.parse_board))

                        yield board
                        # yield scrapy.Request(url, callback=self.parse_board)
                    elif not re.search(ur'folder\.gif', typeSrc) is None:
                        # 抓所有看版
                        print "群組"
                        group=PTTGroupItem()

                        group['name']=prod.css("a::attr(href)").extract()[0].split('/')[-2]
                        group['title']=prod.css("a::text").extract()[0]
                        group['description']=prod.css("::text").extract()[0]
                        group['url']=prod.css("a::attr(href)").extract()[0]
                        group['front']=response.url.split(
                            '/')[-1].replace('.html', '')
                        group['boards']=[]

                        yield group

                        yield scrapy.Request(url, callback=self.parse_group)

                    else:
                        logging.warning(
                            'There are no group or board can be found1.')
            else:
                logging.warning('There are no group or board can be found2.')

    def __isOver18(self, response):
        if len(response.xpath('//div[@class="over18-button-container"]')) > 0:
            if self._retries < PTTSpider.MAX_RETRY:
                self._retries += 1
                logging.warning('retry {} times...'.format(self._retries))
                yield FormRequest.from_response(response,
                                                formdata={'yes': 'yes'},
                                                callback=self.__isOver18)
            else:
                logging.warning('you cannot pass')
                yield false
        else:
            yield true

    def __init__(self):
        super(PttBoard, self).__init__()
