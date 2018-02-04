# -*- coding: utf-8 -*-
'''
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
        self.process = CrawlerProcess(self.settings)

    def run(self):
        # set up settings
        self.process.crawl('property', transaction=self.transaction, property_type=self.property_type, province=self.province)
        self.process.join()
        self.process.start()
        # the script will block here until the crawling is finished

    def stop(self):
        self.process.stop()

    def getIdealistaScheme(self):
        return self.settings.get('IDEALISTA_URL_SCHEME')

    def getIdealistaProvinces(self):
        return self.getIdealistaScheme()['provinces']


# p = CrawlPropertyReactor(property_type='garage', transaction='sale', province='lugo')
# print(p.getIdealistaProvinces())
# p.run()


# no funciona con el for
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from scrapy.utils.log import configure_logging

configure_logging({'LOG_FORMAT': '%(levelname)s: %(message)s'})


class CrawlPropertyReactor:
    def __init__(self, transaction=None, property_type=None, provinces=None, *args, **kwargs):
        self.property_type = property_type
        self.transaction = transaction
        self.provinces = provinces
        self.settings = get_project_settings()
        self.settings.set('ITEM_PIPELINES', {
            'idealista.pipelines.PropertyPipeline': 300,
            'idealista.pipelines.%sPipeline' % property_type.capitalize(): 400,
            'idealista.pipelines.DatePipeline': 500,
            'idealista.pipelines.PricePipeline': 600,
        }, 0)

    def run(self):
        # set up settings
        process = CrawlerProcess(self.settings)
        for province in self.provinces:
            process.crawl('property', transaction=self.transaction, property_type=self.property_type, province=province)
            process.start()
        # the script will block here until the crawling is finished

    def getIdealistaScheme(self):
        return self.settings.get('IDEALISTA_URL_SCHEME')

    def getIdealistaProvinces(self):
        return self.getIdealistaScheme()['provinces']


p = CrawlPropertyReactor(property_type='garage', transaction='sale', provinces=['teruel', 'huesca', 'albacete', 'avila', 'caceres'])
p.run()
# print(p.getIdealistaProvinces())




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


from scrapy import signals
from scrapy.conf import settings
from scrapy.utils.log import configure_logging
from scrapy.crawler import Crawler
from twisted.internet import reactor
from billiard import Process
from 
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
        self.crawler = Crawler('property', self.settings)
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


'''
# funciona genial hasta que finaliza, que hay intento de reinicio del Reactor
from twisted.internet import reactor, defer
from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging
from scrapy.utils.project import get_project_settings
import pprint

configure_logging({'LOG_FORMAT': '%(levelname)s: %(message)s', 'LOG_LEVEL': 'INFO'})


class CrawlPropertyReactor():
    """
    Start a new CrawlerRunner object for the idealista scrapper
    """
    def __init__(self, transaction=None, property_type=None, provinces=None, *args, **kwargs):
        """
        Initialize the CrawlPropertyReactor object
        :param transaction: type of transaction {sale,rent}
        :param property_type: type of property {house,garage,commercial,land,office}
        :param provinces: a list of Spanish provinces to crawl (see idealista scrapper settings for the schema)
        :param args:
        :param kwargs:
        """
        self.property_type = property_type
        # will populate the statistics of the scrapper
        self.stats_dic_list = []
        self.transaction = transaction
        self.provinces = provinces
        # set the ITEM_PIPELINES settings for the specific property_type
        self.settings = get_project_settings()
        self.settings.set('ITEM_PIPELINES', {
            'idealista.pipelines.PropertyPipeline': 300,
            'idealista.pipelines.%sPipeline' % property_type.capitalize(): 400,
            'idealista.pipelines.DatePipeline': 500,
            'idealista.pipelines.PricePipeline': 600,
        }, 0)

    @defer.inlineCallbacks
    def conf(self):
        print(1.1)
        runner = CrawlerRunner(self.settings)
        print(1.2)
        for province in self.provinces:
            print(1.3)
            property_crawler = runner.create_crawler('property')
            print(1.4)
            yield runner.crawl(property_crawler, transaction=self.transaction, property_type=self.property_type, province=province)
            print(1.5)
            province_dic_stats = {}
            province_dic_stats['transaction'] = self.transaction
            province_dic_stats['property_type'] = self.property_type
            province_dic_stats['province'] = province
            province_dic_stats['finish_reason'] = property_crawler.stats.get_value('finish_reason')
            province_dic_stats['start_time'] = property_crawler.stats.get_value('start_time')
            province_dic_stats['finish_time'] = property_crawler.stats.get_value('finish_time')
            province_dic_stats['item_scraped_count'] = property_crawler.stats.get_value('item_scraped_count')
            province_dic_stats['log_count/ERROR'] = property_crawler.stats.get_value('log_count/ERROR', default=0)
            # province_dic_stats.update(property_crawler.stats.get_stats())
            print(1.6)
            self.stats_dic_list.append(province_dic_stats)
            print(1.7)
        print(1.8)
        reactor.stop()  # the script will block here until the crawling is finished
        print(1.9)
        # pp = pprint.PrettyPrinter(indent=4)
        # pp.pprint(self.stats_dic_list)
        return self.stats_dic_list
        # crawler.signals.connect(self.callback, signal=signals.spider_closed)
        # get_stats()
        # get_value(key, default=None)
        # 'item_scraped_count'

    def run(self):
        reactor.run()

    def stop(self):
        reactor.stop()

    def getIdealistaScheme(self):
        return self.settings.get('IDEALISTA_URL_SCHEME')

    def getIdealistaProvinces(self):
        return self.getIdealistaScheme()['provinces'].keys()


# teruel 24 huesca 155 zamora 80 caceres 94
# valencia 3154
# spider = CrawlPropertyReactor(property_type='garage', transaction='sale', provinces=['teruel', 'melilla'])
if __name__ == "__main__":
    print(0)
    spider = CrawlPropertyReactor(property_type='garage', transaction='rent', provinces=['madrid'])
    print(1)
    spider.conf()
    print(2)
    spider.run()
    print(3)

'''
from scrapy.crawler import CrawlerRunner
from scrapy import log, signals
from scrapy.settings import Settings
from twisted.internet import reactor
from datetime import datetime
from scrapy.utils.project import get_project_settings
# from idealista.spiders.property_spider import PropertySpider


class CrawlPropertyReactor():
    def __init__(self, transaction=None, property_type=None, provinces=None, *args, **kwargs):
        self.starttime = datetime.now()
        self.endtime = datetime.now()
        self.property_type = property_type
        self.transaction = transaction
        self.provinces = provinces
        self.settings = get_project_settings()
        self.settings.set('ITEM_PIPELINES', {
            'idealista.pipelines.PropertyPipeline': 300,
            'idealista.pipelines.%sPipeline' % property_type.capitalize(): 400,
            'idealista.pipelines.DatePipeline': 500,
            'idealista.pipelines.PricePipeline': 600,
        }, 0)

    def configure_crawler(self, crawler, province):
        # spider = PropertySpider(self.transaction, self.property_type, province)
        # configure signals
        crawler.signals.connect(self.callback, signal=signals.spider_closed)
        # detach spider
        crawler._spider = None
        # configure and start the crawler
        crawler.configure()
        crawler.crawl('property', self.transaction, self.property_type, province)
    # callback fired when the spider is closed

    def callback(self, spider, reason):
        try:
            province = self.provinces.pop()
            self.configure_crawler(province)
        except IndexError:
            # stop the reactor if no postal codes left
            self.endtime = datetime.now()
            print('start time: %s' % str(self.starttime))
            print('end time: %s' % str(self.endtime))
            reactor.stop()

    def run(self):
        crawler = CrawlerRunner(self.settings)
        self.configure_crawler(crawler, self.provinces.pop())
        crawler.start()
        # start logging
        log.start()
        # start the reactor (blocks execution)
        reactor.run()


p = CrawlPropertyReactor(property_type='garage', transaction='sale', provinces=['huesca', 'teruel', 'albacete', 'avila', 'caceres'])
# print(p.getIdealistaProvinces())
p.run()
'''
