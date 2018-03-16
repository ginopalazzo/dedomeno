# -*- coding: utf-8 -*-

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
        runner = CrawlerRunner(self.settings)
        for province in self.provinces:
            property_crawler = runner.create_crawler('property')
            yield runner.crawl(property_crawler, transaction=self.transaction, property_type=self.property_type, province=province)
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
            self.stats_dic_list.append(province_dic_stats)
        reactor.stop()  # the script will block here until the crawling is finished
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
    spider = CrawlPropertyReactor(property_type='land', transaction='sale', provinces=['salamanca'])
    spider.conf()
    spider.run()

