# -*- coding: utf-8 -*-

'''
# Scrapy imports
from scrapy.crawler import Crawler
from scrapy.contrib.loader import ItemLoader
from scrapy.contrib.loader.processor import Join, MapCompose, TakeFirst
from scrapy import log, signals, Spider, Item, Field
from scrapy.settings import Settings
from twisted.internet import reactor
'''
# from twisted.internet import reactor

# from scrapy.utils.log import configure_logging

# import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

# Django DB imports

import sys
import os
import django

proj_path = "/Users/ginopalazzo/Magic/dedomeno-proyect/dedomeno"
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "myproject.settings")
sys.path.append(proj_path)
os.environ['DJANGO_SETTINGS_MODULE'] = 'dedomeno.settings'
django.setup()

from houses.models import Price, Date, Property, Commercial

# Other imports
# from datetime import date
# import json
from pprint import pprint


property_list = []


class DictPipeline(object):
    def process_item(self, item, spider):
        property_list.append(dict(item))


class CrawlProperty:
    ''' Include all the utils for crawling
        and realate the properties and real estates
    '''

    def __init__(self, _property, _transaction, _provinces):
        self.property = _property
        self.transaction = _transaction
        self.provinces = _provinces
        self.idealista_urls = get_project_settings().get('IDEALISTA_URL_SCHEME')

    def composeUrlList(self):
        ''' [0] = Comose a list of the properties urls relatetd
            https://www.idealista.com/venta-viviendas/a-coruna-provincia/?ordenado-por=fecha-publicacion-desc
            [1] = Comose a list of the real estate urls relatetd
            https://www.idealista.com/pro/venta-viviendas/a-coruna-provincia/agencias-inmobiliarias
        '''
        _url = self.idealista_urls['url']
        _transaction = self.idealista_urls[self.transaction]
        _separator = self.idealista_urls['separator']
        _property = self.idealista_urls[self.transaction + '_transaction'][self.property]
        _query = self.idealista_urls['query_pub_date']
        _pro = self.idealista_urls['pro']
        _real_estate = self.idealista_urls['real estate']
        property_list = []
        real_estate_list = []
        if self.provinces == 'all':
            _provinces = self.idealista_urls['provinces'].values()
        else:
            _provinces = [self.idealista_urls['provinces'][self.provinces]]
        for province in _provinces:
            property_list.append(_url + _transaction + _separator + _property + '/' + province + '/' + _query)
            real_estate_list.append(_url + _pro + '/' + _transaction + _separator + _property + '/' + province + '/' + _real_estate)
        return (property_list, real_estate_list)

    def startSpiderList(self):
        property_url_list = self.composeUrlList()[0]
        # set up settings
        settings = get_project_settings()
        settings.overrides['ITEM_PIPELINES'] = {'__main__.DictPipeline': 1}
        process = CrawlerProcess(settings)
        process.crawl('property_list', start_urls=property_url_list)
        process.start()
        # pprint(property_list)
        # the script will block here until the crawling is finished

    def checkPriceChange(self, property_object, item):
        print("prices: " + str(property_object.date_set.first().online))
        print('item: ' + str(item))
        print('property_object: ' + str(property_object))
        old_price = Price.objects.filter(property_price=property_object).order_by('-date_start').first()
        # if item['price'] != old_price.value:
        #    pass
        # print('old_price: ' + str(old_price.value))
        # if item['price'] == property_object.

    def main(self):
        self.startSpiderList()
        ''' Properties offline
        '''
        # [d['slug'] for d in property_list]
        # offlines_query = Commercial.objects.exclude(slug=item['slug'])
        ''' Properties has change price
        '''
        for item in property_list:
            property_object = Commercial.objects.filter(slug=item['slug']).first()
            if property_object:
                self.checkPriceChange(property_object, item)
        ''' New Properties
        '''


p = CrawlProperty('commercial', 'sale', 'alava')
p.main()
