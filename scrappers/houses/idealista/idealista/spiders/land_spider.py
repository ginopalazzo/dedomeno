import scrapy
from idealista.items import LandItem


class LandSpider(scrapy.Spider):
    name = "land"
    custom_settings = {
        'ITEM_PIPELINES': {
            'idealista.pipelines.PropertyPipeline': 300,
            'idealista.pipelines.LandPipeline': 400
        }
    }
    start_urls = [
        'https://www.idealista.com/venta-terrenos/madrid-provincia/?ordenado-por=fecha-publicacion-desc',
        # 'https://www.idealista.com/venta-viviendas/alava/?ordenado-por=fecha-publicacion-desc',
        # 'https://www.idealista.com/venta-viviendas/albacete-provincia/?ordenado-por=fecha-publicacion-desc',
    ]

    def parse(self, response):
        # parse every property in the list
        for item in response.xpath('//a[@class="item-link "]/@href').extract():
            item_page = response.urljoin(item)
            yield scrapy.Request(item_page, callback=self.parse_property_land)
        # next page definition: Siguiente. Follow each page
        next_page = response.xpath('//a[@class="icon-arrow-right-after"]/@href').extract_first()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)

    def parse_property_land(self, response):
        ''' Will parse all the land atributes and return a landItem object.
        '''
        land = LandItem()
        title = response.xpath('//span[@class="txt-bold"]/text()')
        # PROPERTY fields
        land['title'] = title.extract_first()
        land['price_raw'] = int("".join((response.xpath('//p[@class="price"]/text()')[0].re('(\d)'))))
        land['source'] = 'idealista'
        land['url'] = response.url
        land['slug'] = 'id-' + response.url.split("/")[4]
        land['transaction'] = title.re('(Alquiler|venta)')[0].lower()
        # land['html'] = response.text
        land['desc'] = response.xpath('//div[@class="adCommentsLanguage expandable"]/text()').extract_first()
        land['name'] = response.xpath('//div[@class="advertiser-data txt-soft"]/p/text()').extract_first()
        land['phones'] = response.xpath('//p[@class="txt-big txt-bold _browserPhone"]/text()').extract()
        land['address_raw'] = ".".join(response.xpath('//div[@id="addressPromo"]/ul/li/text()').extract())
        land['real_estate_raw'] = response.xpath('//a[@class="about-advertiser-name"]/@href').extract_first()
        # LAND fields
        # Basic
        basic = response.xpath('//div[h2/text()="Características básicas"]/ul/li/text()')
        land['m2_total'] = basic.re('uperficie\stotal\sdel\sterreno\s([0-9]*[.]?[0-9]+)\sm²')
        land['m2_min_rent'] = basic.re('uperficie\smínima\sen\sAlquiler\s([0-9]*[.]?[0-9]+)\sm²')
        land['m2_min_sale'] = basic.re('uperficie\smínima\sen\sVenta\s([0-9]*[.]?[0-9]+)\sm²')
        land['m2_to_build'] = basic.re('uperficie\sedificable\s([0-9]*[.]?[0-9]+)\sm²')
        land['access'] = "".join(basic.re('Acceso\s(.+)'))
        land['nearest_town'] = "".join(basic.re('Distancia\smunicipio\smás\scercano:\s(.+)'))
        # Urban situation
        urban = response.xpath('//div[h2/text()="Situación urbanística"]/ul/li/text()')
        land['ground'] = "".join(urban.re('Terreno\s(.+)'))
        land['zoned'] = "".join(urban.re('Calificado\spara\s(.+)'))
        land['building_floors'] = urban.re('([0-9]*[.]?[0-9]+)\splanta')
        # Equipment
        equipment = response.xpath('//div[h2/text()="Equipamiento"]/ul/li/text()')
        land['sewerage'] = bool(equipment.re('(lcantarillado)'))
        land['street_lighting'] = bool(equipment.re('(lumbrado p)'))
        land['water'] = bool(equipment.re('(gua)'))
        land['electricity'] = bool(equipment.re('(lectricidad)'))
        land['sidewalks'] = bool(equipment.re('(ceras)'))
        land['natural_gas'] = bool(equipment.re('(as natural)'))
        yield land
