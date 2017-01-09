# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from houses.models import Source, Country, TerritorialEntity, URLSourceTerritory

# Global variables
country = Country.objects.get_or_create(country_name='Spain')[0]
source = Source.objects.get_or_create(source_name='Idealista', slug='id')[0]


class TerritorialEntityPipeline(object):

    def process_item(self, item, spider):
        provincia = TerritorialEntity.objects.get_or_create(country=country, territorial_entity_name=item['territorial_entity_name'], depth_number=item['depth_number'], depth_name=item['depth_name'], depth_last=item['depth_last'], father=item['father'])[0]
        URLSourceTerritory.objects.get_or_create(url_source_territory_name=item['url_source_territory_name'], url_source_territory_name_list=item['url_source_territory_name_list'], source=source, territory=provincia)
