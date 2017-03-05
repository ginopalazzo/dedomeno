# -*- coding: utf-8 -*-
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

class CrawlPropertyReactor:
    def __init__(self, transaction=None, property_type=None, province=None, *args, **kwargs):
        self.property_type = property_type
        self.transaction = transaction
        self.province = province
        self.settings = get_project_settings()
        self.settings.set('ITEM_PIPELINES', {
            'idealista.pipelines.PropertyPipeline': 300,
            'idealista.pipelines.%sPipeline' % property_type.capitalize(): 400,
            'idealista.pipelines.DatePipeline': 500,
            'idealista.pipelines.PricePipeline': 600,
        }, 0)
        # self.startPropertySpider()

    def run(self):
        # set up settings
        process = CrawlerProcess(self.settings)
        process.crawl('property', transaction=self.transaction, property_type=self.property_type, province=self.province)
        process.start()
        # the script will block here until the crawling is finished

    def getIdealistaScheme(self):
        return self.settings.get('IDEALISTA_URL_SCHEME')

    def getIdealistaProvinces(self):
        return self.getIdealistaScheme()['provinces']


p = CrawlPropertyReactor(property_type='garage', transaction='sale', province='lugo')
# print(p.getIdealistaProvinces())
p.run()


'''
from scrapy.crawler import Crawler
from twisted.internet import reactor
from billiard import Process
from scrapy.utils.project import get_project_settings
from idealista.spiders.property_spider import PropertySpider

class CrawlPropertyReactor(Process):
    def __init__(self, spider):
        Process.__init__(self)
        self.settings = get_project_settings()
        self.settings.set('ITEM_PIPELINES', {
            'idealista.pipelines.PropertyPipeline': 300,
            'idealista.pipelines.%sPipeline' % property_type.capitalize(): 400,
            'idealista.pipelines.DatePipeline': 500,
            'idealista.pipelines.PricePipeline': 600,
        }, 0)
        self.crawler = Crawler(self.settings)
        self.crawler.configure()
        self.crawler.signals.connect(reactor.stop, signal=signals.spider_closed)
        self.spider = spider

    def run(self):
        self.crawler.crawl(self.spider)
        self.crawler.start()
        reactor.run()

    def getIdealistaScheme(self):
        return self.settings.get('IDEALISTA_URL_SCHEME')

    def getIdealistaProvinces(self):
        return self.getIdealistaScheme()['provinces']


def run_spider(transaction, property_type, province):
    spider = PropertySpider(transaction=transaction, property_type=property_type, province=province)
    crawler = CrawlPropertyReactor(spider)
    crawler.start()
    crawler.join()


from scrapy.conf import settings
from scrapy.utils.log import configure_logging
from scrapy.crawler import Crawler
from twisted.internet import reactor
from billiard import Process
from scrapy.utils.project import get_project_settings

configure_logging({'LOG_FORMAT': '%(levelname)s: %(message)s'})


class CrawlPropertyReactor(Process):
    def __init__(self, transaction=None, property_type=None, province=None, *args, **kwargs):
        Process.__init__(self)
        self.property_type = property_type
        self.transaction = transaction
        self.province = province
        self.settings = get_project_settings()
        self.settings.set('ITEM_PIPELINES', {
            'idealista.pipelines.PropertyPipeline': 300,
            'idealista.pipelines.%sPipeline' % property_type.capitalize(): 400,
            'idealista.pipelines.DatePipeline': 500,
            'idealista.pipelines.PricePipeline': 600,
        }, 0)
        self.crawler = Crawler(self.settings)
        self.crawler.configure()
        self.crawler.signals.connect(reactor.stop, signal=signals.spider_closed)

    def run(self):
        self.crawler.crawl('property', transaction=self.transaction, property_type=self.property_type, province=self.province)
        self.crawler.start()
        reactor.run()


def run_spider(transaction, property_type, province):
    crawler = CrawlPropertyReactor(transaction=transaction, property_type=property_type, province=province)
    crawler.start()
    crawler.join()

run_spider('rent', 'garage', 'almeria')


from twisted.internet import reactor
import scrapy
from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging
from scrapy.utils.project import get_project_settings

configure_logging({'LOG_FORMAT': '%(levelname)s: %(message)s'})


class CrawlPropertyReactor():
    def __init__(self, transaction=None, property_type=None, province=None, *args, **kwargs):
        self.property_type = property_type
        self.transaction = transaction
        self.province = province
        self.settings = get_project_settings()
        self.settings.set('ITEM_PIPELINES', {
            'idealista.pipelines.PropertyPipeline': 300,
            'idealista.pipelines.%sPipeline' % property_type.capitalize(): 400,
            'idealista.pipelines.DatePipeline': 500,
            'idealista.pipelines.PricePipeline': 600,
        }, 0)
        self.runner = CrawlerRunner(self.settings)

    def run(self):
        self.runner.crawl('property', transaction=self.transaction, property_type=self.property_type, province=self.province)
        d = self.runner.join()
        d.addBoth(lambda _: reactor.stop())
        reactor.run()  # the script will block here until the crawling is finished

    def stop():
        reactor.stop()

    def getIdealistaScheme(self):
        return self.settings.get('IDEALISTA_URL_SCHEME')

    def getIdealistaProvinces(self):
        return self.getIdealistaScheme()['provinces'].keys()


# spider = CrawlPropertyReactor(property_type='garage', transaction='sale', province='zamora')
# print(spider.getIdealistaProvinces())
# spider.run()
'''
