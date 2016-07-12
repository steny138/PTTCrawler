# -*- coding: utf-8 -*-
from scrapy.crawler import CrawlerProcess
from ptt_crawler.spiders.boards import PttBoard

from twisted.internet import reactor
from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging
from scrapy.utils.project import get_project_settings


def main():
    configure_logging({'LOG_FORMAT': '%(levelname)s: %(message)s'})
    runner = CrawlerRunner()
    settings = get_project_settings()

    settings.set('FEED_FORMAT','json')
    settings.set('FEED_URI', 'result.json')

    d = runner.crawl(PttBoard)
    d.addBoth(lambda _: reactor.stop())
    result = reactor.run() # the script will block here until the crawling is finished

    print result
if __name__ == "__main__":
    main()
