import scrapy
from idealista.items import HouseItem


class HouseSpider(scrapy.Spider):
    name = "house"
    custom_settings = {
        'ITEM_PIPELINES': {
            'idealista.pipelines.PropertyPipeline': 300,
            'idealista.pipelines.HousePipeline': 400
        }
    }
    start_urls = [
        'https://www.idealista.com/venta-viviendas/madrid-provincia/?ordenado-por=fecha-publicacion-desc',
        # 'https://www.idealista.com/venta-viviendas/alava/?ordenado-por=fecha-publicacion-desc',
        # 'https://www.idealista.com/venta-viviendas/albacete-provincia/?ordenado-por=fecha-publicacion-desc',
    ]

    def parse(self, response):
        # parse every property in the list
        for item in response.xpath('//a[@class="item-link "]/@href').extract():
            item_page = response.urljoin(item)
            yield scrapy.Request(item_page, callback=self.parse_property_house)
        # next page definition: Siguiente. Follow each page
        next_page = response.xpath('//a[@class="icon-arrow-right-after"]/@href').extract_first()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)

    def parse_property_house(self, response):
        ''' Will parse all the House atributes and return a HouseItem object.
        '''
        house = HouseItem()
        title = response.xpath('//span[@class="txt-bold"]/text()')
        # PROPERTY fields
        house['title'] = title.extract_first()
        # house['price_raw'] = int("".join(re.compile('(\d)', re.IGNORECASE).findall(response.xpath('//p[@class="price"]/text()').extract_first())))
        house['price_raw'] = int("".join((response.xpath('//p[@class="price"]/text()')[0].re('(\d)'))))
        house['source'] = 'idealista'
        house['url'] = response.url
        house['slug'] = 'id-' + response.url.split("/")[4]
        # house['html'] = response.text
        house['desc'] = response.xpath('//div[@class="adCommentsLanguage expandable"]/text()').extract_first()
        house['transaction'] = title.re('(Alquiler|venta)')[0].lower()
        house['house_type'] = "".join(title[0].re('Alquiler\sde\s(\w*)\sen|(\D*)\sen\sventa')).strip().lower()
        house['phones'] = response.xpath('//p[@class="txt-big txt-bold _browserPhone"]/text()').extract()
        house['name'] = response.xpath('//div[@class="advertiser-data txt-soft"]/p/text()').extract_first().strip()
        house['address_raw'] = ".".join(response.xpath('//div[@id="addressPromo"]/ul/li/text()').extract())
        house['real_estate_raw'] = response.xpath('//a[@class="about-advertiser-name"]/@href').extract_first()
        # HOUSE fields
        basic = response.xpath('//div[h2/text()="Características básicas"]/ul/li/text()')
        building = response.xpath('//div[h2/text()="Edificio"]/ul/li/text()')
        equipment = response.xpath('//div[h2/text()="Equipamiento"]/ul/li/text()')
        house['m2_total'] = basic.re('([0-9]*[.]?[0-9]+)\sm²\sconstruidos')
        house['m2_to_use'] = basic.re('([0-9]*[.]?[0-9]+)\sm²\sútiles')
        house['m2_terrain'] = basic.re('Parcela de (.+) m²')
        house['rooms'] = basic.re('(\d+)\shabitaci')
        house['wc'] = basic.re('(\d+)\swc')
        house['orientation'] = basic.re('(norte|sur|este|oeste)')
        house['preservation'] = "".join(basic.re('(buen estado|para reformar)'))
        house['floor_num'] = "".join(building.re('Planta\s(\d+)|(Bajo)|(Sótano)|(Semi-Sótano)|(Entreplanta)'))
        house['outside'] = "".join(building.re('(exterior|interior)'))
        house['terrace'] = bool(basic.re('(erraza)'))
        house['chimney'] = bool(basic.re('(himenea)'))
        house['has_garage'] = bool(basic.re('(garaje incluida)'))
        house['builtin_wardrobes'] = bool(basic.re('(rmarios empotrados)'))
        house['store_room'] = bool(basic.re('(trastero)'))
        house['elevator'] = bool(building.re('on (ascensor)'))
        house['garden'] = bool(equipment.re('(ardín)'))
        house['air_conditioning'] = bool(equipment.re('(ire acondicionado)'))
        house['swimming_pool'] = bool(equipment.re('(iscina)'))
        house['furnished'] = bool(equipment.re('(otalmente amueblado y equipado)'))
        house['furnished_kitchen'] = bool(equipment.re('(ocina equipada)|(otalmente amueblado y equipado)'))
        yield house
