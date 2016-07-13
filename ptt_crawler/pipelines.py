# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import leveldb
from scrapy.conf import settings
import logging
import json
from unqlite import UnQLite

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
        try:
            self.db.Put(keyPrefix + item['name'], json.dumps(dict(item)))
        except Exception, e:
            logging.warning(e)
        finally:
            logging.log(logging.INFO, 'Question added to LevelDB database!')

        return item

    def __init__(self):
        self.db = leveldb.LevelDB(settings['LEVELDB_PATH'])
        
class UnqlitePipeline(object):
    def process_item(self, item, spider):
        keyPrefix = ''
        if 'articles' in item:
            keyPrefix = 'board'
        elif 'boards' in item:
            keyPrefix = 'group'
        elif 'score' in item:
            keyPrefix = 'article'
        elif 'kind' in item:
            keyPrefix = 'comment'
        else:
            keyPrefix = 'none'

        records = self.db.collection(keyPrefix)
        if not records.exists():
            logging.info("records collection created.")
            records.create()
        try:
            records.store(dict(item))
        except Exception, e:
            logging.warning(e)
        finally:
            logging.log(logging.INFO, 'Question added to Unqlite database!')
        return item
    def __init__(self):
        self.db = UnQLite(settings['UNQLITE_PATH'])

class PttCrawlerPipeline(object):
    def process_item(self, item, spider):
        return item
