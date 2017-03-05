# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy_djangoitem import DjangoItem
from houses.models import Price, Date, RealEstate, Property, House, Room, Office, Garage, Land, Commercial


class PropertyListItem(scrapy.Item):
    slug = scrapy.Field()
    url = scrapy.Field()
    price = scrapy.Field()
    date = scrapy.Field()


class RealEstateItem(DjangoItem):
    django_model = RealEstate


class PriceItem(DjangoItem):
    django_model = Price


class DateItem(DjangoItem):
    django_model = Date


class PropertyItem(DjangoItem):
    django_model = Property


class HouseItem(DjangoItem):
    django_model = House
    phones = scrapy.Field()


class RoomItem(DjangoItem):
    django_model = Room
    phones = scrapy.Field()


class OfficeItem(DjangoItem):
    django_model = Office
    phones = scrapy.Field()


class GarageItem(DjangoItem):
    django_model = Garage
    phones = scrapy.Field()


class LandItem(DjangoItem):
    django_model = Land
    phones = scrapy.Field()


class CommercialItem(DjangoItem):
    django_model = Commercial
    phones = scrapy.Field()
