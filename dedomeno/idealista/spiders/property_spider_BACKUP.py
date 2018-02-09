# -*- coding: utf-8 -*-
# Scrapy imports
import scrapy
from scrapy.exceptions import CloseSpider
from scrapy.utils.project import get_project_settings
from idealista.items import RealEstateItem, HouseItem, RoomItem, OfficeItem, LandItem, GarageItem, CommercialItem, StoreRoomItem, BuildingItem
# Django model imports
from houses.models import Date, Price, RealEstate, House, Room, Office, Land, Garage, Commercial, StoreRoom, Building
# Other imports
from datetime import date
import re


class PropertySpider(scrapy.Spider):
    """ The PropertySpider will crawl every property for a transaction, property type and province given.
        It will also crawl every Real Estate associate with the Property.
        Example of the pipelines needed to crawl. Be aware that the type of Property (i.e. Commercial) is needed.
        Usually you want to declare this in the script calling the spider.
        custom_settings = {
            'ITEM_PIPELINES': {
                'idealista.pipelines.PropertyPipeline': 300,
                'idealista.pipelines.{House, Room, Office, Garage, Land, Commercial, Storeroom, Building}Pipeline': 400,
                'idealista.pipelines.DatePipeline': 500,
                'idealista.pipelines.PricePipeline': 600,
            }
    }
    """
    name = "property"

    def __init__(self, transaction=None, property_type=None, province=None, *args, **kwargs):
        """
        Initialize the spider with the console parameters
        :param transaction: could be rent or sale
        :param property_type: must be a correct property type
        :param province: must be a supported province or 'all'
        :param args: TODO
        :param kwargs: TODO
        """
        super(PropertySpider, self).__init__(*args, **kwargs)
        self.property_type = property_type
        self.transaction = transaction
        self.province = province
        # self.spiderset is use to check en the close_spider pipeline if there is a offline property in the db.
        self.spiderset = set()
        # set the start_urls with the console parameters
        self.urls_scheme = get_project_settings().get('IDEALISTA_URL_SCHEME')
        self.country = self.urls_scheme['country']
        self.check_args(transaction, property_type, province)
        self.start_urls = self.set_start_urls(transaction, property_type, province)

    def check_args(self, transaction, property_type, province):
        """
        Will check if the parameters of the __init__ method are well formatted.
        :param transaction: must be either rent or sale
        :param property_type: must be a correct property type
        :param province: must be a supported province or 'all'
        @raise CloseSpider: if the parameters doesnt fit with settings.IDEALISTA_URL_SCHEME
        """
        if transaction != 'rent' and transaction != 'sale':
            raise CloseSpider('Transaction not supported')
        # TODO: Change string concatenation
        if property_type not in self.urls_scheme[transaction + '_transaction']:
            raise CloseSpider('Property type not supported')
        if province not in self.urls_scheme['provinces'] and province != 'all':
            raise CloseSpider('Province not supported')

    def set_start_urls(self, transaction_name, property_name, provinces_name):
        """
        Compose property url list like:
        https://www.idealista.com/venta-viviendas/a-coruna-provincia/?ordenado-por=fecha-publicacion-desc
        :param transaction_name: type of transaction {sale, rent}
        :param property_name: type of property {house, room, office, garage, land, commercial}
        :param provinces_name: list of provinces to crawls
        :return: the a list with all the initial urls to start to crawl
        """
        # TODO: It could be more flexible and mix properties and transactions as we do with provinces?
        url = self.urls_scheme['url']
        transaction = self.urls_scheme[transaction_name]
        separator = self.urls_scheme['separator']
        # TODO: Change string concatenation
        property_name = self.urls_scheme[transaction_name + '_transaction'][property_name]
        query = self.urls_scheme['query_pub_date']
        property_list = []
        if provinces_name == 'all':
            provinces = self.urls_scheme['provinces'].values()
        else:
            provinces = [self.urls_scheme['provinces'][provinces_name]]
        for province in provinces:
            # TODO: Change string concatenation
            property_list.append(url + transaction + separator + property_name + '/' + province + '/' + query)
        return property_list

    def set_property_item(self):
        """
        Create a new Property Item type for the current spider.
        It depends of the property set in the command line
        :return: a Property child Item
        """
        return {
            'house': HouseItem(),
            'room': RoomItem(),
            'office': OfficeItem(),
            'garage': GarageItem(),
            'land': LandItem(),
            'commercial': CommercialItem(),
            'storeroom': StoreRoomItem(),
            'building': BuildingItem(),
        }.get(self.property_type, 'Not a valid property')

    def set_property_object(self, slug):
        """
        Create a new Property Object that will be stored in the database.
        :param slug: id of the property (prefix(id for Idealista) + - + property number)
        :return: a new Property child object, initialize with his slug.
        """
        return {
            'house': House.objects.filter(slug=slug).first(),
            'room': Room.objects.filter(slug=slug).first(),
            'office': Office.objects.filter(slug=slug).first(),
            'garage': Garage.objects.filter(slug=slug).first(),
            'land': Land.objects.filter(slug=slug).first(),
            'commercial': Commercial.objects.filter(slug=slug).first(),
            'storeroom': StoreRoom.objects.filter(slug=slug).first(),
            'building': Building.objects.filter(slug=slug).first(),
        }.get(self.property_type, 'Not a valid property')

    def parse(self, response):
        """
        Will parse every property url list in self.start_urls, and capture the property and next page url
        :param response: response of a list of properties page
        :return: yield the property page or next list of properties page
        """
        """
        FIRST, GO DEEPER!!
        address_level = response.xpath('//span[@class="breadcrumb-title icon-arrow-dropdown-after"]/text()').extract_first()
        bread = response.xpath('//div[@class="breadcrumb-subitems"]/ul/li/ul/li')
        
        """
        breadcrumb_list = response.xpath('//div[@class="breadcrumb-subitems"]/ul/li/ul/li/a/@href').extract()
        if len(breadcrumb_list) is not 0:
            for crumb in breadcrumb_list:
                next_page = response.urljoin(crumb+self.urls_scheme['query_pub_date'])
                yield scrapy.Request(next_page, callback=self.parse)
        else:
            geo_path = response.xpath('//div[@class="breadcrumb-geo wrapper clearfix"]/ul/li/a/text()').extract()
            geo_current = response.xpath('//span[@class="breadcrumb-title icon-arrow-dropdown-after"]/text()').extract()
            geo = list(map(str.strip, [*geo_path, *geo_current]))
            for item in response.xpath('//div[@class="item-info-container"]'):
                item_page = response.urljoin(item.xpath('.//a[@class="item-link "]/@href').extract_first())
                # TODO: Change string concatenation
                slug = 'id-' + item_page.split("/")[4]
                self.spiderset.add(slug)
                price = int("".join((item.xpath('.//span[contains(@class, "item-price")]/text()')[0].re('(\d)'))))
                property_obj = self.set_property_object(slug)
                # if there is already a property object in the db with that slug and check for changes: price & offline
                if property_obj:
                    # check if last price has change
                    property_price = property_obj.price_set.order_by('-date_start').first()
                    # check just in case we have a property without price value
                    if property_price:
                        # Update the price if the new one is different from the one store in the db
                        if property_price.value != price:
                            property_price.date_end = date.today()
                            property_price.save()
                            Price.objects.create(value=int(price), date_start=date.today(), property_price=property_obj)
                        # check if a property that was offline now is online
                        if not property_obj.online:
                            property_obj.online = True
                            property_obj.save()
                            Date.objects.create(online=date.today(), property_date=property_obj)
                            if property_price.value == price:
                                Price.objects.create(value=int(price), date_start=date.today(), property_price=property_obj)
                                # new Date
                # if there is not a property with that slug, scrapy it
                else:
                    yield scrapy.Request(item_page, callback=self.parse_property,
                                         meta={'geo': geo})
            # next page definition: Siguiente. Follow each page
            next_page = response.xpath('//a[@class="icon-arrow-right-after"]/@href').extract_first()
            if next_page is not None:
                next_page = response.urljoin(next_page)
                yield scrapy.Request(next_page, callback=self.parse)

    def parse_property(self, response):
        """
        Will parse all the property attributes and return a propertyItem object.
        :param response: response of a property page
        :return: yield property item (to the PipeLines!!) or a RealEstate Request
        """
        # example: property_item = GarageItem()
        property_item = self.set_property_item()
        title = response.xpath('/html/head/title/text()')
        # PROPERTY fields
        # property_item['proxy'] = response.meta['proxy']
        property_item['title'] = title.extract_first()
        property_item['price_raw'] = int("".join((response.xpath('//span[@class="h3-simulated txt-bold"]/text()')[0].re('(\d)'))))
        property_item['source'] = 'idealista'
        property_item['url'] = response.url
        property_item['country'] = self.country
        # TODO: Change string concatenation
        property_item['slug'] = 'id-' + response.url.split("/")[4]
        property_item['transaction'] = title.re('(Alquiler|venta)')[0].lower()
        property_item['property_type'] = self.property_type
        property_item['address_province'] = self.province
        property_item['address_path'] = response.meta['geo']
        # property_item['html'] = response.text
        property_item['desc'] = response.xpath('//div[@class="adCommentsLanguage expandable"]/text()').extract_first()
        property_item['name'] = response.xpath('//div[@class="advertiser-data txt-soft"]/p/text()').extract_first()
        # FIXED: phone sometimes is shown as:
        phones = [response.xpath('//p[@class="txt-big txt-bold _browserPhone"]/text()').extract_first(),
                  response.xpath('//p[@class="txt-bold _browserPhone icon-phone"]/text()').extract_first(),
                  response.xpath('//a[@class="_mobilePhone"]/text()').extract_first(),
                  response.xpath('//div[@class="phone last-phone"]/text()').extract_first()]
        property_item['phones'] = phones
        property_item['address_exact'] = not bool(
            response.xpath('//div[@class="contextual full-width warning icon-feedbk-alert"]/text()').extract_first())
        property_item['address_raw'] = ".".join(response.xpath('//div[@id="addressPromo"]/ul/li/text()').extract())
        # mapConfig={latitude:"42.0064667",longitude:"-5.6714257",
        match = re.search(r"latitude:\"(.*)\",longitude:\"(.*)\",onMapElements", response.text)
        property_item['latitude'] = match.group(1)
        property_item['longitude'] = match.group(2)
        property_item['real_estate_raw'] = response.xpath('//a[@class="about-advertiser-name"]/@href').extract_first()
        # Will continue parsing the child property, with the correct specific child parameters
        # Example: property_item = self.parse_garage(response, property_item)
        property_item = self.parse_property_middleware(response, property_item)

        # If property has a real estate
        if property_item['real_estate_raw']:
            # TODO: Change string concatenation
            real_estate_slug = 'id-' + property_item['real_estate_raw'].split('/')[2]
            real_estate = RealEstate.objects.filter(slug=real_estate_slug)
            # if the real estate is not in de db
            if not real_estate:
                real_estate_page = response.urljoin(property_item['real_estate_raw'])
                yield scrapy.Request(real_estate_page, callback=self.parse_real_estate,
                                     meta={'property_item': property_item})
            else:
                property_item['real_estate'] = real_estate.first()
                yield property_item
        else:
            yield property_item

    def parse_property_middleware(self, response, property_item):
        """
        Behave as a middleware between the parse_property and parse_(property_type)
        :param response: response of a property page
        :param property_item: a father property item waiting to fill the property child attributes
        :return: a call to the specific parse property type function
        """
        dic = {
            'house': self.parse_house,
            'room': self.parse_room,
            'office': self.parse_office,
            'garage': self.parse_garage,
            'land': self.parse_land,
            'commercial': self.parse_commercial,
            'storeroom': self.parse_storeroom,
            'building': self.parse_building,
        }
        return dic.get(self.property_type, 'Not a valid property')(response, property_item)

    def parse_house(self, response, property_item):
        """
        Will parse house property type specific attributes
        :param response: response of a property house page
        :param property_item: a father property item waiting to fill the property house attributes
        :return: return a property item
        """
        # Características básicas
        basic = response.xpath('//div[h2/text()="Características básicas"]/ul/li/text()')
        title = response.xpath('//span[@class="txt-bold"]/text()')
        meta = response.xpath('/html/head/meta[@name="description"]/@content')[0]
        property_item['house_type'] = meta.re('(\D*)\sde\s')[0].strip()
        property_item['m2_total'] = basic.re('([0-9]*[.]?[0-9]+)\sm²\sconstruidos')
        property_item['m2_to_use'] = basic.re('([0-9]*[.]?[0-9]+)\sm²\sútiles')
        property_item['m2_terrain'] = basic.re('arcela de (.+) m²')
        property_item['rooms'] = basic.re('(\d+)\shabitaci')
        property_item['wc'] = basic.re('(\d+)\sbaño')
        property_item['orientation'] = basic.re('(norte|sur|este|oeste)')
        property_item['preservation'] = "".join(basic.re('(buen estado|para reformar)'))
        property_item['terrace'] = bool(basic.re('(erraza)'))
        property_item['chimney'] = bool(basic.re('(himenea)'))
        property_item['has_garage'] = bool(basic.re('(araje incluida)'))
        property_item['builtin_wardrobes'] = bool(basic.re('(rmarios empotrados)'))
        property_item['store_room'] = bool(basic.re('(rastero)'))
        property_item['furnished'] = bool(basic.re('(otalmente amueblado y equipado)'))
        property_item['furnished_kitchen'] = bool(basic.re('(ocina equipada)|(otalmente amueblado y equipado)'))
        property_item['construction_year'] = basic.re('onstruido\sen\s([0-9]*[.]?[0-9]+)')
        # Edificio
        building = response.xpath('//div[h2/text()="Edificio"]/ul/li/text()')
        property_item['floor_num'] = "".join(building.re('Planta\s(\d+)|(Bajo)|(Sótano)|(Semi-Sótano)|(Entreplanta)'))
        property_item['outside'] = "".join(building.re('(exterior|interior)'))
        property_item['elevator'] = bool(building.re('on (ascensor)'))
        # Equipamiento
        equipment = response.xpath('//div[h2/text()="Equipamiento"]/ul/li/text()')
        property_item['garden'] = bool(equipment.re('(ardín)'))
        property_item['air_conditioning'] = bool(equipment.re('(ire acondicionado)'))
        property_item['swimming_pool'] = bool(equipment.re('(iscina)'))
        return property_item

    def parse_room(self, response, property_item):
        """
        Will parse room property type specific attributes
        :param response: response of a property room page
        :param property_item: a father property item waiting to fill the property room attributes
        :return: return a property item
        """
        # Características básicas
        basic = response.xpath('//div[h2/text()="Características básicas"]/ul/li/text()')
        property_item['house_type'] = "".join(basic.re('abitación en (.+) de')).strip().lower()
        property_item['m2_total'] = basic.re('de ([0-9]*[.]?[0-9]+)\sm²')
        property_item['floor_num'] = "".join(basic.re('Planta\s(\d+)|(Bajo)|(Sótano)|(Semi-Sótano)|(Entreplanta)'))
        property_item['elevator'] = bool(basic.re('on (ascensor)'))
        property_item['wc'] = basic.re('(\d+)\sbaño')
        property_item['min_month_stay'] = basic.re('nima\sde\s(\d+)')
        property_item['people_max'] = basic.re('máxima\s(\d+)\spersonas')
        property_item['people_now_living_gender'] = "".join(basic.re('hora\sson\s(.+),')).strip().lower()
        property_item['people_now_living_age_min'] = basic.re('entre\s(\d+)\sy')
        property_item['people_now_living_age_max'] = basic.re('y\s(\d+)\saños')
        property_item['smoking_allowed'] = bool(basic.re('(Se puede fumar)'))
        property_item['pet_allowed'] = bool(basic.re('(Se admiten mascotas)'))
        # Looking for
        looking_for = response.xpath('//div[h2/text()="Buscan"]/ul/li/text()')
        property_item['looking_for_male'] = bool(looking_for.re('(Chico)|(chico)'))
        property_item['looking_for_female'] = bool(looking_for.re('(Chica)|(chica)'))
        property_item['looking_for_student'] = bool(looking_for.re('(studiante)'))
        property_item['looking_for_worker'] = bool(looking_for.re('(on trabajo)'))
        property_item['gay_friendly'] = bool(looking_for.re('(ay friendly)'))
        # Equipment
        equipment = response.xpath('//div[h2/text()="Equipamiento"]/ul/li/text()')
        property_item['air_conditioning'] = bool(equipment.re('(ire acondicionado)'))
        property_item['internet'] = bool(equipment.re('(a internet)'))
        property_item['builtin_wardrobes'] = bool(equipment.re('(empotrado)'))
        property_item['furnished'] = bool(equipment.re('(mueblado)'))
        property_item['house_cleaners'] = bool(equipment.re('(Asistente)'))
        return property_item

    def parse_office(self, response, property_item):
        """
        Will parse office property type specific attributes
        :param response: response of a property office page
        :param property_item: a father property item waiting to fill the property office attributes
        :return: return a property item
        """
        # Basic
        basic = response.xpath('//div[h2/text()="Características básicas"]/ul/li/text()')
        property_item['m2_total'] = basic.re('([0-9]*[.]?[0-9]+)\sm²\sconstruidos')
        property_item['m2_to_use'] = basic.re('([0-9]*[.]?[0-9]+)\sm²\sútiles')
        property_item['m2_terrain'] = basic.re('Parcela de (.+) m²')
        property_item['num_of_floors'] = basic.re('Oficina\sde\s([0-9]*[.]?[0-9]+)\spiso')
        property_item['distribution'] = "".join(basic.re('Distribución\s(.+)')).strip().lower()
        property_item['kitchen'] = bool(basic.re('ocina'))
        property_item['wc'] = basic.re('([0-9]*[.]?[0-9]+)\s[ba][as][ñe]')
        property_item['wc_location'] = "".join(basic.re('(dentro|fuera)'))
        property_item['orientation'] = basic.re('(norte|sur|este|oeste)')
        property_item['has_garage'] = bool(basic.re('(garaje incluid)'))
        property_item['preservation'] = "".join(basic.re('(buen estado|para reformar)'))
        # Building
        building = response.xpath('//div[h2/text()="Edificio"]/ul/li/text()')
        property_item['floor_num'] = "".join(building.re('Planta\s(\d+)|(Bajo)|(Sótano)|(Semi-Sótano)|(Entreplanta)'))
        property_item['outside'] = "".join(building.re('(exterior|interior)'))
        property_item['elevators'] = building.re('([0-9]*[.]?[0-9]+)\sascensor')
        property_item['office_type'] = "".join(building.re('(mixto|exclusivo)'))
        property_item['janitor'] = bool(building.re('(Conserje)'))
        property_item['access_control'] = bool(building.re('(ontrol de accesos)'))
        property_item['security_system'] = bool(building.re('(istema de seguridad)'))
        property_item['security_door'] = bool(building.re('(uerta de seguridad)'))
        property_item['fire_extinguishers'] = bool(building.re('(xtintores)'))
        property_item['fire_detectors'] = bool(building.re('(etectores de incendios)'))
        property_item['sprinklers'] = bool(building.re('(spersores)'))
        property_item['fire_door'] = bool(building.re('(uerta cortafuegos)'))
        property_item['emergency_exit'] = bool(building.re('(alida de emergencia)'))
        property_item['emergency_exit_lights'] = bool(building.re('(uces de salida emergencia)'))
        # Equipment
        equipment = response.xpath('//div[h2/text()="Equipamiento"]/ul/li/text()')
        property_item['store_room'] = bool(equipment.re('(archivo)'))
        property_item['hot_water'] = bool(equipment.re('(gua caliente)'))
        property_item['heating'] = bool(equipment.re('(alefacción)'))
        property_item['air_conditioning_cold'] = bool(equipment.re('(de frío)'))
        property_item['air_conditioning_hot'] = bool(equipment.re('(calor)'))
        property_item['double_glazed_windows'] = bool(equipment.re('(doble acristalamiento)'))
        property_item['false_ceiling'] = bool(equipment.re('(also techo)'))
        property_item['false_floor'] = bool(equipment.re('(also suelo)'))
        return property_item

    def parse_garage(self, response, property_item):
        """
        Will parse garage property type specific attributes
        :param response: response of a property garage page
        :param property_item: a father property item waiting to fill the property garage attributes
        :return: return a property item
        """
        # Características básicas
        basic = response.xpath('//div[h2/text()="Características básicas"]/ul/li/text()')
        property_item['garage_type'] = "".join(basic.re('Plaza\spara\s(.+)')).strip().lower()
        property_item['garage_number'] = basic.re('Plaza\snúmero\s([0-9]*[.]?[0-9]+)')
        property_item['covered'] = bool(basic.re('(ubierta)'))
        property_item['elevator'] = bool(basic.re('(on ascensor)'))
        # Extras
        extra = response.xpath('//div[h2/text()="Extras"]/ul/li/text()')
        property_item['automatic_door'] = bool(extra.re('(rta automática de ga)'))
        property_item['security_cameras'] = bool(extra.re('(aras de seguridad)'))
        property_item['alarm'] = bool(extra.re('(larm)'))
        property_item['security_guard'] = bool(extra.re('(al de seguridad)'))
        return property_item

    def parse_land(self, response, property_item):
        """
        Will parse land property type specific attributes
        :param response: response of a property land page
        :param property_item: a father property item waiting to fill the property land attributes
        :return: return a property item
        """
        # Basic
        basic = response.xpath('//div[h2/text()="Características básicas"]/ul/li/text()')
        property_item['m2_total'] = basic.re('uperficie\stotal\sdel\sterreno\s([0-9]*[.]?[0-9]+)\sm²')
        property_item['m2_min_rent'] = basic.re('uperficie\smínima\sen\sAlquiler\s([0-9]*[.]?[0-9]+)\sm²')
        property_item['m2_min_sale'] = basic.re('uperficie\smínima\sen\sVenta\s([0-9]*[.]?[0-9]+)\sm²')
        property_item['m2_to_build'] = basic.re('uperficie\sedificable\s([0-9]*[.]?[0-9]+)\sm²')
        property_item['access'] = "".join(basic.re('Acceso\s(.+)'))
        property_item['nearest_town'] = "".join(basic.re('más\scercano:\s(.+)'))
        # Urban situation
        urban = response.xpath('//div[h2/text()="Situación urbanística"]/ul/li/text()')
        property_item['ground'] = "".join(urban.re('Terreno\s(.+)'))
        property_item['zoned'] = "".join(urban.re('Calificado\spara\s(.+)'))
        property_item['building_floors'] = urban.re('([0-9]*[.]?[0-9]+)\splanta')
        # Equipment
        equipment = response.xpath('//div[h2/text()="Equipamiento"]/ul/li/text()')
        property_item['sewerage'] = bool(equipment.re('(lcantarillado)'))
        property_item['street_lighting'] = bool(equipment.re('(lumbrado p)'))
        property_item['water'] = bool(equipment.re('(gua)'))
        property_item['electricity'] = bool(equipment.re('(lectricidad)'))
        property_item['sidewalks'] = bool(equipment.re('(ceras)'))
        property_item['natural_gas'] = bool(equipment.re('(as natural)'))
        return property_item

    def parse_commercial(self, response, property_item):
        """
        Will parse commercial property type specific attributes
        :param response: response of a property commercial page
        :param property_item: a father property item waiting to fill the property commercial attributes
        :return: return a property item
        """
        meta = response.xpath('/html/head/meta[@name="description"]/@content')[0]
        property_item['commercial_type'] = meta.re('(\D*)\sde\s')[0].strip()
        # Basic
        basic = response.xpath('//div[h2/text()="Características básicas"]/ul/li/text()')
        property_item['transfer_price'] = response.xpath(
            '//div[@class="details-block clearfix"]/p[@class="more-details"]/text()').re(
            'Traspaso\spor\s([0-9]*[.]?[0-9]+)\s€')
        property_item['m2_total'] = basic.re('([0-9]*[.]?[0-9]+)\sm²\sconstruidos')
        property_item['m2_to_use'] = basic.re('([0-9]*[.]?[0-9]+)\sm²\sútiles')
        property_item['m2_terrain'] = basic.re('Parcela de (.+) m²')
        property_item['num_of_floors'] = basic.re('([0-9]*[.]?[0-9]+)\splanta')
        property_item['distribution'] = "".join(basic.re('Distribución\s(.+)')).strip().lower()
        property_item['location'] = "".join(basic.re('Situado\s(.+)')).strip().lower()
        property_item['corner'] = bool(basic.re('(ace esquina)'))
        property_item['show_windows'] = basic.re('([0-9]*[.]?[0-9]+)\sescaparate')
        property_item['last_activity'] = "".join(basic.re('ltima\sactividad:\s(.+)')).strip().lower()
        property_item['preservation'] = "".join(basic.re('(buen estado|para reformar)'))
        property_item['wc'] = basic.re('([0-9]*[.]?[0-9]+)\saseos\so\sbaños')
        # Building
        building = response.xpath('//div[h2/text()="Edificio"]/ul/li/text()')
        property_item['floor_num'] = "".join(building.re('Planta\s(\d+)|(Bajo)|(Sótano)|(Semi-Sótano)|(Entreplanta)'))
        property_item['facade'] = "".join(building.re('Fachada\sde\s(.+)'))
        # Equipment
        equipment = response.xpath('//div[h2/text()="Equipamiento"]/ul/li/text()')
        property_item['air_conditioning'] = bool(equipment.re('(ire acondicionado)'))
        property_item['alarm_system'] = bool(equipment.re('(stema de alarma)'))
        property_item['store_room'] = bool(equipment.re('(lmacén)'))
        property_item['heating'] = bool(equipment.re('(alefacci)'))
        property_item['kitchen'] = bool(equipment.re('(ocina)'))
        property_item['security_door'] = bool(equipment.re('(uerta de seguridad)'))
        property_item['smoke_extractor'] = bool(equipment.re('(alida de humos)'))
        return property_item

    def parse_storeroom(self, response, property_item):
        """
        Will parse storeroom property type specific attributes
        :param response: response of a property storeroom page
        :param property_item: a father property item waiting to fill the property commercial attributes
        :return: return a property item
        """
        # Basic
        basic = response.xpath('//div[h2/text()="Características básicas"]/ul/li/text()')
        property_item['m2_total'] = basic.re('([0-9]*[.]?[0-9]+)\sm²\sconstruidos')
        property_item['m_height'] = basic.re('([0-9]*[.]?[0-9]+)\sm\sde\saltura')
        property_item['access_24h'] = bool(basic.re('(ccesible\s24h)'))
        property_item['limited_parking'] = bool(basic.re('(ona\sde\scarga)'))
        return property_item

    def parse_building(self, response, property_item):
        """
        Stores a Building type :model:`houses.Property`
        """
        # Basic
        basic = response.xpath('//div[h2/text()="Características básicas"]/ul/li/text()')
        property_item['m2_total'] = basic.re('([0-9]*[.]?[0-9]+)\sm²\sconstruidos')
        property_item['m2_min_rent'] = basic.re('([0-9]*[.]?[0-9]+)\sm²\sde\ssuperficie')
        property_item['building_type'] = "".join(basic.re('(Edificio\s\D*)')).strip().lower()
        property_item['elevator_num'] = basic.re('([0-9]*[.]?[0-9]+)\sascensore')
        property_item['floor_num'] = basic.re('([0-9]*[.]?[0-9]+)\splanta')
        property_item['garage_num'] = basic.re('([0-9]*[.]?[0-9]+)\splazas\sde\sgaraje')
        property_item['security'] = bool(basic.re('(igilancia)'))
        property_item['preservation'] = "".join(basic.re('(Buen estado|Para reformar)'))
        property_item['tenant'] = "".join(basic.re('(Con\sinquilino|Sin\sinquilino)'))
        property_item['house_num'] = basic.re('([0-9]*[.]?[0-9]+)\svivienda')
        property_item['construction_year'] = basic.re('onstruido\sen\s([0-9]*[.]?[0-9]+)')
        return property_item

    def parse_real_estate(self, response):
        """
        Will parse real estate attributes and save a real estate object in the db.
        :param response: response of a Real Estate page.
        :return: yield the property item linked with the RealEstate Item.
        """
        real_estate = RealEstateItem()
        real_estate['name'] = response.xpath('//div[@class="office-title"]/h2/text()').extract_first()
        # TODO: Change string concatenation
        real_estate['slug'] = 'id-' + response.url.split('/')[4]
        real_estate['country'] = self.country
        logo = response.xpath('//div[@class="logo-branding"]/img/@src').extract_first()
        if logo:
            # TODO: Change string concatenation
            real_estate['logo'] = 'https:' + logo
        real_estate['web'] = response.xpath('//div[@id="online"]/a/@href').extract_first()
        # str(real_estate['web'])[:199]
        if real_estate['web'] is not None:
            real_estate['web'] = real_estate['web'][:199]
        real_estate['url'] = response.url
        # real_estate['html'] = response.text
        real_estate['desc'] = response.xpath('//p[@class="office-description"]/text()').extract_first()
        real_estate['telephone'] = response.xpath('//*[@class="icon-phone"]/span/text()').extract_first()
        real_estate['address'] = ''.join(
            # TODO: Change string concatenation
            response.xpath('//a[@class="showMap icon-location"]/div/span/text()').extract()) + ''.join(
            response.xpath('//span[@class="regular-address"]/span/text()').extract())
        real_estate['source'] = 'idealista'
        real_estate_ob = real_estate.save()
        property_item = response.meta['property_item']
        property_item['real_estate'] = real_estate_ob
        yield property_item
