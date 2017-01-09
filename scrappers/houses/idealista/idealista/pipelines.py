# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from datetime import date


class RealEstatePipeline(object):
    def process_item(self, item, spider):
        item.save()
        return item


class PropertyPipeline(object):
    def process_item(self, item, spider):
        phone = self.compose_phone(item['phones'])
        item['phone_1'] = phone[0]
        item['phone_2'] = phone[1]
        item['transaction'] = self.compose_transaction(item['transaction'])
        item['real_estate_raw'] = self.compose_real_estate(item['real_estate_raw'])
        item['date_raw'] = date.today()
        return item

    def compose_real_estate(self, real_estate):
        if real_estate is not None:
            real_estate = real_estate.split('/')[2]
        return real_estate

    def compose_phone(self, phones):
        phone_list = [None, None]
        i = 0
        for phone in phones:
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


class HousePipeline(object):
    def process_item(self, item, spider):
        item['m2_total'] = self.compose_int(item['m2_total'])
        item['m2_to_use'] = self.compose_int(item['m2_to_use'])
        item['m2_terrain'] = self.compose_int(item['m2_terrain'])
        item['rooms'] = self.compose_int(item['rooms'])
        item['wc'] = self.compose_int(item['wc'])
        item.save()
        return item

    def compose_int(self, string):
        if string:
            return int("".join(string[0].strip().split('.')))
        else:
            return None


class RoomPipeline(object):
    def process_item(self, item, spider):
        item['m2_total'] = self.compose_int(item['m2_total'])
        item['wc'] = self.compose_int(item['wc'])
        item['min_month_stay'] = self.compose_int(item['min_month_stay'])
        item['people_max'] = self.compose_int(item['people_max'])
        item['people_now_living_age_min'] = self.compose_int(item['people_now_living_age_min'])
        item['people_now_living_age_max'] = self.compose_int(item['people_now_living_age_max'])
        item.save()
        return item

    def compose_int(self, string):
        if string:
            return int("".join(string[0].strip().split('.')))
        else:
            return None


class OfficePipeline(object):
    def process_item(self, item, spider):
        item['m2_total'] = self.compose_int(item['m2_total'])
        item['m2_to_use'] = self.compose_int(item['m2_to_use'])
        item['m2_terrain'] = self.compose_int(item['m2_terrain'])
        item['wc'] = self.compose_int(item['wc'])
        item['elevators'] = self.compose_int(item['elevators'])
        item['num_of_floors'] = self.compose_int(item['num_of_floors'])
        item.save()
        return item

    def compose_int(self, string):
        if string:
            return int("".join(string[0].strip().split('.')))
        else:
            return None


class GaragePipeline(object):
    def process_item(self, item, spider):
        item['garage_number'] = self.compose_int(item['garage_number'])
        item.save()
        return item

    def compose_int(self, string):
        if string:
            return int("".join(string[0].strip().split('.')))
        else:
            return None


class LandPipeline(object):
    def process_item(self, item, spider):
        item['m2_total'] = self.compose_int(item['m2_total'])
        item['m2_min_rent'] = self.compose_int(item['m2_min_rent'])
        item['m2_min_sale'] = self.compose_int(item['m2_min_sale'])
        item['m2_to_build'] = self.compose_int(item['m2_to_build'])
        item['building_floors'] = self.compose_int(item['building_floors'])
        item.save()
        return item

    def compose_int(self, string):
        if string:
            return int("".join(string[0].strip().split('.')))
        else:
            return None


class CommercialPipeline(object):
    def process_item(self, item, spider):
        'transfer_price'
        item['transfer_price'] = self.compose_int(item['transfer_price'])
        item['m2_total'] = self.compose_int(item['m2_total'])
        item['m2_to_use'] = self.compose_int(item['m2_to_use'])
        item['m2_terrain'] = self.compose_int(item['m2_terrain'])
        item['num_of_floors'] = self.compose_int(item['num_of_floors'])
        item['show_windows'] = self.compose_int(item['show_windows'])
        item['wc'] = self.compose_int(item['wc'])
        item.save()
        return item

    def compose_int(self, string):
        if string:
            return int("".join(string[0].strip().split('.')))
        else:
            return None
