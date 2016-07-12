# -*- coding: utf-8 -*-

import re
import scrapy
import logging
from ptt_crawler.items import PttCrawlerItem, PTTGroupItem, PttBoardItem, PttArticleItem,PTTCommentItem
from datetime import datetime


class PTTArticle(scrapy.Spider):

    name = 'article'
    domain = 'https://www.ptt.cc'
    allowed_domains = ['ptt.cc']
    start_urls = ['https://www.ptt.cc/bbs/movie/index.html']
    _retries = 0
    MAX_RETRY = 1
    MAX_PAGE = 1000
    _page = 0
    def parse(self, response):
        page = 0
        if len(response.css('div#main-container div.r-list-container> div.r-ent')) > 0:
            for ent in response.css('div#main-container div.r-list-container> div.r-ent'):
                href = ent.css("div.title>a::attr(href)")
                if href:
                    url = self.domain + href.extract()[0]
                    yield scrapy.Request(url, callback=self.parse_article)
            
            if self._page <= self.MAX_PAGE:
                next_page = response.xpath(
                    u'//div[@id="action-bar-container"]//a[contains(text(), "上頁")]/@href')
                if next_page:
                    url = response.urljoin(next_page[0].extract())
                    yield scrapy.Request(url, callback=self.parse)
                else:
                    logging.warning('no next page')
                self._page += 1
                print '============= Now Page is : %d ================' % self._page

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

        article_comments = response.css('#main-content > div.push')
        article['comments'] = []
        if article_comments:
            for comment in article_comments:
                comment_item = PTTCommentItem()
                comment_item['name'] = response.url.split('/')[-1].replace('.html', '')
                comment_item['url'] = response.url
                comment_item['kind'] = comment.css('span.push-tag::text').extract()[0]
                comment_item['content'] = comment.css('span.push-content::text').extract()[0]
                comment_item['author'] = comment.css('span.push-userid::text').extract()[0]
                comment_item['date'] = comment.css('span.push-ipdatetime::text').extract()[0]
                article['comments'].append(comment_item)
        ipMatch = re.search('[0-9]{2,3}.[0-9]{2,3}.[0-9]{2,3}.[0-9]{2,3}',  
            response.css(u'div#main-content > span.f2:contains("發信站")::text').extract()[0])

        if ipMatch:
            article['ip'] = ipMatch.group(0)

        yield article
