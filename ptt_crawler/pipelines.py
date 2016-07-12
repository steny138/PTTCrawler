# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import leveldb
from scrapy.conf import settings
import logging
import json

class LeveldbPipeline(object):
    """docstring for LeveldbPipeline"""
    def process_item(self, item, spider):
        keyPrefix = ''
        if 'articles' in item:
            keyPrefix = 'board_'
        elif 'boards' in item:
            keyPrefix = 'group_'
        elif 'score' in item:
            keyPrefix = 'article_'
        elif 'kind' in item:
            keyPrefix = 'comment_'
        else:
            keyPrefix = 'none_'
        print " key is : %s" % keyPrefix + item['name']
        try:
            self.db.Put(keyPrefix + item['name'], json.dumps(dict(item)))
            print self.db.Get(keyPrefix + item['name'])
        except Exception, e:
            logging.warning(e)
        finally:
            logging.log(logging.INFO, 'Question added to MongoDB database!')

        return item


    def __init__(self):
        self.db = leveldb.LevelDB(settings['LEVELDB_PATH'])
        

class PttCrawlerPipeline(object):
    def process_item(self, item, spider):
        return item
