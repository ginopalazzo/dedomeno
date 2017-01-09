import scrapy
from idealista.items import RoomItem


class RoomSpider(scrapy.Spider):
    name = "room"
    custom_settings = {
        'ITEM_PIPELINES': {
            'idealista.pipelines.PropertyPipeline': 300,
            'idealista.pipelines.RoomPipeline': 400
        }
    }
    start_urls = [
        'https://www.idealista.com/alquiler-habitacion/madrid/zona-noroeste/?ordenado-por=fecha-publicacion-desc',
        # 'https://www.idealista.com/venta-viviendas/alava/?ordenado-por=fecha-publicacion-desc',
        # 'https://www.idealista.com/venta-viviendas/albacete-provincia/?ordenado-por=fecha-publicacion-desc',
    ]

    def parse(self, response):
        # parse every property in the list
        for item in response.xpath('//a[@class="item-link "]/@href').extract():
            item_page = response.urljoin(item)
            yield scrapy.Request(item_page, callback=self.parse_property_room)
        # next page definition: Siguiente. Follow each page
        next_page = response.xpath('//a[@class="icon-arrow-right-after"]/@href').extract_first()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)

    def parse_property_room(self, response):
        ''' Will parse all the Room atributes and return a RoomItem object.
        '''
        room = RoomItem()
        title = response.xpath('//span[@class="txt-bold"]/text()')
        # PROPERTY fields
        room['title'] = title.extract_first()
        room['price_raw'] = int("".join((response.xpath('//p[@class="price"]/text()')[0].re('(\d)'))))
        room['source'] = 'idealista'
        room['url'] = response.url
        room['slug'] = 'id-' + response.url.split("/")[4]
        room['transaction'] = 'alquiler'
        # room['html'] = response.text
        room['desc'] = response.xpath('//div[@class="adCommentsLanguage expandable"]/text()').extract_first()
        room['name'] = response.xpath('//div[@class="advertiser-data txt-soft"]/p/text()').extract_first()
        room['phones'] = response.xpath('//p[@class="txt-big txt-bold _browserPhone"]/text()').extract()
        room['address_raw'] = ".".join(response.xpath('//div[@id="addressPromo"]/ul/li/text()').extract())
        room['real_estate_raw'] = response.xpath('//a[@class="about-advertiser-name"]/@href').extract_first()
        # ROOM fields
        # Características básicas
        basic = response.xpath('//div[h2/text()="Características básicas"]/ul/li/text()')
        room['house_type'] = "".join(basic.re('abitación en (.+) de')).strip().lower()
        room['m2_total'] = basic.re('de ([0-9]*[.]?[0-9]+)\sm²')
        room['floor_num'] = "".join(basic.re('Planta\s(\d+)|(Bajo)|(Sótano)|(Semi-Sótano)|(Entreplanta)'))
        room['elevator'] = bool(basic.re('on (ascensor)'))
        room['wc'] = basic.re('(\d+)\swc')
        room['min_month_stay'] = basic.re('nima\sde\s(\d+)')
        room['people_max'] = basic.re('máxima\s(\d+)\spersonas')
        room['people_now_living_gender'] = "".join(basic.re('hora\sson\s(.+),')).strip().lower()
        room['people_now_living_age_min'] = basic.re('entre\s(\d+)\sy')
        room['people_now_living_age_max'] = basic.re('y\s(\d+)\saños')
        room['smoking_allowed'] = bool(basic.re('(Se puede fumar)'))
        room['pet_allowed'] = bool(basic.re('(Se admiten mascotas)'))
        # Looking for
        looking_for = response.xpath('//div[h2/text()="Buscan"]/ul/li/text()')
        room['looking_for_male'] = bool(looking_for.re('(Chico)|(chico)'))
        room['looking_for_female'] = bool(looking_for.re('(Chica)|(chica)'))
        room['looking_for_student'] = bool(looking_for.re('(studiante)'))
        room['looking_for_worker'] = bool(looking_for.re('(on trabajo)'))
        room['gay_friendly'] = bool(looking_for.re('(ay friendly)'))
        # Equipment
        equipment = response.xpath('//div[h2/text()="Equipamiento"]/ul/li/text()')
        room['air_conditioning'] = bool(equipment.re('(ire acondicionado)'))
        room['internet'] = bool(equipment.re('(a internet)'))
        room['builtin_wardrobes'] = bool(basic.re('(rmarios empotrados)'))
        room['furnished'] = bool(basic.re('(mueblado)'))
        room['house_cleaners'] = bool(basic.re('(Asistente)'))
        yield room
