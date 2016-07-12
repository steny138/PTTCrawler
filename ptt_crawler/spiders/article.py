# -*- coding: utf-8 -*-

import re
import scrapy
import logging
from ptt_crawler.items import PttCrawlerItem, PTTGroupItem, PttBoardItem, PttArticleItem
from datetime import datetime


class PTTArticle(scrapy.Spider):

    name = 'article'
    domain = 'https://www.ptt.cc'
    allowed_domains = ['ptt.cc']
    start_urls = ['https://www.ptt.cc/bbs/movie/index.html']
    _retries = 0
    MAX_RETRY = 1
    MAX_PAGE = 2

    def parse(self, response):
        page = 0
        if len(response.css('div#main-container div.r-list-container> div.r-ent')) > 0:
            for ent in response.css('div#main-container div.r-list-container> div.r-ent'):
                href = ent.css("div.title>a::attr(href)")
                if href:
                    url = self.domain + href.extract()[0]
                    yield scrapy.Request(url, callback=self.parse_article)
                                
            while page < self.MAX_PAGE:
                next_page = response.xpath(
                    '//div[@id="action-bar-container"]//a[contains(text(), "上頁")]/@href')
                if next_page:
                    url = response.urljoin(next_page[0].extract())
                    yield scrapy.Request(url, callback=self.parse_movie_page)
                else:
                    logging.warning('no next page')
                page += 1

    def parse_movie_page(self, response):
        page = 0
        if len(response.css('div#main-container div.r-list-container> div.r-ent')) > 0:
            for ent in response.css('div#main-container div.r-list-container> div.r-ent'):
                url = self.domain + \
                    ent.css("div.title>a::attr(href)").extract()[0]
                yield scrapy.Request(url, callback=self.parse_article)
        else:
            logging.warning('no articles in page.')

    def parse_article(self, response):
        author = response.css(
            '#main-content > div:nth-child(1) > span.article-meta-value::text').extract()[0]
       
        date = datetime.strptime(
            response.css('#main-content > div:nth-child(4) > span.article-meta-value::text')
                .extract()[0],
            '%a %b %d %H:%M:%S %Y')

        article = PttArticleItem()
        article['name'] = response.url.split('/')[-1].replace('.html', '')
        article['title'] = response.css(
            '#main-content > div:nth-child(3) > span.article-meta-value::text').extract()[0]
        article['url'] = response.url

        article['author'] = re.search('^[^\(]+(?=\()', author).group(0)
        article['authorName'] = re.search('[^\(]*(?=\))', author).group(0)
        article['date'] = date.strftime('%d/%m')
        article['fullDate'] = response.css('#main-content > div:nth-child(4) > span.article-meta-value::text').extract()[0]

        article['content'] = response.css('div#main-content::text').extract()[0]
        # article['ip'] = response.css('div#main-content span.f2:nth-child(1)::text').extract()[0]
        # article['comments'] = scrapy.Field()
        # article['score'] = scrapy.Field()
        # article['mark'] = scrapy.Field()

        yield article
