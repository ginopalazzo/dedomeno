# -*- coding: utf-8 -*-
# from scrapy.utils.log import configure_logging
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings


class CrawlProperty:
    ''' Include all the utils for crawling
        and realate the properties and real estates
    '''

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

    def startPropertySpider(self):
        # set up settings
        process = CrawlerProcess(self.settings)
        process.crawl('property', transaction=self.transaction, property_type=self.property_type, province=self.province)
        process.start()
        # the script will block here until the crawling is finished


p = CrawlProperty(property_type='garage', transaction='rent', province='almeria')
p.startPropertySpider()
