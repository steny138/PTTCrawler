# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class PttCrawlerItem(scrapy.Item):
    name = scrapy.Field()
    title = scrapy.Field()
    description = scrapy.Field()
    url = scrapy.Field()
    front = scrapy.Field()

class PTTGroupItem(PttCrawlerItem):
    boards = scrapy.Field()
        
class PttBoardItem(PttCrawlerItem):
    articles = scrapy.Field()

class PttArticleItem(PttCrawlerItem):
    author = scrapy.Field()
    authorName = scrapy.Field()
    date = scrapy.Field()
    fullDate = scrapy.Field()
    content = scrapy.Field()
    ip = scrapy.Field()
    comments = scrapy.Field()
    score = scrapy.Field()
    mark = scrapy.Field()

class PTTCommentItem(PttCrawlerItem):
    kind = scrapy.Field()
    author = scrapy.Field()
    date = scrapy.Field()
    content = scrapy.Field()
        