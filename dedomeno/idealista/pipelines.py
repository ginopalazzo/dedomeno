# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from datetime import date
from idealista.items import DateItem, PriceItem
from houses.models import Property
from geopy.geocoders import GoogleV3, Nominatim
import os
import random
import logging


log = logging.getLogger(__name__)


class PropertyPipeline(object):
    """
    Is a pipeline to process all the Property Items and clean them
    """
    def process_item(self, item, spider):
        """
        Clean and format the attributes of the property item.
        :param item: property item.
        :param spider: spider that has crawl the property item.
        :return: the property item .
        """
        phone = self.compose_phone(item['phones'])
        item['phone_1'] = phone[0]
        item['phone_2'] = phone[1]
        item['transaction'] = self.compose_transaction(item['transaction'])
        item['real_estate_raw'] = self.compose_real_estate(item['real_estate_raw'])
        item['date_raw'] = date.today()
        # item['address'] = self.compose_address(item['latitude'], item['longitude'], item['address_raw'], item['proxy'], spider.settings)
        return item
    '''
    # This was used to compose an address with a GeoService (i.e Google, OpenStreetMaps...)
    def compose_address(self, latitude, longitude, address_raw, proxy_raw, settings):
        print('PROXY: %s' % proxy_raw)
        print('ADDRESS_RAW: %s' % address_raw)
        coordinates = (latitude, longitude)
        print('COORDINATES: %s' % str(coordinates))
        proxy_raw = proxy_raw.split('//')[1]
        proxy_list = settings.get('CUSTOM_PROXY_LIST')
        # google_api_ley_list = settings.get('GOOGLE_API_KEY_LIST')
        proxy = next(x for x in proxy_list if proxy_raw in x)
        os.environ['http_proxy'] = proxy
        os.environ['https_proxy'] = proxy
        print('PROXY_DIC: %s' % proxy)
        # g = GoogleV3(api_key=random.choice(google_api_ley_list))
        # address = g.reverse(coordinates, exactly_one=True, timeout=10)
        n = Nominatim()
        address = n.reverse(coordinates, exactly_one=True, language='es', timeout=10)
        os.environ.pop('http_proxy')
        os.environ.pop('https_proxy')
        print('ADDRESS: %s' % address.raw)
        return address.raw
    '''

    def compose_real_estate(self, real_estate):
        if real_estate is not None:
            real_estate = real_estate.split('/')[2]
        return real_estate

    def compose_phone(self, phones):
        phone_list = [None, None, None, None]
        i = 0
        for phone in phones:
            if phone is not None:
                phone_list[i] = phone.strip()
                i = i + 1
        return phone_list

    def compose_transaction(self, transaction):
        if transaction == "alquiler":
            return "rent"
        elif transaction == "venta":
            return "sale"
        else:
            return None

    def compose_int(self, string):
        if string:
            return int("".join(string[0].strip().split('.')))
        else:
            return None

    def close_spider(self, spider):
        """
        Check in the db for any property that doesnt belong to scarpped properties and set it offline.
        :param spider: spider has spiderset atribute with all the slugs of the scrapped properties.
        """
        log.info('SPIDER CLOSE, checking for offline items: %s as %s in %s' % (
            spider.property_type, spider.transaction, spider.province))
        set_spider = spider.spiderset
        set_db = set(Property.objects.filter(
            online=True,
            transaction=spider.transaction,
            address_province=spider.province,
            property_type=spider.property_type).values_list('slug', flat=True)
        )
        set_offline = set_db - set_spider
        today = date.today()
        for slug in set_offline:
            item = Property.objects.get(slug=slug)
            item.online = False
            item_price = item.price_set.order_by('-date_start').first()
            item_date = item.date_set.order_by('-online').first()
            item_price.date_end = today
            item_date.offline = today
            item_price.save()
            item_date.save()
            item.save()
        log.info('%d properties offline' % len(set_offline))


class HousePipeline(PropertyPipeline):
    def process_item(self, item, spider):
        item['m2_total'] = self.compose_int(item['m2_total'])
        item['m2_to_use'] = self.compose_int(item['m2_to_use'])
        item['m2_terrain'] = self.compose_int(item['m2_terrain'])
        item['rooms'] = self.compose_int(item['rooms'])
        item['wc'] = self.compose_int(item['wc'])
        item['construction_year'] = self.compose_int(item['construction_year'])
        house = item.save()
        return item, house


class RoomPipeline(PropertyPipeline):
    def process_item(self, item, spider):
        item['m2_total'] = self.compose_int(item['m2_total'])
        item['wc'] = self.compose_int(item['wc'])
        item['min_month_stay'] = self.compose_int(item['min_month_stay'])
        item['people_max'] = self.compose_int(item['people_max'])
        item['people_now_living_age_min'] = self.compose_int(item['people_now_living_age_min'])
        item['people_now_living_age_max'] = self.compose_int(item['people_now_living_age_max'])
        room = item.save()
        return item, room


class OfficePipeline(PropertyPipeline):
    def process_item(self, item, spider):
        item['m2_total'] = self.compose_int(item['m2_total'])
        item['m2_to_use'] = self.compose_int(item['m2_to_use'])
        item['m2_terrain'] = self.compose_int(item['m2_terrain'])
        item['wc'] = self.compose_int(item['wc'])
        item['elevators'] = self.compose_int(item['elevators'])
        item['num_of_floors'] = self.compose_int(item['num_of_floors'])
        office = item.save()
        return item, office


class GaragePipeline(PropertyPipeline):
    def process_item(self, item, spider):
        item['garage_number'] = self.compose_int(item['garage_number'])
        garage = item.save()
        return item, garage


class LandPipeline(PropertyPipeline):
    def process_item(self, item, spider):
        item['m2_total'] = self.compose_int(item['m2_total'])
        item['m2_min_rent'] = self.compose_int(item['m2_min_rent'])
        item['m2_min_sale'] = self.compose_int(item['m2_min_sale'])
        item['m2_to_build'] = self.compose_int(item['m2_to_build'])
        item['building_floors'] = self.compose_int(item['building_floors'])
        land = item.save()
        return item, land


class CommercialPipeline(PropertyPipeline):
    def process_item(self, item, spider):
        item['transfer_price'] = self.compose_int(item['transfer_price'])
        item['m2_total'] = self.compose_int(item['m2_total'])
        item['m2_to_use'] = self.compose_int(item['m2_to_use'])
        item['m2_terrain'] = self.compose_int(item['m2_terrain'])
        item['num_of_floors'] = self.compose_int(item['num_of_floors'])
        item['show_windows'] = self.compose_int(item['show_windows'])
        item['wc'] = self.compose_int(item['wc'])
        commercial = item.save()
        return item, commercial


class StoreroomPipeline(PropertyPipeline):
    def process_item(self, item, spider):
        item['m2_total'] = self.compose_int(item['m2_total'])
        item['m_height'] = self.compose_int(item['m_height'])
        storeroom = item.save()
        return item, storeroom


class BuildingPipeline(PropertyPipeline):
    def process_item(self, item, spider):
        item['m2_total'] = self.compose_int(item['m2_total'])
        item['m2_min_rent'] = self.compose_int(item['m2_min_rent'])
        item['elevator_num'] = self.compose_int(item['elevator_num'])
        item['floor_num'] = self.compose_int(item['floor_num'])
        item['garage_num'] = self.compose_int(item['garage_num'])
        item['house_num'] = self.compose_int(item['house_num'])
        item['construction_year'] = self.compose_int(item['construction_year'])

        building = item.save()
        return item, building


class DatePipeline(object):
    def process_item(self, item, spider):
        date_item = DateItem()
        date_item['online'] = date.today()
        date_item['property_date'] = item[1]
        date_item.save()
        return item


class PricePipeline(object):
    def process_item(self, item, spider):
        price_item = PriceItem()
        price_item['value'] = item[0]['price_raw']
        price_item['date_start'] = date.today()
        price_item['property_price'] = item[1]
        price_item.save()
        return item
