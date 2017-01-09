# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy_djangoitem import DjangoItem


class AgencyItem(DjangoItem):
    django_model = Agency


'''
class PropertyItem(DjangoItem):
    django_model = Property


class HouseItem(DjangoItem):
    django_model = House


class RoomItem(DjangoItem):
    django_model = Room


class OfficeItem(DjangoItem):
    django_model = Office


class GarageItem(DjangoItem):
    django_model = Garage


class LandItem(DjangoItem):
    django_model = Land


class CommercialItem(DjangoItem):
    django_model = Commercial
'''
